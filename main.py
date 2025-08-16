import scipy as sc                   # Import de scipy qui va nous permettre de solvez les porblèmes d'optimisation
import numpy as np                   # numpy toujours utile pour manipuler des vecteurs & matrices
import matplotlib.pyplot as plt      # pour graphiques éventuels
import extracte 
import Plot
import Energie_Rendements
from scipy.optimize import linprog

def main () : 
    chemin_sites = "Data-partie-1/Sites.csv"
    chemin_onshore = "Data-partie-1/Rendements_onshore.csv"
    chemin_offshore = "Data-partie-1/Rendements_offshore.csv"
    #On créer une varaible Data pour extraire les données 
    Data = extracte.FichierData(chemin_sites , chemin_offshore ,chemin_onshore)
    Nombre_sites = 642
    P = 500000
    k = 0.17
    
    def mod1 (): 
        #Donc en se renseignant sur la fonction linprog utilisé lors du labo 1 en optimisation et en regardant sa documentation on se rend compte qu'on doit formuer notre porblème sous cette forme : 
        #minimize c @ x 
        #such that

        #A_ub @ x <= b_ub
        #A_eq @ x == b_eq
        #lb <= x <= ub   0 et 1 dans notre cas     
        
        # Dans notre cas on va formuler le projet comme suit : 
        # Min (-min -y)
        #        y <= A^T * x En gros on multiplie chaque colonne de A par x et on borne y du coup --> ça devient 
        #        0 <= x <= 1 ---> x <= 1 et -x <= 0
        #        c * (1 0) * (x y)^T   == P On doit avoir une puissance maximale sur l'années de 500 000MW
        #        c * (xj y)   == P*k Proportion de variable xj qui sont les variables offshore attribués a une certaine puissanec                                                         

        
        # On va dabord créer A_1 car c'est la plus facile : 
        Ron = Data.extract_on() #On extrait les données pour les Rendements Onshore
        Roff = Data.extract_off() #On extrait les données pour les Rendements offShore
        Nbre_offshore = len(Roff) #On extrait le nombre de Site offshore 
        Nbre_heure = 8760   #Le nombre d'heure total dans une année 365 * 24

        c = Data.extract_Capacite() #On extrait les capacitées 
        R = np.concatenate((Ron,Roff)) #On rassemble les rendements dans l'ordre de Sites.csv
        A = c[:,np.newaxis]*R #On multiplie nos rendement par nos capacitée par heure pour obtenir A 
        
        #On va commencer a superposer nos matrices à savoir celle pour faire la Condition 1.
        #1 ère condition à savoir  c * xi  == P : 
        A = np.transpose(A) #A doit être transposée pour avoir sur la ligne 1 la production de chaque usine a l'heure 1 
        Nouvelle_colonne_pour_y = np.zeros((Nbre_heure, 1))  
        A = np.hstack((A , Nouvelle_colonne_pour_y)) #Rajouter une nouvelle colonne pour la nouvelle variable y
        
        
        b_1 = [P] #Premier vecteur b_1 


        #2 eme conditions à savoir  c * xj == P * k : 


        b_2 = [P * k]
        indice = Nombre_sites - Nbre_offshore 
        # Création de A_1 en concaténant c avec un tableau de zéros de longueur 1
        A_1 = np.concatenate((c, [0]))

        

        # Création de A_eq2 en concaténant un tableau de zéros de longueur len(Ron) avec une partie de c à partir de l'indice indice
        A_2 = np.concatenate((np.zeros(len(Ron)), c[indice:]))

        # Concaténation de A_eq2 avec un tableau de zéros de longueur 1
        A_2 = np.concatenate((A_2, [0]))

        # Création de A_eq en regroupant A_eq1 et A_eq2 dans un tableau 2D
        
        
        #Superposition des deux matrices : 
        
        b_eq = np.hstack((b_1,b_2)) 
        A_eq = np.array([A_1, A_2])
        print(b_eq)


        #Maintenant les conditions d'inégalitées : 
        #1 ere conditions à savoir -x <= 0 et x <= 1 
        Identité = np.identity((Nombre_sites)) #Creation de la matrice identitée
        zeros_colonne = np.zeros((Nombre_sites , 1)) # Rajout d'une colonne de Zero à la matrice identité pour le y
        Identité = np.hstack((Identité , zeros_colonne))
        
        A_ub_1 = Identité # matrice A_ub_1     Aub1 * x <= bub1 
        
        b_ub_1 = np.ones(Nombre_sites ) # matrice b_ub_1    Aub1 * x <= bub1   Avec Aub1 = I
        


        opp_Identité = -Identité # matrice Identité de signe inverse     Aub2 * x <= bub2  Avec Aub2 = -I
        

        A_ub_2 = opp_Identité 
        b_ub_2 = np.zeros(Nombre_sites + Nbre_heure)  #On rajoute les 0 pour l'inégalitées de suivante c'est plus facile 
        #Derniere inégalitée à savooir 
        A_ub2 = -A
        A_ub2[:, -1] = np.ones(Nbre_heure) #y doit aussi être plus petit que 1
        
        
        A_ub_t = np.concatenate((A_ub_1 , A_ub_2))
        
        A_ub = np.concatenate((A_ub_t , A_ub2))
        
        b_ub = np.hstack((b_ub_1 , b_ub_2)) #On rassemble les matrices 



        C = np.concatenate((np.zeros((Nombre_sites)), np.array([-1]))) #Nos coefficients à savoir que les notres sont (0 0 0 0 0 ... -1) car nous avons -min -y ---> On voit aussi qu'on devra prendre l'inverse du résultat


        

        

        
        
        
        # Résolution du problème d'optimisation linéaire
        finale = linprog(C, A_ub, b_ub, A_eq, b_eq)
        #Recuperation des resultats 
        
        x = finale.x[:-1] # Vecteurs des solutions optimisées 
        fun = -finale.fun  # Vecteur de la fonction objective 
        #Appelle de la fonction permettant de representer les points 
        Nombre_site = Plot.representation(x , Data.liste_ordre())
        Rendements_tot = Energie_Rendements.Rendement_tot(R , Nombre_site , x ) #Input = Liste des rendements pour les sites onshore et offshore
        Rendement_2 = Energie_Rendements.rendement_2(R , x)
        p = x * Data.extract_Capacite()
        Energie = Energie_Rendements.Energie_produite(R , Data.liste_ordre() , p )
        
        return x ,fun , Nombre_site
    x, fun , Nbre_sites = mod1()

    #Energie totale produite ? 

    print(f"L'energie totale produite sur l'année est de {fun} MW.")
    print(f"Le nombre totales de sites ayant été séléctionnée est de {Nbre_sites}")

    #Rendement moyen ? 
    #Calculé avec (R1 + R2 + R3 + R4 .... RN) / N
   
     

main()

#CVXPY    

