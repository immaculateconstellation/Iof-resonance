"""
JellyfishMesh — Distributed Photonic Calibration Engine
========================================================
Biologically-inspired control architecture for TFLN Penteract.

Topology: 5-node mesh following Tesla 3-6-9 connectivity
  W, X, Y, Z  →  radial bell nodes    (3 neighbors each)
  V           →  subumbrella ganglion  (4 neighbors, hub/completion)

Each NodeGanglion runs its own PID + Kuramoto phase coupling.
Corrections propagate as a wave W→X→Y→Z→V with configurable
phase lag — emergent stabilization, no central controller.

Install: pip install websockets numpy scipy
"""

import asyncio
import time
import json
import math
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict

import numpy as np

log = logging.getLogger("JELLYFISH")

# ── Tesla 3-6-9 connectivity map ──────────────────────────────────────────────
#   V is the subumbrella ring (4 edges = completion/9 node)
#   W/X/Y/Z are radial bell nodes (3 edges each)
#   Total: 8 edges, fully connected, no single-point bottleneck
CONNECTIVITY: Dict[str, List[str]] = {
    "W": ["X", "Y", "V"],       # 3 — bell NW
    "X": ["W", "Z", "V"],       # 3 — bell NE
    "Y": ["W", "Z", "V"],       # 3 — bell SW
    "Z": ["X", "Y", "V"],       # 3 — bell SE
    "V": ["W", "X", "Y", "Z"], # 4 — subumbrella ganglion (9/completion)
}

# ── Nonlinear error → pulse delay (ms) curve ─────────────────────────────────
# Jellyfish pulse faster under stress but not linearly — sigmoid-clamped.
# error=0.0  → 150ms (resting)
# error=0.5  →  60ms (active)
# error=1.0  →  25ms (stress)
def map_error_to_ms(error: float) -> float:
    e = abs(float(error))
    # Inverse sigmoid: fast at high error, slow at low error
    base   = 150.0   # resting interval ms
    floor  = 25.0    # minimum interval ms
    k      = 6.0     # steepness
    rate   = 1.0 / (1.0 + math.exp(-k * (e - 0.5)))
    return base - (base - floor) * rate


# ── Optical trigger signal ────────────────────────────────────────────────────
@dataclass
class OpticalTrigger:
    node_id:    str
    phase:      float          # radians, wrapped [0, 2π)
    amplitude:  float          # normalised 0–1
    timestamp:  float          # Unix epoch
    error:      float          # signed local error
    step_delay: float          # ms until next pulse

    def to_dict(self) -> dict:
        return asdict(self)


# ── PID state per node ────────────────────────────────────────────────────────
@dataclass
class NodePID:
    kp: float = 0.8
    ki: float = 0.05
    kd: float = 0.01
    setpoint: float = 0.0
    integral: float = 0.0
    prev_error: float = 0.0
    last_t: float = 0.0
    clamp: float = 0.5

    def step(self, measurement: float) -> float:
        now = time.time()
        dt  = (now - self.last_t) if self.last_t else 0.015
        self.last_t = now
        err = self.setpoint - measurement
        self.integral  = np.clip(self.integral + err * dt, -10, 10)
        deriv = (err - self.prev_error) / max(dt, 1e-6)
        self.prev_error = err
        output = self.kp * err + self.ki * self.integral + self.kd * deriv
        return float(np.clip(output, -self.clamp, self.clamp))


