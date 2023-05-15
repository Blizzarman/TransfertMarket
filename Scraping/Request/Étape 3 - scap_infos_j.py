# Importation des modules nécessaires
import re
import pandas as pd
import numpy as np
import os

# fonction pour extraire une sous-chaîne de texte entre deux chaînes spécifiées
def pap(X,Y):
    pattern = X +'(.+?(?=' + Y + '))' # utiliser les expressions régulières pour trouver la sous-chaîne entre X et Y
    return(re.findall(pattern,txt)) # rechercher le motif dans le texte et renvoyer la sous-chaîne trouvée

# fonction qui recherche et affiche un extrait de texte autour de la chaîne X dans le texte txt
def find(X):
    print(txt[txt.find(X)-500:txt.find(X)+500])

# dictionnaire qui stockera les données pour chaque joueur
dico ={}
dico['#Id'] = []
dico['nom'] = []
dico['age'] = []
dico['taille'] = []
dico['pied'] = []
dico['nationalite'] = []
dico['position'] = []
dico['club'] = []
dico['ligue'] = []
dico['fin_contrat'] = []
dico['valeur_actuelle'] = []
dico['valeur_max'] = []
dico['montant_transfert'] = []
dico['CDM'] = []
dico['LDC'] = [] 
dico['nb_selections'] = []
dico['nb_buts'] = []

# liste des fichiers à traiter (chacun contient les données d'un joueur)
L = os.listdir('Data/Pages')
# pour chaque fichier :
for i in L:
    with open('Data/Pages/'+i,'r',encoding='utf8') as output:
        # on lit le texte du fichier
        txt = output.read()

        # on ajoute l'ID du joueur au dictionnaire
        dico['#Id'].append(i)

        # on cherche le nom du joueur dans le texte
        nom=pap('href="/','/erfolge/spieler')
        # on ajoute le nom du joueur au dictionnaire
        dico['nom'].append(nom[0])

        # on cherche l'âge du joueur dans le texte
        age=pap('info-table__content--regular">Âge:</span>\n                        <span class="info-table__content info-table__content--bold">','</span>\n')
        # on ajoute l'âge du joueur au dictionnaire
        dico['age'].append(age[0])

        # on cherche la taille du joueur dans le texte
        taille=pap('<span itemprop="height" class="data-header__content">',' m</span>')
        # on ajoute la taille du joueur au dictionnaire
        dico['taille'].append((taille[0]).replace(',', '.'))

        # on cherche le pied du joueur dans le texte
        pied=pap('info-table__content--regular">Pied:</span>\n                    <span class="info-table__content info-table__content--bold">','</span>\n')
        # on cherche la pied du joueur dans le texte       
        dico['pied'].append(pied[0])

        # on cherche la nationalité du joueur dans le texte
        nationalite=pap('" alt="','" class="flaggenrahmen"')
        # on cherche la nationalité du joueur dans le texte
        dico['nationalite'].append(nationalite[1])

        # on cherche la position du joueur dans le texte
        position=pap('<dd class="detail-position__position">','</dd>')
        # on cherche la position du joueur dans le texte
        dico['position'].append(position[0])
        
        # on cherche le club du joueur dans le texte
        club=pap('<div class="data-header__club-info">\n                    <span class="data-header__club" itemprop="affiliation">\n                        <a title="','" href=')
        # on cherche le club du joueur dans le texte
        dico['club'].append(club[0])

        # on cherche la ligue du joueur dans le texte
        ligue=pap('class="data-header__league-link" href="/','/startseite/wettbewerb/')
        # on cherche la ligue du joueur dans le texte
        dico['ligue'].append(ligue[0])

        # on cherche le contrat du joueur dans le texte
        contrat=pap('info-table__content--regular">Contrat jusqu’à:</span>\n                    <span class="info-table__content info-table__content--bold">(.{1,7})','</span>\n')
        if len(contrat)==1:
            dico['fin_contrat'].append(contrat[0][1])
        else:
            dico['fin_contrat'].append(np.nan)

        # on cherche la valeur actuelle du joueur dans le texte
        valeur_act=pap('data-header__market-value-wrapper">',' <span class="waehrung">')
        # on cherche la valeur actuelle du joueur dans le texte
        dico['valeur_actuelle'].append((valeur_act[0]).replace(',00', ''))

        # on cherche la valeur maximale du joueur dans le texte
        valeur_max=pap('<div class="tm-player-market-value-development__max-value">','</div')
        # on cherche la valeur maximale du joueur dans le texte
        dico['valeur_max'].append((valeur_max[0]).replace(',00 mio. €', ''))

        # on cherche le montant du transfert du joueur dans le texte
        transfert=pap('<div class="tm-player-transfer-history-grid__fee">','</div')
        # on cherche la montant du transfert du joueur dans le texte
        transfert=transfert[0]
        if "mio. €" in transfert:
            dico['montant_transfert'].append((transfert.replace(',', '.')).replace('mio. €', ''))
        elif len(transfert)<=4:
            dico['montant_transfert'].append('0.0' + (transfert.replace('K €', '')))
        else :
            dico['montant_transfert'].append('0.' + (transfert.replace('K €', '')))

        # on cherche si le joueur à gagné une Coupe du Monde dans le texte
        monde=pap('alt="Weltmeister" class="" style="height: 30px;" />                                                <span class="data-header__success-number">','</span>')    
        if len(monde)==1:
            dico['CDM'].append(1)
        else:
            dico['CDM'].append(0)

        # on cherche si le joueur à gagné une Ligue des Champions dans le texte
        ldc=pap('"Champions-League-Sieger" class="" style="height: 30px;" />                                                <span class="data-header__success-number">','</span>')
        if len(ldc)==1:
            dico['LDC'].append(ldc[0])
        else:
            dico['LDC'].append(0)

        # on cherche le nombre de sélections du joueur dans le texte
        if "nationalmannschaft/spieler/" in txt:
            selection=pap('<a href="/(.{1,40})/nationalmannschaft/spieler/(.{1,10})/verein_id/(.{1,6})">',  "</a>")
            if len(selection[0])==4:
                selection = selection[0][3]
                if selection =='-':
                    selection = selection.replace('-','0')
                    dico['nb_selections'].append(selection)
                else:
                    dico['nb_selections'].append(selection)
            else :
                dico['nb_selections'].append(np.nan)
        else:
            dico['nb_selections'].append(np.nan)

        # on cherche le nombre de buts du joueur dans le texte 
        if "nationalmannschaft/spieler/" in txt:
            but=pap('<a href="/(.{1,40})/nationalmannschaft/spieler/(.{1,10})/verein_id/(.{1,6})/nurEinsatz/2">',  "</a>")
            if len(but[0])==4:
                but = but[0][3]
                if but =='-':
                    but = but.replace('-', '0')
                    dico['nb_buts'].append(but)
                else:
                    dico['nb_buts'].append(but)
            else:
                dico['nb_buts'].append(np.nan)
        else :
            dico['nb_buts'].append(np.nan)

# on enregistre le dictionnaire en format csv
df = pd.DataFrame(dico)
df = df.set_index('#Id')
df.to_csv("Data/Joueurs.csv",sep='|')    
 
 
        
              



