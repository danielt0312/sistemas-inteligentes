from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
import numpy as np

class NaiveBayesClassifier:
    def __init__(self):
        self.class_probs = {}
        self.feature_probs = {}

    def fit(self, X, y):
        """  This method takes input data `X` (features) and `y` 
        (labels) and calculates the probabilities needed for classification.
        It first calculates the probabilities of each class occurring in the
        dataset (`class_probs`).
        Then, it calculates for each class the probabilities of each feature 
        given the class (`feature_probs`).
        It uses Laplace smoothing to handle cases where a feature value is 
        unseen in the training data."""
        
        # Calculate class probabilities
        class_counts = defaultdict(int)
        for label in y:
            class_counts[label] += 1
        total_samples = len(y)
        for label, count in class_counts.items():
            self.class_probs[label] = count / total_samples

        # Calculate feature probabilities
        self.feature_probs = {}
        for label in self.class_probs:
            #create a boolean array (label_indices) indicating which samples 
            # in the dataset have the current class label:
            label_indices = (y == label)
            # This selects the samples from the input dataset X that belong 
            # to the current class:
            label_X = X[label_indices]
            feature_probs = {}
            for feature in range(X.shape[1]):
                feature_counts = defaultdict(int)
                for sample in label_X:
                    feature_val = sample[feature]
                    feature_counts[feature_val] += 1
                total_samples_label = len(label_X)
                feature_probs[feature] = {val: count / total_samples_label for val, count in feature_counts.items()}


                feature_probs[feature] = {val: (count + 1) / (total_samples_label + len(feature_counts))  # Laplace smoothing
                                                 for val, count in feature_counts.items()}
            self.feature_probs[label] = feature_probs

    def _calculate_probability(self, x, feature, label):
        """ This method calculates the probability of a given feature 
        value occurring given a class label."""
        if x in self.feature_probs[label][feature]:
            return self.feature_probs[label][feature][x]
        else:
            return 1e-6  # Smoothing for unseen feature values

    def _predict_sample(self, x):
        """  This method predicts the label of a single sample by 
        calculating the probability of each class given the sample's 
        features and selecting the class with the highest 
        probability."""
        max_prob = -1
        best_label = None
        for label, class_prob in self.class_probs.items():
            prob = class_prob
            for feature, value in enumerate(x):
                prob *= self._calculate_probability(value, feature, label)
            if prob > max_prob:
                max_prob = prob
                best_label = label
        return best_label

    def predict(self, X):
        """ This method takes input data `X` and predicts the labels for each sample using
        the `_predict_sample` method. """
        return [self._predict_sample(sample) for sample in X]

# Data
data = [
    ["Strawberry", "Red", "Smooth", "Sweet", "Desserts", "Fruit"],
    ["Celery", "Green", "Crisp", "Mild", "Salads", "Vegetable"],
    ["Pineapple", "Yellow", "Rough", "Sweet", "Snacks", "Fruit"],
    ["Spinach", "Green", "Tender", "Mild", "Salads", "Vegetable"],
    ["Blueberry", "Blue", "Smooth", "Sweet", "Baking", "Fruit"],
    ["Cucumber", "Green", "Crisp", "Mild", "Salads", "Vegetable"],
    ["Watermelon", "Red", "Juicy", "Sweet", "Snacks", "Fruit"],
    ["Carrot", "Orange", "Crunchy", "Sweet", "Salads", "Vegetable"],
    ["Grapes", "Purple", "Juicy", "Sweet", "Snacks", "Fruit"],
    ["Bell Pepper", "Red", "Crisp", "Mild", "Cooking", "Vegetable"],
    ["Kiwi", "Brown", "Fuzzy", "Tart", "Snacks", "Fruit"],
    ["Lettuce", "Green", "Tender", "Mild", "Salads", "Vegetable"],
    ["Mango", "Orange", "Smooth", "Sweet", "Desserts", "Fruit"],
    ["Potato", "Brown", "Starchy", "Mild", "Cooking", "Vegetable"],
    ["Apple", "Red", "Crunchy", "Sweet", "Snacks", "Fruit"],
    ["Onion", "White", "Firm", "Pungent", "Cooking", "Vegetable"],
    ["Orange", "Orange", "Smooth", "Sweet", "Snacks", "Fruit"],
    ["Garlic", "White", "Firm", "Pungent", "Cooking", "Vegetable"],
    ["Peach", "Orange", "Smooth", "Sweet", "Desserts", "Fruit"],
    ["Broccoli", "Green", "Tender", "Mild", "Cooking", "Vegetable"],
    ["Cherry", "Red", "Juicy", "Sweet", "Snacks", "Fruit"],
    ["Peas", "Green", "Soft", "Sweet", "Cooking", "Vegetable"],
    ["Pear", "Green", "Juicy", "Sweet", "Snacks", "Fruit"],
    ["Cabbage", "Green", "Crisp", "Mild", "Cooking", "Vegetable"],
    ["Grapefruit", "Pink", "Juicy", "Tart", "Snacks", "Fruit"],
    ["Asparagus", "Green", "Tender", "Mild", "Cooking", "Vegetable"]
]

# Convert data to a numpy array
data = np.array(data)

# Split features and labels
X = data[:, :-1]  # Features
y = data[:, -1]   # Labels

# Encode categorical features into numerical values
# Encode categorical features into numerical values using a single LabelEncoder
label_encoder = LabelEncoder()
X_encoded = np.array([label_encoder.fit_transform(sample) for sample in X])

print (X_encoded)

# Split data into training and test sets
X_train = X_encoded[:20]
y_train = y[:20]
X_test = X_encoded[20:]
y_test = y[20:]

print(len(X_train))
print(len(X_test))

# Train the classifier
nb_classifier = NaiveBayesClassifier()
nb_classifier.fit(X_train, y_train)

# Predict on the test data
y_pred = nb_classifier.predict(X_test)

print(y_pred)

# Calculate accuracy
correct_predictions = sum(1 for pred, true in zip(y_pred, y_test) if pred == true)
total_predictions = len(y_test)
accuracy = correct_predictions / total_predictions
print("Accuracy:", accuracy)