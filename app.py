import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
main_url = "https://packaging.python.org/en/latest/guides/section-install/"
driver.get(main_url)
time.sleep(5)
links = driver.find_elements(By.XPATH, '//section[@id="installation"]//ul/li/a')
all_data = []

for link in links:
    url = link.get_attribute('href')
    print("Scraping:", url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headings, subheadings, codes = [], [], []
        all_headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in all_headings:
            level = int(heading.name[1]) if heading.name.startswith('h') else None
            if level == 1:
                headings.append(heading.text.strip())
            elif level == 2:
                subheadings.append(heading.text.strip())
        code_snippets = soup.select('.tab-content.docutils.container .highlight-bash.notranslate .highlight pre, .tab-content.docutils.container .highlight-text.notranslate .highlight pre')
        for code_snippet in code_snippets:
            codes.append(code_snippet.text.strip())
        max_length = max(len(headings), len(subheadings), len(codes))
        headings.extend([''] * (max_length - len(headings)))
        subheadings.extend([''] * (max_length - len(subheadings)))
        codes.extend([''] * (max_length - len(codes)))
        page_data = [{'Heading': h, 'Subheading': s, 'Code': c} for h, s, c in zip(headings, subheadings, codes)]
        all_data.extend(page_data)
    else:
        print("Failed to fetch URL:", url)

df = pd.DataFrame(all_data)
df.to_csv('scraped_data_all_urls27.csv', index=False)
print("Data saved to 'scraped_data_all_urls.csv'")
driver.quit()
