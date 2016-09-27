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


class CommandError(RedditBotError):
    """CommandError class for exceptions with RedditBot commands.

    Used to report errors with Command with the  RedditBot

    Extends:
        RedditBotError

    Variables:
        Keyword Arguments:
            cmd {str} -- the command string passed in kwargs
            action {str} -- the action string passed in kwargs

        Returns:
            Reports the error
    """

    def __init__(self, *args, **kwargs):
        """CommandError constructor."""
        cmd = kwargs.pop("cmd", None)
        if cmd:
            print(cmd, "is an undefined Command.")
        super().__init__(args, kwargs)


class EmptyCommandError(CommandError):
    """Class to handle an empty command."""

    def __init__(self, *args, **kwargs):
        """EmptyCommandError Constructor."""
        print("The Command is empty")
        super().__init__(args, kwargs)


class FormatCommandError(CommandError):
    """Class to handle an invalid format command."""

    def __init__(self, _list, *args, **kwargs):
        """Constructor of FormatCommandError."""
        self.list = _list
        super().__init__(args, kwargs)


class InvalidCommandError(CommandError):
    """Class to handle an invalid command."""

    def __init__(self, cmd, *args, **kwargs):
        """Constructor of InvalidCommandError."""
        self.cmd = cmd
        super().__init__(args, kwargs)


class InvalidActionCommandError(CommandError):
    """Class to handle an invalid action in a command."""

    def __init__(self, msg, *args, **kwargs):
        """Constructor of InvalidActionCommandError."""
        print("Invalid Actions were found in the Command.\n", msg)
        super().__init__(args, kwargs)


class RedditBot(object):
    """A class for all bot interactions with the Reddit website.

    Attributes:
        action_separator {str} -- The separator used to split actions. (Default: '=')
        cmd_separator {str} -- The separator used to split a command. (Default: None)
            NOTE: Highly recommend to use Default!
        config {ConfigParser} -- ConfigParser used to parse .ini configuration files.
        end_message {str} -- Represents the end of the message for all comments submitted
            by a bot instance.
        ini_path {str} -- The path to the configuration options of PRAW4.
        reddit {Reddit} -- Reddit instance from PRAW4 to communicate with the Reddit API & website.
        seen_comment {list} -- Comments id's of previously parsed comments.
    """

    end_message = (
        "\n\n_______\n\n"
        "|[^(FAQs)](/r/TopMusicCharts/comments/50d7zl/topmusiccharts_bot_info/)"
        "|[^(Commands)](/r/TopMusicCharts/comments/)"
        "|[^(Feedback)](/message/compose/?to=TopMusicCharts&subject=Feedback)"
        "\n|-|-|-|-|-|-|"
    )
    seen_comment = []

    def __init__(self, *args, **kwargs):
        """Constructor for RedditBot.

        Sets default values and initializes the connection to the Reddit API.

        Raises:
            APIException: Exception coming from the Reddit API
            ClientException: Exception not coming from the Reddit API
        """
        self.ini_path = kwargs.get("praw_ini", "./praw.ini")
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
