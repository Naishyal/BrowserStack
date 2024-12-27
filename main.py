import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack.local import Local
from googletrans import Translator
import time
from collections import Counter
import re

BROWSERSTACK_USERNAME = 'naishyalpatel_6nDdvC'
BROWSERSTACK_ACCESS_KEY = 'xEaXzBopJNyxpJEgwYFz'

local = Local()
local_args = { "key": "xEaXzBopJNyxpJEgwYFz" }
local.start(**local_args)

browsers = [
    {"os": "Windows", "os_version": "10", "browser": "chrome", "browser_version": "latest", "name": "Desktop Chrome"},
    {"os": "Windows", "os_version": "10", "browser": "firefox", "browser_version": "latest", "name": "Desktop Firefox"},
    {"os": "OS X", "os_version": "Big Sur", "browser": "safari", "browser_version": "latest", "name": "Desktop Safari"},
    {"os": "Android", "os_version": "10.0", "browser": "android", "browser_version": "latest", "name": "Mobile Chrome"},
    {"os": "iOS", "os_version": "14", "browser": "iphone", "browser_version": "latest", "name": "Mobile Safari"}
]

translator = Translator()

def run_browserstack_test(capabilities):
    driver = webdriver.Remote(
        command_executor=f'https://naishyalpatel_6nDdvC:xEaXzBopJNyxpJEgwYFz@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=capabilities
    )
    
    try:
        driver.get("https://elpais.com/")
        time.sleep(5)

        try:
            opinion_section = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Opinión"))
            )
            opinion_section.click()
            print(f"Navigated to the Opinión section on {capabilities['name']}")
            time.sleep(5)
        except Exception as e:
            print(f"Error navigating to the Opinión section on {capabilities['name']}: {e}")

        translated_titles = []  
        try:
            articles = driver.find_elements(By.XPATH, "//article")[:5]
            print(f"Found {len(articles)} articles to scrape on {capabilities['name']}.")
            
            for idx, article in enumerate(articles, start=1):
                try:
                    title = article.find_element(By.XPATH, ".//h2").text
                    print(f"Title of article {idx} on {capabilities['name']}: {title}")
                    
                    translated_title = translator.translate(title, src='es', dest='en').text
                    print(f"Translated title of article {idx} on {capabilities['name']}: {translated_title}")
                    translated_titles.append(translated_title)

                    content = article.find_element(By.XPATH, ".//p[contains(@class, 'c_d')]").text
                    print(f"Content of article {idx} on {capabilities['name']}: {content[:150]}...")
                    
                    translated_content = translator.translate(content, src='es', dest='en').text
                    print(f"Translated content of article {idx} on {capabilities['name']}: {translated_content[:150]}...")
                    
                    img = article.find_element(By.XPATH, ".//img")
                    img_url = img.get_attribute("src")
                    print(f"Cover image URL of article {idx} on {capabilities['name']}: {img_url}")
                    
                    if img_url:
                        image_name = f"article_{idx}_cover.jpg"
                        image_path = os.path.join("images", image_name)
                        os.makedirs("images", exist_ok=True)
                        with open(image_path, "wb") as f:
                            img_data = requests.get(img_url).content
                            f.write(img_data)
                        print(f"Image downloaded for article {idx} on {capabilities['name']}: {image_name}")
                except Exception as e:
                    print(f"Error processing article {idx} on {capabilities['name']}: {e}")
            
        except Exception as e:
            print(f"Error scraping articles on {capabilities['name']}: {e}")
        
    finally:
        driver.quit()

from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_browserstack_test, browsers)

local.stop()
