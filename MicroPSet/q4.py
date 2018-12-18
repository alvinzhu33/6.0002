import numpy as np
import random

def minkowskiDist(v1, v2, p):
    #Assumes v1 and v2 are equal length arrays of numbers
    dist = 0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    return dist**(1/p)

class Example(object):
    def __init__(self, name, features, label = None):
        #Assumes features is an array of floats
        self.name = name
        self.features = features
        self.label = label
    def dimensionality(self):
        return len(self.features)
    def getFeatures(self):
        return self.features[:]
    def getLabel(self):
        return self.label
    def getName(self):
        return self.name
    def distance(self, other):
        return minkowskiDist(self.features, other.getFeatures(), 2)
    def __str__(self):
        return self.name +':'+ str(self.features) + ':'\
               + str(self.label)

class Cluster(object):
    def __init__(self, examples):
        """Assumes examples a non-empty list of Examples"""
        self.examples = examples
        self.centroid = self.computeCentroid()
    def update(self, examples):
        """Assume examples is a non-empty list of Examples
           Replace examples; return amount centroid has changed"""
        oldCentroid = self.centroid
        self.examples = examples
        self.centroid = self.computeCentroid()
        return oldCentroid.distance(self.centroid)
    def computeCentroid(self):
        vals = np.array([0.0]*self.examples[0].dimensionality())
        for e in self.examples: #compute mean
            vals += e.getFeatures()
        centroid = Example('centroid', vals/len(self.examples))
        return centroid
    def getCentroid(self):
        return self.centroid
    def variability(self):
        totDist = 0
        for e in self.examples:
            totDist += (e.distance(self.centroid))**2
        return totDist
    def members(self):
        for e in self.examples:
            yield e
    def diameter(self):
        point1 = 0
        dist = self.examples[0].distance(self.examples[0])
        while point1 < len(self.examples):
            point2 = point1 + 1
            while point2 < len(self.examples):
                store = self.examples[point1].distance(self.examples[point2])
                if store > dist:
                    dist = store
                point2 += 1
            point1 += 1
        return dist
    def __str__(self):
        names = []
        for e in self.examples:
            names.append(e.getName())
        names.sort()
        result = 'Cluster with centroid '\
               + str(self.centroid.getFeatures()) + ' contains:\n  '
        for e in names:
            result = result + e + ', '
        return result[:-2] #remove trailing comma and space    

def old_dissimilarity(clusters):
    """Assumes clusters a list of clusters
       Returns a measure of the total dissimilarity of the
       clusters in the list"""
    totDist = 0
    for c in clusters:
        totDist += c.variability()
    return totDist

def scaleAttrs(vals):
    vals = np.array(vals)
    mean = sum(vals)/len(vals)
    sd = np.std(vals)
    vals = vals - mean
    return vals/sd

def kmeans(examples, k):
    #Get k randomly chosen initial centroids, create cluster for each
    initialCentroids = random.sample(examples, k)
    clusters = []
    for e in initialCentroids:
        clusters.append(Cluster([e]))
        
    #Iterate until centroids do not change
    converged = False
    numIterations = 0
    while not converged:
        numIterations += 1
        #Create a list containing k distinct empty lists
        newClusters = []
        for i in range(k):
            newClusters.append([])
            
        #Associate each example with closest centroid
        for e in examples:
            #Find the centroid closest to e
            smallestDistance = e.distance(clusters[0].getCentroid())
            index = 0
            for i in range(1, k):
                distance = e.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            #Add e to the list of examples for appropriate cluster
            newClusters[index].append(e)

        for c in newClusters: #Avoid having empty clusters
            if len(c) == 0:
                raise ValueError('Empty Cluster')
        
        #Update each cluster; check if a centroid has changed
        converged = True
        for i in range(k):
            if clusters[i].update(newClusters[i]) > 0.0:
                converged = False
    return clusters
      
def dissimilarity(clusters):
    squared = 0
    for c in clusters:
        squared += c.diameter()**2
    return squared

def trykmeans(examples, numClusters, numTrials):
    """Calls kmeans numTrials times and returns the result with the
          lowest dissimilarity"""
    best = kmeans(examples, numClusters)
    minDissimilarity = dissimilarity(best)
    trial = 1
    while trial < numTrials:
        try:
            clusters = kmeans(examples, numClusters)
        except ValueError:
            continue #If failed, try again
        currDissimilarity = dissimilarity(clusters)
        if currDissimilarity < minDissimilarity:
            best = clusters
            minDissimilarity = currDissimilarity
        trial += 1
    return best

def printClustering(clustering):
    """Assumes: clustering is a sequence of clusters
       Prints information about each cluster"""
    for c in clustering:
        numPts = 0
        for p in c.members():
            numPts += 1
        print('Cluster of size', numPts)
        for p in c.members():
            print('   ' + p.__str__())

#Patriots' example
edelman = ['edelman', 70, 200]
hogan = ['hogan', 73, 210]
gronkowski = ['gronkowski', 78, 265]
gordon = ['gordon', 75, 225]
hollister = ['hollister', 76, 245]
dorsett = ['dorsett', 70, 192]
allen = ['allen', 75, 265]
cannon = ['cannon', 77, 335]
brown = ['brown', 80, 380]
shelton = ['shelton', 74, 345]
guy = ['guy', 76, 315]
mason = ['mason', 73, 310]
thuney = ['thuney', 77, 305]
karras = ['karras', 76, 305]
mason = ['mason', 73, 310]
michel = ['michel', 71, 215]
white = ['white', 70, 205]
patterson = ['patterson', 74, 228]
develin = ['develin', 75, 255]
brady = ['brady', 76, 225]

receivers = [edelman, hogan, gordon, dorsett]
dLine = [guy, shelton]
oLine = [brown, cannon, mason, karras, thuney]
tights = [gronkowski, hollister, allen]
backs = [michel, white, patterson, develin, brady]

pats = []
for p in receivers:
    pats.append((p, 'receiver'))
for p in dLine:
    pats.append((p, 'Dline'))
for p in oLine:
    pats.append((p, 'Oline'))
for p in tights:
    pats.append((p, 'tight end'))
for p in backs:
    pats.append((p, 'back'))

class Player(Example):
    pass

def buildPatriotsData(players, toScale = False):
    heightList, weightList = [],[]
    for p in players:
        heightList.append(p[0][1])
        weightList.append(p[0][2])
    if toScale:
        heightList = scaleAttrs(heightList)
        weightList = scaleAttrs(weightList)
    #Build points
    points = []
    for i in range(len(players)):
        features = np.array([heightList[i], weightList[i]])
        features = np.array([heightList[i], weightList[i]])
        points.append(Player(players[i][0][0], features, players[i][1]))
    return points

for n in range(20):
    players = buildPatriotsData(pats, True)
    bestClustering = trykmeans(players, 4, 40)
    print(round(dissimilarity(bestClustering), 4))
players = buildPatriotsData(pats, True)
bestClustering = trykmeans(players, 4, 40)
print(round(dissimilarity(bestClustering), 4))