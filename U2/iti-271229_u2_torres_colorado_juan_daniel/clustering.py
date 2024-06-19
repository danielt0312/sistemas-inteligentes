import numpy as np
import pandas as pd
import nltk     # instalar: pip install nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3    # instalar: pip install mpld3

from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import joblib


"""
VARIABLES IMPLEMENTADAS POR MI (NO SE ENCUENTRAN EN LA PAGINA)
"""
titles = ['The Godfather', 'The Shawshank Redemption', "Schindler's List", 'Raging Bull', 'Casablanca', "One Flew Over the Cuckoo's Nest", 'Gone with the Wind', 'Citizen Kane', 'The Wizard of Oz', 'Titanic']
synopses = []
synopses.append("On the day of his only daughter's wedding, Vito Corleone hears requests in his role as the Godfather, the Don of a New York crime family. Vito's youngest son, Michael")
synopses.append("Andy Dufresne, a banker, is wrongfully imprisoned for the murder of his wife and her lover. In Shawshank prison, he befriends Red and finds a way to bring hope and redemption to the inmates.")
synopses.append("During World War II, businessman Oskar Schindler saves over a thousand Jewish refugees from the Holocaust by employing them in his factories, risking his life in the process.")
synopses.append("The rise and fall of middleweight boxing champion Jake LaMotta, whose violent temper and jealousy destroy his relationships outside the ring.")
synopses.append("In Casablanca during World War II, exiled American and former freedom fighter Rick Blaine runs the most popular nightspot in town and struggles with choosing between love and virtue.")
synopses.append("Randle McMurphy, a criminal, pleads insanity and is admitted to a mental institution where he challenges the oppressive Nurse Ratched and rallies the patients to rebel.")
synopses.append("Set against the backdrop of the American Civil War, Scarlett O'Hara, a Southern belle, struggles to maintain her family's plantation and navigate turbulent romantic relationships.")
synopses.append("The life and legacy of publishing tycoon Charles Foster Kane is revealed through the investigation of his last word, 'Rosebud")
synopses.append("Dorothy Gale is swept away from her Kansas farm to the magical land of Oz in a tornado. She embarks on a journey to meet the Wizard with her new friends: a Scarecrow, a Tin Man, and a Cowardly Lion.")
synopses.append("A young aristocrat falls in love with a kind but poor artist aboard the ill-fated R.M.S. Titanic. Their romance is put to the test as the ship meets its tragic end.")

ranks = list(range(len(titles)))

### Init

# print (titles[:10]) #first 10 titles

# print (synopses[0][:200] )#first 200 characters in first synopses (for 'The Godfather')


"""
Stopwords, stemming, and tokenizing
"""

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')

# print (stopwords[:10])

# load nltk's SnowballStemmer as variabled 'stemmer'
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopses:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

print (vocab_frame.head())

"""
Tf-idf and document similarity
"""

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names_out()

dist = 1 - cosine_similarity(tfidf_matrix)

 
"""
K-means clustering
"""

num_clusters = 5

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

print(clusters)


#### ¡¡¡¡ IMPORTANTE !!!!! 
#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

#joblib.dump(km,  'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

print(clusters)

films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters, 'genre': genres }

frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster', 'genre'])