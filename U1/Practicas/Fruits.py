import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



iris = datasets.load_iris()
data = iris.data
labels = iris.target

for i in [0, 79, 99, 121]:
    print(f"index: {i:3}, features: {data[i]}, label: {labels[i]}")

# seeding is only necessary for the website
#so that the values are always equal:
np.random.seed(42)
indices = np.random.permutation(len(data))

n_test_samples = 12     # number of test samples
learn_data = data[indices[:-n_test_samples]]
learn_labels = labels[indices[:-n_test_samples]]
test_data = data[indices[-n_test_samples:]]
test_labels = labels[indices[-n_test_samples:]]

print("The first samples of our learn set:")
print(f"{'index':7s}{'data':20s}{'label':3s}")
for i in range(5):
    print(f"{i:4d}   {learn_data[i]}   {learn_labels[i]:3}")

print("The first samples of our test set:")
print(f"{'index':7s}{'data':20s}{'label':3s}")
for i in range(5):
    print(f"{i:4d}   {learn_data[i]}   {learn_labels[i]:3}")

def vote(neighbors):
    class_counter = Counter()
    for neighbor in neighbors:
        class_counter[neighbor[2]] += 1
    return class_counter.most_common(1)[0][0]

def create_features(number_samples, *min_max_features):
    """ Creates an array with number_samples rows and len(min_max_features) columns """
    features = []
    for min_val, max_val,rounding in min_max_features:
        features.append(np.random.uniform(min_val, max_val, number_samples).round(rounding))
    result = np.column_stack(features)
    return result

def get_neighbors(training_set, 
                  labels, 
                  test_instance, 
                  k, 
                  distance):
    """
    get_neighors calculates a list of the k nearest neighbors
    of an instance 'test_instance'.
    The function returns a list of k 3-tuples.
    Each 3-tuples consists of (index, dist, label)
    where 
    index    is the index from the training_set, 
    dist     is the distance between the test_instance and the 
             instance training_set[index]
    distance is a reference to a function used to calculate the 
             distances
    """
    distances = []
    for index in range(len(training_set)):
        dist = distance(test_instance, training_set[index])
        distances.append((training_set[index], dist, labels[index]))
    distances.sort(key=lambda x: x[1])
    neighbors = distances[:k]
    return neighbors

def distance(instance1, instance2):
    """ Calculates the Eucledian distance between two instances""" 
    return np.linalg.norm(np.subtract(instance1, instance2))

print(distance([3, 5], [1, 1]))
print(distance(learn_data[3], learn_data[44]))

num_apples, num_mangos, num_lemons = 150, 150, 150
sweetness = (10, 18, 0)
acidity = 3.4, 4, 2
weight = 140.0, 250.0, 0
apples = create_features(num_apples, sweetness, acidity, weight)
apples[:20] # The first 20 fruits
print(apples[:20])


sweetness = (6, 14, 0)
acidity = 3.6, 6, 1       # should be between 5.8 and 6
weight = 100.0, 300.0, 0
mangos = create_features(num_mangos, sweetness, acidity, weight)

sweetness = (6, 12, 0)
acidity = 2.0, 2.6, 1
weight = 130, 170, 0
lemons = create_features(num_lemons, sweetness, acidity, weight)

# Combine the data and create labels
X = np.vstack((apples, mangos, lemons))
y = np.array(['Apple'] * num_apples + ['Mango'] * num_mangos + ['Lemon'] * num_lemons)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Define the DataFrame
df = pd.DataFrame(X, columns=['Sweetness', 'Acidity', 'Weight'])
df['Fruit'] = y

# Write DataFrame to CSV file
df.to_csv('fruits_data.csv', index=False)





n_test_samples = len(X_test)
    
for i in range(20):
    neighbors = get_neighbors(X_train, 
                              y_train, 
                              X_test[i], 
                              6, 
                              distance=distance)

    print("index: ", i, 
          ", result of vote: ", 
          vote_harmonic_weights(neighbors,
                                all_results=True))