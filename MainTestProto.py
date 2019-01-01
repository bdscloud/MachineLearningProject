import numpy as np
import Espace
import Prototype
import Point
import PointGenerator
import random as rd
import Affichage
import copy
import matplotlib.pyplot as plt
import time

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
    
if 0 :
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 1)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    espace = Espace.Espace(points,proto)
        
    espace.associerProtosPoints()
    affichage = Affichage.Affichage()
    
    espace.ajusterProtos(15, 1e-5, fKSource, gradKSource)
    nEtapes = 10
    thetaMax = 0.2
    # *****      Debut du Transfert      *****
    for i in range(nEtapes):
        theta = (i+1)/nEtapes
        if(theta > thetaMax):
            break
        pointsTargetCorrects = generator.generateWholeDriftProblemTheta(100, theta)
        pointsTargetGeneres = generator.eraseLabels(pointsTargetCorrects)
        #affichage.printPoints(pointsTargetGeneres)
        espaceTarget = Espace.Espace(pointsTargetGeneres,[])
        for i in espaceTarget.listeProtos:
            if i.getCoordonnee(0)>2:
                print("ca merde1")
        espaceTarget = espace.transfert(espaceTarget)
        espaceTarget.associerProtosPoints()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        espaceTarget.associerProtosPointsEtModifLabels()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        #affichage.afficherEspace(espaceTarget,True)
        espace = copy.deepcopy(espaceTarget)
    print("Le taux de réussite est de = "+str(espaceTarget.calculErreur(pointsTargetCorrects)))
    affichage.afficherEspace(espaceTarget,True)

    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 1)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    espace = Espace.Espace(points,proto)
    espace.associerProtosPoints()
    espace.ajusterProtos(15, 1e-5, fKSource, gradKSource)
    
if 0:
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(100, 0)
    proto = generator.generatePrototypes([6, 2], points, [0, 1])
    espace = Espace.Espace(points,proto)
    espace.associerProtosPoints()
    espace.ajusterProtos(15, 1e-5, fKSource, gradKSource)
    
    etapes = generator.generateWholeDriftProblemByStep(100, 1, 10)
    espaceTarget, erreur = espace.transfertParEtapes(espace, etapes, fKSource, gradKSource)
    print("Le taux de réussite est de "+str(erreur))
    affichage = Affichage.Affichage()
    affichage.afficherEspace(espaceTarget, True)
    
if 0:
    affichage = Affichage.Affichage()
    generator = PointGenerator.PointGenerator()
    points = generator.generateWholeDriftProblemTheta(200, 0)
    proto = generator.generatePrototypes([5, 2], points, [0, 1])
    espace = Espace.Espace(points,proto)
    espace.associerProtosPoints()
    espace.ajusterProtos(500, 1e-5, fKSource, gradKSource)
    affichage.afficherEspace(espace, True)
    etapes = generator.generateWholeDriftProblemByStep(200, 1, 10)
    espaceTarget, erreur = espace.transfertParEtapes(espace, etapes, fKSource, gradKSource)
    print("Le taux de réussite est de "+str(erreur))
    
    affichage.afficherEspace(espaceTarget, True)

start = time.time()

if 1:
    generator = PointGenerator.PointGenerator()
    fracs = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
    fracs = [0.4]
    results = []
    for i in fracs:
        for k in range(5):
            digit = generator.digits()
            espaceDigit = Espace.Espace(digit, [])
            digits = espaceDigit.getListePoints()
            for i in digits:
                if(i.getLabel() != 1):
                    i.setLabel(0)
            X, y = generator.pointsToMatrixAndLabels(digits)
    
            Xs, Xt, Ys, Yt = train_test_split(X, y, test_size=.4)
            
            source = generator.matrixAndLabelsToPoints(Xs, Ys)
            protos = generator.generatePrototypes([40, 10], source, [0, 1])
            espaceSource = Espace.Espace(source, protos)
            espaceSource.associerProtosPoints()
            espaceSource.ajusterProtos(500, 1e-5, fKSource, gradKSource)
            
            target = generator.matrixAndLabelsToPoints(Xt, Yt)
            targetWithoutLabel = generator.eraseLabels(target)
            espaceTarget = Espace.Espace(targetWithoutLabel, [])
            espaceTarget = espaceSource.transfert(espaceTarget)
            espaceTarget.associerProtosPoints()
            espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
            espaceTarget.associerProtosPointsEtModifLabels()
            espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
            succes = espaceTarget.calculErreur(target)
            print("Succes : ", str(succes))
            results.append(succes)
    for r in results:
        print(str(r))
    
