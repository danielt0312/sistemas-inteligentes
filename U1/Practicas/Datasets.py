from sklearn import datasets
import matplotlib.pyplot as plt

wine = datasets.load_wine()

print (wine.target)
#print(wine.DESCR)
print(len(wine.feature_names))



#features = 'ash', 'color_intensity'
features = 'magnesium', 'proline'
features_index = [wine.feature_names.index(features[0]),
                  wine.feature_names.index(features[1])]


colors = ['blue', 'red', 'green']

for label, color in zip(range(len(wine.target_names)), colors):
    plt.scatter(wine.data[wine.target==label, features_index[0]], 
                wine.data[wine.target==label, features_index[1]],
                label=wine.target_names[label],
                c=color)

plt.xlabel(features[0])
plt.ylabel(features[1])
plt.legend(loc='upper left')
plt.show() # wine dataset scatter plot