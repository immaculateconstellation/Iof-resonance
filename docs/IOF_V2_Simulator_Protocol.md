# IOF v2 software simulator protocol

**Status:** Initial software baseline; not a quantum-optical simulation and not a validated IOF result.

This experiment operationalizes the v2 research note's first falsifiable step. It compares three equal-size software systems over the same bipolar pattern corpus:

1. **Exact lookup** — nearest stored pattern using only the observed symbols.
2. **Classical Hopfield** — asynchronous sign updates using a Hebbian coupling matrix.
3. **Spin-glass-inspired** — the same associative coupling matrix plus quenched symmetric random disorder and a small deterministic temperature schedule.

The third model is intentionally modest. It is a computational proxy for disordered/frustrated couplings, not a model of atoms, photons, cavity-QED, optical locking, or a physical IOF device.

## Registered defaults

- 32 binary units
- 6 stored patterns
- 30% of each query masked (`0` means unobserved; observed symbols are not corrupted)
- 20 trials per stored pattern
- seeds `7, 19, 31`
- maximum 80 asynchronous relaxation sweeps
- spin-glass disorder strength `0.18`
- exact recall means the recovered state is closest to the target stored pattern

The 30% condition is therefore defined as **30% partial input**, not 30% symbol-flip noise. A later protocol should add a separately registered noisy-input arm rather than silently combining the two conditions.

## Run

From the repository root:

```bash
python3 simulations/iof_v2_associative_memory.py \
  --output results/iof_v2_partial30.json \
  --csv results/iof_v2_partial30.csv
```

Run the deterministic checks without third-party test dependencies:

```bash
python3 -m unittest discover -s tests -p 'test_iof_v2_*.py' -v
```

The JSON includes the full protocol, per-model summary, and every trial. The CSV is intended for later plotting or statistical review.

## Metrics

- **Recall fidelity:** fraction of final binary symbols matching the target pattern.
- **Exact recall rate:** fraction whose nearest stored pattern is the target.
- **False-attractor rate:** fraction whose nearest stored pattern is not the target.
- **Mean relaxation steps:** computational cost proxy for the iterative models; exact lookup is zero.

Capacity is not inferred from one run. A capacity sweep must vary stored-pattern count at fixed unit count and report the complete recall curve at a pre-registered threshold. The current script's `n_patterns` option supports that sweep, but no capacity claim is made by the default run.

## Evidence boundary

This simulator can test whether one simple disordered associative software model behaves differently from exact lookup and a classical Hopfield baseline under the registered input condition. It cannot establish quantum advantage, optical storage time, cavity performance, photonic scalability, or hardware feasibility. Any improvement or failure should be reported as a result of this numerical model only.
