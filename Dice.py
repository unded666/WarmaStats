import numpy as np
import pandas as pd

class Dice:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self, num_rolls=1):
        return np.random.randint(1, self.sides + 1, size=num_rolls)

    def simulate_rolls(self, num_rolls=1000):
        rolls = self.roll(num_rolls)
        return pd.Series(rolls).value_counts().sort_index()

if __name__ == "__main__":
    # sample testing here
    dice = Dice()
    # print("Rolling a die 10 times:")
    # print(dice.roll(20))

    # Simulate 100 000 dice rolls, plot the resulting
    # distribution to determine if the dice rolls are fair
    import matplotlib.pyplot as plt

    def format_scientific(value):
        mantissa, exponent = f"{value:.2e}".split("e")
        mantissa = mantissa.rstrip("0").rstrip(".")
        # Use matplotlib mathtext so the exponent renders as a superscript.
        return rf"${mantissa}\times 10^{{{int(exponent)}}}$"

    num_rolls = 4200000
    distribution = dice.simulate_rolls(num_rolls)
    distribution.plot(kind='bar')
    plt.title(f'Distribution of {format_scientific(num_rolls)} Dice Rolls')
    plt.xlabel('Die Face')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)

    # display the probabilities of each roll on the graph
    probabilities = distribution / num_rolls
    ax = plt.gca()
    for bar, prob in zip(ax.patches, probabilities):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        plt.text(x, y, f'{prob:.2%}', ha='center', va='bottom')
    plt.show()




