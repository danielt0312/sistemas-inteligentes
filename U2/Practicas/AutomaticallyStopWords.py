from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

corpus = ["""People say you cannot live without love, 
             but I think oxygen is more important""",
          "Sometimes, when you close your eyes, you cannot see."
          "A horse, a horse, my kingdom for a horse!",
          """Horse sense is the thing a horse has which 
          keeps it from betting on people."""
          """I’ve often said there is nothing better for 
          the inside of the man, than the outside of the horse.""",
          """A man on a horse is spiritually, as well as physically, 
          bigger then a man on foot.""",
          """No heaven can heaven be, if my horse isn’t there 
          to welcome me."""]

cv = CountVectorizer(min_df=2)
count_vector = cv.fit_transform(corpus)

print(cv.vocabulary_)
print(cv.stop_words_)

print("number of docus, size of vocabulary, stop_words list size")
for i in range(1, len(corpus)):
    cv = CountVectorizer(min_df=i)
    count_vector = cv.fit_transform(corpus)
    len_voc = len(cv.vocabulary_)
    len_stop_words = len(cv.stop_words_)
    print(f"{i:10d} {len_voc:15d} {len_stop_words:19d}")
    