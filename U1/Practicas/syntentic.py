import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

centers = [[2, 3], [4, 5], [7, 9]]
data, labels = make_blobs(n_samples=1000, 
                          centers=np.array(centers),
                          random_state=1)

labels[:7]

# some more blobs
fig, ax = plt.subplots()

colours = ('green', 'orange', 'blue')
for label in range(len(centers)):
    ax.scatter(x=data[labels==label, 0], 
               y=data[labels==label, 1], 
               c=colours[label], 
               s=40, 
               label=label)

ax.set(xlabel='X',
       ylabel='Y',
       title='Blobs Examples')


ax.legend(loc='upper right')

plt.show()

labels = labels.reshape((labels.shape[0],1))
all_data = np.concatenate((data, labels), axis=1)
all_data[:7]

np.savetxt("squirrels.txt", 
           all_data,
           fmt=['%.3f', '%.3f', '%1d'])
all_data[:10]