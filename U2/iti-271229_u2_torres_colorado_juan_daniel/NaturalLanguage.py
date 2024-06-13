from sklearn.feature_extraction import text

corpus = ["To be, or not to be, that is the question:",
          "Whether 'tis nobler in the mind to suffer",
          "The slings and arrows of outrageous fortune,"]

vectorizer = text.CountVectorizer()
print(vectorizer)
print(vectorizer.fit(corpus))
print("Vocabulary: ", vectorizer.vocabulary_)
print(vectorizer.get_feature_names_out())
print(list(vectorizer.vocabulary_.keys()))

token_count_matrix = vectorizer.transform(corpus)
print(token_count_matrix)

dense_tcm = token_count_matrix.toarray()
print(dense_tcm)

feature_names = vectorizer.get_feature_names_out()
for el in vectorizer.vocabulary_:
    print(el, end=(", "))