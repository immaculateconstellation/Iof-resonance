#!/usr/bin/env python3
"""Generate the IOF demo data in this directory (seed 7).

Regenerates oscillator-state.json (tick-0 state) and demo-run.json
(100 ticks of sync / entropy / energy / constellation score).

Model: 12 Kuramoto oscillators, four node types cycled 3x each
(stabilizer, explorer, external, noop — the arena node classes from
the IOF v3 addendum). Coupling K=0.8, dt=0.1, phase noise 0.05.

Per tick:
  sync    = |mean(exp(i*theta))|           (order parameter R, 0..1)
  entropy = Shannon entropy of the 12-bin phase histogram, / ln(12)
  energy  = mean (1 - cos(dtheta)) over oscillator pairs (coupling
            effort proxy: high while desynced, ~0 at lockstep)
  score   = sync**PHI * entropy**(1/PHI) - 0.3 * energy
            (constellation_score from the IOF Companion Module)
  mode    = health band from sync: >0.8 Immaculate, >0.5 Coherent,
            >0.2 Flowing, else Diffuse

Usage: python3 generate_demo_run.py
"""
import json
import math
import random

PHI = (1 + math.sqrt(5)) / 2
SEED = 7
N = 12
TICKS = 100
K = 0.8
DT = 0.1
NOISE = 0.05
TYPES = ["stabilizer", "explorer", "external", "noop"]

rng = random.Random(SEED)
oscillators = []
for i in range(N):
    oscillators.append({
        "id": i,
        "node_type": TYPES[i % 4],
        "phase": round(2 * math.pi * i / N + rng.uniform(-0.2, 0.2), 6),
        "frequency": round(0.95 + 0.1 * rng.random(), 6),
    })

thetas = [o["phase"] for o in oscillators]
freqs = [o["frequency"] for o in oscillators]

def sync_of(th):
    re = sum(math.cos(t) for t in th) / len(th)
    im = sum(math.sin(t) for t in th) / len(th)
    return math.hypot(re, im)

def entropy_of(th):
    bins = [0] * 12
    for t in th:
        bins[int((t % (2 * math.pi)) / (2 * math.pi) * 12) % 12] += 1
    h = 0.0
    for b in bins:
        if b:
            p = b / len(th)
            h -= p * math.log(p)
    return h / math.log(12)

def energy_of(th):
    # Coupling effort: mean (1 - cos(dtheta)) over all pairs. High when
    # desynced (the coupling is working), ~0 at lockstep. Documented
    # proxy, not a measured joule count.
    total = 0.0
    pairs = 0
    for i in range(len(th)):
        for j in range(i + 1, len(th)):
            total += 1 - math.cos(th[j] - th[i])
            pairs += 1
    return total / pairs

def mode_of(sync):
    if sync > 0.8:
        return "Immaculate"
    if sync > 0.5:
        return "Coherent"
    if sync > 0.2:
        return "Flowing"
    return "Diffuse"

run = []
for tick in range(TICKS + 1):
    dtheta = []
    for i in range(N):
        coupling = sum(math.sin(thetas[j] - thetas[i]) for j in range(N)) / N
        dtheta.append(freqs[i] + K * coupling)
    sync = sync_of(thetas)
    ent = entropy_of(thetas)
    energy = energy_of(thetas)
    # Round first, then score from the rounded values, so anyone
    # recomputing from the file gets exactly the stored score.
    sync_r = round(sync, 4)
    ent_r = round(ent, 4)
    energy_r = round(energy, 4)
    score = sync_r ** PHI * ent_r ** (1 / PHI) - 0.3 * energy_r if ent_r > 0 else -0.3 * energy_r
    run.append({
        "tick": tick,
        "sync": sync_r,
        "entropy": ent_r,
        "energy": energy_r,
        "score": round(score, 4),
        "mode": mode_of(sync),
    })
    for i in range(N):
        thetas[i] += dtheta[i] * DT + NOISE * rng.gauss(0, 1) * DT

state = {
    "seed": SEED,
    "oscillators": oscillators,
    "params": {"coupling": K, "dt": DT, "noise": NOISE, "ticks": TICKS},
    "note": "Tick-0 state. Run generate_demo_run.py to regenerate this file and demo-run.json.",
}
with open("oscillator-state.json", "w") as f:
    json.dump(state, f, indent=2)
with open("demo-run.json", "w") as f:
    json.dump({"seed": SEED, "ticks": run}, f, indent=2)
print(f"wrote {len(run)} ticks; sync {run[0]['sync']} -> {run[-1]['sync']}, "
      f"score {run[0]['score']} -> {run[-1]['score']}, final mode {run[-1]['mode']}")
