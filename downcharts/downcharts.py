"""TopMusicChart main module of the platform to acquire, prepare and deliver music charts."""
import sys
import configparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Driver(object):
    """Wrapper to selenium webdriver.

    Wraps all the required Driver functionalities required to scrape and prepare music charts.

    Attributes:
        driver_string: String representing which driver to instanciate from selenium's webdrivers.
        driver: Webdriver instance from Selenium.
    """

    def __init__(self, driver='Chrome'):
        """Constructor to the Driver class.

        Args:
            driver: Driver type (string). Defaults to 'Chrome'.
        """
        self.driver_string = driver

    def __str__(self):
        """Return a string representation of a Driver instance."""
        return self.driver_string + " Driver"

    def setup_driver(self):
        """Driver setup function.

        Used to setup the instance of a webdriver based on
            the passed driver type to the Constructor.
        """
        if self.driver_string == 'Chrome':
            self.driver = webdriver.Chrome()
        if self.driver_string == 'Firefox':
            self.driver = webdriver.Firefox()
        # TODO: Add other driver types (IE, generic, etc.)

    def get_source(self, url):
        """Getter for a source webpage.

        Args:
            url: Url (string) of the source we are requesting
        """
        self.driver.get(url)


class Website(object):
    """Class of a website hosting music charts rankings.

    The Website class is the handler for all functionalities related to a website and
        implements methods to scrape and compile music charts from a Website.

    Arguments:
        config_path: Path to the configuration options of a Website. (string)
        config: ConfigParser instance. (ConfigParser)
        url: URL of the website requested. (string)
        website: Website configuration id. (string)
            Must match a configuration id under 'config_path'
        driver: Driver instance used to request the website. (Driver)
        results: Results of a map between the genres and their top tracks. (dict)
        count: Number of tracks in the Website's charts. (int)
    """

    config_path = './website.ini'
    config = configparser.ConfigParser()

    def __init__(self, url, website_name):
        """Constructor for Website class.

        Args:
            url: The url for the requested website. (string)
            website_name: The identifier used in the configuration file
                to represent that website. (string)

        Raises:
            NoSectionError: An error happened reading a configuration file subsection. (.ini)
        """
        try:
            self.url = url
            self.config.read(self.config_path)
            # Testing if the website_name variable is a valid configuration id
            self.config.items(website_name)
            # Does not raise error? Then proceed.
            self.website = website_name
            self.driver = Driver()
            # NOTE: Could add a driver_string to Driver() instance to modify the default Chrome driver
            self.driver.setup_driver()
            self.results = {}
            self.count = 0
        except configparser.NoSectionError as e:
            print(str(e) + " in the Configuration File.\nSupply a valid website configuration id.")
            raise SystemExit

    def __str__(self):
        """Return a string representation of a Website instance."""
        return ' : '.join([str(self.driver), self.url, '(' + str(self.count) + ') tracks'])

    def get_source(self):
        """Wrapper around the Driver url Getter."""
        self.driver.get_source(self.url)

    def _parse_songs_by_genre(self, chart_genre):
        """Private helper function to compile_chart().

        Args:
            chart_genre: The root node for a genre in the webpage.
                This node is parent to all the nodes containing the information for top tracks,
                including title and artist information.

        Returns:
            A dict mapping genre name's with a list of dict objects containing
                a track's artist and title that represent the chart matching that genre.
            Ex:
                {
                    'house': [{'artist': 'ARTIST', 'title': 'TITLE'}, {}, {}, etc.],
                    'GENRE': [],
                    etc.
                }
            If a genre key is missing, then it was not on the website or
                did not use the same xpaths
        """
        # CONFIG: the element attribute that identifies the Genre
        #   (ex: the attribute to get 'house-container' in djcity)
        genre_id = chart_genre.get_attribute(
            self.config.get(self.website, 'parse_songs_genre_id')
        )
        # CONFIG: the part of the above Genre identifier that
        #   needs to be cut out of the end to represent a valid Genre
        #   (ex: 'house-container' - '-container' => 'house'.
        #       In this case the configuration would be '-container')
        genre = genre_id[:genre_id.find(
            self.config.get(self.website, 'parse_songs_genre_name')
        )]

        # CONFIG: The xpath to find a List of tracks for that root element.
        #   (ex: './li' is the xpath to find, from the element 'house' all the tracks)
        tracks = chart_genre.find_element_by_id(genre).find_elements_by_xpath(
            self.config.get(self.website, 'parse_songs_track_list_xpath')
        )

        # Initialize the basic structure for the results
        result = {
            genre: []
        }

        for track in tracks:
            # Maybe use if's to split on websites if the paths vary too much
            # CONFIG: The element class to find the Track title and the CSS selector
            #   to get the title text
            t_title = track.find_element_by_class_name(
                self.config.get(self.website, 'parse_songs_title_class_name')
            ).find_element_by_css_selector(
                self.config.get(self.website, 'parse_songs_title_css_selector')
            ).text
            # CONFIG: The element class to find the Track's artist and the CSS selector
            #   to get the artist text
            t_artist = track.find_element_by_class_name(
                self.config.get(self.website, 'parse_songs_artist_class_name')
            ).find_element_by_css_selector(
                self.config.get(self.website, 'parse_songs_artist_css_selector')
            ).text
            result[genre].append(
                {
                    'title': t_title,
                    'artist': t_artist
                }
            )
            self.count += 1
        return result

    def find_charts(self):
        """Function used to find the root node of charts within a Website.

        Returns:
            A List of root elements for each genre of music in the charts.
            This list is ready to be processed one genre at a time.
        """

        # CONFIG: this configured class is an element you wait for,
        #   before beginning to parse the website.
        #   (Basically the closest CLASS to what you want to retrieve)
        d = self.driver.driver
        WebDriverWait(d, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, self.config.get(self.website, 'find_charts_class'))))

        root = d.find_element_by_id(self.config.get(self.website, 'find_charts_root_id'))

        # CONFIG: The xpath to retrieve a List of elements containing all the genre for the charts.
        #   (ex: "//*[contains(@id, '-container')]" will retrieve all the genre for djcity)
        charts_by_genre = root.find_elements_by_xpath(
            self.config.get(self.website, 'find_charts_genre_list_xpath')
        )
        return charts_by_genre

    def compile_chart(self):
        """Compile the music charts of this Website."""
        # FIXME: add exception handling.
        try:
            self.get_source()
            charts = self.find_charts()
            for c_genre in charts:
                self.results.update(self._parse_songs_by_genre(c_genre))
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup routine to properly shutdown the Driver instance of the Website."""
        # FIXME: make quit handling by Driver and refactor into better named method.
        self.driver.driver.quit()

    def get_results(self):
        """Getter for results dict."""
        return self.results

    def get_count(self):
        """Getter for track count."""
        return self.count


def main():
    """Main entry to test Website platform."""
    url = "http://www.djcity.com/charts/"
    djcity = Website(url, 'djcity')
    djcity.compile_chart()
    print(djcity.get_results())
    print("Website Info:\n{}".format(str(djcity)))


if __name__ == '__main__':
    sys.exit(main())
