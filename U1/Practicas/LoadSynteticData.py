import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from sklearn.datasets import fetch_olivetti_faces


file_data = np.loadtxt("squirrels.txt")

data = file_data[:,:-1]
labels = file_data[:,-1]

print (data)
print (labels)

# sahara squirrel dataset graph

colours = ('green', 'red', 'blue', 'magenta', 'yellow', 'cyan')
n_classes = 3

fig, ax = plt.subplots()
for n_class in range(0, n_classes):
    ax.scatter(data[labels==n_class, 0], data[labels==n_class, 1], 
               c=colours[n_class], s=10, label=str(n_class))

ax.set(xlabel='Night Vision',
       ylabel='Fur color from sandish to black, 0 to 10 ',
       title='Sahara Virtual Squirrel')


ax.legend(loc='upper right')

"""
data_sets = train_test_split(data, 
                       labels, 
                       train_size=0.8,
                       test_size=0.2,
                       random_state=42 # garantees same output for every run
                      )
train_data, test_data, train_labels, test_labels = data_sets
"""


res = train_test_split(data, labels, 
                       train_size=0.8,
                       test_size=0.2,
                       random_state=12)
train_data, test_data, train_labels, test_labels = res 


iris = datasets.load_iris()   # - 3%        (1/30)
# iris = datasets.load_wine()   - 27%       (10/36)
# iris = datasets.load_digits() - .5%       (9/360)
#iris = fetch_olivetti_faces()  - 266       (21/80)
data, labels = iris.data, iris.target

print ("Total de datos:" , len(data))
print ("Total de entren.:", len(train_data))
print ("Total de prueba:", len(test_data))
print ("Etiquetas de entren.:", len(train_labels))
print ("Etiquetas de prueba:", len(test_labels))

# Create and fit a nearest-neighbor classifier
knn = KNeighborsClassifier()
knn.fit(train_data, train_labels) 

predicted = knn.predict(test_data)
print("Predictions from the classifier:")
print(predicted)
print("Target values:")
print(test_labels)

malos = 0
for i, predict in enumerate(predicted):
    if (predict != test_labels[i]): 
        malos+=1

print ("Erroneos: ", malos)

plt.show()

