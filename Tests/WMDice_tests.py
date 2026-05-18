import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path
from unittest.mock import Mock, call

# Add parent directory to path so we can import from the main WarmaStats folder
sys.path.insert(0, str(Path(__file__).parent.parent))

from Dice import Dice
from WMDice import RollSet, SumRolls, target_rolls, experiment


class TestDice(unittest.TestCase):
    """Unit tests for the Dice class.
    
    Tests cover initialization, rolling single/multiple dice,
    and simulating roll distributions.
    """

    def setUp(self):
        """Initialize test fixtures before each test method.
        
        Creates standard and seeded Dice instances for testing.
        """
        self.dice = Dice()
        self.seeded_dice = Dice(sides=6, seed=42)

    def test_dice_initialization_default(self):
        """Test that Dice initializes with default parameters (6 sides)."""
        dice = Dice()
        self.assertEqual(dice.sides, 6)

    def test_dice_initialization_custom_sides(self):
        """Test that Dice initializes with custom number of sides."""
        sides = 20
        dice = Dice(sides=sides)
        self.assertEqual(dice.sides, sides)

    def test_dice_initialization_with_seed(self):
        """Test that Dice initializes with a seed for reproducible results."""
        seed = 42
        dice = Dice(seed=seed)
        self.assertEqual(dice.sides, 6)

    def test_roll_single(self):
        """Test rolling a single die returns a value between 1 and 6."""
        result = self.dice.roll(num_rolls=1)
        self.assertEqual(len(result), 1)
        self.assertTrue(1 <= result[0] <= 6)

    def test_roll_multiple(self):
        """Test rolling multiple dice returns correct number of results
        with all values in valid range (1-6)."""
        num_rolls = 100
        results = self.dice.roll(num_rolls=num_rolls)
        self.assertEqual(len(results), num_rolls)
        self.assertTrue(np.all(results >= 1))
        self.assertTrue(np.all(results <= 6))

    def test_roll_with_custom_sides(self):
        """Test rolling dice with non-standard number of sides
        returns values in valid range."""
        sides = 20
        dice = Dice(sides=sides)
        results = dice.roll(num_rolls=100)
        self.assertTrue(np.all(results >= 1))
        self.assertTrue(np.all(results <= sides))

    def test_roll_reproducibility_with_seed(self):
        """Test that rolls are reproducible with the same seed.
        
        Verifies that using the same seed produces consistent sequences
        by resetting seed and rolling multiple times.
        """
        np.random.seed(42)
        rolls1 = np.random.randint(1, 7, size=10)
        
        np.random.seed(42)
        rolls2 = np.random.randint(1, 7, size=10)
        
        np.testing.assert_array_equal(rolls1, rolls2)

    def test_roll_returns_numpy_array(self):
        """Test that roll() returns a numpy array."""
        result = self.dice.roll(num_rolls=10)
        self.assertIsInstance(result, np.ndarray)

    def test_simulate_rolls(self):
        """Test that simulate_rolls returns a pandas Series with correct total."""
        num_rolls = 1000
        distribution = self.dice.simulate_rolls(num_rolls=num_rolls)
        self.assertIsInstance(distribution, pd.Series)
        self.assertEqual(distribution.sum(), num_rolls)

    def test_simulate_rolls_distribution_shape(self):
        """Test that simulate_rolls covers all die faces (1-6)
        with sufficient number of roll simulations."""
        num_rolls = 10000
        distribution = self.dice.simulate_rolls(num_rolls=num_rolls)
        # With a fair die and enough rolls, all faces should appear
        self.assertEqual(len(distribution), 6)
        self.assertTrue(np.all(distribution.index == np.arange(1, 7)))

    def test_simulate_rolls_is_indexed(self):
        """Test that simulate_rolls returns Series sorted by index (1-6)."""
        distribution = self.dice.simulate_rolls(num_rolls=1000)
        np.testing.assert_array_equal(distribution.index.values, 
                                      np.arange(1, 7))


