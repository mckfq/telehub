import requests
import re
import os

# URL de la playlist source (celle qui est mise à jour)
URL_SOURCE = "https://raw.githubusercontent.com/LITUATUI/M3UPT/refs/heads/main/M3U/M3UPT.m3u"

# Nom du fichier de ta playlist (dans ton repo)
FICHIER_CIBLE = "geral.m3u"

# Les chaînes à mettre à jour
CHAINES_A_METTRE_A_JOUR = ["TVI", "CNN Portugal"]

# Télécharger la playlist source
response = requests.get(URL_SOURCE)
if response.status_code != 200:
    print("Erreur lors du téléchargement de la playlist source.")
    exit()

playlist_source = response.text

# Récupérer les nouvelles URLs des chaînes
nouveaux_liens = {}
for chaine in CHAINES_A_METTRE_A_JOUR:
    match = re.search(rf'#EXTINF.*?,{chaine}\n(https?://[^\s]+)', playlist_source)
    if match:
        nouveaux_liens[chaine] = match.group(1)

if not nouveaux_liens:
    print("Aucune mise à jour trouvée pour les chaînes spécifiées.")
    exit()

# Lire la playlist cible
try:
    with open(FICHIER_CIBLE, "r", encoding="utf-8") as file:
        playlist_cible = file.read()
except FileNotFoundError:
    print("Fichier de playlist cible non trouvé.")
    exit()

# Mettre à jour les liens des chaînes spécifiques
for chaine, new_url in nouveaux_liens.items():
    playlist_cible = re.sub(rf'(#EXTINF.*?,{chaine}\n)https?://[^\s]+', rf'\1{new_url}', playlist_cible)

# Écrire la playlist mise à jour
with open(FICHIER_CIBLE, "w", encoding="utf-8") as file:
    file.write(playlist_cible)

print("Mise à jour terminée avec succès !")

# Commit et push automatique
os.system("git config --global user.name 'GitHub Actions'")
os.system("git config --global user.email 'actions@github.com'")
os.system("git add geral.m3u")
os.system("git commit -m 'Mise à jour automatique des chaînes spécifiques' || exit 0")
os.system("git push")