# ── NodeGanglion ──────────────────────────────────────────────────────────────
class NodeGanglion:
    """
    Single node in the jellyfish distributed nerve net.

    Each ganglion:
      - Maintains its own optical phase (Kuramoto oscillator)
      - Runs a local PID against its TFLN param
      - Propagates phase-stamped corrections to neighbors
      - Adapts its pulse rate to local error magnitude
    """

    def __init__(self, node_id: str, neighbors: List["NodeGanglion"]):
        self.id                = node_id
        self.neighbors: List["NodeGanglion"] = neighbors
        self.phase             = np.random.uniform(0, 2 * math.pi)   # random IC
        self.coupling_strength = 0.8
        self.local_error       = 0.0
        self.measurement       = 0.0
        self.correction        = 0.0
        self.step_delay        = 150.0   # ms, adaptive
        self.pid               = NodePID()
        self._last_trigger: Optional[OpticalTrigger] = None
        self._propagation_lag  = 0.012   # 12ms inter-node latency (axon delay analogue)

    # ── Kuramoto phase update ─────────────────────────────────────────────────
    def _update_phase(self):
        """
        Normalised Kuramoto coupling:
          dφᵢ/dt = ωᵢ + (K/N) Σⱼ sin(φⱼ − φᵢ)

        Normalising by N prevents amplitude blow-up in dense graphs.
        Phase wrapped to [0, 2π).
        """
        n = len(self.neighbors)
        if n == 0:
            return
        coupling_sum = sum(
            math.sin(nb.phase - self.phase)
            for nb in self.neighbors
        )
        # Natural frequency ω tied to error magnitude (stressed nodes run faster)
        omega = 0.1 + 0.4 * abs(self.local_error)
        self.phase += omega + (self.coupling_strength / n) * coupling_sum
        self.phase  = self.phase % (2 * math.pi)

    # ── Pulse ─────────────────────────────────────────────────────────────────
    def pulse(self, input_signal: float) -> OpticalTrigger:
        """
        Process incoming measurement, update phase, emit optical trigger.

        Args:
            input_signal: raw measurement from TFLN hardware (drift, Vπ, etc.)

        Returns:
            OpticalTrigger — phase-stamped optical correction signal
        """
        self.measurement  = float(input_signal)
        self.correction   = self.pid.step(self.measurement)
        self.local_error  = self.pid.setpoint - self.measurement

        self._update_phase()

        # Adaptive pulse rate — nonlinear, sigmoid-clamped
        self.step_delay = map_error_to_ms(self.local_error)

        # Amplitude: phase-modulated correction (biophotonic signal analogue)
        amplitude = 0.5 + 0.5 * math.sin(self.phase)   # [0, 1]

        trigger = OpticalTrigger(
            node_id    = self.id,
            phase      = round(self.phase, 6),
            amplitude  = round(amplitude, 4),
            timestamp  = time.time(),
            error      = round(self.local_error, 6),
            step_delay = round(self.step_delay, 2),
        )
        self._last_trigger = trigger
        return trigger

    # ── Receive neighbor signal ───────────────────────────────────────────────
    async def receive_propagation(self, trigger: OpticalTrigger):
        """
        Accept a phase-stamped signal from a neighbor.
        Applies propagation lag (axon delay analogue) then biases local phase.
        """
        await asyncio.sleep(self._propagation_lag)
        # Soft pull toward neighbor's phase (not override — just influence)
        phase_diff = trigger.phase - self.phase
        self.phase += 0.15 * math.sin(phase_diff)
        self.phase  = self.phase % (2 * math.pi)

    @property
    def state(self) -> dict:
        return {
            "id":              self.id,
            "phase":           round(self.phase, 4),
            "amplitude":       round(0.5 + 0.5 * math.sin(self.phase), 4),
            "localError":      round(self.local_error, 6),
            "correction":      round(self.correction, 6),
            "stepDelay":       round(self.step_delay, 1),
            "couplingStrength":self.coupling_strength,
            "neighbors":       [nb.id for nb in self.neighbors],
        }


