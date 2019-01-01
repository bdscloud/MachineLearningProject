from sklearn import datasets
import Point
import Prototype
import random as rd
import copy
import numpy as np
import matplotlib.pyplot as plt

class PointGenerator:
    
    def __init__(self):
        return
        
    def digits(self):
        digit = datasets.load_digits()
        return self.matrixAndLabelsToPoints(digit.data, digit.target)
        
    def pointsUniforme(self,n, dim, a, b):
        "Retourne un liste de points générés"
        X=[]
        for i in range(0,n):
            xi = Point.Point(-1,[i for i in range(dim)],30)
            for j in range(dim):
                xi.setCoordonnee(rd.uniform(a,b), j)
            xi.setId(i)
            
            if (xi.getCoordonnee(0) < (b+a)/2):
                xi.setLabel(0)
            else :
                xi.setLabel(1)
                
            X += [xi]
        return X   
        
    def splitDistrib(self, X, f):
        x1 = X[0:(int)(f*len(X))]
        x2 = X[(int)(f*len(X)):len(X)]
        return x1, x2

    def pointsUniformeWithoutLabel(self,n, dim, a, b):
        "Retourne un liste de points générés"
        X=[]
        for i in range(0,n):
            xi = Point.Point(-1,[i for i in range(dim)],30)
            for j in range(dim):
                xi.setCoordonnee(rd.uniform(a,b), j)
            xi.setId(i)
                
            X += [xi]
        return X
        
    def putLabelsMoitieUniforme(self, listeDePoints, a,b):
        "Remet les labels pour une distribution moitie moitie uniforme"
        listeDeTravail = copy.deepcopy(listeDePoints)
        j=0
        for i in listeDeTravail:
            if (i.getCoordonnee(0)<((b+a)/2)):
                i.setLabel(-1)
                j+=1
            else :
                i.setLabel(1)
        return listeDeTravail
            
    def matrixAndLabelsToPoints(self, X, labs):
        points = []
        for i in range(X.shape[0]):
            coordonnees = []
            for j in range(X.shape[1]):
                coordonnees.append(X[i,j])
            points.append(Point.Point(i, coordonnees, labs[i]))
        return points
        
    def pointsToMatrixAndLabels(self, points):
        X = np.zeros((len(points), len(points[0].getCoordonnees())))
        Y = np.zeros((len(points)))
        for i in range(len(points)):
            for j in range(len(points[i].getCoordonnees())):
                X[i,j] = points[i].getCoordonnee(j)
            Y[i] = points[i].getLabel()
        return X,Y
    
    def blobToPoints(self, blobs, labs):
        points = []
        for k in range(len(blobs)):
            X = blobs[k]
            for i in range(X.shape[0]):
                coordonnees = []
                for j in range(X.shape[1]):
                    coordonnees.append(X[i,j])
                points.append(Point.Point(i, coordonnees, labs[i]))
        return points
        
    def generateNoisyCircles(self, n_samples):
        (X, labs) = datasets.make_circles(n_samples=n_samples, factor=.5,noise=.05)
        return self.matrixAndLabelsToPoints(X, labs)
    
    def generateNoisyMoons(self, n_samples):
        (X, labs) = datasets.make_moons(n_samples=n_samples, noise=.05)
        return self.matrixAndLabelsToPoints(X, labs)
        
    def generateBlobs(self, n_samples):
        blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
        print(blobs)
        (X, labs) = blobs
        return self.matrixAndLabelsToPoints(X, labs)
        
    def generateDeformation(self, nPointsSide, delta, length):
        angle = delta
        nPoints = 2 * nPointsSide + 1
        X = np.zeros((nPoints,2))
        for i in range(nPointsSide):
            x = X[2*i,:]
            X[2*i+2,:] = [x[0] + length * np.sin(angle), x[1] + length * np.cos(angle)]
            X[2*i+1,:] = [X[2*i+2,0], -X[2*i+2,1]]
            angle = angle + delta
        return X
    
    def generateBlob(self, nPoints):
        rhos = np.random.rand(nPoints)
        thetas = 2 * np.pi * np.random.rand(nPoints)
        x = rhos * np.cos(thetas)
        y = rhos * np.sin(thetas)
        
        return np.transpose(np.vstack((x,y)))
        
    def eraseLabels(self, points):
        pointsCopy = copy.deepcopy(points)
        for i in pointsCopy:
            i.setLabel(30)
        return pointsCopy
    
    def generateWholeDriftProblemByStep(self, nbPoints, thetaMax, nbEtapes):
        listeEtapes = []
        for i in range(nbEtapes):
            theta = (i+1)*thetaMax/nbEtapes
            listeEtapes.append(self.generateWholeDriftProblemTheta(nbPoints, theta))
        return listeEtapes
        
    def generateWholeDriftProblemTheta(self, nbrePoints, theta = 0):
        nPointsSide = nbrePoints - 1
        radius = 1
        nPointsBlob = nbrePoints
        nPoints = 2 * nPointsSide + 1
        maxAngle = 2 * np.pi / nPoints
        L0 = 1.0 / nPointsSide
        L1 = 2 * radius * np.sin(np.pi / nPoints)        
        delta = maxAngle * theta
        length = L0 + (L1 - L0) * theta
        X = self.generateDeformation(nPointsSide, delta, length)
        blob = [1.0, 0.0] + 0.25 * self.generateBlob(nPointsBlob)
        #return blobs, transf, Y
#        print(len(transf[0]))
#        print(len(Y))
#        return (self.matrixAndLabelsToPoints(blobs, Y), self.matrixAndLabelsToPoints(transf, Y))
        return self.matrixAndLabelsToPoints(X, np.zeros((len(X)))) + self.matrixAndLabelsToPoints(blob, np.ones((len(X))))

        
        
    def decouper_X(self, X, labels):
        listXByLabels = []
        for label in labels:
            labelI = []
            for i in X:
                if(i.getLabel() == label):
                    labelI.append(i)
            listXByLabels.append(labelI)
        return listXByLabels
        
    def generatePrototypes(self, m, X, labels):
        listP = []
        listXByLabel = self.decouper_X(X, labels)
        listeIndices = []
        for i in range(len(labels)):
            listeIndices.append([])
        maxM = m
        for i in range(maxM):
            for j in range(len(labels)):
                if i > m[j] - 1:
                    continue
                proto=Prototype.Prototype(-1,[i for i in range(len(X[0].getCoordonnees()))],30,[])
                indice = rd.randint(0, len(listXByLabel[j])-1)
                while indice in listeIndices[j]:
                    indice = rd.randint(0, len(listXByLabel[j])-1)
                listeIndices[j].append(indice)
                for k in range(len(listXByLabel[j][indice].getCoordonnees())):
                    proto.setCoordonnee(listXByLabel[j][indice].getCoordonnee(k),k)
                proto.label = labels[j]
                proto.reseau = []
                proto.id = i + labels[j]*maxM
                listP.append(proto)
        return listP
        