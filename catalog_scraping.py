from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = '/usr/bin/google-chrome' # Explicitly set Chrome binary location to google-chrome-stable

# Use Service object for Selenium 4+
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

for start in range(0, 12*32 , 12):
    url = f"https://www.shl.com/products/product-catalog/?start={start}&type=1"
    try:
        driver.get(url)
        # time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all("tr", attrs={"data-entity-id": True})

        for row in rows:
            title_cell = row.find("td", class_="custom__table-heading__title")
            link_tag = title_cell.find("a") if title_cell else None
            title = link_tag.get_text(strip=True) if link_tag else "N/A"
            href = "https://www.shl.com" + link_tag.get("href") if link_tag else "N/A"

            support_cells = row.find_all("td", class_="custom__table-heading__general")
            remote = "Yes" if len(support_cells) > 0 and support_cells[0].find("span", class_="catalogue__circle -yes") else "No"
            adaptive = "Yes" if len(support_cells) > 1 and support_cells[1].find("span", class_="catalogue__circle -yes") else "No"

            keys_cell = row.find("td", class_="custom__table-heading__general product-catalogue__keys")
            key_map = {
                "A": "Ability & Aptitude",
                "B": "Biodata & Situational Judgement",
                "C": "Competencies",
                "D": "Development & 360",
                "E": "Assessment Exercises",
                "K": "Knowledge & Skills",
                "P": "Personality & Behavior",
                "S": "Simulations"
            }

            keys = [k.get_text(strip=True) for k in keys_cell.find_all("span")] if keys_cell else []
            expanded_keys = [key_map.get(k, k) for k in keys]
            keys_str = ", ".join(expanded_keys)


            # Visit assessment detail page
            driver.get(href)
            # time.sleep(1)
            detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

            description = job_level = languages = time_required = "N/A"
            for block in detail_soup.select("div.product-catalogue-training-calendar__row"):
                heading = block.find("h4")
                content = block.find("p")
                if not heading or not content:
                    continue
                label = heading.get_text(strip=True)
                text = content.get_text(strip=True)

                if "Description" in label:
                    description = text
                elif "Job level" in label:
                    job_level = text
                elif "Languages" in label:
                    languages = text
                elif "Assessment length" in label and "minutes" in text:
                    match = re.search(r'(\d+)', text)
                    time_required = match.group(1) + " min" if match else "N/A"

            full_description = f"{description} | Job Levels: {job_level} | Languages: {languages}"

            data.append({
                "name": title,
                "url": href,
                "remote_support": remote,
                "adaptive_support": adaptive,
                "test_type": keys_str,
                "description": full_description,
                "duration": time_required
            })
            logging.info(f"Successfully scraped {href}") # Log after each detail page is scraped

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}") # Use logging.error for exceptions

# Close browser
driver.quit()

df = pd.DataFrame(data)
df.to_csv("shl_products_catalog.csv", index=False)