# Optimisation de la localisation des capacités de production éoliennes en Europe

## Description

Ce projet étudie la faisabilité d'un système de production d'électricité européen fortement basé sur l'énergie éolienne. L'objectif est de déterminer l'emplacement optimal et la capacité d'installation d'éoliennes onshore et offshore pour maximiser la production d'énergie tout en contrôlant la variabilité.

DISCLAIMER : Comme les données étaient trop volumineuse nous ne pouvions pas les inclures dans le github 

## Contexte académique

- **Cours** : LINMA1702 - Modèles et méthodes d'optimisation 2023-2024
- **Partie** : Analyse d'un modèle européen intégré (Partie I)
- **Objectif** : Résolution de problèmes d'optimisation linéaire pour la planification énergétique

## Structure du projet

```
Projet-Opti-main/
├── main.py                    # Script principal d'optimisation
├── extracte.py               # Module d'extraction et traitement des données
├── Plot.py                   # Module de visualisation cartographique
├── Energie_Rendements.py     # Module d'analyse des rendements et production
├── main.ipynb               # Notebook Jupyter pour analyse interactive
├── README.md                # Documentation du projet
├── Projet-2024-partie-1-v2.pdf  # Énoncé du projet
└── image/                   # Dossier contenant les graphiques générés
    ├── Energie_produite_jours.png
    ├── Rendementmoyen.png
    ├── Sites_selectionnée_mod_1.png
    └── ...
```

## Fonctionnalités

### 1. Modèle d'optimisation principal (`main.py`)
- Formulation du problème sous forme de programmation linéaire
- Maximisation de la production minimale d'énergie sur toutes les heures de l'année
- Contraintes sur la puissance totale installée (P = 500,000 MW)
- Contrainte sur la proportion offshore (κ = 0.17)

### 2. Extraction de données (`extracte.py`)
- Classe `FichierData` pour le traitement des fichiers CSV
- Extraction des sites, rendements onshore et offshore
- Gestion de 642 sites éoliens européens
- Données horaires sur une année complète (8760 heures)

### 3. Visualisation (`Plot.py`)
- Représentation cartographique des sites sélectionnés
- Utilisation de Basemap pour la projection européenne
- Taille des points proportionnelle à la capacité installée
- Distinction visuelle onshore/offshore par couleur

### 4. Analyse des performances (`Energie_Rendements.py`)
- Calcul et visualisation des rendements moyens
- Graphiques de production d'énergie au cours du temps
- Analyse de la variabilité temporelle

## Données requises

Le projet nécessite les fichiers de données suivants (non inclus) :
- `Data-partie-1/Sites.csv` : Base de données des 642 sites éoliens
- `Data-partie-1/Rendements_onshore.csv` : Rendements horaires onshore
- `Data-partie-1/Rendements_offshore.csv` : Rendements horaires offshore

## Installation et utilisation

### Prérequis
```bash
pip install scipy numpy matplotlib pandas basemap
```

### Exécution
```bash
python main.py
```

### Analyse interactive
```bash
jupyter notebook main.ipynb
```

## Paramètres du modèle

- **P** : 500,000 MW (puissance totale à installer)
- **κ** : 0.17 (fraction offshore)
- **Sites** : 642 sites européens
- **Période** : 8760 heures (1 année)

## Résultats

Le modèle génère :
- **Énergie totale produite** sur l'année
- **Nombre de sites sélectionnés**
- **Cartes de localisation** des installations optimales
- **Graphiques de production** temporelle
- **Analyse des rendements** par site

## Méthodes d'optimisation

- **Solveur** : `scipy.optimize.linprog`
- **Type** : Programmation linéaire
- **Variables** : Continues (capacités installées)
- **Objectif** : Maximisation du minimum de production horaire

## Hypothèses du modèle

1. Puissance installable entre 0 et la capacité maximale par site
2. Production calculée heure par heure
3. Production = Puissance installée × Rendement horaire
4. Puissance constante durant chaque heure

## Extensions possibles

Le projet prévoit une Partie II avec :
- Interconnexions entre pays
- Possibilité de stockage d'électricité
- Prise en compte des émissions CO₂
- Modèles plus sophistiqués

## Auteurs

Projet académique réalisé dans le cadre du cours LINMA1702.