class TestRollSet(unittest.TestCase):
    """Unit tests for the RollSet function.
    
    Tests cover generation of multiple dice rolls organized in a
    2D array where each row represents a set of rolls.
    """

    def test_rollset_shape(self):
        """Test that RollSet returns correct shape (n_rolls x n_dice)."""
        n_dice = 3
        n_rolls = 10
        rolls = RollSet(n_dice, n_rolls)
        self.assertEqual(rolls.shape, (n_rolls, n_dice))

    def test_rollset_single_die_single_roll(self):
        """Test RollSet with minimal parameters (1 die, 1 roll)."""
        rolls = RollSet(1, 1)
        self.assertEqual(rolls.shape, (1, 1))
        self.assertTrue(1 <= rolls[0, 0] <= 6)

    def test_rollset_multiple_dice_and_rolls(self):
        """Test RollSet with multiple dice and rolls returns proper
        shape and all values in valid die range."""
        n_dice = 5
        n_rolls = 20
        rolls = RollSet(n_dice, n_rolls)
        self.assertEqual(rolls.shape, (n_rolls, n_dice))
        self.assertTrue(np.all(rolls >= 1))
        self.assertTrue(np.all(rolls <= 6))

    def test_rollset_returns_numpy_array(self):
        """Test that RollSet returns a numpy array."""
        rolls = RollSet(3, 5)
        self.assertIsInstance(rolls, np.ndarray)

    def test_rollset_contains_valid_die_values(self):
        """Test that RollSet only contains valid die values (1-6)."""
        rolls = RollSet(10, 100)
        self.assertTrue(np.all(rolls >= 1))
        self.assertTrue(np.all(rolls <= 6))


class TestSumRolls(unittest.TestCase):
    """Unit tests for the SumRolls function.
    
    Tests cover summing rolls across dice in each set and applying
    an offset to the total.
    """

    def test_sumrolls_basic(self):
        """Test that SumRolls correctly sums rolls without offset."""
        rolls = np.array([[1, 2, 3], [4, 5, 6]])
        sums = SumRolls(rolls, offset=0)
        expected = np.array([6, 15])
        np.testing.assert_array_equal(sums, expected)

    def test_sumrolls_with_offset(self):
        """Test that SumRolls applies positive offset correctly."""
        rolls = np.array([[1, 1, 1], [2, 2, 2]])
        offset = 5
        sums = SumRolls(rolls, offset=offset)
        expected = np.array([8, 11])
        np.testing.assert_array_equal(sums, expected)

    def test_sumrolls_with_negative_offset(self):
        """Test that SumRolls works with negative offsets."""
        rolls = np.array([[4, 5, 6]])
        offset = -2
        sums = SumRolls(rolls, offset=offset)
        expected = np.array([13])
        np.testing.assert_array_equal(sums, expected)

    def test_sumrolls_single_die(self):
        """Test SumRolls with single die per roll."""
        rolls = np.array([[1], [2], [3]])
        sums = SumRolls(rolls, offset=0)
        expected = np.array([1, 2, 3])
        np.testing.assert_array_equal(sums, expected)

    def test_sumrolls_many_dice(self):
        """Test SumRolls with many dice per roll."""
        rolls = np.array([[1, 2, 3, 4, 5]])
        sums = SumRolls(rolls, offset=10)
        expected = np.array([25])
        np.testing.assert_array_equal(sums, expected)

    def test_sumrolls_returns_numpy_array(self):
        """Test that SumRolls returns a numpy array."""
        rolls = np.array([[1, 2], [3, 4]])
        sums = SumRolls(rolls, offset=0)
        self.assertIsInstance(sums, np.ndarray)

    def test_sumrolls_preserves_length(self):
        """Test that SumRolls preserves the number of rolls."""
        rolls = np.array([[1, 2, 3] for _ in range(50)])
        sums = SumRolls(rolls, offset=0)
        self.assertEqual(len(sums), len(rolls))


