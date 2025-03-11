#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# FR

# Sources des flux M3U
SOURCE_M6="https://www.stream4free.tv/m6-live-streaming"
SOURCE_W9="https://www.stream4free.tv/w9-france"
SOURCE_TF1_SERIES="https://www.stream4free.tv/tf1-series-films"
SOURCE_6TER="https://www.stream4free.tv/6ter-france"

# Fonction pour récupérer l'URL M3U pour chaque chaîne
get_m3u_url() {
  local source=$1
  # Utilise wget pour récupérer le code source de la page
  PAGE=$(wget -qO- "$source")

  # Extraction de l'URL M3U à partir de la page (on évite l'option -P)
  echo "$PAGE" | sed -n 's/.*\(https:\/\/[^"]*\.m3u8\).*/\1/p' | head -n 1
}

# Mise à jour du flux M6
M6_URL=$(get_m3u_url "$SOURCE_M6")
if [[ -n "$M6_URL" ]]; then
  echo "Mise à jour du flux M6 : $M6_URL"
  sed -i "/M6/ c # M6 - $M6_URL" "$M3U_FILE"
else
  echo "Erreur : Impossible de récupérer l'URL M3U de M6"
fi

# Mise à jour du flux W9
W9_URL=$(get_m3u_url "$SOURCE_W9")
if [[ -n "$W9_URL" ]]; then
  echo "Mise à jour du flux W9 : $W9_URL"
  sed -i "/W9/ c # W9 - $W9_URL" "$M3U_FILE"
else
  echo "Erreur : Impossible de récupérer l'URL M3U de W9"
fi

# Mise à jour du flux TF1 Séries Films
TF1_SERIES_URL=$(get_m3u_url "$SOURCE_TF1_SERIES")
if [[ -n "$TF1_SERIES_URL" ]]; then
  echo "Mise à jour du flux TF1 Séries Films : $TF1_SERIES_URL"
  sed -i "/TF1 Séries Films/ c # TF1 Séries Films - $TF1_SERIES_URL" "$M3U_FILE"
else
  echo "Erreur : Impossible de récupérer l'URL M3U de TF1 Séries Films"
fi

# Mise à jour du flux 6Ter
TER_URL=$(get_m3u_url "$SOURCE_6TER")
if [[ -n "$TER_URL" ]]; then
  echo "Mise à jour du flux 6Ter : $TER_URL"
  sed -i "/6Ter/ c # 6Ter - $TER_URL" "$M3U_FILE"
else
  echo "Erreur : Impossible de récupérer l'URL M3U de 6Ter"
fi
