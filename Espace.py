import numpy as np
import Prototype
import Point
import Calculateur
import copy
from math import sqrt
import scipy.ndimage
import PointGenerator
import Affichage

class Espace:
    "Un espace contient tous les points et protos de notre espace"

    
    def __init__(self): # Notre méthode constructeur
        self.listePoints = []
        self.listeProtos = []
        self.listeLabel = []
        self.listeAncienProto = []
        self.graph_K = []
        self.listeProtosInitiaux = []
        
    def __init__(self,listePoints,listeProtos): # Notre méthode constructeur
        self.listePoints = listePoints
        self.listeLabel = []
        for i in self.listePoints:
            if((i.getLabel() in self.listeLabel) == False):
                self.listeLabel.append(i.getLabel())
        self.listeProtos = listeProtos
        self.listeAncienProto = []
        self.graph_K = []
        self.listeProtosInitiaux = copy.deepcopy(listeProtos)
        
    def setListeLabel(self,listeLabelSource):
        self.listeLabel = listeLabelSource
        
    def calculDistance(self,a,b):
        "A et B sont des points, on rend la distance qui vaut racine du carré des composantes"
        s=0
        for i in range(len(a.getCoordonnees())):
            s+=(a.getCoordonnees()[i]-b.getCoordonnees()[i])**2
        return sqrt(s)
        
    def getListePoints(self):
        return self.listePoints
        
    def getListeProtos(self):
        return self.listeProtos
        
    def addProto(self, P):
        self.listeProtos.append(P)

    def getGraph(self):
        return self.graph_K
    
    def nombrePoints(self):
        return len(self.listePoints)
    
    def nombreProtos(self):
        return len(self.listeProtos)
    
# Permet d'obtenir une matrice contenant les coordonnes des points     
    def listePointsToMatrix(self):
        return np.array(np.array([i.getCoordonnees() for i in self.listePoints]))
  
