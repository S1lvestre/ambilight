import numpy as np

# assigns one of the centroids to each datapoint
def assign(data, means):
    
    # get distances from all points to each centroid: array (width*height,k)
    dists = np.zeros( ( np.shape(data)[0], np.shape(means)[0] ), dtype="int64" )
    
    # for each cluster
    for i in range(np.shape(means)[0]):
        # euclidean distance
        dists[:,i] = np.sqrt( np.sum( np.power( (data - means[i]), 2 ), axis = 1 ) )
    
    # each point is assigned the values of the closest centroid
    clusters = np.zeros( (np.shape(data)[0],3), dtype="int64" )
    clusters = means[ np.argmin( dists, axis=1 ) ]
    
    return clusters


# calculates new centroids
def update( clusters, data, means ):
    
    new_means = []
    
    # there migh be a more efficient way other than zip
    for a, elms in zip(range(np.shape(means)[0]), getElementCounts(clusters, means)):
        
        # sum of each channel from all elements of each cluster
        sums = np.sum( np.where( clusters == means[a], data, 0 ), axis=0 )
        
        # calculate new average of each channel
        new_means.append( np.divide( sums, elms ).astype(np.uint16) )
    
    return np.asarray( new_means, dtype="int64" )


def getElementCounts(clusters, means):
    
    counts = []
    
    for centroid in means:
        
        array = np.where( clusters == centroid, clusters, 0 )
        
        counts.append( np.sum( np.where( array.any(axis = 1), 1, 0 ) ) )
        
    return np.asarray(counts)

###############################################################################

def kmeans(k, max_iters, data):
    """ receives (n,3) data array """
    
    # initialize means array with random points from data
    means = data[np.random.randint(0, np.shape(data)[0], size=k),:]
    
    i = 0
    while True:
        
        clusters = assign(data, means)
        
        if i == max_iters:
            break
            
        means = update(clusters, data, means)
        
        i += 1
    
    return clusters, means

def getDominant(clusters, means):
    
    dominantColor = means[np.argmax(getElementCounts(clusters, means))]
    
    return dominantColor

###############################################################################
