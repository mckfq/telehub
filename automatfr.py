import os
import time
import re
import json
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

# 🎯 Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🖥 URL de la page à analyser
url_page = "https://www.stream4free.tv/m6-live-streaming"

# 📄 Fichier M3U à modifier
fichier_m3u = "geral.m3u"

# 🛠️ Configurer Selenium avec Chrome en mode headless et capture réseau
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Activation des logs réseau

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    logging.info("✅ Selenium lancé avec succès.")
except Exception as e:
    logging.error(f"❌ Erreur lors du lancement de Selenium : {e}")
    exit(1)

try:
    # Charger la page
    driver.get(url_page)
    logging.info("🌍 Chargement de la page...")
    
    # Attendre que le contenu JS soit chargé
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    logging.info("✅ Page chargée avec succès.")
    
    # 🖱️ Simuler une interaction (scroll & clic sur un éventuel player vidéo)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Pause pour laisser les éléments se charger

    try:
        video_player = driver.find_element(By.TAG_NAME, "video")
        ActionChains(driver).move_to_element(video_player).click().perform()
        logging.info("🎬 Interaction avec le player vidéo.")
        time.sleep(3)  # Laisser le temps à l'URL de charger après le clic
    except Exception:
        logging.warning("⚠️ Aucun player vidéo détecté.")

    # 🕵️ Extraire les logs réseau pour trouver l'URL M3U8
    def extract_m3u8_from_logs(driver):
        logs = driver.get_log("performance")
        for log in logs:
            try:
                log_data = json.loads(log["message"])["message"]
                if log_data["method"] == "Network.responseReceived":
                    url = log_data["params"]["response"]["url"]
                    if ".m3u8" in url:
                        return url
            except (KeyError, json.JSONDecodeError):
                continue
        return None

    # 🔍 Récupérer la vraie URL M3U8
    nouvelle_url = extract_m3u8_from_logs(driver)
    
    if nouvelle_url:
        logging.info(f"✅ URL M3U8 détectée : {nouvelle_url}")

        # Vérifier si l'URL est accessible
        try:
            response = requests.get(nouvelle_url, timeout=5)
            if response.status_code != 200:
                logging.warning(f"⚠️ L'URL M3U8 semble invalide (HTTP {response.status_code}) : {nouvelle_url}")
                exit(1)
        except requests.RequestException:
            logging.error(f"❌ Impossible d'accéder à l'URL M3U8 : {nouvelle_url}")
            exit(1)

        # Vérifier si le fichier M3U existe
        if not os.path.exists(fichier_m3u):
            logging.error(f"❌ Fichier {fichier_m3u} introuvable !")
            exit(1)

        # 🔄 Mettre à jour uniquement les lignes des URLs
        with open(fichier_m3u, "r") as file:
            lines = file.readlines()

        with open(fichier_m3u, "w") as file:
            update_next_line = False
            for line in lines:
                if update_next_line and line.startswith("http"):
                    logging.info(f"🔄 Mise à jour de l'URL : {line.strip()} → {nouvelle_url}")
                    file.write(nouvelle_url + "\n")
                    update_next_line = False
                else:
                    file.write(line)
                    if 'tvg-name="M6"' in line:
                        update_next_line = True  # La ligne suivante contient l’URL à changer

        logging.info(f"✅ M6 mis à jour avec la nouvelle URL dans {fichier_m3u} !")
    else:
        logging.warning("⚠️ Aucune URL M3U8 détectée dans les logs réseau.")

finally:
    driver.quit()
    logging.info("🛑 Selenium fermé proprement.")
