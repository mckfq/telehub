from seleniumwire import webdriver  # Remplace selenium par selenium-wire
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# 🖥 URL de la page à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛠️ Configurer Selenium avec Chrome en mode headless
options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# 🚀 Lancer le navigateur avec selenium-wire pour intercepter les requêtes
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 🔽 Charger la page avec Selenium
    driver.get(url_page)
    time.sleep(10)  # Attendre que le JS charge la page

    # 📡 Scanner toutes les requêtes réseau du navigateur
    urls_m3u8 = []
    for request in driver.requests:
        if request.response and ".m3u8" in request.url:
            urls_m3u8.append(request.url)

    if urls_m3u8:
        nouvelle_url = urls_m3u8[0]  # Prendre la première URL M3U8 détectée
        print(f"✅ URL M3U8 trouvée : {nouvelle_url}")

        # 🔄 Mettre à jour uniquement les lignes des URLs dans geral.m3u
        with open(fichier_m3u, "r") as file:
            lines = file.readlines()

        with open(fichier_m3u, "w") as file:
            update_next_line = False
            for line in lines:
                if update_next_line and line.startswith("http"):
                    print(f"🔄 Mise à jour de l'URL : {line.strip()} → {nouvelle_url}")
                    file.write(nouvelle_url + "\n")
                    update_next_line = False
                else:
                    file.write(line)
                    if 'tvg-id="M6.fr"' in line:
                        update_next_line = True  

        print(f"✅ M6 mis à jour avec la nouvelle URL dans {fichier_m3u} !")
    
    else:
        print("⚠️ Aucune URL M3U8 détectée dans les requêtes réseau.")

finally:
    driver.quit()  # Fermer Selenium proprement
