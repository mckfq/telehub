#!/bin/bash

cd geral

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

#FR M6
M3U_FILE="geral.m3u"

# URL source contenant le flux à extraire
SOURCE_URL="https://www.stream4free.tv/m6-live-streaming"

# Extraire l'URL du flux M3U8 (adapte selon la structure HTML)
NEW_STREAM=$(curl -s "$SOURCE_URL" | grep -oP 'https://.*?\.m3u8' | sed -n '766p')

# Vérifier si l'extraction a fonctionné
if [[ -z "$NEW_STREAM" ]]; then
    echo "Erreur : Impossible d'extraire le flux M3U8"
    exit 1
fi

# Remplacer l'ancien lien dans le fichier M3U
sed -i "/M6/c #EXTINF:-1,M6\n$NEW_STREAM" "$M3U_FILE"

echo "Mise à jour du flux M6 réussie : $NEW_STREAM"
