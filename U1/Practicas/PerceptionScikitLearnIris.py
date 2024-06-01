import numpy as np
import random
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.metrics import classification_report

iris = load_iris()

iris.target_names

datasets = train_test_split(iris.data, 
                            iris.target,
                            test_size=0.2)

train_data, test_data, train_labels, test_labels = datasets

p = Perceptron(random_state=42,
               max_iter=30,
               tol=0.001)
p.fit(train_data, train_labels)

sample = random.sample(range(len(train_data)), 10)

for i in sample:
    #print(i, p.predict([train_data[i]]))
    print(i, p.predict([train_data[i]]), train_labels[i])


print(classification_report(p.predict(train_data), train_labels))

print(classification_report(p.predict(test_data), test_labels))
