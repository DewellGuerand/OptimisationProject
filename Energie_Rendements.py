import matplotlib.pyplot as plt
import numpy as np
def Rendement_tot(Data ,nbre_sites , x) : 
    
    
    # Génération de données aléatoires pour les rendements de 642 sites sur une année
    np.random.seed(0)  # Pour rendre les résultats reproductibles
    nb_sites = nbre_sites
    rendements = []  # Génération de rendements aléatoires
    for i in range(len(Data)) : 
        if x[i] != 0 : 
            n = 0
            for j in range(len(Data[i])) : 
                n += Data[i][j]
            final = n/len(Data[i]) 
            final = final * 100
            rendements.append(final) 


        
    # Création du graphique
    plt.figure(figsize=(20, 8))
    plt.bar(range(1, nb_sites + 1), rendements, color='skyblue')

    # Ajout de titres et d'étiquettes
    plt.title('Rendements des sites sur une année')
    plt.xlabel('Sites')
    plt.ylabel('Rendement moyen (%)')

    # Affichage du graphique
    plt.grid(axis='y')
    plt.ylim(0, 100)  # Définir la limite de l'axe y entre 0 et 1 (pourcentage)
    plt.xticks([])  # Supprimer les étiquettes des sites sur l'axe x
    plt.show()

def Energie_produite(R , Data , x) : 
    

    #
      # Pour rendre les résultats reproductibles
    nb_jours = 365
    # Production d'énergie pour chaque jour
    Energie = []
    for i in range(nb_jours) : 
            somme = 0 
            for k in range(len(x)) : 
                
                for j in range(24*i , 24*i + 24) : 
                    somme += x[k] * R[k][j]
            somme = somme /1000
            Energie.append(somme)

    # Création du graphique
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, nb_jours + 1), Energie, color='blue', linestyle='-')

    # Ajout de titres et d'étiquettes
    plt.title('Production d\'énergie au cours du temps')
    plt.xlabel('Jours')
    plt.ylabel('Production d\'énergie (GW)')

    # Affichage du graphique
    plt.grid(True)
    plt.show()

def rendement_2(Data  , x ) : 
    nb_heure = 24*365
    nombre = 0 
    for i in range(len(x)) : 
        if x[i] != 0 : 
            nombre += 1 
    nombre_site_selectionné = nombre
    lst = []
    for j in range(nb_heure)  :
        somme = 0
        for k in range(len(x)) : 
            if x[k] != 0 : 
                somme += Data[k][j] 
        somme = (somme / nombre_site_selectionné) * 100
        lst.append(somme)

    plt.figure(figsize=(12, 6))
    plt.plot(range(1, nb_heure + 1), lst, color='blue', linestyle='-')

    # Ajout de titres et d'étiquettes
    plt.title('Rendement moyen au cours du temps')
    plt.xlabel('Heure')
    plt.ylabel('Rendement moyen')

    # Affichage du graphique
    plt.grid(True)
    plt.show()