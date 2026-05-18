from typing import Optional

from Analyse_Results import analyse_results
from WMDice import experiment


def run_wm_analytics(
    defence: int,
    attack: int,
    power: int,
    armour: int,
    n_attacks: int = 1,
    n_tests: int = 10000,
    to_hit_dice: int = 2,
    damage_dice: int = 2,
    infantry_wounds: Optional[int] = None,
    charge_attack: bool = False,
    cavalry_charge: bool = False,
) -> dict:
    """Run a WMDice experiment and return analysis-ready output.

    The function accepts user-selected parameters, runs the matching simulation,
    and returns a dictionary that includes expectation plus probability and
    cumulative distributions suitable for plotting.

    Args:
        defence: Target defence value to beat on a successful hit.
        attack: Attack modifier added to each to-hit roll.
        power: Power modifier added to each damage roll.
        armour: Armour value subtracted from calculated damage.
        n_attacks: Number of attacks in each episode.
        n_tests: Number of episodes to simulate.
        to_hit_dice: Number of d6 used for to-hit rolls.
        damage_dice: Number of d6 used for damage rolls.
        infantry_wounds: If set, simulation uses infantry casualty mode where
            this value defines wounds required to remove a model.
        charge_attack: If True, first damage roll in each episode uses +1 die.
        cavalry_charge: If True, first to-hit roll in each episode uses +1 die.

    Returns:
        Dictionary containing:
            - metric: "damage" or "casualties"
            - expectation
            - probability_distribution
            - cumulative_distribution
            - simulated_results (per-episode outputs as a list)
            - parameters (echoed inputs for traceability)
    """
    odd_parameters = {
        "to_hit_dice": int(to_hit_dice),
        "damage_dice": int(damage_dice),
        "charge_attack": bool(charge_attack),
        "cavalry_charge": bool(cavalry_charge),
    }
    if infantry_wounds is not None:
        odd_parameters["infantry_wounds"] = int(infantry_wounds)

    run = experiment(
        defence=defence,
        attack=attack,
        power=power,
        armour=armour,
        odd_parameters=odd_parameters,
        n_attacks=n_attacks,
        n_tests=n_tests,
    )

    simulated_results = run.run_experiment()
    analysis_type = "casualties" if infantry_wounds is not None else "damage"
    analysis = analyse_results(simulated_results=simulated_results, analysis_type=analysis_type)

    return {
        **analysis,
        "simulated_results": simulated_results.tolist(),
        "parameters": {
            "defence": defence,
            "attack": attack,
            "power": power,
            "armour": armour,
            "n_attacks": n_attacks,
            "n_tests": n_tests,
            "to_hit_dice": int(to_hit_dice),
            "damage_dice": int(damage_dice),
            "infantry_wounds": infantry_wounds,
            "charge_attack": bool(charge_attack),
            "cavalry_charge": bool(cavalry_charge),
        },
    }

