import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

def text2paragraphs(filename, min_size=1):
    """ A text contained in the file 'filename' will be read 
    and chopped into paragraphs.
    Paragraphs with a string length less than min_size will be ignored.
    A list of paragraph strings will be returned"""
    
    txt = open(filename).read()
    paragraphs = [para for para in txt.split("\n\n") if len(para) > min_size]
    return paragraphs

path = "train/"

files = os.listdir(path)
labels = {fname[:2] for fname in files if fname.endswith(".txt")}
labels = sorted(list(labels))
print(labels)

data = []
targets = []

for fname in files:
    if fname.endswith(".txt"):
        paras = text2paragraphs(path + fname, min_size=150)
        data.extend(paras)
        country = fname[:2]
        index = labels.index(country)
        targets += [index] * len(paras)

res = train_test_split(data, targets, 
                       train_size=0.8,
                       test_size=0.2,
                       random_state=42)
train_data, test_data, train_targets, test_targets = res

vectorizer = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
print(vectorizer)

vectors = vectorizer.fit_transform(train_data)

# creating a classifier
classifier = MultinomialNB(alpha=.01)
classifier.fit(vectors, train_targets)

vectors_test = vectorizer.transform(test_data)

predictions = classifier.predict(vectors_test)
accuracy_score = metrics.accuracy_score(test_targets, 
                                        predictions)
f1_score = metrics.f1_score(test_targets, 
                            predictions, 
                            average='macro')

print("accuracy score: ", accuracy_score)
print("F1-score: ", f1_score)


path = "/home/daniel/Descargas/test/documentos/txt/"
files = os.listdir(path)
# print(files)
for fname in files:
    # some_text = read_file_content(path+fname)
    some_text = text2paragraphs(path + fname, min_size=150)
    vtest = vectorizer.transform(some_text)

    # Predict the language of the entire text
    prediction = classifier.predict(vtest)[0]
    print(f"El archivo '{fname}' está en:", labels[prediction])