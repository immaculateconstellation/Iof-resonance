#!/usr/bin/env python3
"""Software-only comparison for the IOF v2 associative-resonance proposal.

This is a transparent numerical baseline, not a quantum-optical simulator.
It compares:
  * exact lookup by nearest stored pattern,
  * a classical asynchronous Hopfield network, and
  * a spin-glass-inspired network with quenched symmetric coupling disorder.

The protocol uses bipolar (+1/-1) patterns, masks 30% of each query by default,
and records recall fidelity, false-attractor rate, and relaxation cost. Every
random process is seeded and all reported settings are included in JSON output.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0


@dataclass(frozen=True)
class Protocol:
    n_units: int = 32
    n_patterns: int = 6
    partial_fraction: float = 0.30
    trials_per_pattern: int = 20
    seeds: tuple[int, ...] = (7, 19, 31)
    max_steps: int = 80
    disorder_strength: float = 0.18
    threshold: float = 0.90


@dataclass(frozen=True)
class Trial:
    model: str
    seed: int
    target: int
    fidelity: float
    exact_recall: bool
    false_attractor: bool
    steps: int


def _validate_protocol(protocol: Protocol) -> None:
    if protocol.n_units < 4 or protocol.n_patterns < 1:
        raise ValueError("n_units must be >= 4 and n_patterns must be positive")
    if not 0.0 <= protocol.partial_fraction <= 1.0:
        raise ValueError("partial_fraction must be in [0, 1]")
    if protocol.trials_per_pattern < 1 or protocol.max_steps < 1:
        raise ValueError("trials_per_pattern and max_steps must be positive")
    if protocol.disorder_strength < 0.0:
        raise ValueError("disorder_strength must be non-negative")


def generate_patterns(n_patterns: int, n_units: int, rng: np.random.Generator) -> np.ndarray:
    """Generate unique bipolar patterns without hidden global state."""
    patterns: list[np.ndarray] = []
    seen: set[tuple[int, ...]] = set()
    while len(patterns) < n_patterns:
        candidate = rng.choice(np.array([-1, 1], dtype=np.int8), size=n_units)
        key = tuple(int(x) for x in candidate)
        if key not in seen:
            seen.add(key)
            patterns.append(candidate)
    return np.asarray(patterns, dtype=np.int8)


def make_partial_query(target: np.ndarray, partial_fraction: float, rng: np.random.Generator) -> np.ndarray:
    """Mask a fixed fraction of symbols with 0; observed symbols remain exact."""
    query = target.astype(np.int8, copy=True)
    n_mask = int(round(query.size * partial_fraction))
    if n_mask:
        masked = rng.choice(query.size, size=n_mask, replace=False)
        query[masked] = 0
    return query


def fidelity(state: np.ndarray, target: np.ndarray) -> float:
    return float(np.mean(state == target))


def nearest_pattern(state: np.ndarray, patterns: np.ndarray) -> tuple[int, float]:
    scores = np.mean(patterns == state, axis=1)
    index = int(np.argmax(scores))
    return index, float(scores[index])


def exact_lookup(query: np.ndarray, patterns: np.ndarray) -> tuple[np.ndarray, int, int]:
    """Return nearest stored pattern; masked positions do not affect distance."""
    observed = query != 0
    if not np.any(observed):
        index = 0
    else:
        distances = np.sum(patterns[:, observed] != query[observed], axis=1)
        index = int(np.argmin(distances))
    return patterns[index].copy(), index, 0


def hebbian_weights(patterns: np.ndarray) -> np.ndarray:
    n_units = patterns.shape[1]
    weights = (patterns.T @ patterns).astype(float) / n_units
    np.fill_diagonal(weights, 0.0)
    return weights


def spin_glass_weights(
    patterns: np.ndarray, rng: np.random.Generator, disorder_strength: float
) -> np.ndarray:
    """Embed memories plus quenched symmetric disorder in an Ising coupling matrix.

    The random term is a deliberately simple software proxy for frustrated,
    disordered couplings. It is not a model of cavity QED, atom-photon dynamics,
    or any experimentally calibrated optical device.
    """
    base = hebbian_weights(patterns)
    noise = rng.normal(0.0, 1.0, size=base.shape)
    noise = (noise + noise.T) / 2.0
    np.fill_diagonal(noise, 0.0)
    return base + disorder_strength * noise / math.sqrt(patterns.shape[1])


def relax(
    query: np.ndarray,
    weights: np.ndarray,
    max_steps: int,
    rng: np.random.Generator,
    temperature: float = 0.0,
) -> tuple[np.ndarray, int]:
    """Asynchronously relax a partially observed state to a binary attractor."""
    state = np.where(query == 0, 1, query).astype(np.int8)
    free = np.flatnonzero(query == 0)
    if free.size == 0:
        return state, 0

    # A golden-ratio decay is retained as a named, inspectable schedule parameter;
    # it is not a physical claim about optical timing.
    for step in range(1, max_steps + 1):
        changed = False
        for unit in rng.permutation(free):
            field = float(weights[unit] @ state)
            if temperature > 0.0:
                field += float(rng.normal(0.0, temperature * (PHI ** (-step / 10.0))))
            proposed = np.int8(1 if field >= 0.0 else -1)
            if proposed != state[unit]:
                state[unit] = proposed
                changed = True
        if not changed:
            return state, step
    return state, max_steps


def run_seed(protocol: Protocol, seed: int) -> list[Trial]:
    rng = np.random.default_rng(seed)
    patterns = generate_patterns(protocol.n_patterns, protocol.n_units, rng)
    hopfield = hebbian_weights(patterns)
    spin_rng = np.random.default_rng(seed + 1_000_003)
    spin = spin_glass_weights(patterns, spin_rng, protocol.disorder_strength)
    trials: list[Trial] = []

    models: Iterable[tuple[str, Callable[[np.ndarray, np.random.Generator], tuple[np.ndarray, int]]]] = (
        ("exact_lookup", lambda query, local: (exact_lookup(query, patterns)[0], 0)),
        ("hopfield", lambda query, local: relax(query, hopfield, protocol.max_steps, local)),
        ("spin_glass_inspired", lambda query, local: relax(query, spin, protocol.max_steps, local, temperature=0.035)),
    )
    for target_index, target in enumerate(patterns):
        for trial_index in range(protocol.trials_per_pattern):
            query = make_partial_query(target, protocol.partial_fraction, rng)
            for model_index, (name, infer) in enumerate(models):
                local_rng = np.random.default_rng(seed * 100_000 + target_index * 1_000 + trial_index * 10 + model_index)
                state, steps = infer(query, local_rng)
                if name == "exact_lookup":
                    steps = 0
                recovered_index, _ = nearest_pattern(state, patterns)
                score = fidelity(state, target)
                trials.append(
                    Trial(
                        model=name,
                        seed=seed,
                        target=target_index,
                        fidelity=score,
                        exact_recall=bool(recovered_index == target_index),
                        false_attractor=bool(recovered_index != target_index),
                        steps=int(steps),
                    )
                )
    return trials


def summarize(trials: list[Trial]) -> list[dict[str, object]]:
    grouped: dict[str, list[Trial]] = {}
    for trial in trials:
        grouped.setdefault(trial.model, []).append(trial)
    rows: list[dict[str, object]] = []
    for model in sorted(grouped):
        items = grouped[model]
        rows.append(
            {
                "model": model,
                "trials": len(items),
                "mean_recall_fidelity": round(float(np.mean([x.fidelity for x in items])), 6),
                "exact_recall_rate": round(float(np.mean([x.exact_recall for x in items])), 6),
                "false_attractor_rate": round(float(np.mean([x.false_attractor for x in items])), 6),
                "mean_relaxation_steps": round(float(np.mean([x.steps for x in items])), 6),
            }
        )
    return rows


def run(protocol: Protocol) -> dict[str, object]:
    _validate_protocol(protocol)
    trials = [trial for seed in protocol.seeds for trial in run_seed(protocol, seed)]
    return {
        "status": "software_baseline_only",
        "interpretation": "No optical, quantum, or hardware performance is measured.",
        "protocol": asdict(protocol),
        "summary": summarize(trials),
        "trials": [asdict(trial) for trial in trials],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write complete results as JSON")
    parser.add_argument("--csv", type=Path, help="Write per-trial results as CSV")
    parser.add_argument("--n-patterns", type=int, default=6)
    parser.add_argument("--trials-per-pattern", type=int, default=20)
    parser.add_argument("--partial-fraction", type=float, default=0.30)
    parser.add_argument("--seed", type=int, action="append", dest="seeds")
    args = parser.parse_args()
    protocol = Protocol(
        n_patterns=args.n_patterns,
        trials_per_pattern=args.trials_per_pattern,
        partial_fraction=args.partial_fraction,
        seeds=tuple(args.seeds) if args.seeds else Protocol.seeds,
    )
    result = run(protocol)
    print(json.dumps({"protocol": result["protocol"], "summary": result["summary"]}, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as handle:
            rows = result["trials"]
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
