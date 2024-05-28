import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

number_of_samples = 9
centers = [(1, 1.5), (1.5, 1)]
#centers = [(0,0), (10,10)]
data, labels = make_blobs(n_samples=number_of_samples, 
                          cluster_std=0.2,
                          centers=np.array(centers),
                          random_state=42)

fruits = [(data[i], labels[i]) for i in range(len(data))]

fig, ax = plt.subplots()
colours = ["yellow", "orange"]
label_name = ["Lemons", "Oranges"]
for label in range(0, 2):
    ax.scatter(data[labels==label, 0], 
               data[labels==label, 1], 
               c=colours[label], 
               s=60, 
               label=label_name[label])

ax.set(xlabel='X', ylabel='Y', title='fruits');

slope = 0.3

def adjust(slope=0.3, delta=0.1):
    # Initialize variables
    counter = -1
    
    # Iterate through data points and labels
    for point, label in zip(data, labels):
        counter += 1
        x, y = point
        
        # Plot data points
        ax.scatter(x, y, color="yellow" if label == 0 else "orange")
        ax.annotate(str(counter), (x, y))
        
        # Calculate position of the point relative to the line
        pos2line = slope * x - y
        # Calculate target slope for adjusting the line
        target_slope = (y + delta) / x
        # Calculate error in current slope
        error = target_slope - slope
        
        # Adjust slope based on point's label and position relative to the line
        if (label == 1 and pos2line < 0) or (label == 0 and pos2line > 0):
            # Update slope based on error
            slope += error 
        
        # Plot the adjusted line
        ax.plot(X, slope * X, linewidth=2, label=str(counter))
    
    # Return the adjusted slope
    return slope


X = np.arange(0, 3)
fig, ax = plt.subplots()
colours = ["orange", "yellow"]
label_name = ["Oranges", "Lemons"]

ax.set(xlabel='X', ylabel='Y', title='fruits')
slope_count = 1
ax.plot(X, 
        slope * X,  
        linewidth=2,
        label="initial")
slope = adjust(slope, delta=0.1)

ax.legend()
ax.grid()

print(f'The final value for the slope: {slope}')

plt.show()




start_slope = 0.3

def adjust(slope=0.3, delta=0.1):
    # Initialize variables
    counter = -1
    
    # Iterate through data points and labels
    for point, label in zip(data, labels):
        counter += 1
        x, y = point
        
        # Plot data points
        ax.scatter(x, y, color="yellow" if label == 0 else "orange")
        ax.annotate(str(counter), (x, y))
        
        # Calculate position of the point relative to the line
        pos2line = slope * x - y
        # Calculate target slope for adjusting the line
        target_slope = (y + delta) / x
        # Calculate error in current slope
        error = target_slope - slope
        
        # Adjust slope based on point's label and position relative to the line
        if (label == 1 and pos2line < 0) or (label == 0 and pos2line > 0):
            # Update slope based on error
            slope += error 
        
        # Plot the adjusted line
        ax.plot(X, slope * X, linewidth=2, label=str(counter))
    
    # Return the adjusted slope
    return slope


fig, ax = plt.subplots()
colours = ["orange", "yellow"]
label_name = ["Oranges", "Lemons"]


ax.set(xlabel='X', ylabel='Y', title='fruits')
slope_count = 1
ax.plot(X, 
        start_slope * X,  
        linewidth=2,
        label="initial")
slope = adjust(start_slope, delta=0.1)

ax.legend()
ax.grid()
print(f'The final value for the slope: {slope}')
plt.show()






learning_rate, start_slope, delta = 0.1, 0.3, 0.1

def adjust(slope=0.3, learning_rate=0.3, delta=0.3):
    counter = -1
    for (x, y), label in zip(data, labels):
        counter += 1 

        # Plot data points
        ax.scatter(x, y, color="yellow" if label == 0 else "orange")
        ax.annotate(str(counter), (x, y))
 
        # Calculate position of the point relative to the line
        pos2line = slope * x - y
        # Calculate target slope for adjusting the line
        target_slope = (y + delta) / x
        # Calculate error in current slope
        error = target_slope - slope
        
        # Adjust slope if the point is on the wrong side of the line
        if (label == 1 and pos2line < 0) or (label == 0 and pos2line > 0):
            slope += error * learning_rate
            # Plot the adjusted line
            ax.plot(X, slope * X, linewidth=2, label=str(counter))
            
    return slope


fig, ax = plt.subplots()
colours = ["orange", "yellow"]
label_name = ["Oranges", "Lemons"]


ax.set(xlabel='X', ylabel='Y', title='fruits')
slope_count = 1
ax.plot(X, 
        start_slope * X,  
        linewidth=2,
        label="initial")
slope = adjust(start_slope, learning_rate, delta)

ax.legend()
ax.grid()
plt.show()

print(slope)







fig, ax = plt.subplots()
colours = ["orange", "yellow"]
label_name = ["Oranges", "Lemons"]


ax.set(xlabel='X', ylabel='Y', title='fruits')
slope_count = 1
ax.plot(X, 
        start_slope * X,  
        linewidth=2,
        label="initial")
slope = adjust(start_slope, learning_rate, delta)
# redo the learning, we use the current slope as the start slope:
slope = adjust(slope, learning_rate, delta)
# and again once more:
slope = adjust(slope, learning_rate, delta)

ax.legend()
ax.grid()
plt.show()

print(slope)