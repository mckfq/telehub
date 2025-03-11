#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# URL de M6 avec le token qui change périodiquement
BASE_URL="https://sv1.data-stream.top/"

# Fonction pour récupérer le token de l'URL dynamique
get_token() {
  # Cette commande est spécifique pour extraire un token
  # À adapter si le token est disponible dans une réponse API ou si le token peut être extrait d'une page HTML
  TOKEN=$(wget -qO- "https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/hls/m6france.m3u8" | grep -oP '(?<=href=")[a-f0-9]{64}(?=")' | head -n 1)

  if [ -z "$TOKEN" ]; then
    echo "Erreur : Impossible de récupérer le token."
    exit 1
  fi

  echo "$TOKEN"
}

# Récupérer le token
TOKEN_M6=$(get_token)

# Si le token a été récupéré avec succès, on met à jour l'URL dans le fichier M3U
if [ -n "$TOKEN_M6" ]; then
  # Remplacer l'ancienne URL de M6 par la nouvelle avec le token mis à jour
  sed -i "/m6france.m3u/ c https://sv1.data-stream.top/$TOKEN_M6/hls/m6france.m3u8" "$M3U_FILE"
  echo "Le token de M6 a été mis à jour dans le fichier M3U."
else
  echo "Le token n'a pas été mis à jour."
fi