# ── JellyfishMesh ─────────────────────────────────────────────────────────────
class JellyfishMesh:
    """
    Full 5-node jellyfish mesh.

    Orchestrates NodeGanglion instances in the Tesla 3-6-9 topology.
    Each tick: pulse all nodes, propagate triggers across edges, emit
    mesh telemetry for the dashboard wave visualiser.
    """

    def __init__(self):
        # Build nodes without neighbors first
        self.nodes: Dict[str, NodeGanglion] = {
            nid: NodeGanglion(nid, []) for nid in CONNECTIVITY
        }
        # Wire neighbors
        for nid, neighbor_ids in CONNECTIVITY.items():
            self.nodes[nid].neighbors = [self.nodes[nb] for nb in neighbor_ids]

        # Stagger initial phases: bell nodes offset by π/4, ganglion at 0
        offsets = {"W": 0.0, "X": math.pi/2, "Y": math.pi, "Z": 3*math.pi/2, "V": math.pi/4}
        for nid, offset in offsets.items():
            self.nodes[nid].phase = offset

        self.wave_history: List[dict] = []   # ring buffer for dashboard
        self._lock = asyncio.Lock()

    # ── Set measurements from TFLN hardware ──────────────────────────────────
    def feed(self, measurements: Dict[str, float]):
        """
        Feed raw hardware measurements into each node.
        measurements: {"W": bias_drift, "X": vpi_error, "Y": drift_rate,
                       "Z": bw_error, "V": er_error}
        """
        self._measurements = measurements

    # ── Single mesh tick ─────────────────────────────────────────────────────
    async def tick(self, measurements: Dict[str, float]) -> dict:
        """
        Pulse all nodes, propagate triggers, return full mesh state.
        """
        async with self._lock:
            triggers: Dict[str, OpticalTrigger] = {}

            # Phase 1: pulse all nodes with their measurement
            for nid, node in self.nodes.items():
                m = measurements.get(nid, 0.0)
                triggers[nid] = node.pulse(m)

            # Phase 2: propagate triggers to neighbors (async, with lag)
            propagation_tasks = []
            for nid, trigger in triggers.items():
                for neighbor in self.nodes[nid].neighbors:
                    propagation_tasks.append(
                        neighbor.receive_propagation(trigger)
                    )
            if propagation_tasks:
                await asyncio.gather(*propagation_tasks, return_exceptions=True)

            # Phase 3: build mesh snapshot
            snap = {
                "type":       "mesh_tick",
                "timestamp":  time.time(),
                "nodes":      {nid: node.state for nid, node in self.nodes.items()},
                "triggers":   {nid: t.to_dict() for nid, t in triggers.items()},
                "wave":       self._compute_wave_front(triggers),
                "sync_order": self._penteract_order(),
                "locked":     self._is_phase_locked(),
            }

            # Ring buffer for sparklines
            self.wave_history.append(snap["wave"])
            if len(self.wave_history) > 200:
                self.wave_history.pop(0)

            return snap

    # ── Wave front computation ────────────────────────────────────────────────
    def _compute_wave_front(self, triggers: Dict[str, OpticalTrigger]) -> dict:
        """
        Describe the propagation wave sweeping the bell.
        Returns phase, amplitude, delay per node for dashboard rendering.
        """
        phases = {nid: t.phase for nid, t in triggers.items()}
        amps   = {nid: t.amplitude for nid, t in triggers.items()}
        delays = {nid: t.step_delay for nid, t in triggers.items()}

        # Phase coherence: 1.0 = fully synchronised, 0.0 = incoherent
        phase_vals = np.array(list(phases.values()))
        r = abs(np.mean(np.exp(1j * phase_vals)))   # Kuramoto order parameter

        return {
            "phases":    {k: round(v, 4) for k, v in phases.items()},
            "amplitudes":{k: round(v, 4) for k, v in amps.items()},
            "delays":    {k: round(v, 1) for k, v in delays.items()},
            "coherence": round(float(r), 4),   # 0–1, target > 0.85 for lock
        }

    # ── Kuramoto order: phase lock detection ──────────────────────────────────
    def _is_phase_locked(self) -> bool:
        phases = np.array([n.phase for n in self.nodes.values()])
        r = abs(np.mean(np.exp(1j * phases)))
        return bool(r > 0.85)

    # ── Canonical penteract propagation order ─────────────────────────────────
    def _penteract_order(self) -> List[str]:
        """
        BFS from W through the 3-6-9 mesh — gives the wave sweep order.
        """
        visited, queue, order = set(), ["W"], []
        while queue:
            nid = queue.pop(0)
            if nid in visited:
                continue
            visited.add(nid)
            order.append(nid)
            queue.extend(nb.id for nb in self.nodes[nid].neighbors if nb.id not in visited)
        return order

    # ── Tune coupling strength across mesh ───────────────────────────────────
    def set_coupling(self, strength: float, node_id: Optional[str] = None):
        strength = float(np.clip(strength, 0.0, 2.0))
        targets  = [self.nodes[node_id]] if node_id else list(self.nodes.values())
        for node in targets:
            node.coupling_strength = strength

    # ── Tune PID for a specific node ─────────────────────────────────────────
    def set_node_pid(self, node_id: str, kp: float = None, ki: float = None,
                     kd: float = None, setpoint: float = None):
        node = self.nodes.get(node_id)
        if not node:
            return
        if kp       is not None: node.pid.kp       = float(kp)
        if ki       is not None: node.pid.ki       = float(ki)
        if kd       is not None: node.pid.kd       = float(kd)
        if setpoint is not None: node.pid.setpoint = float(setpoint)

    # ── Self-heal: reroute around a saturated node ───────────────────────────
    def isolate_node(self, node_id: str):
        """
        Jellyfish reroute — temporarily remove a node from the coupling graph
        without dropping its local PID. Neighbors compensate.
        """
        node = self.nodes.get(node_id)
        if not node:
            return
        for nb in node.neighbors:
            nb.neighbors = [n for n in nb.neighbors if n.id != node_id]
        node.coupling_strength = 0.0
        log.warning("Node %s isolated — mesh rerouted", node_id)

    def restore_node(self, node_id: str):
        node = self.nodes.get(node_id)
        if not node:
            return
        node.coupling_strength = 0.8
        for nb_id in CONNECTIVITY[node_id]:
            nb = self.nodes[nb_id]
            if node not in nb.neighbors:
                nb.neighbors.append(node)
        log.info("Node %s restored to mesh", node_id)


