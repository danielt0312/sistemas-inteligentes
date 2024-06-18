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

        self.vectorizer = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS) + ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'es', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosostros', 'vosostras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'esté', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaría', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviera', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviese', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad'])
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
            print(f"No valid paragraphs in file: {file}")
            return
        vtest = self.vectorizer.transform(paragraphs)
        prediction = self.classifier.predict(vtest)[0]
        probabilities = self.classifier.predict_proba(vtest)[0]
        labels_prob = ", ".join([f"{label}: {prob:.2%}" for label, prob in zip(self.labels, probabilities)])
        print(f"{self.labels[prediction]} [{labels_prob}]\t| '{file}'")

    def loadLabels(self, files):
        self.labels = {fname[:2] for fname in files if fname.endswith(".txt")}
        self.labels = sorted(list(self.labels))

    def text2paragraphs(self, filename, min_size=1):
        txt = open(filename).read()
        paragraphs = [para for para in txt.split("\n\n") if len(para) > min_size]
        return paragraphs
    
    def setDirTrain(self, dir_train):
        self.dir_train = dir_train
