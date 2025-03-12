import requests
import re

# 🖥 URL du site à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 🏷 Nom de la chaîne à modifier dans le fichier M3U
nom_chaine = "M6"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛑 User-Agent pour éviter les blocages du site
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# 🔽 Télécharger la page HTML
response = requests.get(url_page, headers=headers)

if response.status_code == 200:
    # Diviser le code source en lignes
    lines = response.text.split("\n")

    # Vérifier que la ligne 766 existe
    if len(lines) >= 766:
        ligne_766 = lines[765].strip()  # Ligne 766 (index 765)
        print(f"✅ Ligne 766 trouvée : {ligne_766}")

        # 🔍 Extraire l'URL s'il y en a une
        match = re.search(r"https?://[^\s\"']+", ligne_766)
        if match:
            nouvelle_url = match.group(0)
            print(f"🔗 URL extraite : {nouvelle_url}")

            # 🔄 Mettre à jour le fichier M3U
            try:
                with open(fichier_m3u, "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                print(f"❌ Erreur : Le fichier {fichier_m3u} n'existe pas !")
                exit(1)

            with open(fichier_m3u, "w") as file:
                update_next_line = False
                for line in lines:
                    if update_next_line and line.startswith("http"):
                        file.write(nouvelle_url + "\n")  # Mettre la nouvelle URL
                        update_next_line = False
                    else:
                        file.write(line)
                        if f'tvg-name="{nom_chaine}"' in line:
                            update_next_line = True  # La ligne suivante contient l'URL à changer

            print(f"✅ {nom_chaine} mis à jour avec la nouvelle URL dans {fichier_m3u} !")
        else:
            print("⚠️ Aucune URL détectée dans la ligne 766.")
    else:
        print("⚠️ La page ne contient pas 766 lignes.")
else:
    print("⚠️ Erreur lors du téléchargement de la page.")
