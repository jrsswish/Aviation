import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def open_csv(x):
    df = pd.read_csv(x)
    return df


def country_analysis(x):
    df = open_csv(x)
    state_most = df["STATE_NAME"].value_counts().sort_values(ascending=False).head()
    state_most_index = state_most.index
    plt.bar(state_most_index, state_most)

    plt.xlabel("Country")
    plt.ylabel("Delay Count")
    plt.title("The top 5 countries with the most delays")
    plt.show()

def departure_analysis(x):
    df = open_csv(x)
    departure_most = df.groupby("STATE_NAME")["FLT_DEP_1"].sum().sort_values(ascending=False).head()
    departure_most_index = departure_most.index

    plt.bar(departure_most_index, departure_most)
    plt.xlabel("Departure Time")
    plt.ylabel("Departure Count")
    plt.title("The top 5 departure times with the most delays")
    plt.show()

if __name__ == '__main__':
    input1 = sys.argv[1]
    departure_analysis(input1)