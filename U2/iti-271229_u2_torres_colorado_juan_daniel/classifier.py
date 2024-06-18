import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB

"""
Clase para determinar si un archivo TXT está mayormente escrito en español o inglés
"""
class Classifier():
    def __init__(self, dir_train, files_train):
        self.createClassifier(dir_train, files_train)

    def createClassifier(self, dir_train, files_train):
        self.setDirTrain(dir_train)
        self.train_test(files_train)
        self.classifier = MultinomialNB(alpha=.01)
        self.classifier.fit(self.vectors, self.train_targets)

    def train_test(self, files_train):
        self.data = []
        self.targets = []
        self.loadLabels(files_train) # listar

        for fname in files_train:
            if (fname.endswith('.txt')):
                self.load_data_targets(fname)

        self.train_data, self.test_data, self.train_targets, self.test_targets  = train_test_split(self.data, self.targets, train_size=0.8, test_size=0.2, random_state=42)

        self.vectorizer = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
        self.vectors = self.vectorizer.fit_transform(self.train_data)

    def load_data_targets(self, fname):
        paras = self.text2paragraphs(self.dir_train + '/' + fname)
        self.data.extend(paras)
        country = fname[:2]
        index = self.labels.index(country)
        self.targets += [index] * len(paras)

    def classify(self, file):
        paragraphs = self.text2paragraphs(file)
        if not paragraphs:
            print(f"No se encontraron parrafos en el archivo '{file}'. *** Omitiendo ***")
            return

        vtest = self.vectorizer.transform(paragraphs)
        if vtest.shape[0] == 0:
            print(f"El archivo '{file}' no tiene parrafos validos para la clasificacion. *** Omitiendo ***")
            return

        prediction = self.classifier.predict(vtest)[0]
        print(f"'{file}' : ", self.labels[prediction])


    def loadLabels(self, files):
        self.labels = {fname[:2] for fname in files if fname.endswith(".txt")}
        self.labels = sorted(list(self.labels))

    def text2paragraphs(self, filename, min_size=1):
        txt = open(filename).read()
        paragraphs = [para for para in txt.split("\n\n") if len(para) > min_size]
        return paragraphs
    
    def setDirTrain(self, dir_train):
        self.dir_train = dir_train