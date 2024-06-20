from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB

"""
Clase para determinar si un archivo TXT está mayormente escrito en español o inglés
"""
class Classifier():
    # Constructor
    def __init__(self, dir_train, files_train):
        self.createClassifier(dir_train, files_train)

    # Crear clasificador que sirva para poder identificar el idioma de un documento
    def createClassifier(self, dir_train, files_train):
        self.labels = ['es', 'en']
        self.setDirTrain(dir_train)

        self.vectorizer = TfidfVectorizer(stop_words= list(ENGLISH_STOP_WORDS) + self.SPANISH_STOP_WORDS())
        self.train_test(files_train)

        # Perform Grid Search to find the best alpha
        self.classifier = MultinomialNB()
        param_grid = {'alpha': [0.01, 0.1, 0.5, 1.0, 5.0, 10.0]}
        grid_search = GridSearchCV(self.classifier, param_grid, cv=5)
        grid_search.fit(self.vectors, self.train_targets)
        self.classifier = grid_search.best_estimator_

    # Entrenar el clasificador
    def train_test(self, files_train):
        self.data = []
        self.targets = []

        for fname in files_train:
            if fname.endswith('.txt'):
                self.load_data_targets(fname)

        train_data, test_data, self.train_targets, test_targets = train_test_split(self.data, self.targets, train_size=0.8, test_size=0.2, random_state=42)
        self.vectors = self.vectorizer.fit_transform(train_data)

    # Cargar data y targets para los vectores
    def load_data_targets(self, fname):
        paras = self.text2paragraphs(self.dir_train + '/' + fname)
        self.data.extend(paras)
        country = fname[:2]
        index = self.labels.index(country)
        self.targets += [index] * len(paras)

    # Clasificar el idioma de un documento de acuerdo a un archivo proporcionado
    def classify(self, dir_file, fname):
        paragraphs = self.text2paragraphs(dir_file)
        if not paragraphs:
            print(f"No valid paragraphs in file: {dir_file}")
            return

        word_counts = {label: 0 for label in self.labels}
        for paragraph in paragraphs:
            words = paragraph.split()
            vector = self.vectorizer.transform([paragraph])
            prediction = self.classifier.predict(vector)[0]
            word_counts[self.labels[prediction]] += len(words)

        label = 'es' if word_counts['es'] > word_counts['en'] else 'en'
        print(f"{label} [{self.labels[0]}: {word_counts['es']}, {self.labels[1]}: {word_counts['en']}]\t| '{fname}'")
        return label

    # Convertir un archivo TXT a un parrafo
    def text2paragraphs(self, filename, min_size=100):
        with open(filename, 'r', encoding='utf-8') as file:
            txt = file.read()
        paragraphs = [para for para in txt.split("\n\n") if len(para) > min_size]
        return paragraphs
    
    # Establecer el directorio en donde se encuentran los archivos para entrenar el clasificador
    def setDirTrain(self, dir_train):
        self.dir_train = dir_train

    # Stop Words para el idioma español
    def SPANISH_STOP_WORDS(self):
        return [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 
            'su', 'al', 'es', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'sí', 'porque', 'esta', 'entre', 
            'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 
            'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 
            'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 
            'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 
            'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 
            'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 
            'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 
            'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'esté', 'estemos', 'estéis', 'estén', 'estaré', 
            'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaría', 'estaríamos', 
            'estaríais', 'estarían', 'estaba', 'estabas', 'estaba', 'estábamos', 'estabais', 'estaban', 'estuve', 
            'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviera', 
            'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviese', 'estuviésemos', 
            'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad'
        ]
