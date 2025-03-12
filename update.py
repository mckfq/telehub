from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# 🖥 URL de la page à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛠️ Configurer Selenium avec Chrome en mode headless
options = Options()
options.add_argument("--headless")  # Mode sans affichage graphique
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 🔽 Charger la page avec Selenium
    driver.get(url_page)
    time.sleep(10)  # Attendre que le JS charge la page

    # 📜 Récupérer tout le code source de la page
    page_source = driver.page_source

    # 🔍 Trouver toutes les URLs M3U8 dans la page
    urls_m3u8 = re.findall(r"https?://[^\s\"']+\.m3u8", page_source)

    if urls_m3u8:
        print(f"✅ {len(urls_m3u8)} URL(s) M3U8 trouvée(s) :")
        for url in urls_m3u8:
            print(f"🔗 {url}")
        
        # Prendre la première URL trouvée (ou modifier selon ton besoin)
        nouvelle_url = urls_m3u8[0]
        
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
                    if 'tvg-name="M6"' in line:  # Modifier pour d'autres chaînes si besoin
                        update_next_line = True  # La ligne suivante contient l'URL à changer

        print(f"✅ M6 mis à jour avec la nouvelle URL dans {fichier_m3u} !")
    
    else:
        print("⚠️ Aucune URL M3U8 détectée dans la page.")

finally:
    driver.quit()  # Fermer Selenium proprement
