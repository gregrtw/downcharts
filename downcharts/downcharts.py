import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def Driver_get_source(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())

