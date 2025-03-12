#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# Étape 1 : Extraire l'URL M3U pour M6
M6_URL=$(curl -s https://www.stream4free.tv/m6-live-streaming | grep -oP 'https://.*?\.m3u8' | head -n 1)

if [ -n "$M6_URL" ]; then
    # Mettre à jour ou ajouter l'entrée M6 dans le fichier M3U
    sed -i "/m6france/ c $M6_URL" "$M3U_FILE"
    echo "M6 URL mis à jour : $M6_URL"
else
    echo "Erreur : Impossible de récupérer l'URL M6."


