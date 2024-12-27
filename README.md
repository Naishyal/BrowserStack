Below is the screenshot of logs that I have printed for the functionallity i have developed, 
![Screenshot 2024-12-28 021934](https://github.com/user-attachments/assets/4ebb4d4d-6894-4448-bb09-2fc94e62aac4)
![Screenshot 2024-12-28 022035](https://github.com/user-attachments/assets/e7d56d39-61cc-4993-bc22-0ac0883184e2)
![Screenshot 2024-12-28 022054](https://github.com/user-attachments/assets/41aff31f-fa64-4529-9387-259345eebf6c)
![Screenshot 2024-12-28 022115](https://github.com/user-attachments/assets/d48a026f-4ad4-4e57-a904-c14e9b7b11f2)


And below is the code for the same, which was the version just before integrating BrowserStack,

import os import requests from selenium import webdriver from selenium.webdriver.chrome.service import Service from selenium.webdriver.common.by import By from selenium.webdriver.support.ui import WebDriverWait from selenium.webdriver.support import expected_conditions as EC import time from googletrans import Translator from collections import Counter import re # Importing the regex module

DRIVER_PATH = r"C:\Users\naish\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

service = Service(DRIVER_PATH)

driver = webdriver.Chrome(service=service)

translator = Translator()

driver.get("https://elpais.com/")

time.sleep(5)

try: opinion_section = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.LINK_TEXT, "Opinión")) ) opinion_section.click() print("Navigated to the Opinión section.") time.sleep(5) # Wait for the page to load except Exception as e: print(f"Error navigating to the Opinión section: {e}")

translated_titles = [] # List to store translated titles try: articles = driver.find_elements(By.XPATH, "//article")[:5] print(f"Found {len(articles)} articles to scrape.")

for idx, article in enumerate(articles, start=1):
    try:
        title = article.find_element(By.XPATH, ".//h2").text
        print(f"Title of article {idx}: {title}")
        
        translated_title = translator.translate(title, src='es', dest='en').text
        print(f"Translated title of article {idx}: {translated_title}")
        
        translated_titles.append(translated_title)
        
        content = article.find_element(By.XPATH, ".//p[contains(@class, 'c_d')]").text
        print(f"Content of article {idx}: {content[:150]}...")  # Print the first 150 characters of content
        
        translated_content = translator.translate(content, src='es', dest='en').text
        print(f"Translated content of article {idx}: {translated_content[:150]}...")
        
        img = article.find_element(By.XPATH, ".//img")
        img_url = img.get_attribute("src")
        print(f"Cover image URL of article {idx}: {img_url}")
        
        if img_url:
            image_name = f"article_{idx}_cover.jpg"
            image_path = os.path.join("images", image_name)
            os.makedirs("images", exist_ok=True)
            with open(image_path, "wb") as f:
                img_data = requests.get(img_url).content
                f.write(img_data)
            print(f"Image downloaded: {image_name}")
    except Exception as e:
        print(f"Error processing article {idx}: {e}")
except Exception as e: print(f"Error scraping articles: {e}")

all_words = []

for title in translated_titles: words = re.findall(r'\b\w+\b', title.lower()) # \b\w+\b matches words only all_words.extend(words)

word_counts = Counter(all_words)

repeated_words = {word: count for word, count in word_counts.items() if count > 2}

if repeated_words: print("\nRepeated words with counts:") for word, count in repeated_words.items(): print(f"{word}: {count}") else: print("\nNo words repeated more than twice.")

input("Press Enter to close the browser...")

driver.quit()
