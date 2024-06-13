from sklearn.feature_extraction import text
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics


n = 25
print(str(n) + " arbitrary words from ENGLISH_STOP_WORDS:")
counter = 0
for word in text.ENGLISH_STOP_WORDS:
    if counter == n - 1:
        print(word)
        break
    print(word, end=", ")
    counter += 1

vectorizer = CountVectorizer(stop_words=list(text.ENGLISH_STOP_WORDS))

vectors = vectorizer.fit_transform(newsgroups_train.data)

# creating a classifier
classifier = MultinomialNB(alpha=.01)
classifier.fit(vectors, newsgroups_train.target)

vectors_test = vectorizer.transform(newsgroups_test.data)

predictions = classifier.predict(vectors_test)
accuracy_score = metrics.accuracy_score(newsgroups_test.target, 
                                        predictions)
f1_score = metrics.f1_score(newsgroups_test.target, 
                            predictions, 
                            average='macro')

print("accuracy score: ", accuracy_score)
print("F1-score: ", f1_score)