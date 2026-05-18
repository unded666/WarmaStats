import unittest

import numpy as np

from Analyse_Results import analyse_results, analyze_results


class TestAnalyseResults(unittest.TestCase):
    """Unit tests for simulation result analysis helpers."""

    def test_damage_analysis_outputs_expectation_and_distributions(self):
        """Damage mode should produce sorted distributions and expected mean."""
        results = [0.0, 1.0, 1.0, 2.5]

        analysis = analyse_results(results, analysis_type="damage")

        self.assertEqual(analysis["metric"], "damage")
        self.assertAlmostEqual(analysis["expectation"], 1.125)
        self.assertEqual(analysis["probability_distribution"]["values"], [0.0, 1.0, 2.5])
        self.assertEqual(analysis["probability_distribution"]["probabilities"], [0.25, 0.5, 0.25])
        self.assertEqual(
            analysis["cumulative_distribution"]["cumulative_probabilities"],
            [0.25, 0.75, 1.0],
        )

    def test_auto_detects_casualties_for_non_negative_integers(self):
        """Auto mode should classify non-negative integer outputs as casualties."""
        analysis = analyse_results([0, 1, 1, 2], analysis_type="auto")

        self.assertEqual(analysis["metric"], "casualties")
        self.assertAlmostEqual(analysis["expectation"], 1.0)

    def test_alias_returns_same_structure(self):
        """US-English alias should behave the same as the main function."""
        results = np.array([0.0, 2.0, 2.0])

        analysis_main = analyse_results(results, analysis_type="damage")
        analysis_alias = analyze_results(results, analysis_type="damage")

        self.assertEqual(analysis_main, analysis_alias)

    def test_rejects_empty_input(self):
        """An empty result set should raise a helpful error."""
        with self.assertRaises(ValueError):
            analyse_results([], analysis_type="auto")

    def test_rejects_invalid_analysis_type(self):
        """Unknown analysis types should raise a helpful error."""
        with self.assertRaises(ValueError):
            analyse_results([1, 2, 3], analysis_type="unknown")


if __name__ == "__main__":
    unittest.main()

