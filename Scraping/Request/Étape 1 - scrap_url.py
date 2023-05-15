# Importation des modules nécessaires
import re
import requests
import pickle

# Définition de l'URL de base de la page à parcourir et du modèle d'en-tête de requête HTTP
base_url = "https://www.transfermarkt.fr/spieler-statistik/wertvollstespieler/marktwertetop?page={}"
request_headers={'User-Agent': "(Mozilla/5.0 (Windows; U; Windows NT 6.0 \;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" }

# fonction pour extraire une sous-chaîne de texte entre deux chaînes spécifiées
def pap(X,Y):
    pattern = X +'(.+?(?=' + Y + '))' # utiliser les expressions régulières pour trouver la sous-chaîne entre X et Y
    return(re.findall(pattern,html)) # rechercher le motif dans le texte et renvoyer la sous-chaîne trouvée

# fonction qui recherche et affiche un extrait de texte autour de la chaîne X dans le texte txt
def find(X):
    print(html[html.find(X)-500:html.find(X)+500])

# Liste pour stocker les URL des joueurs
url_joueur = []

# Boucle sur les pages de résultats de recherche
for page_num in range(1, 21):
    url = base_url.format(page_num) # Construction de l'URL de la page à parcourir
    response = requests.get(url, headers=request_headers) # Envoi d'une requête HTTP pour récupérer la page
    html = response.text # Extraction du contenu HTML

    # Extraire les noms et les URL des joueurs à partir du code HTML de la page
    url_j = pap('<td class="hauptlink"><a title="(.{1,50})" href="','">(.{1,50})</a></td>')
    for joueur in url_j:
        url_joueur.append(joueur[1])

# Enregistrer les URL de tous les joueurs dans un fichier pickle pour une utilisation ultérieure
pickle.dump (url_joueur, open('Data/url_joueur.dat', 'wb'))

    
