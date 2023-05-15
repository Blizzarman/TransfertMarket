# Importation des bibliothèques nécessaires
import requests
from bs4 import BeautifulSoup as Soup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# URL de la première page à scraper
url = "https://www.transfermarkt.fr/spieler-statistik/wertvollstespieler/marktwertetop?page="

# Headers pour simuler une requête à partir d'un navigateur
request_headers={'User-Agent': "(Mozilla/5.0 (Windows; U; Windows NT 6.0 \;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" }

# Listes pour stocker les URL et les noms de tous les joueurs à scraper
url_joueur = []
nom_joueur = []

# Dictionnaire pour stocker toutes les informations sur chaque joueur
dic ={}
dic['#ID'] = []
dic['nom'] = []
dic['age'] = []
dic['taille'] = []
dic['nationalite'] = []
dic['position'] = []
dic['pied'] = []
dic['club'] = []
dic['ligue'] = []
dic['fin_contrat'] = []
dic['valeur_actuelle'] = []
dic['valeur_max'] = []
dic['montant_transfert'] = []
dic['CDM'] = []
dic['LDC'] = [] # europe
dic['nb_selections'] = []
dic['nb_buts'] = []


# Boucle pour obtenir tous les joueurs de toutes les pages (20 pages au total)
for page in range(1,21):
    # Construire l'URL de la page courante en ajoutant le numéro de page à la fin
    p_url = url + str(page)
    # Récupérer le HTML de la page courante en simulant une requête à partir d'un navigateur
    p_html = requests.get(p_url, headers=request_headers)
    # Parser le HTML avec BeautifulSoup
    p_soup = p_html.text
    p_data = Soup(p_soup,'html.parser')
    # Trouver tous les corps de tableau tbody dans la page courante
    p_table = p_data.find_all('tbody') 
    # Nous n'avons besoin que du deuxième corps de tableau qui contient les informations sur les joueurs
    p_table = p_table[1]  

    # Pour chaque cellule de tableau contenant le nom d'un joueur, obtenir le nom et l'URL du joueur
    for i in p_table.find_all('td', {"class":"hauptlink"}):
       if i.a.get('title')==None:
           pass
       else:
           nom_joueur.append(i.a.get('title'))
       if '/profil/spieler/' in i.a.get('href'):
           url_joueur.append('https://www.transfermarkt.fr'+i.a.get('href'))

# Compteur pour suivre le nombre de joueurs traités
joueur = 0

