import requests
import re

# 📌 URL de la page Stream4Free
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 📌 Headers pour éviter d’être bloqué par le site
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, comme Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Referer": "https://www.stream4free.tv/",
    "Cache-Control": "no-cache",
}

# 🔽 Récupérer le code source de la page
response = requests.get(url_page, headers=headers)

# 🔍 Extraire les URLs M3U8
urls_m3u8 = re.findall(r"https?://[^\s\"']+\.m3u8", response.text)

# ✅ Vérifier si une URL a été trouvée
if urls_m3u8:
    nouvelle_url = urls_m3u8[0]
    print(f"✅ Nouvelle URL M3U8 trouvée : {nouvelle_url}")

    # 🔽 Lire le fichier M3U
    with open(fichier_m3u, "r") as file:
        lines = file.readlines()

    # 🔄 Mettre à jour uniquement l'URL de la chaîne avec tvg-id="M6.fr"
    with open(fichier_m3u, "w") as file:
        update_next_line = False
        for line in lines:
            if update_next_line and line.startswith("http"):
                print(f"🔄 Mise à jour de l'URL : {line.strip()} → {nouvelle_url}")
                file.write(nouvelle_url + "\n")  # Remplace uniquement l'URL
                update_next_line = False
            else:
                file.write(line)
                if 'tvg-id="M6.fr"' in line:  # Cherche la ligne avec M6
                    update_next_line = True  # La ligne suivante contient l’URL à changer

    print(f"✅ M6 mis à jour dans {fichier_m3u} avec la nouvelle URL !")

else:
    print("⚠️ Aucune URL M3U8 trouvée.")
