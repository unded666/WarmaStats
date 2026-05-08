from Dice import Dice
import numpy as np
import pandas as pd

def RollSet (n_dice: int, n_rolls: int):
    dice = Dice()
    rolls = dice.roll(num_rolls=n_dice * n_rolls)
    rolls = rolls.reshape(n_rolls, n_dice)
    # sums = rolls.sum(axis=1)
    return rolls



if __name__ == '__main__':
    n_dice = 3
    n_rolls = 8
    rolls = RollSet(n_dice, n_rolls)

