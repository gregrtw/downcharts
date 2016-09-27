"""TopMusicCharts Bot for Reddit module."""
import configparser
import praw
import re
import requests

from threading import Thread


class RedditBotError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, *args, **kwargs):
        """RedditBotError constructor."""
        super().__init__(args, kwargs)


class RedditBot(object):
    """A class for all bot interactions with the Reddit website.

    Attributes:
        ini_path: String of the path to the configuration options
            of Python Reddit API Wrapper (PRAW).
        end_message: String that represents the end of the message for all comments submitted
            by a bot instance.
        seen_comment: List of the comment id's of previously parsed comments.
        config: Instance of ConfigParser used to parse configuration files.
        reddit: Reddit instance from PRAW to communicate with the Reddit API & website.
    """

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
        """Constructor for RedditBot.

        Sets default values and initializes the connection to the Reddit API.
        """
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
        """String representation of a RedditBot."""
        return self.reddit.user.me()

    def run(self):
        """Runner for RedditBot instance.

        Runner that executes all the tasks required for a complete and atomic action by a bot.
        """
        pass

    def process_submission(self):
        """Process a submission and take appropriate action."""
        pass

    def parse_comment(self, comment):
        """Parse comment to find message and extra command parameter."""
        if (
            "topmusiccharts!" in comment.body.lower() or
            "!topmusiccharts" in comment.body.lower() and
            comment.id not in self.seen_comment and
            'TopMusicCharts' != str(comment.author)
        ):
            t = Thread(target=self.run())
            t.start()

    def build_reply(self, message=""):
        """Build the reply to the call.

        Print the formatted music listing to a end user.
        """
        pass


# # # #
# Comment API
# # # #
"""Pushshift Query API

Options:
    subreddit={name} to restrict
    limit={number} for max return
    before_id={id} for retrieval of comments FROM this id forward (in time)
    author={author} for restricted to an author
    fields={field, field} to restrict the returned data to specific fields
    link_id={id} for all comments for a submission
"""


def get_new_comments(subject="TopMusicCharts", limit=100):
    """New Comment Getter from Reddit using Pushshift api.

    Get new comments from Reddit that contains 'subject' up to a maximum of 'limit'

    Keyword Arguments:
        subject {str} -- the subject to look for in comments (default: {"TopMusicCharts"})
        limit {number} -- the maximum number of comments to get (default: {100})

    Returns:
        Requests response -- The content of the response is a JSON object
    """
    subject = "%22" + subject + "%22"
    return requests.get(
        "https://api.pushshift.io/reddit/search?q={subject}&limit={limit}".format(
            subject=subject, limit=limit
        ),
        headers={'User-Agent': 'TopMusicCharts for reddit 0.1.1 (by /u/TopMusicCharts)'}
    )


# # # #
# Main
# # # #

def main():
    """Main entry that launches a RedditBot session."""
    print("Launched!")
    reddit = RedditBot()
    request = get_new_comments(subject="TopMusicCharts", limit=100)
    results = request.json()["data"]
    for comment in results:
        reddit.parse_comment(comment)


if __name__ == '__main__':
    main()