if 0:
    generator = PointGenerator.PointGenerator()
    resultats = []
    fracs = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
    protoTest = [[10, 3], [20, 5], [30, 8], [40, 10], [60, 15], [80, 20]]
    for i in protoTest:
        digit = generator.digits()
        espaceDigit = Espace.Espace(digit, [])
        digit1 = espaceDigit.getPointsFromLabel(1)
        digit1HalfSource, digit1HalfTarget = generator.splitDistrib(digit1, 0.5)
        sourceAutre = espaceDigit.getPointsFromLabel(2) + espaceDigit.getPointsFromLabel(3) + espaceDigit.getPointsFromLabel(4) + espaceDigit.getPointsFromLabel(5)
        for j in sourceAutre:
            j.setLabel(0)
        targetAutre = espaceDigit.getPointsFromLabel(6) + espaceDigit.getPointsFromLabel(7) + espaceDigit.getPointsFromLabel(8) + espaceDigit.getPointsFromLabel(9)
        for j in targetAutre:
            j.setLabel(0)
        source = digit1HalfSource + sourceAutre
        target = targetAutre + digit1HalfTarget
        targetWithoutLabel = generator.eraseLabels(target)
        protos = generator.generatePrototypes(i, source, [0, 1])
        espaceSource = Espace.Espace(source, protos)
        espaceSource.associerProtosPoints()
        espaceSource.ajusterProtos(500, 1e-5, fKSource, gradKSource)
        espaceTarget = Espace.Espace(targetWithoutLabel, [])
        espaceTarget = espaceSource.transfert(espaceTarget)
        espaceTarget.associerProtosPoints()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        espaceTarget.associerProtosPointsEtModifLabels()
        espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
        succes = espaceTarget.calculErreur(target)
        print("Succes : ", str(succes))
        resultats.append(succes)
    #print(fracs)
    #plt.plot(fracs, resultats)
    #plt.show()
    for i in range(len(protoTest)):
        print(str(protoTest[i]), " : ", resultats[i])

print('temps execute : ' + str(time.time() - start))      
    
if 0:
    affichage = Affichage.Affichage()
    generator = PointGenerator.PointGenerator()
    points = generator.pointsUniforme(200, 2, 0, 20)
    proto = generator.generatePrototypes([4, 4], points, [0, 1])
    espace = Espace.Espace(points,proto)
    espace.associerProtosPoints()
    espace.ajusterProtos(500, 1e-5, fKSource, gradKSource)
    affichage.afficherEspace(espace, True)
    pointsTarget = generator.pointsUniforme(200, 2, 60, 100)
    pointsSansLabels = generator.eraseLabels(pointsTarget)
    espaceTarget = Espace.Espace(pointsSansLabels, [])
    espaceTarget = espace.transfert(espaceTarget)    
    affichage.afficherEspace(espaceTarget, True)
    espaceTarget.associerProtosPoints()
    affichage.afficherEspace(espaceTarget)
    espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
    affichage.afficherEspace(espaceTarget)
    espaceTarget.associerProtosPointsEtModifLabels()
    affichage.afficherEspace(espaceTarget)
    espaceTarget.ajusterProtos(15, 1e-5, fKSource, gradKSource)
    affichage.afficherEspace(espaceTarget)
    erreur = espaceTarget.calculErreur(pointsTarget)
    print("Erreur : ", str(erreur))
#generator = PointGenerator.PointGenerator()
#points = generator.generateNoisyMoons(200)
#protos = generator.generatePrototypes(5,points, [0, 1])
#espace = Espace.Espace(points,protos)
#espace.associerProtosPoints()
#espace.ajusterProtos(500, 1e-5, fKSource, gradKSource)
#
#
#affichage = Affichage.Affichage()
#affichage.afficherEspace(espace)
