import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def open_csv(x):
    df = pd.read_csv(x)
    return df


def country_analysis(x):
    df = open_csv(x)
    delay_most = df["STATE_NAME"].value_counts().sort_values(ascending=False).head()
    delay_most_index = delay_most.index
    plt.bar(delay_most_index, delay_most)
    print(delay_most)
    plt.xlabel("Country")
    plt.ylabel("Delay Count")
    plt.title("The top 5 countries with the most delays")
    # plt.show()

def departure_analysis(x):
    df = open_csv(x)
    departure_most = df.groupby("STATE_NAME")["FLT_DEP_1"].sum().sort_values(ascending=False).head()
    departure_most_index = departure_most.index
    print(departure_most)
    plt.bar(departure_most_index, departure_most)
    plt.xlabel("Departure Time")
    plt.ylabel("Departure Count")
    plt.title("The top 5 departure times with the most delays")
    # plt.show()

def delay_ratio_analysis(x):
    df = open_csv(x)
    delay_most = df["STATE_NAME"].value_counts().sort_values(ascending=False).head()

    delay_most_values = delay_most.values.tolist()
    delay_most_index = delay_most.index

    # this is the departure number of the delayed countries
    delay_most_index_list = delay_most.index.tolist()
    departure_num = df.loc[df['STATE_NAME'].isin(delay_most_index_list)].groupby("STATE_NAME")["FLT_DEP_1"].sum()

    # reindex so it is the same as the most delay list order
    departure_num = departure_num.reindex(delay_most.index)

    departure_num_values = departure_num.values.tolist()
    print(delay_most_values)
    print(departure_num_values)


    delay_percent_values = []
    for num in range(len(delay_most)):
        ratio = delay_most_values[num] / departure_num_values[num]
        delay_percent = ratio * 100
        delay_percent_values.append(delay_percent)

    plt.bar(delay_most_index, delay_percent_values)
    plt.xlabel("Country")
    plt.ylabel("Delay Percentage (Delay Count / Total Departure)")
    plt.title("Delay Percentage on Country")
    plt.show()

if __name__ == '__main__':
    input1 = sys.argv[1]
    # country_analysis(input1)
    # departure_analysis(input1)
    delay_ratio_analysis(input1)