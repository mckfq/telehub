#!/bin/bash

cd geral

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

M3U_FILE="geral.m3u"

# FR
SOURCE_M6="https://www.stream4free.tv/m6-live-streaming"
SOURCE_W9="https://www.stream4free.tv/w9-france"
SOURCE_TF1_SERIES="https://www.stream4free.tv/tf1-series-films"
SOURCE_6TER="https://www.stream4free.tv/6ter-france"

# Extract m3u
extract_m3u8() {
    curl -s "$1" | grep -oP 'https://.*?\.m3u8' | head -1
}

# New links
NEW_M6=$(extract_m3u8 "$SOURCE_M6")
NEW_W9=$(extract_m3u8 "$SOURCE_W9")
NEW_TF1_SERIES=$(extract_m3u8 "$SOURCE_TF1_SERIES")
NEW_6TER=$(extract_m3u8 "$SOURCE_6TER")

# Check if no void
if [[ -z "$NEW_M6" || -z "$NEW_W9" || -z "$NEW_TF1_SERIES" || -z "$NEW_6TER" ]]; then
    echo "Erreur : Impossible d'extraire un ou plusieurs flux M3U8"
    exit 1
fi

# Update
sed -i "/M6/{n;s|https.*m3u8|$NEW_M6|}" "$M3U_FILE"
sed -i "/W9/{n;s|https.*m3u8|$NEW_W9|}" "$M3U_FILE"
sed -i "/TF1 Séries Films/{n;s|https.*m3u8|$NEW_TF1_SERIES|}" "$M3U_FILE"
sed -i "/6ter/{n;s|https.*m3u8|$NEW_6TER|}" "$M3U_FILE"
