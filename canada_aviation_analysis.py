import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import FreqDist

# word tokenize: breaks down the text into words
# sent tokenize: breaks down the text into sentences

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

    idx_column = df.columns.get_loc("Summary Tokenized")
    Stemmer = PorterStemmer()

    for index, row in df.iterrows():

        if index == 3:
            break
        for sentence in row['Summary Tokenized']:
            word_list = sentence.split()
            filtered_word = [word.lower() for word in word_list if word not in stop_words]

        df.iat[index, idx_column] = filtered_word
    # removed all of the word that has numeric
    # we saw that numeric had . so we replaced it with '' so that it can bypass the .isnumeric() function
    all_word = [word for tokens in df['Summary Tokenized'].dropna() for word in tokens if not word.replace('.', '').isnumeric()]
    fdist = FreqDist(all_word)
    print(fdist.most_common(20))

    fdist.plot(20, cumulative=True)
    plt.show()


    # print(df["Summary Tokenized"].head(5))

if __name__ == '__main__':
    input1 = sys.argv[1]
    # location_analysis(input1)
    # occurence_type_analysis(input1)
    occurence_sentence_analysis(input1)