# ── Measurement normaliser ────────────────────────────────────────────────────
def build_measurements(hw_telemetry: dict) -> Dict[str, float]:
    """
    Map raw TFLN telemetry → normalised error signals for each ganglion node.
    Each value is the signed deviation from nominal, used as PID measurement.
    """
    return {
        "W": hw_telemetry.get("biasDrift", 0.0),           # target: 0
        "X": hw_telemetry.get("vpi", 2.4) - 2.4,           # target: Vπ_nominal
        "Y": hw_telemetry.get("driftRate", 3.2) - 3.2,     # target: baseline rate
        "Z": hw_telemetry.get("bandwidth", 100.0) - 100.0, # target: 100 GHz
        "V": hw_telemetry.get("er", 35.0) - 35.0,          # target: 35 dB
    }


# ── Standalone demo ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    async def demo():
        mesh = JellyfishMesh()
        log.info("Jellyfish mesh initialised — 5 nodes, 8 edges, 3-6-9 topology")
        log.info("Connectivity: %s", {k: [n.id for n in mesh.nodes[k].neighbors]
                                      for k in mesh.nodes})

        fake_telem = {
            "biasDrift": 0.012, "vpi": 2.41, "driftRate": 3.4,
            "bandwidth": 98.5,  "er": 34.8,
        }

        for tick_n in range(10):
            measurements = build_measurements(fake_telem)
            snap = await mesh.tick(measurements)
            coherence = snap["wave"]["coherence"]
            order     = snap["sync_order"]
            locked    = snap["locked"]
            log.info(
                "Tick %02d | order: %s | coherence: %.3f | locked: %s",
                tick_n, "→".join(order), coherence, locked
            )
            for nid, ns in snap["nodes"].items():
                log.info(
                    "  [%s] phase=%.3f amp=%.3f err=%.5f delay=%.1fms",
                    nid, ns["phase"], ns["amplitude"],
                    ns["localError"], ns["stepDelay"]
                )
            await asyncio.sleep(0.15)

    asyncio.run(demo())