# Permet d'obtenir une matrice contenant les coordonnes des protos     
    def listeProtosToMatrix(self):
        return np.array([i.getCoordonnees() for i in self.listeProtos])
        
    def listeOtherPointsToMatrix(self, points):
        return np.array(np.array([i.getCoordonnees() for i in points]))
        
    def MatrixToListePoints(self,matrixPoints, labelsPoints):
        return [Point(i,matrixPoints[i], labelsPoints[i]) for i in range(len(matrixPoints))]
        
    def MatrixToListeProtos(self,matrixProtos, labelsProtos):
        #On crée une liste de Protos avec des reseaux initialises a []
        #Si on veut completer les reseaux on utilisera associerProtosPoints
        return [Prototype(i,matrixProtos[i], labelsProtos[i], []) for i in range(len(matrixProtos))]
        
    def transfertParEtapes(self, espaceDepart, listeEtapes, fKSource, gradKSource):
        espace = espaceDepart
        generator = PointGenerator.PointGenerator()
        for i in range(len(listeEtapes)):
            pointsTargetGeneres = generator.eraseLabels(listeEtapes[i])
            espaceTarget = Espace(pointsTargetGeneres,[])
            espaceTarget = espace.transfert(espaceTarget)
            espaceTarget.associerProtosPoints()
            espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
            espaceTarget.associerProtosPointsEtModifLabels()
            espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
            espace = copy.deepcopy(espaceTarget)
        erreur = espace.calculErreur(listeEtapes[len(listeEtapes) - 1])
        return (espace, erreur)
    
    def associerProtosPoints(self):
        "Retourne et modifie la liste P telle que les reseau des protos sont remplis de maniere optimale en fonction des points"
        for l in self.listeProtos:
            l.setReseau([])
        for i in self.listePoints:
        #La distance est une simple norme de la difference entre le point et un proto
            k=0
            while (i.getLabel() != self.listeProtos[k].getLabel()) :
                k+=1
            distance_min = self.calculDistance(i,self.listeProtos[k])    
            proto_min = self.listeProtos[k]
            for j in self.listeProtos:
                if(i.getLabel() == j.getLabel()):
                    distance = self.calculDistance(i,j)
                    #print("distance de proto "+str(j.getId())+" avec point "+str(i.gteId())+" = "+str(distance))
                    if distance < distance_min :
                        distance_min = distance
                        proto_min = j
            proto_min.reseau.append(i)
        return self.listeProtos
        
    def associerProtosPointsEtModifLabels(self):
        "Retourne et modifie la liste P telle que les reseau des protos sont remplis de maniere optimale en fonction des points mais pas des labels"
        for l in self.listeProtos:
            l.setReseau([])
        for i in self.listePoints:
        #La distance est une simple norme de la difference entre le point et un proto
            k=0
            while (i.getLabel() != self.listeProtos[k].getLabel()) :
                k+=1
            distance_min = self.calculDistance(i,self.listeProtos[k])    
            proto_min = self.listeProtos[k]
            for j in self.listeProtos:
                distance = self.calculDistance(i,j)
                #print("distance de proto "+str(j.getId())+" avec point "+str(i.gteId())+" = "+str(distance))
                if distance < distance_min :
                    distance_min = distance
                    proto_min = j
            proto_min.reseau.append(i)
            if (proto_min.getLabel() != i.getLabel()):
                i.setLabel(proto_min.getLabel())
        return self.listeProtos
        
    def setPointLabelFromProto(self):
        for i in self.listePoints:
            protoMini = self.listeProtos[0]
            distMini = self.calculDistance(i, protoMini)
            for j in self.listeProtos:
                if(self.calculDistance(i, j) < distMini):
                    protoMini = j
                    distMini = self.calculDistance(i, j)
            i.setLabel(protoMini.getLabel())
        return 0
         
    def getPointsFromLabel(self, label):
        ret = []
        for i in self.listePoints:
            if(i.getLabel() == label):
                ret.append(i)
        return ret
        
    def getProtosFromLabel(self, label):
        ret = []
        for i in self.listeProtos:
            if(i.getLabel() == label):
                ret.append(i)
        return ret
    
    def getBarycentrePoints(self, points):
        matrix = self.listeOtherPointsToMatrix(points)
        length= len(matrix)        
        barycentre = np.zeros((1, len(matrix[0])))
        for i in range(len(matrix[0])):
            composante_i = np.sum(matrix[:, i])
            barycentre[0][i]=composante_i
        return barycentre[0]/length
        
    def transfert(self, espaceTarget):
        espaceTarget.setListeLabel(self.listeLabel)
        barySource = self.getBarycentrePoints(self.listePoints)
        baryTarget = espaceTarget.getBarycentrePoints(espaceTarget.getListePoints())
        globalTranslation = baryTarget - barySource
        for i in self.listeProtos:
            proto = Prototype.Prototype(i.getId(), copy.copy(i.getCoordonnees()), i.getLabel(), [])
            espaceTarget.addProto(proto)
        for i in espaceTarget.listeProtos:
            coordonnees = []
            for j in range(len(i.getCoordonnees())):
                coordonnees.append(i.getCoordonnee(j) + globalTranslation[j])
            i.setCoordonnees(coordonnees)
        espaceTarget.setPointLabelFromProto()
        for l in espaceTarget.listeLabel:
            baryTargetL = espaceTarget.getBarycentrePoints(espaceTarget.getPointsFromLabel(l))
            protosFromLabel = espaceTarget.getProtosFromLabel(l)
            baryProtoL = espaceTarget.getBarycentrePoints(protosFromLabel)
            classTransformation = baryTargetL - baryProtoL
            for k in protosFromLabel:
                for j in range(len(k.getCoordonnees())):
                    k.setCoordonnee(k.getCoordonnee(j) + classTransformation[j], j)
            
        return espaceTarget
    
    def ajusterProtos(self, nmax, epsilon, fonctionKSource, gradientKSource):
        "Permet de reajuster la position des protos par rapport a leur reseau, elle retourne les historique de valeur descente pour pouvoir tracer"
        n = 0
        continuerBoucle = True
        stockageValeurDescente = []
        while(n < nmax and continuerBoucle):
            print("passage")
            self.listeProtos = self.associerProtosPoints()
            continuerBoucle = False
            tmp_res = 0
            pourcent20 = False
            pourcent40 = False
            pourcent60 = False
            pourcent80 = False
            
            for i in range(len(self.listeProtos)):
                pourcentage = i*100/len(self.listeProtos)
                if(pourcentage > 20 and pourcentage < 30 and pourcent20 == False):
                    print("Descente ", str(pourcentage), " %")
                    pourcent20 = True
                if(pourcentage > 40 and pourcentage < 50 and pourcent40 == False):
                    print("Descente ", str(pourcentage), " %")
                    pourcent40 = True
                if(pourcentage > 60 and pourcentage < 70 and pourcent60 == False):
                    print("Descente ", str(pourcentage), " %")
                    pourcent60 = True
                if(pourcentage > 80 and pourcentage < 90 and pourcent80 == False):
                    print("Descente ", str(pourcentage), " %")
                    pourcent80 = True
                self.listeAncienProto.append(self.listeProtos[i].getCoordonnees())
                calc = Calculateur.Calculateur(fonctionKSource,gradientKSource)
                ancienProto = self.listeProtos[i]
                proto, valeurDescente = calc.descenteGradientSource(self.listeProtos[i],epsilon,nmax)
                tmp_res += calc.executerFonctionK(proto.getCoordonnees(), proto.getReseau())
                if self.calculDistance(proto,ancienProto)!=0:
                    continuerBoucle = True
                    self.listeProtos[i] = proto
            print("Descente 100%")
            stockageValeurDescente.append(valeurDescente)
            self.graph_K.append(tmp_res)
            n += 1
        self.listeProtos = self.associerProtosPoints()
        return stockageValeurDescente
        
    def calculErreur(self,listePointsWithLabels):
        erreur,n = 0, len(self.listePoints)
        for i in range(n):
            if (self.listePoints[i].getLabel() != listePointsWithLabels[i].getLabel()):
                erreur += 1
        return (n-erreur)/n
            