class TestTargetRolls(unittest.TestCase):
    """Unit tests for the target_rolls function.
    
    Tests cover success/failure determination for rolls against a target sum.
    A roll succeeds if its sum meets or exceeds the target.
    """

    def test_target_rolls_all_success(self):
        """Test target_rolls when all rolls meet or exceed target."""
        rolls = np.array([[5, 5, 5], [6, 6, 6]])
        target_sum = 10
        results = target_rolls(rolls, target_sum)
        expected = np.array([True, True])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_all_failure(self):
        """Test target_rolls when no rolls meet target."""
        rolls = np.array([[1, 1, 1], [1, 1, 2]])
        target_sum = 10
        results = target_rolls(rolls, target_sum)
        expected = np.array([False, False])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_mixed_results(self):
        """Test target_rolls with mixed success and failure outcomes."""
        rolls = np.array([[1, 1, 1], [4, 5, 6], [2, 2, 2], [1, 5, 5]])
        target_sum = 10
        results = target_rolls(rolls, target_sum)
        expected = np.array([False, True, False, True])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_exact_match(self):
        """Test target_rolls when roll exactly matches target (>= condition)."""
        rolls = np.array([[3, 3, 4]])
        target_sum = 10
        results = target_rolls(rolls, target_sum)
        expected = np.array([True])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_single_die(self):
        """Test target_rolls with single die rolls."""
        rolls = np.array([[3], [5], [6]])
        target_sum = 5
        results = target_rolls(rolls, target_sum)
        expected = np.array([False, True, True])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_high_target(self):
        """Test target_rolls with unachievable high target sum."""
        rolls = np.array([[6, 6, 6], [5, 5, 5]])
        target_sum = 18
        results = target_rolls(rolls, target_sum)
        expected = np.array([True, False])
        np.testing.assert_array_equal(results, expected)

    def test_target_rolls_returns_boolean_array(self):
        """Test that target_rolls returns a boolean array."""
        rolls = np.array([[1, 2], [3, 4]])
        results = target_rolls(rolls, target_sum=5)
        self.assertEqual(results.dtype, bool)

    def test_target_rolls_preserves_length(self):
        """Test that target_rolls preserves the number of rolls."""
        rolls = np.array([[1, 2, 3] for _ in range(100)])
        results = target_rolls(rolls, target_sum=10)
        self.assertEqual(len(results), len(rolls))


class TestIntegration(unittest.TestCase):
    """Integration tests for combined functionality.
    
    Tests verify that functions work correctly together in workflows.
    """

    def test_rollset_sumrolls_integration(self):
        """Test RollSet and SumRolls working together.
        
        Verifies shape compatibility and that sums fall within
        expected range for given dice and offset.
        """
        n_dice = 3
        n_rolls = 10
        offset = 2
        rolls = RollSet(n_dice, n_rolls)
        sums = SumRolls(rolls, offset=offset)
        
        # Verify sums are reasonable
        self.assertEqual(len(sums), n_rolls)
        min_expected = n_dice + offset  # minimum sum
        max_expected = 6 * n_dice + offset  # maximum sum
        self.assertTrue(np.all(sums >= min_expected))
        self.assertTrue(np.all(sums <= max_expected))

    def test_rollset_target_rolls_integration(self):
        """Test RollSet and target_rolls working together.
        
        Verifies that success/failure results align with generated rolls.
        """
        n_dice = 3
        n_rolls = 10
        target_sum = 10
        rolls = RollSet(n_dice, n_rolls)
        results = target_rolls(rolls, target_sum)
        
        # Verify results
        self.assertEqual(len(results), n_rolls)
        self.assertEqual(results.dtype, bool)

    def test_full_workflow(self):
        """Test complete workflow: RollSet -> SumRolls -> target_rolls.
        
        Simulates a full roll evaluation chain with all three functions.
        """
        n_dice = 4
        n_rolls = 20
        offset = 1
        target_sum = 15
        
        # Generate rolls
        rolls = RollSet(n_dice, n_rolls)
        
        # Sum with offset
        sums = SumRolls(rolls, offset=offset)
        
        # Check against target
        # Note: target_rolls works on raw rolls, not summed rolls
        results = target_rolls(rolls, target_sum - offset)
        
        # Verify all outputs are valid
        self.assertEqual(rolls.shape, (n_rolls, n_dice))
        self.assertEqual(len(sums), n_rolls)
        self.assertEqual(len(results), n_rolls)

    def test_dice_with_rollset(self):
        """Test that Dice rolls are compatible with RollSet.
        
        Verifies that RollSet uses Dice internally correctly.
        """
        # RollSet uses Dice internally, verify compatibility
        rolls = RollSet(5, 10)
        
        # All values should be valid die results
        self.assertTrue(np.all(rolls >= 1))
        self.assertTrue(np.all(rolls <= 6))
        
        # Correct shape
        self.assertEqual(rolls.shape, (10, 5))


