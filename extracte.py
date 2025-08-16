import scipy as sc                   # Import de scipy qui va nous permettre de solvez les porblèmes d'optimisation
import numpy as np                   # numpy toujours utile pour manipuler des vecteurs & matrices
import matplotlib.pyplot as plt      # pour graphiques éventuels
import pandas as pd                  #Librairie permettant la lecture des données 


class FichierData : 
    def __init__(self , chemin_fichier_sites , chemin_fichier_offshore , chemin_fichier_onshore) :
        self.Sites = pd.read_csv(rf"{chemin_fichier_sites}")
        self.offshore = pd.read_csv(rf"{chemin_fichier_offshore}" , header=None)
        self.onshore = pd.read_csv(rf"{chemin_fichier_onshore}" , header = None) 
        self.nombre_site  = 642 
        self.don= self.liste_ordre()
        
    

    def extract_Index(self) : 
        return self.Sites.iloc[:, 0].values
    
    #Serivra pour la representation sur la carte 
    def extract_Latitude(self) : 
        return self.Sites.iloc[:, 1].values
    
    #Serivra pour la representation sur la carte 
    def extract_Longitude(self) : 
        return self.Sites.iloc[:, 2].values
    
    #Serivra pour la representation sur la carte 
    def extract_Pays(self) : 
        return self.Sites.iloc[:, 3].values
    
    #Serivra pour la representation sur la carte 
    def extract_Couleur(self) : 
        return self.Sites.iloc[:, 4].values
    
    #Important pour les calculs 
    def extract_Capacite_offshore(self) : 
        return self.Sites.iloc[:, 5].values
    
    #Sait pas encore a quoi ça sert 
    def extract_scores(self) : 
        return self.Sites.iloc[:, 6].values
    

    def extract_Capacite(self) : 
        return self.Sites.iloc[:, 7].values
    
    
    #Fonction qui extrait les données pour l'onshore et l'offshore et retourne les rendements 
    
    
    def extract_on(self) : 
        
        On = [] 
        
        for i in range(len(self.don)  ) :
            
            if self.don[i][5] == "Non" : 
                index = int(self.don[i][0])
                On.append(self.onshore.iloc[index].to_numpy())
        
        return np.array(On)
    def extract_off(self) : 
        Off = [] 
        
                
        for i in range(len(self.don) ) : 
            
            if self.don[i][5] == "Oui" : 
                index = int(self.don[i][0])
                Off.append(self.offshore.iloc[index].to_numpy())
        return np.array(Off)

        
    #Creation d'ue liste pour stocker les informations mais dans l'ordre 
    def liste_ordre (self) : 
        lst = []
        for i in range (len(self.Sites)) : 
            lst.append(self.Sites.iloc[i , :8].values)
            
        return np.array(lst)



    
# COmmentaire pour que les fichiers puisent être lu : Le fichier Data-partie-1 doit être en dehors du dossier Projet-opti pour qu'il puisse être lu 
chemin_sites = "Data-partie-1/Sites.csv"
chemin_onshore = "Data-partie-1/Rendements_onshore.csv"
chemin_offshore = "Data-partie-1/Rendements_offshore.csv"
Test = FichierData(chemin_sites , chemin_offshore ,chemin_onshore)
test = False 
if test : 
    print(Test.extract_Index())
    print(Test.extract_Latitude())
    print(Test.extract_Longitude())
    print(Test.extract_Pays())
    print(Test.extract_Couleur())
    print(Test.extract_Capacite_offshore())
    print(Test.extract_scores())
    print(Test.extract_Capacite())
    print(len(Test.extract_on()))
    print(len(Test.extract_off()))
    print(Test.extract_Capacite())
    print(Test.liste_ordre())  







