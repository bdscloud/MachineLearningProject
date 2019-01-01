# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 09:04:00 2016

@author: BriceLaTeub
"""
import random 
import numpy as np
import matplotlib.pyplot as plt
import math as math
import copy as cp
import scipy.ndimage

# *****     Déclaration des classes      *****

class Point():
    "Un point de notre plan"
    
class Prototype():
    "Classe pour nos protos"

# *****     Déclaration des fonctions     *****

def nombresAleatoires(n):
    "Retourne un liste de points générés"
    X=[]
    for i in range(0,n):
        xi = Point()
        xi.x = random.uniform(0,10)
        xi.y = random.uniform(0,10)
        
        #Chaque point a un identifiant unique
        xi.id = i
        
        #Les points à gauche de x=5 sont de classe -1
        #les points à droite de classe 1
        if (xi.x<5):
            xi.label=-1
        else :
            xi.label = 1
            
        X += [xi]
    return X
    
def decouper_X(X):
    "Retourne deux listes, chacune contenant les points d'une certaine classe"
    X1,X2 = [],[]
    for i in X:
        if(i.label ==-1):
            X1.append(i)
        else:
            X2.append(i)
    return X1,X2


def prototypes(m,X):
    "Retourne une liste contenant tous les protos de classe -1 puis tous ceux de classe 1"
    P1=[]
    P2=[]
    proto1 = Prototype()
    proto2 = Prototype()
    X1,X2 = decouper_X(X)
    listeindice1 = []
    listeindice2 = []
    for i in range(0,m):
        #On crée un prototype qui fait partie des points de classe -1
        proto1=Prototype()
        indice1 = random.randint(0,len(X1)-1)
        while indice1 in listeindice1:
            indice1 = random.randint(0,len(X1)-1)
        listeindice1.append(indice1)
        proto1.x = X1[indice1].x
        proto1.y = X1[indice1].y
        proto1.label = -1
        proto1.reseau = []
        proto1.id = i
        
        #On crée un prototype qui fait partie des points de classe 1
        proto2=Prototype()
        indice2 = random.randint(0,len(X2)-1)
        while indice2 in listeindice2:
            indice2 = random.randint(0,len(X2)-1)
        listeindice2.append(indice2)
        proto2.x = X2[indice2].x
        proto2.y = X2[indice2].y
        proto2.label = 1
        proto2.reseau = []
        proto2.id = i+m
        
        P1.append(proto1)
        P2.append(proto2)
    
    return  P1+P2
        
def association_points_protos(X,P):
    "Retourne et modifie la liste P telle que les reseau des protos sont remplis de maniere optimale en fonction des points"
    for i in X:
        #La distance est une simple norme de la difference entre le point et un proto
        distance_min = math.sqrt((i.x-P[0].x)**2+(i.y-P[0].y)**2)
        k=0
        while (i.label != P[k].label) :
            k+=1
        proto_min = P[k]
        for j in P:
            if(i.label == j.label):
                distance = math.sqrt((i.x-j.x)**2+(i.y-j.y)**2)
                if distance < distance_min :
                    distance_min = distance
                    proto_min = j
        proto_min.reseau.append(i)
    return P
    
def affiche_point(X) :
    for i in X :
        print("Point = "+str(i.id)+" | X = "+str(i.x)+" | Y = "+str(i.y)+" | label = "+str(i.label))
    
    
def affiche_proto(P):
    for i in P :
        string2 ="Point "
        for j in i.reseau :
            string2 += str(j.id)+", "
        print("Proto  id = "+str(i.id)+" | X = "+str(i.x)+" | Y = "+str(i.y)+" | label = "+str(i.label)+" | Reseau = "+string2)
        
# *****     Partie EM          *****

def descente_gradient(f, gradf, x0list, eps, nmax, gamma, listX):
    mins = []
    immins = []
    for i in range(len(x0list)):
        x0 = x0list[i]
        alpha = gamma
        x = x0
        xsuiv = x - alpha*gradf(listX, x)/norm(gradf(listX, x))
        n = 1
        while(n < nmax and norm(x-xsuiv) > eps):
            x = xsuiv
            xsuiv = x - alpha*gradf(listX, x)/norm(gradf(listX, x))
            #alpha = calculatealpha(f, gradf, x, xsuiv, alpha, gamma, listX)
            #alpha = 0.005
            n += 1
        mins.append(xsuiv)
        immins.append(f(listX, xsuiv))
    return mins[immins.index(min(immins))]
    
def iterationDescenteGradien(f,gradf,reseau,epsilon,Nmax):
    xfinal = scipy.ndimage.measurements.center_of_mass(np.array([[i.x,i.y] for i in reseau]))
    minimum = f([[i.x,i.y] for i in reseau],xfinal)    
    for i in reseau :
        x,valeur = descenteGradientMultiDim(f,gradf,[i.x,i.y],epsilon,Nmax,reseau)
        if valeur < minimum :
            xfinal = x
            minimum = valeur
    return xfinal
    
def descenteGradientMultiDim(f,fp,x0,epsilon,Nmax,reseau):
    #print("*** Fonction descenteGradienMultiDim ***"+str(x0))
    dimension = np.size(x0)
    ecart = epsilon+1;
    x_suivant=np.copy(x0)
    nb_etape = 0
    alpha=1
    graphX =[]
    graphY= []
    
    while ecart>epsilon and nb_etape<Nmax:
        x_precedent = np.copy(x_suivant)
       # print("xprecedent "+str(x_precedent))
        #Le np.int64 permet de gerer les valeurs grandes de gradien en 64 bits
        gradien = np.array(fp(reseau,x_precedent),np.int64)
        
        for i in range(dimension):
            #On fait la distinction si la norme = 0 alors c'est que le gradien est nul
            # mais on ne peut pas faire "0/0" donc on définie a la main le coeff a 0 dans ce cas
            if np.linalg.norm(gradien)!=0:                
                coeff = gradien/np.linalg.norm(gradien)
            else :
                coeff = np.zeros(2)         
            x_suivant[i] = x_precedent[i] - coeff[i]*alpha
            signe = f([[t.x,t.y] for t in reseau], x_suivant)-f([[t.x,t.y] for t in reseau], x_precedent)
            #J'ai choisis d'incrementer peu alpha, car on place normalement les protos pas trop loins de la bonne valeur
            if signe>0 :
                alpha = alpha*2
            else :
                alpha = alpha*0.5
        graphY.append(f([[t.x,t.y] for t in reseau], x_suivant)) 
        graphX.append(nb_etape)        
        ecart = np.linalg.norm(x_precedent-x_suivant)
        nb_etape+=1
      #  print("nb etapes = "+str(nb_etape)+" | alpha = "+str(alpha)+" | ecart = "+str(ecart))
        
   # plt.plot(graphX,graphY ,color = 'r',linestyle = '-', marker='o')    
   # print("Le minimum trouve vaut : "+str(x_suivant))
   # print("***")
    return x_suivant,f([[t.x,t.y] for t in reseau],x_suivant)
    
    
def f(x) : return x[0]**4+x[1]**4-(x[0]-x[1])**2
def fp(x) : return np.array([4*x[0]**3-2*(x[0]-x[1]),4*x[1]**3+2*(x[0]-x[1])])
    
def calculatealpha(f, gradf, x, xsuiv, alpha, gamma, listX):
    xd = gradf(listX, x)
    xdsuiv = gradf(listX, xsuiv)
    if(f(listX, xsuiv) - f(listX, x) <= 0):
        while(f(listX, xsuiv) - f(listX, x) <= 0):
            xdsuiv = gradf(listX, x-alpha*xd)
            alpha = alpha*gamma
        alpha = alpha/gamma
    else:
        while(f(listX, xsuiv) - f(listX, X) >= 0):
            xdsuiv = gradf(listX, x-alpha*xd)
            alpha = alpha/gamma
        alpha = alpha*gamma
    return alpha
    
def samesigns(x, y):
    samesign = True
    for i in range(x.size):
        if(np.sign(x[i]) != np.sign(y[i])):
            samesign = False
    return samesign

def ajusterProtos(X, Xlabel, M, Y, nmax):
    n = 0
    while(n < nmax):
        #print(n)
        for i in range(M.shape[0]):
            Xprotos = protoFromMatrix(M,Y)
            Xprotos = association_points_protos(pointFromMatrix(X,Xlabel),Xprotos)
            listeancienprotolabelX.append(Xprotos[i].x)
            listeancienprotolabelY.append(Xprotos[i].y)
            if(Xprotos[i].reseau==[]):
                J = iterationDescenteGradien(fonction, gradfonction, [Xprotos[i]], 1e-7, 700)
            else:
                J = iterationDescenteGradien(fonction, gradfonction, Xprotos[i].reseau, 1e-7, 700)
            #P = descenteGradientMultid(fonction,gradfonction,[M[i]],0.0001,500,0.005, getPointsAttachedToProto(X, Xprotos, i))
            M[i] = J
        n += 1
    return M
    
def protoFromMatrix(M,Y):
    listeProto =[]
    for i in range(len(M)):
        proto = Prototype()
        proto.x = M[i][0]
        proto.y = M[i][1]
        proto.label = Y[i]
        proto.id = i
        proto.reseau = []
        listeProto.append(proto)
    return listeProto
        
def pointFromMatrix(X,Xlabel):
    listePoint =[]
    for i in range(len(X)):
        point = Point()
        point.x = X[i][0]
        point.y = X[i][1]
        point.label = Xlabel[i]
        point.id = i
        listePoint.append(point)
    return listePoint
    
    
def getPointsAttachedToProto(X, Xprotos, proto):
    listX = []
    for i in range(len(Xprotos)):
        if(Xprotos[i] == proto):
            listX.append(X[i])
    return listX
    
    
def getPrototype(x, label, M, Y): 
    attrib = False
    dmin = norm(x-M[0])
    min = 0
    for i in range(M.shape[0]):
        dist = norm(x-M[i])
        if((label == Y[i] and dist < dmin) or (attrib == False and label == Y[i])):
            dmin = dist
            min = i
            attrib = True
    return min
    
def fonction(listX, P):
    resultat = 0
    for i in range(len(listX)):
        for j in range(len(P)):
            resultat += np.log2(1+np.abs(listX[i][j]-P[j]))
    return resultat
    
def gradfonction(listX, P):
    list2X = [[i.x,i.y] for i in listX]
    R = np.zeros(P.shape[0])
    #print(P)
    for i in range(P.shape[0]):
        resultat = 0
        for j in range(len(list2X)):
           # print("test "+str((P[i])*(-1)))
            resultat += np.sign(list2X[j][i]-P[i])*(-1)/(1+np.abs(list2X[j][i]-P[i]))
           # print(resultat)
        R[i] = resultat
    return R
        
def norm(x):
    s = 0;
    for i in range(x.shape[0]):
        s += x[i]**2
    return np.sqrt(s)


# *****     Partie Calculs     *****

listeancienprotolabelX = []
listeancienprotolabelY = []

X=nombresAleatoires(40)
P = prototypes(3,X)

# ** Pour graphique :
X1,X2=decouper_X(X)
XX1 = [i.x for i in X1]
XX2 = [i.x for i in X2]
YY1 = [i.y for i in X1]
YY2 = [i.y for i in X2]


P1 = P[0:len(P)//2]
P2 = P[len(P)//2:len(P)]
Xp1 = [P1[i].x for i in range(len(P1))]
Yp1 = [P1[i].y for i in range(len(P1))]
Xp2 = [P2[i].x for i in range(len(P2))]
Yp2 = [P2[i].y for i in range(len(P2))]

Xpp1=cp.copy(Xp1)
Ypp1=cp.copy(Yp1)
Xpp2=cp.copy(Xp2)
Ypp2=cp.copy(Yp2)

plt.close()
plt.plot(Xpp1,Ypp1 ,color = 'r',linestyle = '', marker='o', markersize = 10)
plt.plot(Xpp2,Ypp2,color = 'b',linestyle = '', marker='o', markersize = 10)
plt.plot(Xp1,Yp1 ,color = 'r',linestyle = '', marker='o', markersize = 2)
plt.plot(Xp2,Yp2,color = 'b',linestyle = '', marker='o', markersize = 2)

plt.plot(XX1,YY1,color = 'r', linestyle = '', marker = 'x', markersize = 15)
plt.plot(XX2,YY2,color = 'b', linestyle = '', marker = 'x', markersize = 15)

plt.axis([-1.,11.,-1.,11.])
plt.grid()
plt.show()

# ** On calcule les reseaux des protos

Passociation=association_points_protos(X,P1+P2)

affiche_proto(Passociation)

affiche_point(X)

#Format matrices

mat_X = np.array([[i.x, i.y] for i in X])
mat_P = np.array([[i.x, i.y] for i in Passociation])
label_X = np.array([i.label for i in X])
label_P = np.array([i.label for i in Passociation])


NewP  = ajusterProtos(mat_X, label_X, mat_P, label_P, 50)
plt.plot(NewP[:,0],NewP[:,1],color = 'g', linestyle = '', marker = 's')
plt.plot(listeancienprotolabelX,listeancienprotolabelY,color='b',linestyle='',marker='o',markersize=2)

plt.show()
#Valeurs des coefficients des matrices

print ('Matrice de coordonnées des points')
print (mat_X)

print('Matrice de coordonnées des prototypes')
print (mat_P)

print('Matrice des labels des points')
print (label_X)

print('Matrice des labels des prototypes')
print (label_P)
print("")
print("Reseau final ")
affiche_proto(association_points_protos(X,protoFromMatrix(NewP,label_P)))

      
        
