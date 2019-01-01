import numpy as np
import Point

class Prototype(Point.Point):
    #Variables :
    #reseau : liste de points
    
    def __init__(self):
        super(Point,self).__init__()
        self.reseau = []
    
    def __init__(self, id, coordonnees, label, reseau):
        super(Point.Point,self).__init__()
        self.id=id
        self.coordonnees = coordonnees
        self.label=label
        self.reseau = reseau
    
    def getReseau(self):
        return self.reseau
        
    def setReseau(self, reseau):
        self.reseau = reseau
    
    def reseauToMatrix(self):
        reseau = np.zeros((len(self.reseau), len(self.reseau[0].getCoordonnees())))
        for i in range (len(self.reseau)):
            coordonnees = self.reseau[i].getCoordonnees()
            for j in range (len(coordonnees)):
                reseau[i,j] = coordonnees[j]
        return reseau
        