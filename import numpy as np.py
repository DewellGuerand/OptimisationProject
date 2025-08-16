def mod4 (Data , n , k , Nombre_sites ,Periode , C_Ion , C_Ioff ,turbinage , pompage): 
                                                       
    
    
    
    Ron = Data.extract_on() #On extrait les données pour les Rendements Onshore
    Roff = Data.extract_off() #On extrait les données pour les Rendements offShore
    Nbre_offshore = len(Roff) #On extrait le nombre de Site offshore 
    Nbre_onshore = len(Ron)
    Nbre_heure = Periode   #Le nombre d'heure total dans une année 365 * 24
    

    c = Data.extract_Capacite() #On extrait les capacitées 
    # R = np.concatenate((Ron,Roff)) #On rassemble les rendements dans l'ordre de Sites.csv
    # A = c[:,np.newaxis]*R[:,:Nbre_heure] #On multiplie nos rendement par nos capacitée par heure pour obtenir A 
    C_Ion = ((C_Ion )/(365*24) )* Nbre_heure
    C_Ioff = (C_Ioff /(365*24))* Nbre_heure
    #On commence par créer la fonction objectif : 
    #Creation des variables donc qu'on ne connait pas encore : 

    x_on = cp.Variable( Nbre_onshore ,nonneg = True)  # Variables pour les sites éoliens onshore
    x_of = cp.Variable( Nbre_offshore, nonneg = True)  # Variables pour les sites éoliens offshore
    y = cp.Variable(Nbre_heure//3,nonneg = True)  # Variable pour le niveau minimal de production d'énergie (pompage)
    z = cp.Variable(Nbre_heure//3,nonneg = True)  # Variable pour le niveau maximal de production d'énergie (turbinage)
    s = cp.Variable(Nbre_heure//3,nonneg = True)  # Variable pour le niveau de srockage de l'energie
    #Fonction objectif : 
    objective = cp.Minimize(cp.sum(C_Ion * x_on) +
                        cp.sum(C_Ioff * x_of))      # Coûts d'investissement des sites éoliens
    #En suite on fait les contraintes : 
    #Initialisation des matrix pour les contraintes :
    Ron = np.transpose(Ron)[:Nbre_heure] #Matrice avec 8760 lignes et 487 colonnes
    Roff = np.transpose(Roff)[:Nbre_heure] #Matrice avec 8760 lignes et 155 colonnes
    # Initialiser la nouvelle matrice avec la première ligne inchangée
    num_new_rows = len(Ron) // 3
    new_Ron = np.zeros((num_new_rows, Ron.shape[1]), dtype=float)
    new_Ron[0] = Ron[0]

    # Calculer les sommes des groupes de trois lignes après la première
    for i in range(1, len(new_Ron)):
        start_index = 3 * (i - 1) + 1
        end_index = start_index + 3
        new_Ron[i] = np.sum(Ron[start_index:end_index], axis=0)

    num_new_rows = len(Roff) // 3
    new_Roff = np.zeros((num_new_rows, Roff.shape[1]), dtype=float)
    new_Roff[0] = Roff[0]

    # Calculer les sommes des groupes de trois lignes après la première
    for i in range(1, len(new_Roff)):
        start_index = 3 * (i - 1) + 1
        end_index = start_index + 3
        new_Roff[i] = np.sum(Roff[start_index:end_index], axis=0)
    
    #Matrice de Demande 
    D = np.transpose(Data.extract_conso())[:Nbre_heure]
    D = np.sum(D, axis=1)

    new_D = [D[0]]
    sum = 0
    for i in range(1,len(D)) : 
        if i % 3 != 0 :
            sum += D[i]
        else : 
            new_D.append(sum)


    #Matrice des bassins 
    A = np.transpose(Data.extract_apport())[:Nbre_heure]
    A = np.sum(A, axis=1)
    new_A = [A[0]]
    
    sum = 0
    for i in range(1,len(A)) : 
        if i % 3 != 0 :
            sum += A[i]
        else : 
            new_A.append(sum)
    

   
    
    #Matrcie de capa totale 
    S = [0.3*1e6 , 3.2*1e6 , 0.01*1e6 , 0 , 18.4*1e6 , 9.8*1e6 , 0.24*1e6 , 7.9*1e6 , 0.005*1e6 , 84.147*1e6 , 0 , 2.6*1e6 , 1.2*1e6 , 33.756*1e6 , 8.4*1e6]    
    sum_pompage = cp.sum(pompage)*3
    sum_turbinage = cp.sum(turbinage)*3
    sum_S = cp.sum(S)
    Ron = Ron[::3]
    Roff = Roff[::3]

    Constraints = []
    Constraints.append(s[0] == sum_S*0.5)
    Constraints.append(s[Nbre_heure//3-1] == sum_S*0.5)
    Constraints.append(new_Ron @ x_on + new_Roff @ x_of - y + n*z >= new_D)
    for t in range(Nbre_heure//3):
        # Contrainte de non négativité des variables
        if t != 0  :
            Constraints.append(s[t] == s[t-1] -  z[t] + y[t] + new_A[t])

        

    # Contraine du bassin
    Constraints.append(s <= sum_S*3)
    # Contrainte de la puissance minimale
    Constraints.append(y <= sum_pompage)
    # Contrainte de la puissance maximale
    Constraints.append(z <= sum_turbinage)
    Constraints.append(x_on <= c[:Nbre_onshore])
    Constraints.append(x_of <= c[Nbre_onshore:])
    problem = cp.Problem(objective, Constraints)
    print(cp.installed_solvers())
    problem.solve(solver=cp.SCIPY )
    
    
    print("Valeur de la fonction objectif :", problem.value)
    a = x_on.value
    b = x_of.value
    print(f"Valeur du cout moyen (MW): " ,problem.value/(np.sum(a) + np.sum(b)))
    print(f"Valeur du cout moyen (MW/h): " ,(problem.value/(np.sum(a) + np.sum(b)))/Periode)
    return problem.value , a , b , s.value ,y.value , z.value

