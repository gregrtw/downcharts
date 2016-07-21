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

    def _parse_songs_by_genre( self, chart_genre ):
        """
        Private helper function to compile_chart()
            FIXME: hardcoded values for www.djcity.com
        """
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
            self.count += 1
        return result

    def find_charts( self ):
        """
        FIXME: hardcoded values for www.djcity.com
        """
        d = self.driver.driver
        WebDriverWait( d, 10 ).until(
            EC.presence_of_element_located(
                    (By.CLASS_NAME, 'djc-track-artist')
                )
            )
        root = d.find_element_by_id('trends-charts')
        charts_by_genre = root.find_elements_by_xpath(
            "//*[contains(@id, '-container')]")
        return charts_by_genre  
  
    def compile_chart( self ):
        """
            FIXME: add exception handling
        """
        try:
            self.get_source()
            charts = self.find_charts()
            for c_genre in charts:
                self.results.update(self._parse_songs_by_genre(c_genre))
        finally:
            self.cleanup()

    def cleanup( self ):
        """
            FIXME: make quit handling by Driver and refactor into better named method
        """
        self.driver.driver.quit()

    def get_results( self ):
        return self.results

    def get_count( self ):
        return self.count


def main():


if __name__ == '__main__':
    sys.exit(main())

