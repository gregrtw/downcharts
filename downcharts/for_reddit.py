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

    def run(self):
        pass

    def process_submission(self):
        pass

    def parse_comment(self, comment):
        """
        Parse comment to find message and extra command parameter
        """

    def build_reply(self):
        """
        Build the reply to the call.
        Print the formatted listing (Bullet/Numbered)
        """
        pass


# # # #
# Main
# # # #

def main():
    print("Launched!")
    reddit = RedditBot()




if __name__ == '__main__':
    main()
