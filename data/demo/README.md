# IOF demo data

Sample oscillator state and one demo run for the Intelligent
Oscillator Framework (`docs/intelligent-oscillator-framework.md`).

- `oscillator-state.json` — tick-0 state: 12 oscillators, four node
  types cycled 3x each, phases, frequencies, and the run params.
- `demo-run.json` — 101 records (ticks 0–100): sync, entropy,
  energy, constellation score, and health mode per tick.
- `generate_demo_run.py` — regenerates both files, seed 7.

## Model

12 Kuramoto oscillators, coupling K=0.8, dt=0.1, phase noise 0.05.
Per tick: sync is the order parameter R; entropy is the normalized
Shannon entropy of the 12-bin phase histogram; energy is a demo
proxy — mean `1 - cos(dtheta)` over oscillator pairs, i.e. coupling
effort: high while desynced, near zero at lockstep; score is
`constellation_score` from the IOF Companion Module —
`sync**PHI * entropy**(1/PHI) - 0.3 * energy` — computed from the
rounded columns, so recomputing from the file reproduces the stored
score exactly; mode is the health band from sync (Immaculate >0.8,
Coherent >0.5, Flowing >0.2, else Diffuse).

Note what the run shows: sync locks to ~0.99, entropy collapses
toward 0, and the score falls back toward 0. That is the formula
working as designed — pure lockstep scores nothing, because the
score rewards balance (order times freedom), not order alone.
The framework's target is the middle, not the lock.

## Node types

The four types (stabilizer, explorer, external, noop) are the arena
node classes from the IOF v3 addendum. They label the oscillators
here; the demo dynamics do not yet treat types differently — that
is a modeling step, not hidden in this data.

## Regenerate

`python3 generate_demo_run.py` — deterministic, seed 7, stdlib only.
