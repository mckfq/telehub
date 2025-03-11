#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# FR
# Récupérer le token dynamique
TOKEN=$(wget -qO- "https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/hls/m6france.m3u8" | grep -oP '(?<=token":")[^"]+')
# Mettre à jour l'URL de M6 avec le token
sed -i "/m6france/ c https://sv1.data-stream.top/$TOKEN/hls/m6france.m3u8" "$M3U_FILE"

# Exemple pour W9 (similaire à M6)
TOKEN_W9=$(wget -qO- "https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/hls/w9france.m3u8" | grep -oP '(?<=token":")[^"]+')
# Mettre à jour l'URL de W9 avec le token
sed -i "/w9france/ c https://sv1.data-stream.top/$TOKEN_W9/hls/w9france.m3u8" "$M3U_FILE"

# Exemple pour TF1 Séries Films
TOKEN_TF1=$(wget -qO- "https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/hls/tf1series.m3u8" | grep -oP '(?<=token":")[^"]+')
# Mettre à jour l'URL de TF1 Séries Films avec le token
sed -i "/seriesfilmes/ c https://sv1.data-stream.top/$TOKEN_TF1/hls/seriesfilmes.m3u8" "$M3U_FILE"

# Exemple pour 6Ter
TOKEN_6TER=$(wget -qO- "https://sv1.data-stream.top/a52fe0410da1ab301761aacd0eb9e9bb77f9295639f2d980f837343f5569aaa4/hls/6terfrance.m3u8" | grep -oP '(?<=token":")[^"]+')
# Mettre à jour l'URL de 6Ter avec le token
sed -i "/6ter/ c https://sv1.data-stream.top/$TOKEN_6TER/hls/6ter.m3u8" "$M3U_FILE"
