import matplotlib.pyplot as plt
import numpy as np

def plot_fruits(p1, p2, point_on_line=(5,1)):
    X = np.arange(0, 7)
    fig, ax = plt.subplots()
    ax.plot(p1[0], p1[1], "o", 
            color="darkorange", 
            markersize=15)
    ax.annotate("Orange", 
                xy=(p1[0], p1[1]), 
                xytext=(p1[0]+0.5, p1[1]+0.5),
                arrowprops=dict(facecolor='orange', shrink=0.05))
    ax.plot(p2[0], p2[1], "o", 
            color="yellow", 
            markersize=15)
    ax.annotate("Lemon", 
                xy=(p2[0], p2[1]), 
                xytext=(p2[0]-0.5, p2[1]-0.5),
                arrowprops=dict(facecolor='orange', shrink=0.05))
    ax.plot(*point_on_line, "x", 
            color="darkorange", 
            markersize=15)
    # calculate gradient:
    m = point_on_line[1] / point_on_line[0]  
    ax.plot(X, m * X, "g-", linewidth=3)
    plt.show()


orange = (4, 2)
lemon = (1, 3)
point = (5, 1)
plot_fruits(p1=orange, p2=lemon, point_on_line=point)