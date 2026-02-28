from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementNotInteractableException


def main():
    listings_website = "https://appbrewery.github.io/Zillow-Clone/"
    doc_form = "https://forms.gle/1citmvY9cnR2bwxR8"

    header = {
        "Accept-Language": "de-DE,de;q=0.9,en-DE;q=0.8,en-US;q=0.7,en;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }

    response = requests.get(listings_website, header)

    web_content = response.text

    soup = BeautifulSoup(web_content, "html.parser")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    prices_elements = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
    prices = [price.text for price in prices_elements]

    accurate_prices = []
    for item in prices:
        item = item.lstrip("$")
        num = ""
        for ch in item:
            if ch.isdigit() or ch == ",":
                num = num + ch 
            else:
                break
        accurate_prices.append("$" + num)

    print(len(accurate_prices))

    addresses_elements = soup.find_all("address")
    addresses = [address.text.strip() for address in addresses_elements]
    accurate_addresses = ["".join(item.split("|")) for item in addresses]
    print(len(accurate_addresses))

    all_links = soup.find_all("a", class_="property-card-link")
    house_links = [item.get("href") for item in all_links]
    print(len(house_links))


    for n in range(len(accurate_prices)):
        bot = driver.get(doc_form)
        
        address_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        address_input.send_keys(accurate_addresses[n])
            
        price_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        price_input.send_keys(accurate_prices[n])

        link_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        link_input.send_keys(house_links[n])

        send_button = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')))
        send_button.click()
        
        send_more_replies = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Weitere Antwort senden')]")))
        

if __name__ == "__main__":    
    main()