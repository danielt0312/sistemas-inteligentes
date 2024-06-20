import pandas as pd
import nltk     # instalar: pip install nltk
import re

from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import joblib

import matplotlib.pyplot as plt

from sklearn.manifold import MDS

from scipy.cluster.hierarchy import ward, dendrogram


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
genres = ['Crime', 'Drama', 'History', 'Sports', 'Romance', 'Drama', 'History', 'Drama', 'Fantasy', 'Romance']

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
                                 use_idf=True,tokenizer=tokenize_and_stem, ngram_range=(1,3))

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

# joblib.dump(km,  'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

print(clusters)

films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters}

frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster'])

print(frame)

grouped = frame['rank'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

print(grouped.mean()) #average rank (1 to 100) per cluster


print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d titles:" % i, end='')
    for title in frame.loc[i]['title'].values.tolist():
        print(' %s,' % title, end='')
    print() #add whitespace
    print() #add whitespace


"""
Multidimensional scaling
"""

MDS()

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()

"""
Visualizing document clusters
"""

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

#set up cluster names using a dict
cluster_names = {0: 'Love, fall, american', 
                 1: 'World, war, during', 
                 2: 'New, meet, world', 
                 3: 'Life, relationships, american', 
                 4: 'Family, american, relationships'}

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 

#group by cluster
groups = df.groupby('label')


# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
            label=cluster_names[name], color=cluster_colors[name], 
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')
    
ax.legend(numpoints=1)  #show legend with only 1 point

#add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.loc[i]['x'], df.loc[i]['y'], df.loc[i]['title'], size=8)  


plt.show() #show the plot

#uncomment the below to save the plot if need be
# plt.savefig('clusters_small_noaxes.png', dpi=200)

"""
Hierarchical document clustering
"""


linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="left", labels=titles);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout
plt.show()

#uncomment below to save figure
# plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
