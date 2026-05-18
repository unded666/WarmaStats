import unittest
from unittest.mock import patch

from web_app import app


class TestWebApp(unittest.TestCase):
    """Basic tests for the web UI endpoints."""

    def setUp(self):
        self.client = app.test_client()

    def test_index_get_renders_form(self):
        """GET / should render the parameter form."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WarmaStats Experiment Runner", response.data)
        self.assertIn(b"Run Experiment", response.data)

    @patch("web_app.run_wm_analytics")
    def test_index_post_runs_experiment_and_renders_results(self, mock_run_wm_analytics):
        """POST / should call analytics and render returned metric/output."""
        mock_run_wm_analytics.return_value = {
            "metric": "damage",
            "expectation": 1.25,
            "probability_distribution": {
                "values": [0, 1, 2],
                "probabilities": [0.2, 0.3, 0.5],
            },
            "cumulative_distribution": {
                "values": [0, 1, 2],
                "cumulative_probabilities": [0.2, 0.5, 1.0],
            },
            "simulated_results": [0, 1, 2, 2],
            "parameters": {},
        }

        response = self.client.post(
            "/",
            data={
                "defence": "10",
                "attack": "3",
                "power": "5",
                "armour": "2",
                "n_attacks": "1",
                "n_tests": "100",
                "to_hit_dice": "2",
                "damage_dice": "2",
                "infantry_wounds": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"damage", response.data)
        self.assertIn(b"1.2", response.data)
        self.assertIn(b"probability distribution function (PDF)", response.data)
        self.assertIn(b"Probability of at least X", response.data)
        self.assertIn(b"PDF:", response.data)
        self.assertIn(b"%:", response.data)
        mock_run_wm_analytics.assert_called_once()


if __name__ == "__main__":
    unittest.main()

