import pandas as pd
import nltk     # instalar: pip install nltk
import re
import joblib
import os
import matplotlib.pyplot as plt

from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram

class Cluster():
    def __init__(self):
        pass

    def tokenize_and_stem(self, text):
        stemmer = SnowballStemmer("english")

        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems


    def tokenize_only(self, text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens
    
    def vocab(self):
        #not super pythonic, no, not at all.
        #use extend so it's a big flat list of vocab
        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for i in self.content:
            allwords_stemmed = self.tokenize_and_stem(i) #for each item in 'content ', tokenize/stem
            totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
            
            allwords_tokenized = self.tokenize_only(i)
            totalvocab_tokenized.extend(allwords_tokenized)

        self.vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

    def vectorizer(self):
        #define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                        min_df=0.2, stop_words='english',
                                        use_idf=True,tokenizer=self.tokenize_and_stem, ngram_range=(1,3))

        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.content) #fit the vectorizer to synopses

        # print(tfidf_matrix.shape)
        self.terms = tfidf_vectorizer.get_feature_names_out()
        self.dist = 1 - cosine_similarity(self.tfidf_matrix)

    def kmeansClustering(self, num_clusters = 3):
        self.km = KMeans(n_clusters=num_clusters)
        self.km.fit(self.tfidf_matrix)
        self.saveModel()
        self.clusters = self.km.labels_.tolist()
        self.showTopTerms(num_clusters)
    
    def saveModel(self):
        if not os.path.exists('./doc_cluster.pkl'):
            joblib.dump(self.km, 'doc_cluster.pkl')
        self.km = joblib.load('doc_cluster.pkl')

    def loadModel(self):
        files = {'title': self.titles, 'content': self.content, 'cluster': self.clusters}
        frame = pd.DataFrame(files, index = [self.clusters] , columns = ['title', 'cluster'])
        grouped = frame['rank'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

    def showTopTerms(self, num_clusters = 3):
        print("Top terms per cluster:")
        print()
        #sort cluster centers by proximity to centroid
        order_centroids = self.km.cluster_centers_.argsort()[:, ::-1] 

        for i in range(num_clusters):
            print("Cluster %d words:" % i, end='')
            
            for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
                print(' %s' % self.vocab_frame.loc[self.terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
            print() #add whitespace
            print() #add whitespace
            
            print("Cluster %d titles:" % i, end='')
            for title in self.frame.loc[i]['title'].values.tolist():
                print(' %s,' % title, end='')
            print() #add whitespace
            print() #add whitespace

    def scaling(self):
        # convert two components as we're plotting points in a two-dimensional plane
        # "precomputed" because we provide a distance matrix
        # we will also specify `random_state` so the plot is reproducible.
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(self.dist)  # shape (n_components, n_samples)
        self.xs, self.ys = pos[:, 0], pos[:, 1]

    def setClusters(self):
        self.cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

        #set up cluster names using a dict
        self.cluster_names = {0: 'Love, fall, american', 
                        1: 'World, war, during', 
                        2: 'New, meet, world', 
                        3: 'Life, relationships, american', 
                        4: 'Family, american, relationships'}
        
        #create data frame that has the result of the MDS plus the cluster numbers and titles
        self.df = pd.DataFrame(dict(x=self.xs, y=self.ys, label=self.clusters, title=self.titles)) 

        #group by cluster
        self.groups = self.df.groupby('label')

        # set up plot
        fig, self.ax = plt.subplots(figsize=(17, 9)) # set size
        self.ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

    def groupLayers(self):
        #iterate through groups to layer the plot
        #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
        for name, group in self.groups:
            self.ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                    label=self.cluster_names[name], color=self.cluster_colors[name], 
                    mec='none')
            self.ax.set_aspect('auto')
            self.ax.tick_params(\
                axis= 'x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off')
            self.ax.tick_params(\
                axis= 'y',         # changes apply to the y-axis
                which='both',      # both major and minor ticks are affected
                left='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelleft='off')
        
        self.ax.legend(numpoints=1)  #show legend with only 1 point
    
    def showVisualDocument(self):
        #add label in x,y position with the label as the film title
        for i in range(len(self.df)):
            self.ax.text(self.df.loc[i]['x'], self.df.loc[i]['y'], self.df.loc[i]['title'], size=8)  

        plt.show()

    def showHierarchicalDocument(self):
        linkage_matrix = ward(self.dist) #define the linkage_matrix using ward clustering pre-computed distances

        fig, self.ax = plt.subplots(figsize=(15, 20)) # set size
        self.ax = dendrogram(linkage_matrix, orientation="left", labels=self.titles);

        plt.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')

        plt.tight_layout() #show plot with tight layout
        plt.show()
