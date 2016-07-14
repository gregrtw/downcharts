import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def Driver_get_source(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def find_charts(driver):
    """
    Hardcoded example with citydj.com
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
                (By.CLASS_NAME, 'djc-track-artist') | (By.CLASS_NAME, 'djc-track-title')
                | (By.ID, 'trends-charts')
            )
        )
    root = driver.find_element_by_id('trends-charts')
    charts_by_genre = root.find_elements_by_xpath(
        "//*[contains(@id, '-container')]")
    return charts_by_genre
def main():
    pass


if __name__ == '__main__':
    sys.exit(main())

