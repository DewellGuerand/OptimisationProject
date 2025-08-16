import matplotlib.pyplot as plt  #Import a matplot lib 
from mpl_toolkits.basemap import Basemap #Import de basemap

def representation (Solution , Donnée ) : 
    # Création de la carte d'Europe
    plt.figure(figsize=(20, 8))
    m = Basemap(projection='merc', llcrnrlat=35, urcrnrlat=70, llcrnrlon=-10, urcrnrlon=30, resolution='i')

    # Ajout des éléments de la carte
    m.drawcountries(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)

    # Coordonnées des points à représenter (latitude, longitude)$
    Nombre = 0
    importance = []
    couleurs = []
    lats = []
    lons = []
    for i in range(len(Donnée)) : 
        if (Solution[i] != 0) :
            Nombre+=1 
            lats.append(Donnée[i][1])
            lons.append(Donnée[i][2])
            couleurs.append(Donnée[i][4])
            importance.append(Solution[i]*25)





    # Convertir les coordonnées en coordonnées de la carte
    x, y = m(lons, lats)

    # Tracer les points sur la carte
    m.scatter(x, y, color=couleurs, marker='o', s=importance)
    
    # Affichage de la carte
    plt.title('Points sur une carte d\'Europe')
    plt.show()
    return Nombre

