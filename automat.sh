#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
#sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
#sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# FR M6
# URL du site
URL="https://www.stream4free.tv/m6-live-streaming"

# Fichier de cookies temporaire
COOKIE_FILE="cookies.txt"

# Effectuer la requête HTTP avec curl en enregistrant les cookies dans un fichier
curl -s -c $COOKIE_FILE $URL -o page.html

sed -i "/m6france.m3u8/ c https://sv1.data-stream.top/$(wget -qO- $COOKIE_FILE $URL | grep -oP 'https://sv1\.data-stream\.top/\K([^/]+)(?=/hls/m6france\.m3u8)' | head -n 1)/hls/m6france.m3u8/" geral.m3u
