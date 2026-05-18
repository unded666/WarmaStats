from Dice import Dice
import numpy as np
import pandas as pd

def RollSet (n_dice: int, n_rolls: int):
    dice = Dice()
    rolls = dice.roll(num_rolls=n_dice * n_rolls)
    rolls = rolls.reshape(n_rolls, n_dice)
    # sums = rolls.sum(axis=1)
    return rolls

def SumRolls (rolls: np.ndarray, offset: int):
    sums = rolls.sum(axis=1) + offset
    return sums

def target_rolls (rolls: np.ndarray, target_sum: int):
    """ tests each roll to see if it matches the target sum,
    returns a boolean array of success or failure for each roll"""
    sums = rolls.sum(axis=1)
    return sums >= target_sum

class experiment:
    def __init__ (
            self,
            defence: int,
            attack: int,
            power: int,
            armour: int,
            odd_parameters: dict = None,
            n_attacks: int = 1,
            n_tests: int = 10000):
    
        self.defence = defence
        self.attack = attack
        self.power = power
        self.armour = armour
        self.n_attacks = int(n_attacks)
        if self.n_attacks < 1:
            raise ValueError("n_attacks must be >= 1")
        self.n_tests = n_tests
        self.odd_parameters = odd_parameters or {}
        self.dice = Dice()
    
    def run_single_episode (self) -> float:
        """
        runs a single episode of the experiment and returns cumulative output.
        Each episode contains n_attacks independent attacks. For each attack, a to-hit
        roll is made, the attack modifier is added, and it must meet or exceed defence.
        A to-hit roll of all ones is always a miss. On a hit, damage is power - armour
        plus a damage roll, with a minimum of zero damage per attack.

        Optional odd-parameter modifiers:
        - 'charge_attack': first damage roll in the episode gains +1 damage die.
        - 'cavalry_charge': first to-hit roll in the episode gains +1 to-hit die.

        If odd_parameters includes 'infantry_wounds', attacks are resolved against a
        sequence of infantry models. Damage is applied to one model at a time until it
        becomes a casualty, then the next model starts taking damage. Excess damage on
        a killing blow is wasted. In this mode, casualties are returned.

        :return: cumulative damage dealt in the episode, or casualties in infantry mode
        """
        to_hit_dice = int(self.odd_parameters.get('to_hit_dice', 2))
        damage_dice = int(self.odd_parameters.get('damage_dice', 2))
        infantry_wounds = self.odd_parameters.get('infantry_wounds')
        charge_attack = bool(self.odd_parameters.get('charge_attack', False))
        cavalry_charge = bool(self.odd_parameters.get('cavalry_charge', False))

        total_damage = 0
        casualties = 0
        current_model_damage = 0
        charge_attack_available = charge_attack

        for attack_index in range(self.n_attacks):
            current_to_hit_dice = to_hit_dice + 1 if cavalry_charge and attack_index == 0 else to_hit_dice
            to_hit_rolls = self.dice.roll(num_rolls=current_to_hit_dice)
            to_hit_roll = int(np.sum(to_hit_rolls))
            total_to_hit = to_hit_roll + self.attack

            # Snake-eyes style rule: all ones on the to-hit roll is always a miss.
            if np.all(to_hit_rolls == 1):
                continue

            if total_to_hit < self.defence:
                continue

            current_damage_dice = damage_dice + 1 if charge_attack_available else damage_dice
            damage_roll = int(np.sum(self.dice.roll(num_rolls=current_damage_dice)))
            charge_attack_available = False
            damage = max(0, damage_roll + self.power - self.armour)

            if infantry_wounds is None:
                total_damage += damage
                continue

            infantry_wounds_int = int(infantry_wounds)
            if infantry_wounds_int < 1:
                raise ValueError("infantry_wounds must be >= 1")

            current_model_damage += damage
            if current_model_damage >= infantry_wounds_int:
                casualties += 1
                # Excess damage is wasted; next model starts fresh.
                current_model_damage = 0

        if infantry_wounds is not None:
            return casualties

        return total_damage
    
    def run_experiment (self) -> np.ndarray:
        """
        runs the experiment for n_tests episodes and returns the full per-episode result array.
        In non-infantry mode, each element is cumulative damage for one episode.
        In infantry mode, each element is casualties for one episode.

        :return: numpy array of length n_tests containing one result per episode
        """
        return np.array([self.run_single_episode() for _ in range(self.n_tests)])
        

if __name__ == '__main__':
    n_dice = 3
    n_rolls = 8
    rolls = RollSet(n_dice, n_rolls)
    offset = 1 #Dice + 1
    sums = SumRolls(rolls, offset)
    print(f"Rolling {n_dice} dice {n_rolls} times:")
    print(rolls)
    print(f"Sums of rolls with offset {offset}:")
    print(sums)
    target_sum = 10
    successes = target_rolls(rolls, target_sum)
    print(f"Rolls that meet or exceed target sum {target_sum}:")
    print(successes)
