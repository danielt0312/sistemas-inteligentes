import matplotlib.pyplot as plt
import numpy as np

X = np.arange(0, 7)
print (X)
fig, ax = plt.subplots()

ax.plot(3.5, 1.8, "o", 
        color="darkorange", 
        markersize=15)
ax.plot(1.1, 3.9, "oy", 
        markersize=15)

point_on_line = (4, 4.5)
# calculate gradient:
m = point_on_line[1] / point_on_line[0]  
print (m*X)
ax.plot(X, m * X, "g-", linewidth=3)

lemon = (1.1, 3.9)
orange = (3.5, 1.8)
m = 4.5 / 4

# check if the orange is below the line,
# a positive value is expected:
print(orange[0] * m - orange[1])

# check if the lemon is above the line,
# a negative value is expected:
print(lemon[0] * m - lemon[1])

plt.show()