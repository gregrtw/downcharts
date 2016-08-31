import praw
import configparser



class RedditBot(object):
    ini_path = "./praw.ini"
    end_message = (
        "\n\n_______\n\n"
        "|[^(FAQs)](/r/TopMusicCharts/comments/50d7zl/topmusiccharts_bot_info/)"
        "|[^(Commands)](/r/TopMusicCharts/comments/)"
        "|[^(Feedback)](/message/compose/?to=TopMusicCharts&subject=Feedback)"
        "\n|-|-|-|-|-|-|"
    )

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(self.ini_path)
        self.reddit = praw.Reddit(
            'DOWNCHARTS',
            user_agent=config.get('DOWNCHARTS', 'user_agent'),
            client_id=config.get('DOWNCHARTS', 'oauth_client_id'),
            client_secret=config.get('DOWNCHARTS', 'oauth_client_secret'),
            username=config.get('DOWNCHARTS', 'user'),
            password=config.get('DOWNCHARTS', 'pswd'))

    def __str__(self):
        return self.reddit.user.me()

subreddit = reddit.subreddit('TopMusicCharts')
