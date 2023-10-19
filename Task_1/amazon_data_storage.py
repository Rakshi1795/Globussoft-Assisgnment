import csv
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def amazon_input(prod_val: str):
    prod_name = prod_val
    driver = webdriver.Chrome()
    web_link = "https://www.amazon.in/"
    driver.get(web_link)
    try:
        search_val = driver.find_element(By.ID, "twotabsearchtextbox")
        search_val.send_keys(prod_val)
        search_btn = driver.find_element(By.ID, "nav-search-submit-button")
        search_btn.click()
    except Exception as e:
        search_val = driver.find_element(By.ID, "nav-bb-search")
        search_val.send_keys(prod_val)
        search_btn = driver.find_element(By.CLASS_NAME, "nav-bb-button")
        search_btn.click()

    product_nav = driver.find_element(By.XPATH, "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
    product_nav.click()
    time.sleep(3)
    product_source = driver.page_source
    soup = BeautifulSoup(product_source, 'html.parser')

    product_price = soup.find("span", class_="a-price-whole")
    product_price_symbol = soup.find('span', class_="a-price-symbol")
    star_rating = soup.find('span', class_="a-icon-alt").text
    product_img_link = soup.find('img', class_='s-image')
    product_img_src = product_img_link.get('src')
    try:
        product_description = soup.find(class_='a-size-medium a-color-base a-text-normal').get_text()
    except Exception as e:
        product_description = soup.find(class_='a-size-large product-title-word-break').get_text()
    product_global_ratings = soup.find(class_="a-size-base s-underline-text").get_text()

    product_star_rating = re.match(r"([\d.]+)", star_rating).group(1)

    amazon_result = {
        "product_description": product_description,
        "product_price": str(product_price_symbol.text) + str(product_price.text.strip()),
        "product_star_ratings": product_star_rating,
        "product_global_ratings": product_global_ratings,
        "product_img_src": product_img_src
    }

    # Store the data in a CSV file
    save_to_csv(amazon_result)

    driver.quit()
    return amazon_result

def save_to_csv(data):
    csv_filename = "amazon_data.csv"

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["product_description", "product_price", "product_star_ratings", "product_global_ratings", "product_img_src"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the CSV file is empty and write header if needed
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

if __name__ == "__main__":
    result = amazon_input("Realme_11_pro")   #Replace the name here
    print(result)