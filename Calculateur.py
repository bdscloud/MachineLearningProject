import numpy as np
import scipy.ndimage
import Affichage
import Espace
import random as rd
import copy

class Calculateur:
    #Variables
    #fonctionK : la fonction de complexite
    #gradientK : le gradient de la fonction de complexite
    
    def __init__(self, FKSource, GKSource):
        "Constructeur avec FK la fonction de complexite source et GK le gradient de complexite source"
        self.fonctionKSource = FKSource
        self.gradientKSource = GKSource
        
    def executerFonctionK(self, coordonneesPoint, reseau):
        "Execute la fonction de complexite coordonneesPoint est une liste numpy des coordonnees du point et reseau une liste de Points"
        return self.fonctionKSource(reseau, coordonneesPoint)
    
    def executerGradientK(self, coordonneesPoint, reseau):
        "Execute le gradient de la fonction de complexite coordonneesPoint est une liste numpy des coordonnees du point et reseau une liste de Points"
        return self.gradientKSource(reseau, coordonneesPoint)
        
    def getValeurStockageDescente(self):
        return self.valeurStockageDescente
        
    def norm(self, a):
        s = 0
        for i in range(a.shape[0]):
            s += a[i]**2
        return np.sqrt(s)
        
    def descenteGradientMultiDim(self,f,fp,x0,epsilon,Nmax,reseau): 
        "reseau est une liste de points et x0 le vecteur numpy des coordonnees de x0"
        #print("*** Fonction descenteGradienMultiDim ***"+str(x0))
        dimension = np.size(x0)
        ecart = epsilon+1;
        x_suivant=np.copy(x0)
        nb_etape = 0
        alpha=0.01
        #graphX =[]
        #graphY= []
        
        while ecart>epsilon and nb_etape<Nmax:
        
            x_precedent = np.copy(x_suivant)
        # print("xprecedent "+str(x_precedent))
            #Le np.int64 permet de gerer les valeurs grandes de gradien en 64 bits
            gradien = np.array(fp(reseau, x_precedent),np.int64)
            
            for i in range(dimension):
                #On fait la distinction si la norme = 0 alors c'est que le gradien est nul
                # mais on ne peut pas faire "0/0" donc on définie a la main le coeff a 0 dans ce cas
                if np.linalg.norm(gradien)!=0:                
                    coeff = gradien/self.norm(gradien)
                else :
                    coeff = np.zeros(dimension)
                x_suivant[i] = x_precedent[i] - coeff[i]*alpha
                signe = f(reseau, x_suivant)-f(reseau, x_precedent)
                #J'ai choisis d'incrementer peu alpha, car on place normalement les protos pas trop loins de la bonne valeur
                if signe>0 :
                    alpha = alpha*2
                else :
                    alpha = alpha*0.5
            #graphY.append(x_suivant, reseau) 
            #graphX.append(nb_etape)        
            ecart = self.norm(x_precedent-x_suivant)
            nb_etape+=1
        #  print("nb etapes = "+str(nb_etape)+" | alpha = "+str(alpha)+" | ecart = "+str(ecart))
        
    # plt.plot(graphX,graphY ,color = 'r',linestyle = '-', marker='o')    
    # print("Le minimum trouve vaut : "+str(x_suivant))
    # print("***")
        return x_suivant,f(reseau,x_suivant)
        
    def getRandomPoints(self, X, f):
        L = copy.copy(X)
        i = 0
        ret = []
        while(i < (len(X)*f)):
            indice = rd.randint(0, len(L) - 1)
            ret.append(L[indice])
            del L[indice]
            i += 1
        return ret
    
    def descenteGradientSource(self,P,epsilon,Nmax): #Descente de gradient
        reseau = self.getRandomPoints(P.getReseau(), 0.01)
        reseau = reseau + [P]
        valeurDescente = []
        espacePourBary = Espace.Espace([],[])
        barycentre = espacePourBary.getBarycentrePoints(P.getReseau() + [P])
        xfinal,minimum = self.descenteGradientMultiDim(self.fonctionKSource, self.gradientKSource, barycentre, epsilon, Nmax, reseau)
        for i in reseau :
            x,valeur = self.descenteGradientMultiDim(self.fonctionKSource, self.gradientKSource, np.array(i.getCoordonnees()),epsilon,Nmax,reseau)
            valeurDescente.append(valeur)
            if valeur < minimum :
                xfinal = x
                minimum = valeur
        for i in range(xfinal.shape[0]):
            P.setCoordonnee(xfinal[i], i)
        return P,valeurDescente