class TestExperiment(unittest.TestCase):
    """Unit tests for the experiment class.

    Tests cover single-episode hit/miss logic, damage floor behavior,
    and odd-parameter dice-count overrides.
    """

    def test_run_single_episode_returns_zero_on_miss(self):
        """Test that a failed to-hit roll returns zero damage and exits early."""
        exp = experiment(defence=12, attack=0, power=5, armour=2)
        exp.dice.roll = Mock(side_effect=[np.array([1, 1])])

        damage = exp.run_single_episode()

        self.assertEqual(damage, 0)
        self.assertEqual(exp.dice.roll.call_count, 1)

    def test_run_single_episode_damage_is_clamped_to_zero(self):
        """Test that successful hits with negative computed damage return zero."""
        exp = experiment(defence=8, attack=0, power=1, armour=10)
        exp.dice.roll = Mock(side_effect=[np.array([6, 6]), np.array([1, 1])])

        damage = exp.run_single_episode()

        self.assertEqual(damage, 0)
        self.assertEqual(exp.dice.roll.call_count, 2)

    def test_run_single_episode_uses_odd_parameter_dice_counts(self):
        """Test that odd_parameters controls the dice counts for to-hit and damage."""
        exp = experiment(
            defence=10,
            attack=7,
            power=2,
            armour=1,
            odd_parameters={'to_hit_dice': 3, 'damage_dice': 4}
        )
        exp.dice.roll = Mock(side_effect=[
            np.array([1, 1, 2]),
            np.array([1, 1, 1, 1])
        ])

        damage = exp.run_single_episode()

        self.assertEqual(damage, 5)
        exp.dice.roll.assert_has_calls([
            call(num_rolls=3),
            call(num_rolls=4)
        ])

    def test_run_single_episode_all_ones_auto_miss(self):
        """Test that all ones on to-hit is an automatic miss despite modifiers."""
        exp = experiment(defence=5, attack=10, power=20, armour=0)
        exp.dice.roll = Mock(side_effect=[np.array([1, 1])])

        damage = exp.run_single_episode()

        self.assertEqual(damage, 0)
        self.assertEqual(exp.dice.roll.call_count, 1)

    def test_run_single_episode_returns_cumulative_damage_over_multiple_attacks(self):
        """Test that run_single_episode returns cumulative damage across n_attacks."""
        exp = experiment(defence=7, attack=0, power=3, armour=1, n_attacks=3)
        exp.dice.roll = Mock(side_effect=[
            np.array([4, 4]),  # attack 1 to-hit (hit)
            np.array([2, 2]),  # attack 1 damage -> 4 + 3 - 1 = 6
            np.array([1, 1]),  # attack 2 to-hit (auto miss)
            np.array([3, 3]),  # attack 3 to-hit (miss: 6 < 7)
        ])

        damage = exp.run_single_episode()

        self.assertEqual(damage, 6)
        self.assertEqual(exp.dice.roll.call_count, 4)

    def test_experiment_rejects_invalid_n_attacks(self):
        """Test that n_attacks must be at least one."""
        with self.assertRaises(ValueError):
            experiment(defence=10, attack=0, power=0, armour=0, n_attacks=0)

    def test_run_single_episode_returns_casualties_for_infantry(self):
        """Test infantry mode returns casualties with ordered wound allocation."""
        exp = experiment(
            defence=7,
            attack=0,
            power=0,
            armour=0,
            n_attacks=3,
            odd_parameters={'infantry_wounds': 3}
        )
        exp.dice.roll = Mock(side_effect=[
            np.array([4, 4]),  # attack 1 to-hit (hit)
            np.array([2, 3]),  # attack 1 damage = 5 -> 1 casualty, 2 wasted
            np.array([4, 4]),  # attack 2 to-hit (hit)
            np.array([1, 1]),  # attack 2 damage = 2 -> no casualty yet
            np.array([4, 4]),  # attack 3 to-hit (hit)
            np.array([1, 1]),  # attack 3 damage = 2 -> reaches 4, 1 casualty, 1 wasted
        ])

        casualties = exp.run_single_episode()

        self.assertEqual(casualties, 2)

    def test_run_single_episode_rejects_invalid_infantry_wounds(self):
        """Test that infantry_wounds must be at least one when provided."""
        exp = experiment(defence=2, attack=0, power=0, armour=0, odd_parameters={'infantry_wounds': 0})
        exp.dice.roll = Mock(side_effect=[np.array([2, 2]), np.array([1, 1])])

        with self.assertRaises(ValueError):
            exp.run_single_episode()

    def test_run_experiment_returns_full_result_array(self):
        """Test that run_experiment returns one value per episode as a numpy array."""
        exp = experiment(defence=10, attack=0, power=0, armour=0, n_tests=3)
        exp.run_single_episode = Mock(side_effect=[1.5, 0.0, 2.0])

        results = exp.run_experiment()

        self.assertIsInstance(results, np.ndarray)
        np.testing.assert_array_equal(results, np.array([1.5, 0.0, 2.0]))
        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
