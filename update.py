from seleniumwire import webdriver  # Remplace selenium par selenium-wire
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# 🖥 URL de la page à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛠️ Configurer Selenium avec Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-data-dir=/tmp/selenium")  # ✅ Correction de l'erreur
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")  # Éviter détection anti-bot
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Démarrer le navigateur
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def mettre_a_jour_m3u(nouvelle_url):
    if not os.path.exists(fichier_m3u):
        print(f"❌ Fichier {fichier_m3u} introuvable !")
        return
    
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
                if 'tvg-id="M6.fr"' in line:  # Modifier si besoin selon geral.m3u
                    update_next_line = True  # La ligne suivante contient l’URL à changer

try:
    driver.get(url_page)
    time.sleep(10)  # Laisser le JS charger

    # 📡 Vérifier les requêtes réseau
    urls_m3u8 = {req.url for req in driver.requests if req.response and ".m3u8" in req.url}

    if urls_m3u8:
        print(f"✅ {len(urls_m3u8)} URL(s) M3U8 trouvée(s) :")
        for url in urls_m3u8:
            print(f"🔗 {url}")
        
        nouvelle_url = list(urls_m3u8)[0]
        mettre_a_jour_m3u(nouvelle_url)
        print(f"✅ M6 mis à jour avec la nouvelle URL dans {fichier_m3u} !")
    else:
        print("⚠️ Aucune URL détectée.")

finally:
    driver.quit()  # Fermer proprement Selenium
