#!/bin/bash

M3U_FILE="geral.m3u"

# PT TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# PT CNN
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" geral.m3u

# FR M6 Récupérer le contenu de la page
PAGE_CONTENT=$(curl -s "https://www.stream4free.tv/m6-live-streaming")
# Extraire l'URL dynamique de la page
DYNAMIC_URL=$(echo "$PAGE_CONTENT" | grep -oP 'https://sv1.data-stream.top/[^"]+/hls/m6france.m3u8')
# Remplacer uniquement la ligne qui contient "w9france" dans le fichier M3U
sed -i "/m6france/c $DYNAMIC_URL" geral.m3u

# FR W9 Récupérer le contenu de la page
PAGE_CONTENT=$(curl -s "https://www.stream4free.tv/mw9-france)
# Extraire l'URL dynamique de la page
DYNAMIC_URL=$(echo "$PAGE_CONTENT" | grep -oP 'https://sv7.data-stream.top/[^"]+/hls/w9france.m3u8')
# Remplacer uniquement la ligne qui contient "w9france" dans le fichier M3U
sed -i "/w6france/c $DYNAMIC_URL" geral.m3u

# FR 6Ter Récupérer le contenu de la page
PAGE_CONTENT=$(curl -s "https://www.stream4free.tv/6ter-france")
# Extraire l'URL dynamique de la page
DYNAMIC_URL=$(echo "$PAGE_CONTENT" | grep -oP 'https://sv1.data-stream.top/[^"]+/hls/6ter.m3u8')
# Remplacer uniquement la ligne qui contient "w9france" dans le fichier M3U
sed -i "/6ter.m3u/c $DYNAMIC_URL" geral.m3u

# FR TF1SF Récupérer le contenu de la page
PAGE_CONTENT=$(curl -s "https://www.stream4free.tv/tf1-series-films")
# Extraire l'URL dynamique de la page
DYNAMIC_URL=$(echo "$PAGE_CONTENT" | grep -oP 'https://sv1.data-stream.top/[^"]+/hls/seriefilmes.m3u8')
# Remplacer uniquement la ligne qui contient "w9france" dans le fichier M3U
sed -i "/seriefilmes/c $DYNAMIC_URL" geral.m3u
