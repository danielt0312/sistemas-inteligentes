from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

corpus = ["A horse, a horse, my kingdom for a horse!",
          "Horse sense is the thing a horse has which keeps it from betting on people."
          "I’ve often said there is nothing better for the inside of the man, than the outside of the horse.",
          "A man on a horse is spiritually, as well as physically, bigger then a man on foot.",
          "No heaven can heaven be, if my horse isn’t there to welcome me."]

cv = CountVectorizer(stop_words=["my", "for","the", "has", "than", "if", 
                                 "from", "on", "of", "it", "there", "ve",
                                 "as", "no", "be", "which", "isn", "to", 
                                 "me", "is", "can", "then"])
count_vector = cv.fit_transform(corpus)
count_vector.shape

print (cv.vocabulary_)
print ()

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

newsgroups_train = fetch_20newsgroups(subset='train',
                                      remove=('headers', 'footers', 'quotes'))
newsgroups_test = fetch_20newsgroups(subset='test',
                                     remove=('headers', 'footers', 'quotes'))

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