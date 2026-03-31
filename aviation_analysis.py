import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def open_csv(x):
    df = pd.read_csv(x)
    return df


def country_analysis(x):
    df = open_csv(x)
    state_most = df["STATE_NAME"].value_counts().head().values
    state_most_index = df["STATE_NAME"].value_counts().head().index
    plt.bar(state_most_index, state_most)
    plt.xlabel("Country")
    plt.ylabel("Delay Count")
    plt.title("The top 5 countries with the most delays")
    plt.show()

    print(state_most)
if __name__ == '__main__':
    input1 = sys.argv[1]
    country_analysis(input1)