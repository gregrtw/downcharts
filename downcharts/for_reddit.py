import praw
import configparser
import requests

from threading import Thread


class RedditBot(object):
    ini_path = "./praw.ini"
    end_message = (
        "\n\n_______\n\n"
        "|[^(FAQs)](/r/TopMusicCharts/comments/50d7zl/topmusiccharts_bot_info/)"
        "|[^(Commands)](/r/TopMusicCharts/comments/)"
        "|[^(Feedback)](/message/compose/?to=TopMusicCharts&subject=Feedback)"
        "\n|-|-|-|-|-|-|"
    )
    seen_comment = []

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
        if (
            "topmusiccharts!" in comment.body.lower()
            or "!topmusiccharts" in comment.body.lower()
            and comment.id not in self.seen_comment
            and 'TopMusicCharts' != str(comment.author)
        ):
            t = Thread(target=self.run())
            t.start()

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
    # # # # # # # # # # # #
    # PUSHSHIFT options
    # # # # # # # # # # # #
    # subreddit={name} to restrict
    # limit={number} for max return
    # before_id={id} for retrieval of comments FROM this id forward (in time)
    # author={author} for restricted to an author
    # fields={field,field} to restrict the returned data to specific fields
    # link_id={id} for all comments for a submission
    request = requests.get(
        "https://api.pushshift.io/reddit/search?q={0}&limit={1}".format(
            "%22TopMusicCharts%22", "100"
        ),
        headers={ 'User-Agent': 'downcharts for reddit 0.1.1 (by /u/TopMusicCharts)'}
    )
    json_results = request.json()
    results = json_results["data"]
    for comment in results:
        comment['_replies'] = ''
        reddit_comment = praw.objects.Comment(reddit, comment)
        reddit.parse_comment(reddit_comment)




if __name__ == '__main__':
    main()
