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




