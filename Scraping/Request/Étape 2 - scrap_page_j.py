# Importation des modules nécessaires
import requests
import pickle

# Définition de l'URL de base pour le site Transfermarkt et du header pour les requêtes HTTP
url = "https://www.transfermarkt.fr"
request_headers={'User-Agent': "(Mozilla/5.0 (Windows; U; Windows NT 6.0 \;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" }

# Chargement des URLs des joueurs depuis le fichier pickle généré par le premier script
with open('Data/url_joueur.dat', 'rb') as Base1:
    Base = pickle.load(Base1)

# Boucle pour accéder aux pages de chaque joueur et enregistrer le contenu HTML de chaque page dans un fichier
x=0
for i in Base:
    # Construction de l'URL du joueur en utilisant l'URL de base et l'URL spécifique du joueur
    url_joueur = url + str(i)
    # Envoi d'une requête HTTP pour récupérer le contenu HTML de la page du joueur
    req = requests.get(url_joueur, headers=request_headers)
    contenu = req.text
    # Ecriture du contenu HTML de la page dans un fichier avec un nom de fichier unique pour chaque joueur
    with open ('Data/Pages/'+(str(x))+'.html', 'w', encoding='utf8') as output:
        output.write(contenu)
    x+=1



