from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# 🖥 URL du site à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 🏷 Nom de la chaîne à modifier dans le fichier M3U
nom_chaine = "M6"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛠️ Configurer Selenium avec Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode sans affichage graphique
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 🔽 Charger la page avec Selenium
    driver.get(url_page)
    time.sleep(5)  # Attendre le chargement de JavaScript

    # 📜 Récupérer le code source de la page
    source_code = driver.page_source
    lines = source_code.split("\n")

    # 🔍 Vérifier si la ligne 766 existe
    if len(lines) >= 766:
        ligne_766 = lines[765].strip()
        print(f"✅ Ligne 766 trouvée : {ligne_766}")

        # 🔗 Extraire l'URL M3U8
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

finally:
    driver.quit()  # Fermer Selenium proprement
