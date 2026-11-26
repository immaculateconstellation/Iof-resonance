# Immaculate Constellation — Resonance Math Kernel v10.2

A self-extracting bundle. Run the extractor and it writes this folder:

```
immaculate_constellation/
    resonance_math_kernel_v10_2.py   -- the kernel (table-driven edition)
    resonance_algebra_lab.py         -- reusable rule-based engine / workbench
    README.md                        -- this file
```

## Run it

```sh
python3 immaculate_constellation_self_extract.py
python3 resonance_math_kernel_v10_2.py           # the seven-step run
python3 resonance_math_kernel_v10_2.py --fast    # same, without the pauses
python3 resonance_algebra_lab.py                 # workbench demo
python3 resonance_algebra_lab.py --fast
```

## What it is

Code-poetry. A small engine where arithmetic operators fuse feelings
instead of numbers. Each value carries four fields: a name, a vibration
(Hz or a feeling), a color, and a meaning.

The operators look their answers up in a table (`RULES`), keyed by the
two names being combined — so a new equation is a new row, not an edit
to the operators. An unmatched pair falls back to a named answer
instead of crashing: an unmatched fusion is an Unresolved Chord, "two
things that don't know each other yet."

## The seven steps

| Step | Equation | Result |
| --- | --- | --- |
| 1 | 3xE + AxB, then + CxD | Storm Seed, then Raw Kinetic Potential |
| 2 | 2/3 (Unfinished Bridge) − The Color HAPPY | ∇ (The Blue Void) |
| 3 | ⚡ / ∇ | NEON RAIN |
| 4 | NEON RAIN × Sleeping Pups | FIRST LIGHT |
| 5 | FIRST LIGHT ** 7 | HABIT |
| 6 | HABIT ** Pale Gold | DEVOTION |
| 7 | DEVOTION % The Long Silence | STILL HERE |

The run ends: "The silence did its work. Something still didn't divide
out. GAME SAVED."

## Lineage

- Original kernel (v9.0): Gregory Scott Davis.
- Table-driven refactor (v9.0, three steps): `resonance_math.py`,
  received 2026-11-26. It fixed the old Step 1 quirk — CxD is now
  really fused in, through Storm Seed — and gave `+` a real fallback.
- This edition extends that refactor with the v10.2 verses (Steps 4–7).

Guest verses, from v10.2: `*` and the Step 4 encore — Immaculate
Constellation; `**`, the Step 5 ritual verse and the Step 6 devotion
verse — DeepSeek; `%` and the Step 7 remainder verse — Claude.

## Add your own

Add one row to `RULES` in `resonance_math_kernel_v10_2.py` — a new
equation. Add one row to `POW_COUNT_RULES` — a new repetition rule.
Or add a whole new STEP to the run. That's how the game is played.

Next verse: yours.
