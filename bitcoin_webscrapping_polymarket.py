from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar el driver de Chrome
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome()


crypto='bitcoin'
# Abrir la página de Polymarket
driver.get("https://polymarket.com/markets/all?_q="+crypto)

# Esperar a que la página cargue completamente
time.sleep(5)  # Se puede mejorar usando WebDriverWait

# Obtener todos los enlaces de apuestas
elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/event/')]")

# Extraer y mostrar los enlaces
links = [element.get_attribute("href") for element in elements if element.get_attribute("href")]

import re

# Lista para almacenar enlaces únicos
clean_links = []
seen_events = set()

for link in links:
    # Extraer solo la parte clave después de "/event/" y antes del siguiente "/"
    match = re.search(r'/event/([^/]+)', link)
    if match:
        event_key = match.group(1)  # Obtener la parte clave del evento

        # Si no hemos agregado este evento antes, lo guardamos
        if event_key not in seen_events:
            seen_events.add(event_key)
            clean_links.append(link)  # Guardamos solo la versión más corta del enlace

used_links = set()

for link in links:
    
    match = re.search(r'/event/([^/]+)', link)
    if match.group(1) in used_links or 'comments' in link:
        continue
    else:
        print(match.group(1))
        used_links.add(match.group(1))
        # Configuración del driver (Asegúrate de tener instalado el driver correspondiente a tu navegador)
        driver = webdriver.Chrome()
        driver.get(link)
        # Ruta del ChromeDriver (ajustar si es necesario)

        #service = Service("chromedriver-win64/chromedriver.exe")
        #driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Paso 1: Abrir el pop-up de descarga
        popup_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'c-fEYZoB')]")))
        popup_button.click()

        time.sleep(2)  # Pequeña pausa para asegurar que el pop-up se abra

        # Paso 2: Seleccionar el timeframe (cambiar de 'daily' a 'hourly')
        timeframe_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@role, 'combobox')]")))
        timeframe_button.click()

        # Seleccionar la opción 'hourly'
        hourly_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'hourly')]")))
        hourly_option.click()
        #import pdb;pdb.set_trace()
        try:
            # Esperar hasta que el div contenedor del botón sea visible
            select_all_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[label[contains(text(), 'Select all')]]")))

            # Buscar el botón dentro del div correcto
            select_all_button = select_all_container.find_element(By.XPATH, ".//button[@role='checkbox']")

            # Hacer scroll hasta el botón
            driver.execute_script("arguments[0].scrollIntoView();", select_all_button)
            time.sleep(1)

            # Hacer clic en el botón
            select_all_button.click()
        except:
            pass  # Si no está presente, continuar sin error


        
        # Paso 3: Hacer clic en el botón de descarga
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download (.csv)')]")))
        download_button.click()

        # Esperar unos segundos para la descarga
        time.sleep(4)

        

        print("Descarga completada.")

# Cerrar el navegador
driver.quit()