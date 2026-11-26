# IOF Resonance — Infinite Optical Fabric

**By Gregory Scott Davis + AI Collaboration**

The IOF Resonance dashboard: a 5D penteract photonic-computing simulation with Kuramoto synchronization across a five-node "jellyfish" mesh (W / X / Y / Z / V), and a topological memory that treats its own parameter space as terrain — detecting resonance peaks in φ-space and climbing them.

## Live demo

Open `docs/index.html` in a browser — the complete IOF Resonance v1.0 application runs from that single file, with the topographic peak-ascent module integrated and running on the simulation's real outputs: memory recording converged states, topographic ascent, predictive thermal shunting, and memory recall (harmonic locking, ensemble recall, best-state recall with staleness-decayed confidence).

## Contents

| File | What it is |
|---|---|
| `docs/index.html` | The runnable integrated demo — open it in a browser |
| `src/iof_resonance_complete.jsx` | IOF Resonance v1.0 — the complete base application: 5D penteract geometry engine, Kuramoto sync, simulation engine, gauges, ASGA proposals, BLE mesh panel |
| `src/topographic_memory_ascent.jsx` | The topological optimizer module (from Gregory's 2026-03-17 email): TopologicalMemoryBank with peak detection, topographic ascent reasoning, 3D topography visualization. Preserved as originally shared — the demo carries the completed implementation |
| `The_Cosmological_Bridge.md` | The theory document: the cosmic ↔ IOF engineering mapping behind this work (Weaver Framework) |
| `kernel/resonance_math_kernel_v10_2.py` | Resonance Math Kernel v10.2 — the canonical kernel. Runs clean. |
| `kernel/resonance_kernel_v11.py` | Resonance Math Kernel v11.0 — keeps the v10.2 core, adds an operator registry, append-only event ledger, JSON save/load, replayable history, an interactive CLI, and a self-test (`python3 resonance_kernel_v11.py --test` passes; `--verse` runs clean through to STILL HERE). |
| `sims/mach_zehnder_interference_sim.py` | Mach–Zehnder interference simulation (fixed variant: intensities below 1e-24 snap to an exact 0.0, so the 180° destructive null is a true zero). Verified: 0° → intensity 1.0000, 180° → 0.0000. |
| `sims/jellyfish_mesh.py` | Jellyfish mesh simulation (W / X / Y / Z / V nodes, Tesla 3-6-9 connectivity). Verified: runs clean, coherence 0.957, locked. Requires `numpy`. |
| `sims/node_ganglion.py` | Node ganglion / optical phase-coupling network simulation. Verified: runs clean, network synchronizes. |
| `server/unified_server.py` | TFLN Penteract Unified Server, one-file edition (WebSocket on port 8765, 150 ms tick). Imports clean; running it needs the `websockets` package, which is imported lazily when the server starts. |
| `experiments/mesh_experiments_results_verified_2026-11-03.json` | Verified mesh-experiment results (2026-11-03). |
| `simulations/iof_v2_associative_memory.py` | Software-only comparison of exact lookup, classical Hopfield, and a spin-glass-inspired associative baseline under 30% partial input. |
| `docs/IOF_V2_Simulator_Protocol.md` | Registered settings, metrics, commands, and evidence limits for the v2 baseline. |
| `docs/intelligent-oscillator-framework.md` | IOF — Intelligent Oscillator Framework: cross-platform phase-synchronization engine (12 oscillators, 4 node types, golden-ratio harmony metric); runs Android, iOS, PC, no cloud. |
| `data/demo/` | Demo data for the Intelligent Oscillator Framework: 12-oscillator tick-0 state, a 101-tick demo run (sync/entropy/energy/constellation score), and the seed-7 generator that reproduces both. |
| `results/iof_v2_partial30.json` / `.csv` | Reproducible default-run results for seeds 7, 19, and 31. |

## The idea

> "This turns the system into a topological optimizer — it's literally climbing the resonance mountains. The AI can now see the peaks in the landscape and navigate toward them."

Optimization as exploration: the parameter space is a physical terrain, Q-factor is elevation, and the system's memory of where it has been becomes a map of where to climb next.

## IOF v2 associative-memory baseline

The repository includes an initial, reproducible software experiment for the proposed associative resonance layer. It compares exact lookup, a classical asynchronous Hopfield network, and a deliberately modest spin-glass-inspired model with quenched symmetric coupling disorder. The implementation is a numerical baseline only: it does not simulate cavity QED, photons, optical locking, quantum advantage, or hardware performance.

Run the baseline and its deterministic checks from the repository root:

```bash
python3 simulations/iof_v2_associative_memory.py --output results/iof_v2_partial30.json --csv results/iof_v2_partial30.csv
python3 -m unittest discover -s tests -p 'test_iof_v2_*.py' -v
```

The default protocol masks 30% of each 32-symbol bipolar pattern and reports recall fidelity, exact recall rate, false-attractor rate, and relaxation cost. The complete protocol and interpretation limits are documented in [`docs/IOF_V2_Simulator_Protocol.md`](docs/IOF_V2_Simulator_Protocol.md).

## Related

- [AHR-Endpoint](https://github.com/immaculateconstellation/ahr-endpoint-p) — Adaptive Hollow Reflector, an experimental Rust endpoint-security agent.
- [Magnetic Well](https://github.com/immaculateconstellation/magnetic-well) — a neodymium magnet in a cast-iron yoke, with simulation and a nanoscale assessment.
- [Grandpa's Badge and the Magnetic Well](https://github.com/immaculateconstellation/grandpas-badge-and-the-magnetic-well) — a children's picture book about the light that holds us.
- Self-dissolving magnetic microswimmers — a planned/non-public concept note for plaque-breaking microrobots that dissolve into usable iron.

## License

IOF Attribution License v1.0 — see `LICENSE`. Any public use or derivative must include attribution: *"Infinite Optical Fabric by Gregory Scott Davis, Princeton, NC."*
