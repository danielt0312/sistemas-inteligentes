import pandas as pd
import nltk     # instalar: pip install nltk
import re
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np

from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram

class Cluster():
    def __init__(self, titles, contents, num_clusters=3):
        self.setTitles(titles)
        self.setContents(contents)
        print(f"Documentos procesados: {len(self.content)}")
        self.setClusters(num_clusters)
        self.analyze_word_distribution()
    
    def analyze_word_distribution(self):
        count_vectorizer = CountVectorizer(stop_words='english')
        word_count_matrix = count_vectorizer.fit_transform(self.content)
        word_counts = np.asarray(word_count_matrix.sum(axis=0)).flatten()
        word_freq = list(zip(count_vectorizer.get_feature_names_out(), word_counts))
        word_freq_sorted = sorted(word_freq, key=lambda x: x[1], reverse=True)
        return word_freq_sorted
    
    def vocab(self):
        # not super pythonic, no, not at all.
        # use extend so it's a big flat list of vocab
        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for i in self.content:
            allwords_stemmed = self.tokenize_and_stem(i)  # for each item in 'content', tokenize/stem
            totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

            allwords_tokenized = self.tokenize_only(i)
            totalvocab_tokenized.extend(allwords_tokenized)

        # Remove short words from vocab_frame
        vocab_frame_data = {'words': totalvocab_tokenized}
        self.vocab_frame = pd.DataFrame(vocab_frame_data, index=totalvocab_stemmed)
        self.vocab_frame = self.vocab_frame[self.vocab_frame['words'].apply(lambda x: len(x) > 2)]
        
        self.vectorizer()

    def vectorizer(self):
        #define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(max_df=0.85, max_features=200000,
                                        min_df=0.02, stop_words='english',
                                        use_idf=True,tokenizer=self.tokenize_and_stem, ngram_range=(1,3))

        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.content) #fit the vectorizer to synopses

        self.terms = tfidf_vectorizer.get_feature_names_out()
        self.dist = 1 - cosine_similarity(self.tfidf_matrix)
        self.kmeansClustering()

    def kmeansClustering(self):
        self.km = KMeans(n_clusters=self.num_clusters)
        self.km.fit(self.tfidf_matrix)
        self.clusters = self.km.labels_.tolist()
        self.loadModel()
        self.showTopTerms()
        self.scaling()
    
    def saveModel(self):
        if os.path.exists('./doc_cluster.pkl'):
            os.remove('./doc_cluster.pkl')
        joblib.dump(self.km, 'doc_cluster.pkl')
        print("'doc_cluster.pkl' creado")
        self.km = joblib.load('doc_cluster.pkl')

    def loadModel(self):
        self.saveModel()
        files = {'title': self.titles, 'content': self.content, 'cluster': self.clusters}
        self.frame = pd.DataFrame(files, index = [self.clusters] , columns = ['title', 'cluster'])
    
    def showTopTerms(self):
        print("Top terms per cluster:")
        order_centroids = self.km.cluster_centers_.argsort()[:, ::-1] 

        self.cluster_names = {}

        for i in range(self.num_clusters):
            print("Cluster %d words:" % i, end='')

            top_words = []
            for ind in order_centroids[i, :]:
                term = self.terms[ind]
                if len(term) > 2:  # Filtrar palabras cortas
                    if term in self.vocab_frame.index:
                        word = self.vocab_frame.loc[term]['words']
                        if isinstance(word, pd.Series):
                            word = word.iloc[0]  # Si es una serie, toma el primer elemento
                        word = word.encode('utf-8', 'ignore').decode()
                        top_words.append(word)
                    else:
                        top_words.append(term) 
                if len(top_words) >= 3:  # Mostrar solo las 3 principales palabras
                    break

            self.cluster_names[i] = ', '.join(top_words)

            for word in top_words:
                print(f' {word}', end=',')
            print()

            print("Cluster %d titles:" % i, end='')
            for title in self.frame.loc[i]['title'].values.tolist():
                print(f' {title}', end=',')
            print()

    def scaling(self):
        # convert two components as we're plotting points in a two-dimensional plane
        # "precomputed" because we provide a distance matrix
        # we will also specify `random_state` so the plot is reproducible.
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(self.dist)  # shape (n_components, n_samples)
        self.xs, self.ys = pos[:, 0], pos[:, 1]
        self.loadClusters()

    def loadClusters(self):
        self.cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3'}
        
        #create data frame that has the result of the MDS plus the cluster numbers and titles
        self.df = pd.DataFrame(dict(x=self.xs, y=self.ys, label=self.clusters, title=self.titles)) 

        #group by cluster
        self.groups = self.df.groupby('label')

        # set up plot
        fig, self.ax = plt.subplots(figsize=(17, 9)) # set size
        self.ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
        self.groupLayers()

    def showFigures(self):
        self.vocab()
        self.showVisualDocument()
        self.showHierarchicalDocument()

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

    def setClusters(self, num_clusters):
        self.num_clusters = num_clusters
    
    def setContents(self, contents):
        self.content = contents

    def setTitles(self, titles):
        self.titles = titles
