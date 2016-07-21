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



def find_charts(driver):
    """
    Hardcoded example with citydj.com
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
                (By.CLASS_NAME, 'djc-track-artist')
            )
        )
    root = driver.find_element_by_id('trends-charts')
    charts_by_genre = root.find_elements_by_xpath(
        "//*[contains(@id, '-container')]")
    return charts_by_genre


def parse_songs_by_genre(chart_genre):
    genre_id = chart_genre.get_attribute('id')
    genre = genre_id[:genre_id.find('-container')]
    tracks = chart_genre.find_element_by_id(genre).find_elements_by_xpath('./li')
    result = {
        genre: []
    }

    for track in tracks:
        t_title = track.find_element_by_class_name('djc-track-title').find_element_by_css_selector('a').text
        t_artist = track.find_element_by_class_name('djc-track-artist').find_element_by_css_selector('p').text
        result[genre].append(
            {
                'title': t_title,
                'artist': t_artist
            }
        )
    return result


def compile_chart(url):
    compiled = {}
    try:
        driver = Driver(url)
        driver.setup_driver()
        driver.get_source()
        charts = find_charts(driver.driver)
        for c_genre in charts:
            compiled.update(parse_songs_by_genre(c_genre))
    finally:
        driver.driver.quit()
    return compiled


def main():
    print(compile_chart("http://www.djcity.com/charts/"))


if __name__ == '__main__':
    sys.exit(main())

