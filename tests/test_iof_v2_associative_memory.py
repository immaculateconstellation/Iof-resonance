#!/usr/bin/env python3
"""Standard-library tests for the IOF v2 software baseline."""

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np

MODULE_PATH = Path(__file__).parents[1] / "simulations" / "iof_v2_associative_memory.py"
SPEC = importlib.util.spec_from_file_location("iof_v2_associative_memory", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class IOFV2Tests(unittest.TestCase):
    def test_protocol_is_reproducible(self) -> None:
        protocol = MODULE.Protocol(n_patterns=4, trials_per_pattern=3, seeds=(7, 19))
        first = MODULE.run(protocol)
        second = MODULE.run(protocol)
        self.assertEqual(first, second)

    def test_partial_query_has_requested_mask(self) -> None:
        target = np.ones(10, dtype=np.int8)
        query = MODULE.make_partial_query(target, 0.30, np.random.default_rng(4))
        self.assertEqual(int(np.sum(query == 0)), 3)
        self.assertTrue(np.all(query[query != 0] == 1))

    def test_exact_lookup_recovers_unique_partial_match(self) -> None:
        patterns = np.asarray(
            [[1, 1, 1, 1], [-1, -1, -1, -1], [1, -1, 1, -1]], dtype=np.int8
        )
        state, index, steps = MODULE.exact_lookup(np.asarray([1, 0, 1, 0], dtype=np.int8), patterns)
        self.assertEqual(index, 0)
        self.assertEqual(steps, 0)
        np.testing.assert_array_equal(state, patterns[0])

    def test_summary_contains_registered_metrics(self) -> None:
        result = MODULE.run(MODULE.Protocol(n_patterns=2, trials_per_pattern=2, seeds=(7,)))
        self.assertEqual(result["status"], "software_baseline_only")
        self.assertEqual(len(result["summary"]), 3)
        for row in result["summary"]:
            self.assertIn("mean_recall_fidelity", row)
            self.assertIn("false_attractor_rate", row)
            self.assertIn("mean_relaxation_steps", row)


if __name__ == "__main__":
    unittest.main()
