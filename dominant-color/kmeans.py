import numpy as np
import matplotlib.pyplot as plt

# read file
im = plt.imread("greyscale.png")

dataIN = (im[:,:,0] * 255).astype(int)
[width, height] = [np.shape(dataIN)[0], np.shape(dataIN)[1]]

#variable
current = np.zeros((np.shape(dataIN)[0],np.shape(dataIN)[1]))

# variable
k = 9

# variable
centroids = np.linspace(np.amin(dataIN), np.amax(dataIN), num = k).astype(int)

def get_distances(data, centroids):

    distances = np.zeros((np.shape(data)[0], np.shape(data)[1], len(centroids)))
    
    for a in range(len(centroids)):
        distances[:,:,a] = np.absolute(data[:,:] - centroids[a])
    
    return distances

distances = get_distances(dataIN, centroids)

def closest_centroid(distances, centroids):
    for a in range(len(centroids)):
        if distances[a] == np.amin(distances):
            return centroids[a]
    return False

def update_centroid(original, current, centroid):
    summ = 0
    total = 0
    for yy in range(height):
        for xx in range(width):
            if current[xx, yy] == centroid:
                summ += original[xx, yy]
                total += 1
    return (summ / total).astype(int)

# main
iteration = 0
while True:

    for yy in range(height):
        for xx in range(width):
            current[xx, yy] = closest_centroid(distances[xx, yy, :], centroids)
    
    if iteration == 5:
        break
    
    # update centroids
    for cent in range(k):
        centroids[cent] = update_centroid(dataIN, current, centroids[cent])
 
    # calculate new distances
    distances = get_distances(current, centroids)

    iteration += 1

f, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))
ax1.imshow(dataIN, cmap = "gray", aspect = "equal" )
ax2.imshow(current, cmap = "gray", aspect = "equal")
plt.show()



