#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

M6_PAGE_URL="https://www.stream4free.tv/m6-live-streaming"

# Récupérer le code source avec curl
PAGE_SOURCE=$(curl -s "$M6_PAGE_URL")

# Extraire l'URL complète contenant le token
NEW_M6_URL=$(echo "$PAGE_SOURCE" | grep -oP 'https://https://sv1.data-stream.top/[^/]+/[^/]+/hls/m6france.m3u8' | head -n 1)

# Vérifier si l'URL a été trouvée
if [[ -z "$NEW_M6_URL" ]]; then
    echo "Erreur : Impossible de récupérer l'URL contenant le token."
    exit 1
fi

# Mettre à jour uniquement l'URL du flux M6 dans geral.m3u
sed -i "/m6france.m3u8/c\\$NEW_M6_URL" "$M3U_FILE"

echo "Mise à jour du lien M6 terminée."
