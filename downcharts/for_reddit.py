import praw
import configparser

ini_path = "./praw.ini"
config = configparser.ConfigParser()
config.read(ini_path)

r = praw.Reddit(
    'DOWNCHARTS',
    user_agent=config.get('DOWNCHARTS', 'user_agent'),
    client_id=config.get('DOWNCHARTS', 'oauth_client_id'),
    client_secret=config.get('DOWNCHARTS', 'oauth_client_secret'),
    username=config.get('DOWNCHARTS', 'user'),
    password=config.get('DOWNCHARTS', 'pswd'))