# Boucle pour obtenir toutes les informations de tous les joueurs
for x in url_joueur:
    # Récupérer le HTML de la page du joueur courant en simulant une requête à partir d'un navigateur
    j_html = requests.get(x, headers=request_headers)
    # Parser le HTML avec BeautifulSoup
    j_soup = j_html.text
    j_data1 = Soup(j_soup,'html.parser')

    # Obtenir le nom du joueur courant
    dic['nom'].append(nom_joueur[joueur])

    # Obtenir le ID du joueur courant
    Id = j_data1.find_all('span', {"class" : "data-header__shirt-number"})
    Id = Id[0].get_text(strip=True) 
    dic['#ID'].append(Id)
    Id = Id.replace('#', '')

    # Obtenir la position du joueur courant    
    position = j_data1.find_all('dd', {"class":"detail-position__position"})
    if len(position)>=1:
        dic['position'].append(position[0].get_text(strip=True))
    else:
        dic['position'].append(np.nan)

    # Obtenir la valeur actuelle du joueur courant    
    valeur_act = j_data1.find_all('div', {"class":"tm-player-market-value-development__current-value"})
    dic['valeur_actuelle'].append((valeur_act[0].get_text(strip=True)).replace(',00 mio. €', ''))

    # Obtenir la valeur maximale du joueur courant   
    valeur_max = j_data1.find_all('div', {"class":"tm-player-market-value-development__max-value"})
    dic['valeur_max'].append((valeur_max[0].get_text(strip=True)).replace(',00 mio. €', ''))

    # Obtenir le club du joueur courant    
    club = j_data1.find_all('div', {"class":"data-header__box--big"})
    dic['club'].append(club[0].img.get("alt"))

    # Obtenir la date de fin de contrat et le pied du joueur courant    
    url_club = (club[0].a.get("href"))
    url_club = url_club.replace('startseite', 'kader')
    url_club = "https://www.transfermarkt.fr" + url_club + '/saison_id/2022/plus/1'
    club_html = requests.get(url_club, headers=request_headers)
    club_soup = club_html.text
    club_data1 = Soup(club_soup,'html.parser')
    club_table = (club_data1.find_all('tbody'))[1]
    for i in club_table.find_all('tr'):
        num = i.find_all('div', {"class":"rn_nummer"})
        if len(num) == 1:
            num = num[0].get_text(strip=True)
        else:
            pass
        if Id == num:  
            fin_contrat = i.find_all('td', {"class":"zentriert"})
            dic['fin_contrat'].append((fin_contrat[7].get_text(strip=True))[-4:])
            dic['pied'].append(fin_contrat[4].get_text(strip=True))

    # Obtenir la ligue du joueur courant    
    ligue = j_data1.find_all('span', {"class":"data-header__league"})
    dic['ligue'].append(ligue[0].get_text(strip=True))

    # Obtenir l'age du joueur courant    
    age = j_data1.find_all('span', {"class":"data-header__content"})
    age = age[0].get_text(strip=True)
    dic['age'].append(age[age.find( '(' )+1 : age.find( ')' ) ])

    # Obtenir la nationalité du joueur courant
    nationalite = j_data1.find_all('span', {"class":"data-header__content"})
    dic['nationalite'].append(nationalite[1].get_text(strip=True))

    # Obtenir la taille du joueur courant    
    taille = j_data1.find_all('span', {"class":"data-header__content"})
    dic['taille'].append(((taille[2].get_text(strip=True)).replace('m', '')).replace(',', '.'))

    # Obtenir le nombre de selection et de buts du joueur courant    
    if "grid national-career__row national-career__row--header" in j_soup :
        nb_selections = j_data1.find_all('div', {"class":"grid__cell grid__cell--center"})
        selection = (nb_selections[1].get_text(strip=True))
        if selection =='-':
            selection = selection.replace('-', '0')
        dic['nb_selections'].append(selection)
    
        nb_buts = j_data1.find_all('div', {"class":"grid__cell grid__cell--center"})
        but = nb_buts[2].get_text(strip=True)
        if but =='-':
            but = but.replace('-', '0')
        dic['nb_buts'].append(but)
    else:
        dic['nb_selections'].append(np.nan)
        dic['nb_buts'].append(np.nan)

    # Obtenir le montant du transfert du joueur courant
    transfert = j_data1.find_all('div', {"class":"tm-player-transfer-history-grid__fee"})
    transfert = transfert[-1].get_text(strip=True)
    if "mio. €" in transfert:
        dic['montant_transfert'].append((transfert.replace(',', '.')).replace('mio. €', ''))
    elif len(transfert)<=4:
        dic['montant_transfert'].append('0.0' + (transfert.replace('K €', '')))
    else :
        dic['montant_transfert'].append('0.' + (transfert.replace('K €', '')))

    # Obtenir si le joueur à gagner une Coupe du Monde pour le joueur courant
    CDM = j_data1.find_all('a', {"title":"Weltmeister", "class":"data-header__success-data"})
    if len(CDM)==1:
        dic['CDM'].append(CDM[0].get_text(strip=True))
    else:
        dic['CDM'].append(0)

    # Obtenir le nombre de fois que le joueur courant à gagner une Ligue des Champions
    LDC = j_data1.find_all('a', {"title":"Champions-League-Sieger", "class":"data-header__success-data"})
    if len(LDC)==1:
        dic['LDC'].append(LDC[0].get_text(strip=True))
    else:
        dic['LDC'].append(0)

    # Ajouter 1 au compteur joueur
    joueur+=1
    print(joueur)

# Sauvegarde du dictionnaire avec toutes les informations collectées
df = pd.DataFrame(dic)
df = df.set_index('#ID')
df.to_csv("Data/Joueurs.csv",sep='|')    

