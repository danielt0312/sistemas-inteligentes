from sklearn.feature_extraction import text

words = "Cold wind blows over the cornfields".split()
corpus = []
for i in range(1, len(words)+1):
    corpus.append(" ".join(words[:i]))
    
print(corpus)

vectorizer = text.CountVectorizer()

vectorizer = vectorizer.fit(corpus)
vectorized_text = vectorizer.transform(corpus)
tf_idf = text.TfidfTransformer()
tf_idf.fit(vectorized_text)

tf_idf.idf_

word_weight_list = list(zip(vectorizer.get_feature_names_out(), tf_idf.idf_))
word_weight_list.sort(key=lambda x:x[1])  # sort list by the weights (2nd component)
for word, idf_weight in word_weight_list:
    print(f"{word:15s}: {idf_weight:4.3f}")

TfidF = text.TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf = TfidF.fit_transform(vectorized_text)


word_weight_list = list(zip(vectorizer.get_feature_names_out(), tf_idf.idf_))
word_weight_list.sort(key=lambda x:x[1])  # sort list by the weights (2nd component)
for word, idf_weight in word_weight_list:
    print(f"{word:15s}: {idf_weight:4.3f}")