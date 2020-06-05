import numpy as np
import matplotlib.pyplot as plt

def importImage(dir):
    im_array = plt.imread("rgb.png")
    im_array = (im_array * 255).astype(int)

    width = np.shape(im_array)[0]
    height = np.shape(im_array)[1]

    return im_array, width, height

def getDistances(array, targets):

    distances = np.zeros((height, width, k))

    for a in range(k):
        distances[:,:,a] = np.absolute(array[:,:] - targets[a])
    
    return distances

image_dir = "./rgb.png"
original, width, height = importImage(image_dir)

k = 5

centroids = []
for a in range(3):
    centroids.append(np.linspace(np.amin(original[:,:,a]),
            np.amax(original[:,:,a]), num = k).astype(int))
centroids = np.asarray(centroids)

print("k = ", k, "; centroids = ", centroids)
print("centroid[0] = ", centroids[0])

distances = [[], [], []]
for a in range(3):
    for b in range(k):
        print("a,b = ", a, b)
        distances[a].append(getDistances(original[:,:,a], centroids[a])
distances = np.asarray(distances)

print(distances)
