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
        driver = Driver_get_source(url)
        charts = find_charts(driver)
        for c_genre in charts:
            compiled.update(parse_songs_by_genre(c_genre))
    finally:
        driver.quit()
    return compiled


def main():
    print(compile_chart("http://www.djcity.com/charts/"))


if __name__ == '__main__':
    sys.exit(main())

