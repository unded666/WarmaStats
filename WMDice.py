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
            n_tests: int = 10000):
    
        self.defence = defence
        self.attack = attack
        self.power = power
        self.armour = armour
        self.n_tests = n_tests
        self.odd_parameters = odd_parameters or {}
        self.dice = Dice()
    
    def run_single_episode (self) -> int:
        """
        runs a single episode of the experiment, returns the result of the as a damage dealt number.
        This damage is found after running a single dice roll, adding the attack and testing whether or not 
        it matches or beats the defence value. If it hits, then damage is calculated by subtracting the armour 
        from the power and adding a new dice roll. The minimum damage returned is zero, which is the same value 
        returned if the attack misses. to-hit and damage dice are both 2D6 unless a different value is specified 
        in the odd_parameters dictionary, which can have the keys 'to_hit_dice' and 'damage_dice'
        :return: integer damage dealt, minimum of zero
        """
        to_hit_dice = int(self.odd_parameters.get('to_hit_dice', 2))
        damage_dice = int(self.odd_parameters.get('damage_dice', 2))

        to_hit_rolls = self.dice.roll(num_rolls=to_hit_dice)
        to_hit_roll = int(np.sum(to_hit_rolls))
        total_to_hit = to_hit_roll + self.attack

        # Snake-eyes style rule: all ones on the to-hit roll is always a miss.
        if np.all(to_hit_rolls == 1):
            return 0

        if total_to_hit < self.defence:
            return 0

        damage_roll = int(np.sum(self.dice.roll(num_rolls=damage_dice)))
        damage = damage_roll + self.power - self.armour
        return max(0, damage)
        
        
        
        
        

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
