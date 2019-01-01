import numpy as np
import Espace
import Prototype
import Point
import random as rd
import Affichage 
import copy
import PointGenerator
import matplotlib.pyplot as plt

fig = plt.figure()

def fKSource(listX, P):
    "Renvoie le fonction de complexite K pour le cas source"
    resultat = 0
    espacePourConversion = Espace.Espace(listX,None)
    list2X = espacePourConversion.listePointsToMatrix()
    for i in range(len(list2X)):
        for j in range(len(P)):
            resultat += np.log2(1+np.abs(list2X[i][j]-P[j]))
    return resultat
    
def gradKSource(listX, P):
    "Renvoie le gradient de la fonction de complexite K pour le cas source"
    R = np.zeros(len(P))
    espacePourConversion = Espace.Espace(listX,None)
    list2X = espacePourConversion.listePointsToMatrix()
    for i in range(len(P)):
        resultat = 0
        for j in range(len(list2X)):
            
            resultat += np.sign(list2X[j][i]-P[i])*(-1)/(1+np.abs(list2X[j][i]-P[i]))
        R[i] = resultat
    return R
    
def iterateUniforme(n,dim) :
    valeurErreur =0
    for i in range(n):    
        pointGenerator = PointGenerator.PointGenerator()
        pointsGeneres = pointGenerator.pointsUniforme(100,dim,0,30)    
        protosGeneres = pointGenerator.generatePrototypes(4,pointsGeneres,[-1,1])
        
        espace = Espace.Espace(pointsGeneres,protosGeneres)
        
        espace.associerProtosPoints()
        
        #stockageValeurDescente = espace.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        #print(stockageValeurDescente)
        #print("*****     Protos Finaux     *****")
        #affichage.printProtos(espace.getListeProtos())
        #print("teub")
        #affichage.afficherEspace(espace,False)
        #affichage.afficherValeurDescente(stockageValeurDescente)
        
        # *****      Debut du Transfert      *****
        pointsTargetGeneres = pointGenerator.pointsUniformeWithoutLabel(100,dim,30,100)
        espaceTarget = Espace.Espace(pointsTargetGeneres,[])
        #affichage.printPoints(pointsTargetGeneres)
        espaceTarget = espace.transfert(espaceTarget)
        espaceTarget.associerProtosPoints()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        espaceTarget.associerProtosPointsEtModifLabels()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        #affichage.afficherEspace(espaceTarget,True)
        pointsTargetCorrects = pointGenerator.putLabelsMoitieUniforme(pointsTargetGeneres,30,100)
        valeurErreur += espaceTarget.calculErreur(pointsTargetCorrects)
    print("Taux de reussite sur "+str(n)+" iterations est de : "+str(valeurErreur/n))
    return valeurErreur/n

def errorByDim(dimMax,n):
    list_dim = [i for i in range(1,dimMax+1)]
    list_error = []
    for i in range(len(list_dim)):
        list_error.append(iterateUniforme(n,i+1))
    return list_dim, list_error
    
# *****      Debut des instructions      *****

pointGenerator = PointGenerator.PointGenerator()
pointsGeneres = pointGenerator.pointsUniforme(200,3,0,30)    
protosGeneres = pointGenerator.generatePrototypes(4,pointsGeneres,[-1,1])

espace = Espace.Espace(pointsGeneres,protosGeneres)

espace.associerProtosPoints()
affichage = Affichage.Affichage()
#X , Y = errorByDim(10,5)
#
#affichage.afficherErrorByDim(X,Y)

#affichage.printProtos(protosGeneres)
#affichage.printPoints(pointsGeneres)

stockageValeurDescente = espace.ajusterProtos(15, 1e-5, fKSource, gradKSource)
print(stockageValeurDescente)
print("*****     Protos Finaux     *****")
affichage.printProtos(espace.getListeProtos())
print("teub")
dim = len(espace.getListePoints()[0].getCoordonnees())
if(dim==2):
    affichage.afficherEspace(espace,False)
elif(dim==3):
    affichage.afficherEspace3D(espace,False,fig)
#affichage.afficherValeurDescente(stockageValeurDescente)

# *****      Debut du Transfert      *****
pointsTargetGeneres = pointGenerator.pointsUniformeWithoutLabel(200,3,30,100)
espaceTarget = Espace.Espace(pointsTargetGeneres,[])
affichage.printPoints(pointsTargetGeneres)
espaceTarget = espace.transfert(espaceTarget)
espaceTarget.associerProtosPoints()
espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
espaceTarget.associerProtosPointsEtModifLabels()
espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
if(dim==2):
    affichage.afficherEspace(espaceTarget,True)
elif(dim==3):
    affichage.afficherEspace3D(espaceTarget,True,fig)
pointsTargetCorrects = pointGenerator.putLabelsMoitieUniforme(pointsTargetGeneres,30,100)
print("Le taux de réussite est de = "+str(espaceTarget.calculErreur(pointsTargetCorrects)))
if(dim==3):
    plt.show(fig)
    
#iterateUniforme(10)

