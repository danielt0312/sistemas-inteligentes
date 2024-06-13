import pandas as pd
from sklearn.feature_extraction import text
corpus = ["It does not matter what you are doing, just do it!",
          "Would you work if you won the lottery?",
          "You like Python, he likes Python, we like Python, everybody loves Python!"
          "You said: 'I wish I were a Python programmer'",
          "You can stay here, if you want to. I would, if I were you."
         ]
vectorizer = text.CountVectorizer()
vectorizer.fit(corpus)

token_count_matrix = vectorizer.transform(corpus)
print(token_count_matrix)

tf_idf = text.TfidfTransformer()
tf_idf.fit(token_count_matrix)

tf_idf.idf_

vectorizer = text.CountVectorizer()
print(vectorizer)

vectorizer.fit(corpus)

print("Vocabulary: ", vectorizer.vocabulary_)

print(list(vectorizer.vocabulary_.keys()))

token_count_matrix = vectorizer.transform(corpus)
print(token_count_matrix)

dense_tcm = token_count_matrix.toarray()
print(dense_tcm)

feature_names = vectorizer.get_feature_names_out()
for el in vectorizer.vocabulary_:
    print(el, end=(", "))

pd.DataFrame(data=dense_tcm, 
             index=['corpus_0', 'corpus_1', 'corpus_2'],
             columns=vectorizer.get_feature_names_out())

word = "be"
i = 1
j = vectorizer.vocabulary_[word]
print("number of times '" + word + "' occurs in:")
for i in range(len(corpus)):
     print("    '" + corpus[i] + "': " + str(dense_tcm[i][j]))

txt = "That is the question and it is nobler in the mind."
vectorizer.transform([txt]).toarray()

print(vectorizer.get_feature_names_out())

print(vectorizer.vocabulary_)
