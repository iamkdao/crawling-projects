from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.get('https://imdb.com')

try:
    search_box = driver.find_element(By.XPATH, "//label[@id='imdbHeader-navDrawerOpen']")
    search_box.click()
    search_box = driver.find_element(By.XPATH, "//span[contains(text(), 'Top Box Office')]")
    #use JavaScript's click() to click this button since Selenium's doesn't work
    driver.execute_script("arguments[0].click();", search_box)

    results = driver.find_elements(By.XPATH, "//div[@data-testid='chart-layout-main-column']//li[contains(@class, 'ipc')]")

    def yield_content(elements):
        for element in elements:
            yield {
                'Title' : element.find_element(By.XPATH, ".//h3[contains(@class, 'title')]").text,
                'Weekend Gross' : element.find_element(By.XPATH, ".//span[contains(text(), 'Weekend')]/following-sibling::span[1]").text,
                'Total Gross' : element.find_element(By.XPATH, ".//span[contains(text(), 'Total')]/following-sibling::span[1]").text,
                'Weeks Released' : element.find_element(By.XPATH, ".//span[contains(text(), 'Weeks')]/following-sibling::span[1]").text
            }

    # save it to a file
    with open("results.txt", "w", encoding="utf-8") as f:
        for result in yield_content(results):
            # text = result.find_element(By.XPATH, ".//h3[@class='ipc-title__text']").text # extract the number of results
            print(result)
            json.dump(result, f)
            f.write('\n')
except Exception as e:
    print(f"An error occurred: {e}")
