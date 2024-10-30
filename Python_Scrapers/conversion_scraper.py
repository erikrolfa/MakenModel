from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def main():
    # Get the page

    with open('paint_conversion.output', 'w', encoding='utf-8') as output:
        with open('paint_conversion_links.txt', 'r', encoding='utf-8') as paint_links:
            for line in paint_links.readlines():
                base_url, product_code = line.rsplit('/', 1)
                product_code = product_code.strip()
                list_of_same = get_conversion_from_url(line)

                output.write(f'{product_code} : {list_of_same}\n')


def get_conversion_from_url(url):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.headless = True # Uncomment if you don't want the browser GUI to pop up
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    list_of_same = []

    # Explicit wait until the list items are loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "desktop-results-grid__item"))
    )

    time.sleep(1)  # Just a tiny buffer to ensure all items are loaded

    # Get the page source after JavaScript has executed
    html_content = driver.page_source
    driver.quit()

    # Now, you can parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    ul = soup.find('ul', {'class': 'desktop-results-grid__list'})

    if ul:
        li_items = ul.find_all('li', {'class': 'desktop-results-grid__item'})
        # Printing the titles/descriptions as an example
        for li in li_items:
            img_tag = li.find('img', {'class': 'desktop-results-grid__brand-logo'})
            brand = img_tag['alt']
            code = li.find('p', {'class': 'desktop-results-grid__code'})

            list_of_same.append((brand, code.text))

    return list_of_same


if __name__ == "__main__":
    main()