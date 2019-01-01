import matplotlib.pyplot as plt
import Point
from mpl_toolkits.mplot3d import Axes3D


class Affichage:
    "Classe qui permet de generer tous les graphiques necessaires"
        
    def afficherPoints(self,X):
        "X est une liste de points. Affichage pour les points -> sous forme de croix"
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in X :
            couleur = color_list[i.getLabel() % len(color_list)]
            if i.getLabel() == 30:
                couleur = 'k'
            plt.plot(i.getCoordonnees()[0], i.getCoordonnees()[1], color = couleur, linestyle = '', marker='x', markersize = 5)
        plt.grid()
        plt.show()
        
    def afficherPoints3D(self,X, fig):
        "X est une liste de points. Affichage pour les points -> sous forme de croix"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in X :
            ax.scatter(i.getCoordonnees()[0],i.getCoordonnees()[1], i.getCoordonnees()[2] ,color = color_list[i.getLabel() % len(color_list)], marker='o', s = 5, depthshade = True)
        ax.grid()
        
          
        
    def afficherProtosInitiaux(self,P):
        "P est une liste de Protos. Affichage pour protos initiaux -> Ronds"
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P :
            plt.plot(i.getCoordonnees()[0], i.getCoordonnees()[1], color = color_list[i.getLabel() % len(color_list)], linestyle = '', marker='x', markersize = 5)
        plt.grid()
        plt.show()    
        
    def afficherProtosInitiaux3D(self,P, fig):
        "P est une liste de Protos. Affichage pour protos initiaux -> Ronds"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P :
            ax.scatter(i.getCoordonnees()[0],i.getCoordonnees()[1], i.getCoordonnees()[2] , color = color_list[i.getLabel() % len(color_list)], marker='^', s = 50, depthshade = True)
        ax.grid()
        
        
        
    def afficherProtosFinaux(self,P):
        "P est une liste de Protos. Affichage pour protos -> Carrés. Cela affiche aussi le tissage de son reseau"
        color_list=['b', 'r', 'g', 'y', 'm', 'c']        
        for i in P:
            abscisseP = i.getCoordonnees()[0]
            ordonneeP = i.getCoordonnees()[1]
            labelP = i.getLabel()
            plt.plot(abscisseP, ordonneeP, color = color_list[labelP % 6], linestyle = '', marker='s', markersize = 10,  markeredgecolor = 'r')
            reseau = []
            reseau = i.getReseau()
            for j in reseau :
                plt.plot([abscisseP, j.getCoordonnees()[0]], [ordonneeP, j.getCoordonnees()[1]], color = color_list[labelP % len(color_list)], linestyle = '--', marker='', linewidth = '0.5')
        plt.grid()
        plt.show()

    def afficherProtosFinaux3D(self,P, fig):
        "P est une liste de Protos. Affichage pour protos -> Carrés. Cela affiche aussi le tissage de son reseau"
        ax = fig.gca(projection='3d')
        color_list=['b', 'r', 'g', 'y', 'm', 'c']
        for i in P:
            abscisseP = i.getCoordonnees()[0]
            ordonneeP = i.getCoordonnees()[1]
            coteP = i.getCoordonnees()[2]
            labelP = i.getLabel()
            ax.scatter(abscisseP,ordonneeP, coteP ,color = color_list[labelP % 6], marker='^', s = 50, depthshade = True)
            reseau = []
            reseau = i.getReseau()
            for j in reseau :
                ax.plot([abscisseP,j.getCoordonnees()[0]],[ordonneeP,j.getCoordonnees()[1]],[coteP,j.getCoordonnees()[2]],color = color_list[labelP % len(color_list)],linestyle = '--', marker='', linewidth = '0.5')
        ax.grid()
        
        
        
        
        
    def afficherProtosIntermediaires(self,listeAnciensProtos):
        "Prend en entree une liste de coordonnees. Affiche sous forme de petits carres"
        for i in listeAnciensProtos:
            plt.plot(i[0],i[1] ,color = 'k',linestyle = '', marker='s', markersize = 1)
        plt.grid()
        plt.show()
        
    
        
    def afficherFonction(self,X):
        "A faire après l'affichage du graphe de points. Prend en entree une liste de valeur et retourne le graphe de la fonction"
        print("affiche fontion "+str(X))        
        plt.figure()
        plt.plot([i for i in range(len(X))],X)
        plt.show()
        
        
    def afficherEspace(self,espace,finish=True):
       # if finish :
        #    plt.close()
        plt.figure()        
        self.afficherPoints(espace.listePoints)
        self.afficherProtosInitiaux(espace.listeProtosInitiaux)
        self.afficherProtosFinaux(espace.listeProtos)
        self.afficherProtosIntermediaires(espace.listeAncienProto)
        #self.afficherFonction(espace.graph_K)
        
        
    def afficherEspace3D(self,espace,finish,fig):
       # if finish :
        #    plt.close()

        self.afficherPoints3D(espace.listePoints, fig)
        self.afficherProtosInitiaux3D(espace.listeProtosInitiaux, fig)
        self.afficherProtosFinaux3D(espace.listeProtos, fig)
        
        
    
    def printPoints(self,X) :
        for i in X :
            string3=""
            k=0
            for l in i.getCoordonnees():
                k+=1
                string3 += " | X"+str(k)+" = "+str(l)
            print("Point = "+str(i.getId())+string3+" | label = "+str(i.label))
    
    
    def printProtos(self,P):
        for i in P :
            string2 ="Point "
            k=0
            string3=""
            for j in i.reseau :
                string2 += str(j.getId())+", "
            for l in i.getCoordonnees():
                k+=1
                string3 += " | X"+str(k)+" = "+str(l)
            print("Proto  id = "+str(i.getId())+string3+" | label = "+str(i.label)+" | Reseau = "+string2)
            
    def afficherValeurDescente(self,stockageValeurDescente) :
        print(stockageValeurDescente)
      #  for i in stockageValeurDescente:
       #     plt.figure()
      #      plt.plot([j for j in range(len(i))],i)
        plt.figure()
        plt.plot([j for j in range(len(stockageValeurDescente[0]))],stockageValeurDescente[0]) 
        plt.show()
    
    def afficherErrorByDim(self,X,Y):
        plt.figure()
        plt.plot(X,Y)
        plt.show()
        