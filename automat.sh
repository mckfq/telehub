#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

M6_URL="https://www.stream4free.tv/m6-live-streaming"

# Récupérer le token depuis la source de la page
TOKEN=$(wget -qO- "$M6_URL" | grep -oP 'hls/m6france.m3u8\?token=[^"]+' | head -n 1)

# Vérifier si le token a été trouvé
if [[ -z "$TOKEN" ]]; then
    echo "Erreur : Impossible de récupérer le token."
    exit 1
fi

# Construire la nouvelle URL du flux M6
NEW_M6_URL="https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/$TOKEN"

# Mettre à jour uniquement l'URL du flux M6 sans toucher aux autres lignes
sed -i "/m6france.m3u8/c\\$NEW_M6_URL" "$M3U_FILE"

echo "Mise à jour du lien M6 terminée."

