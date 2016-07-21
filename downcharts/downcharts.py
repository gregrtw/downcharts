import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Driver:

    def __init__(self, driver='Chrome'):
        self.driver_string = driver

    def __str__(self):
        return self.driver_string + " Driver"

    def setup_driver(self):
        if self.driver_string == 'Chrome':
            self.driver = webdriver.Chrome()
        if self.driver_string == 'Firefox':
            self.driver = webdriver.Firefox()
        # TODO: Add other driver types (IE, generic, etc.)

    def get_source(self, url):
        self.driver.get(url)


class Website:

    def __init__( self, url ):
        self.url = url
        self.driver = Driver()
        self.driver.setup_driver()  # could add a driver_string to Driver()
                                    # instance to modify the default Chrome driver
        self.results = {}  # resulting categories and tracks go here.
        self.count = 0  # number of tracks on charts in website

    def __str__( self ):
        return ' : '.join([str(self.driver), self.url, '(' + str(self.count) + ') tracks'])

    def get_source( self ):
        self.driver.get_source(self.url)

            )


def main():


if __name__ == '__main__':
    sys.exit(main())

