from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import time

def get_page_source_code(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Ge cko) Chrome/57.0.2987.133 Safari/537.36'}
    #ua = UserAgent()
    resp = requests.get(url, headers=headers)
    soup = BS(resp.content, "html.parser")
    return soup


def read_excel_files():

    df = pd.read_csv("DVTDeedExport_07312019_114441_TX.csv")
    address = df["Address"]
    # cities = df['City']
    states = df['State']
    return address, states
    # zip_codes = [str(zip_code)[:5] for zip_code in df['Zip Code']]
    # print(address)

    # for addr, city, state, zip_code in zip(address, cities, states, zip_codes):
    #     full_address = f"{addr}_{city}_{state}_{zip_code}_M29676-26371"
    #     url = f"https://www.realtor.com/realestateandhomes-detail/{full_address}"
    #     print(url)
    #     soup = get_page_source_code(url)
    #     print(soup.select(".key-fact-data.ellipsis")[-1])
    #     print(soup.select(".summary-datapoint"))
    

def get_data():            
    df = pd.read_csv("DVTDeedExport_07312019_114441_TX.csv")
    addresses = df["Address"]
    # cities = df['City']
    states = df['State']
    # addresses, states = read_excel_files()

    prices = []
    years_built = []
    descriptions = []
    
    for address, state in zip(addresses, states):
        base_url = "https://www.redfin.com/"
        driver.get(base_url)

        search_input_field = driver.find_element_by_xpath(
            '//*[@id="search-box-input"]')
        search_input_field.clear()
        # search_input_field.send_keys("21729 NE COUCH CT")
        search_input_field.send_keys(f"{address} {state}")
        time.sleep(5)
        search_btn = driver.find_element_by_xpath(
            '//*[@id="tabContentId0"]/div/div/form/div[1]/button')
        print(search_btn)
        search_btn.click()
        time.sleep(5)
        try:

            year_built = driver.find_element_by_xpath(
                '//*[@id="overview-scroll"]/div/div/div[2]/div[2]/div/div/span[2]/span[2]')
            description = driver.find_element_by_xpath(
                '//*[@id="marketing-remarks-scroll"]/p/span')
            price = driver.find_element_by_xpath(
                '//*[@id="redfin-estimate"]/div/div[3]/div[1]')

            prices.append(price.text)
            descriptions.append(description.text)
            years_built.append(year_built.text)
            print(description.text)
            print()
            print(year_built.text)
            print(price.text)
            print()

        except Exception as e:
            prices.append("Not found")
            descriptions.append("Not found")
            years_built.append("Not found")
            print(e)
            #input("Enter to quit: ")

    df["Price"] = prices
    df["Descriptions"] = descriptions
    df["Year_built"] = years_built

    df.to_csv("DVTDeedExport_07312019_114441_TX_New.csv")
    driver.quit()


get_data()
