import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import nltk
from nltk import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import FreqDist
import spacy

# Show all rows
pd.set_option('display.max_rows', None)

# Show all columns
pd.set_option('display.max_columns', None)

# Show full content of each cell (no truncation)
pd.set_option('display.max_colwidth', None)

# word tokenize: breaks down the text into words
# sent tokenize: breaks down the text into sentences

nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')

def open_csv(x):
    df = pd.read_csv(x)
    return df


def location_analysis(x):
    df = open_csv(x)
    df = pd.DataFrame(df)
    delay_most = df["Location"].value_counts().sort_values(ascending=False).head()
    delay_most_index = delay_most.index
    plt.bar(delay_most_index, delay_most)
    plt.xlabel("Location")
    plt.ylabel("Occurence Count")
    plt.title("The top 5 location in Canada with the most occurences")
    plt.show()

def occurence_type_analysis(x):
    df = open_csv(x)
    df = pd.DataFrame(df)
    occur_type_most = df["OccIncidentTypeID_DisplayEng"].value_counts().sort_values(ascending=False).head()
    plt.bar(occur_type_most.index, occur_type_most.values)
    plt.xlabel("Occurence Type")
    plt.ylabel("Occurence Count")
    plt.title("Occurence Type that occurs the most")
    plt.show()


def occurence_sentence_analysis(x):
    df = open_csv(x)
    df = pd.DataFrame(df)
    df['Summary Tokenized'] = df["Summary"].dropna().apply(sent_tokenize)
    stop_words = set(stopwords.words("english"))
    stop_words_french = set(stopwords.words("french"))

    idx_column = df.columns.get_loc("Summary Tokenized")

    for index, row in df.iterrows():
        if not isinstance(row['Summary Tokenized'], float):
            for sentence in row['Summary Tokenized']:
                word_list = sentence.split()
                # takes the stop words in english and french
                filtered_word = [word.lower() for word in word_list if word.lower() not in stop_words and word.lower() not in stop_words_french]

            df.iat[index, idx_column] = filtered_word
    # removed all of the word that has numeric
    # we saw that numeric had . so we replaced it with '' so that it can bypass the .isnumeric() function
    all_word = [word for tokens in df['Summary Tokenized'].dropna() for word in tokens if not word.replace('.', '').isnumeric()]
    fdist = FreqDist(all_word)

    fdist.plot(20, cumulative=True)
    plt.show()
    # print(df["Summary Tokenized"].head(5))

def occurence_category_analysis(x):
    df = open_csv(x)
    df['Emergency Tokenized'] = df["ICAO_DisplayEng"].dropna().apply(word_tokenize)
    stop_words = set(stopwords.words("english"))
    stop_words_french = set(stopwords.words("french"))
    idx_column = df.columns.get_loc("Emergency Tokenized")

    for index, row in df.iterrows():
        if not isinstance(row['Emergency Tokenized'], float):
            filtered_words = [word.lower() for word in row['Emergency Tokenized'] if word.lower() not in stop_words and word.lower() not in stop_words_french]
            df.iat[index, idx_column] = filtered_words

    # we know that the most occurence type was EMERGENCY/PRIORITY
    # we will be specifically be diving into summary of those problems

    # this is all words specifically with occurence type of EMERGENCY/PRIORITY
    # print(df['Emergency Tokenized'])
    most_occur_type = df.loc[df["OccIncidentTypeID_DisplayEng"] == "EMERGENCY/PRIORITY (xi)", "Emergency Tokenized"]
    all_words = [word for tokens in most_occur_type.dropna() for word in tokens if not word.replace('.', '').isnumeric() and not word.isalnum()]
    fdist = FreqDist(all_words)
    fdist.plot(20, cumulative=True)
    plt.tight_layout()
    plt.show()

def solutions_OSU(x):
    df = open_csv(x)
    df['Summary Tokenized'] = df['Summary'].dropna().apply(word_tokenize)
    stop_words = set(stopwords.words("english"))
    stop_words_french = set(stopwords.words("french"))
    idx_column_summary = df.columns.get_loc("Summary Tokenized")

    for index, row in df.iterrows():
        if not isinstance(row['Summary Tokenized'], float):
            filtered_words = [word.lower() for word in row['Summary Tokenized'] if word.lower() not in stop_words and word.lower() not in stop_words_french]
            df.iat[index, idx_column_summary] = filtered_words

    df_only_OSU = df.loc[df["ICAO_DisplayEng"] == "UNDERSHOOT/OVERSHOOT (USOS)", "Summary Tokenized"]

    # check the summary for the word the contains summary to review the problems
    df_only_injuries = df.loc[(df["ICAO_DisplayEng"] == "UNDERSHOOT/OVERSHOOT (USOS)") & (df["Summary"].str.contains('injuries')), "Summary"]
    print(df_only_injuries)

    all_word = [word for token in df_only_OSU.dropna() for word in token if word.isalpha()]

    # fdist = FreqDist(all_word)
    # fdist.plot(20, cumulative=True)
    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    input1 = sys.argv[1]
    # location_analysis(input1)
    # occurence_type_analysis(input1)
    # occurence_sentence_analysis(input1)
    # occurence_category_analysis(input1)
    solutions_OSU(input1)