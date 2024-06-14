from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets

# iris = datasets.load_iris()
iris = datasets.fetch_olivetti_faces()

# data, labels = iris.data
X, Y = iris.data, iris.target

print ('Muestras en el Datasets', len(X))

Clasificadores = [
    RandomForestClassifier(n_estimators=100,criterion="entropy"),
    DecisionTreeClassifier(criterion = 'entropy'),
    GaussianNB(),
    KNeighborsClassifier(),
    AdaBoostClassifier(n_estimators=400,learning_rate=1,algorithm='SAMME'),
    MLPClassifier(hidden_layer_sizes=(5,), 
                    activation='logistic', 
                    alpha=1e-4,
                    solver='sgd', 
                    tol=1e-4,
                    random_state=1,
                    learning_rate_init=.3, 
                    verbose=False)
    ]

#Encode the feature values which are strings to integers
# for label in dataset.columns:
#     dataset[label] = LabelEncoder().fit(dataset[label]).transform(dataset[label])


# X = dataset.drop(['target'],axis=1)
# Y = dataset['target']


#Instantiate the model with 100 trees and entropy as splitting criteria
# Random_Forest_model = RandomForestClassifier(n_estimators=100,criterion="entropy")

for c in Clasificadores:
    print (c)
    for i in range(2, 5):
        #Cross validation
        accuracy = cross_validate(c,X,Y,cv=i)['test_score']
        print('\tCV', str(i) ,'The accuracy is: ',sum(accuracy)/len(accuracy)*100,'%')