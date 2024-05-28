import pandas as pd
import numpy as np
from sklearn import datasets
#We use Support Vector classifier as a classifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
# Splitting the dataset to Train and test
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
print (type(iris))

# Convierte un dataset de scikitlearn a Dataframe
df = pd.DataFrame(
    data = np.c_[iris['data'],
    iris['target']],
    columns = iris['feature_names'] + ['target'])

print (type(df))
X = df.drop(['target'], axis = 1)
y = df['target']
print (X)
print (y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#to know the shape of the train and test dataset.
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

# Crear el modelo
knn = KNeighborsClassifier()

# Entregarlo
knn.fit(X_train, y_train)

# Usarlo para predecir (el conjunto de entrenamiento)
knn.predict(X_train)

# Usarlo para predecir el conjunto de prueba
y_pred = knn.predict(X_test)

# Crea la matriz de confusión
cm = confusion_matrix(y_test, y_pred)

print(cm)

# Creating a dataframe for a array-formatted Confusion matrix,so it will be easy for plotting.
cm_df = pd.DataFrame(cm,
                     index = ['SETOSA','VERSICOLR','VIRGINICA'], 
                     columns = ['SETOSA','VERSICOLR','VIRGINICA'])