import numpy as np

class Point:
    #Attribut :
    #id : nombre
    #coordonnees : liste de nombres
    #label : nombre
    
    def __init__(self):
        self.id = 0
        self.coordonnees = []
        self.label = 0
    
    def __init__(self, id, coordonnees, label):
        self.id = id
        self.coordonnees = coordonnees
        self.label = label
    
    def getId(self):
        return self.id
        
    def setId(self, id):
        self.id = id
    
    def getCoordonnees(self):
        return self.coordonnees
        
    def getCoordonnee(self, i):
        return self.coordonnees[i]
        
    def setCoordonnees(self, coordonnees):
        "Argument : liste de coordonnees"
        self.coordonnees = coordonnees
    
    def setCoordonnee(self, coord, i):
        self.coordonnees[i] = coord
    
    def getLabel(self):
        return self.label
        
    def setLabel(self, label):
        self.label = label