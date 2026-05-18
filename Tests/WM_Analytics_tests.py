import unittest
from unittest.mock import Mock, patch

import numpy as np

from WM_Analytics import run_wm_analytics


class TestWMAnalytics(unittest.TestCase):
    """Unit tests for analytics orchestration."""

    @patch("WM_Analytics.experiment")
    def test_run_wm_analytics_returns_damage_analysis_for_non_infantry(self, mock_experiment):
        """Non-infantry simulations should return damage metric and full results."""
        fake_runner = Mock()
        fake_runner.run_experiment.return_value = np.array([0.0, 1.0, 1.0, 2.0])
        mock_experiment.return_value = fake_runner

        output = run_wm_analytics(
            defence=12,
            attack=3,
            power=5,
            armour=2,
            n_attacks=2,
            n_tests=4,
            to_hit_dice=2,
            damage_dice=2,
        )

        self.assertEqual(output["metric"], "damage")
        self.assertAlmostEqual(output["expectation"], 1.0)
        self.assertEqual(output["simulated_results"], [0.0, 1.0, 1.0, 2.0])
        self.assertEqual(output["parameters"]["n_tests"], 4)
        self.assertEqual(output["probability_distribution"]["values"], [0.0, 1.0, 2.0])
        self.assertEqual(output["cumulative_distribution"]["cumulative_probabilities"][-1], 1.0)

    @patch("WM_Analytics.experiment")
    def test_run_wm_analytics_returns_casualties_metric_for_infantry(self, mock_experiment):
        """Infantry simulations should analyze results as casualties."""
        fake_runner = Mock()
        fake_runner.run_experiment.return_value = np.array([0, 1, 1, 2])
        mock_experiment.return_value = fake_runner

        output = run_wm_analytics(
            defence=10,
            attack=4,
            power=6,
            armour=1,
            n_attacks=3,
            n_tests=4,
            infantry_wounds=2,
        )

        self.assertEqual(output["metric"], "casualties")
        self.assertAlmostEqual(output["expectation"], 1.0)
        self.assertEqual(output["parameters"]["infantry_wounds"], 2)

    @patch("WM_Analytics.experiment")
    def test_run_wm_analytics_passes_user_choices_to_experiment(self, mock_experiment):
        """User input parameters should be forwarded to experiment construction."""
        fake_runner = Mock()
        fake_runner.run_experiment.return_value = np.array([0.0])
        mock_experiment.return_value = fake_runner

        run_wm_analytics(
            defence=8,
            attack=1,
            power=2,
            armour=3,
            n_attacks=5,
            n_tests=6,
            to_hit_dice=3,
            damage_dice=4,
            infantry_wounds=2,
            charge_attack=True,
            cavalry_charge=True,
        )

        mock_experiment.assert_called_once_with(
            defence=8,
            attack=1,
            power=2,
            armour=3,
            odd_parameters={
                "to_hit_dice": 3,
                "damage_dice": 4,
                "charge_attack": True,
                "cavalry_charge": True,
                "infantry_wounds": 2,
            },
            n_attacks=5,
            n_tests=6,
        )


if __name__ == "__main__":
    unittest.main()

