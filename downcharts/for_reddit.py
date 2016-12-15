"""TopMusicCharts Bot for Reddit module."""
import configparser
import praw
import re
import requests

from threading import Thread

TRACKS_LIMIT = 250  # artifical limit of tracks returned


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
    action_list = [
        "provider",  # all, djcity, soundcloud, apple, spotify (etc.)
        "genre",  # all, hip hop, rap, edm, tropical house, alternative (etc.)
        "hype",  # top, new
        "order",  # rank, random, interleave
        "amount"  # max returned in playlist
    ]

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
        try:
            self.reddit = praw.Reddit(
                'DOWNCHARTS',
                user_agent=config.get('DOWNCHARTS', 'user_agent'),
                client_id=config.get('DOWNCHARTS', 'oauth_client_id'),
                client_secret=config.get('DOWNCHARTS', 'oauth_client_secret'),
                username=config.get('DOWNCHARTS', 'user'),
                password=config.get('DOWNCHARTS', 'pswd'))
            self.cmd_separator = config.get('DOWNCHARTS', 'cmd_separator', fallback=None)
            self.action_separator = config.get('DOWNCHARTS', 'action_separator', fallback="=")
        except praw.exceptions.APIException as e:
            print("API Exception: " + str(e.message))
        except praw.exceptions.ClientException as e:
            print("Client Exception: " + str(e))

    def __str__(self):
        """String representation of a RedditBot."""
        return self.reddit.user.me()

    def parse_comment(self, comment):
        """Parse comment to find message and extra command parameter."""
        c_body = comment["body"].lower()
        if (
            "topmusiccharts!" in c_body or
            "!topmusiccharts" in c_body and
            comment["id"] not in self.seen_comment and
            'TopMusicCharts' != str(comment["author"])
        ):
            t = Thread(target=self.run(comment))
            t.start()
        self.seen_comment.append(comment["id"])

    def run(self, comment=None):
        """Runner for RedditBot instance.

        Runner that executes all the tasks required for a complete and atomic action by a bot.

        FEATURE:
            Add a banlist for reddit authors that try to abuse the bot.
                Add a gather_information() method that identifies an author and log the attempts.
                Once enough evidence is gathered, we can add the user manually or automatically
                in a banlist.
        """
        if comment:
            command = self.process_submission(comment)
            result = self._process_command(command)
            reply = self.build_reply(result.get("valid_string"))
            if result.get("invalid_string", None):
                reply += self.addon_reply(result["invalid_string"])
            if result.get("badformat_string", None):
                reply += self.addon_reply(result["badformat_string"])
            self.send_reply(reply)
        else:
            raise RedditBotError("MissingComment")  # FIXME: refactor into CommentError?

    def process_submission(self, submission=None):
        """Extract a command from a matching submission.

        Process a submitted comment/posting to find a TopMusicCharts! tag.
            Then, extract the command from the submission and return that command.

        Keyword Arguments:
            submission {dict} -- The submission object containing the body
                and metadata about itself and its author (default: {None})

        Returns:
            str -- The command to be executed (requested by user)
        """
        command = None
        try:
            if submission:
                submission_body = submission["body"]
                assert type(submission_body) == str
                match = re.search(r'(!*)TopMusicCharts(!*)', submission["body"])
                command = submission_body[match.start():].split("\n")[0]
        except KeyError as e:
            print("KeyError:", e)
        except AssertionError as e:
            print("AssertionError: {0}".format(str(type(submission_body))),
                  "\nThe body of the submission is not a string.")
        return command

    def _execute_action(self, action="", value=""):
        """Evaluate the action.

        Take the action command name and the value assigned to it; evaluate the result
            and return the string resulting from the action.

        Keyword Arguments:
            action {str} -- Action identifier (default: {""})
            value {str} -- Value assigned to action (default: {""})

        Returns:
            result {str} -- Evaluated action string (ex: Formatted top music list)
        """
        pass

    def _process_command(self, command=""):
        """[Private] Process a command, execute appropriate action.

        The command is split on spaces, then the resulting chunks are split on '=' sign
            and stored as tuples in a list. Each tuple is parsed and evaluated to a certain action.
        Each action is then executed to build the "action" part of the reply.

        Keyword Arguments:
            command {str} -- the command to execute (1 or more parts space separated)

        Returns:
            result_action {dict} -- A dict of:
                valid_string {str} -- The result of all actions.
                    Will be added to the response message. (Default: "")
                badformat_string {str} -- The result of all actions that are of wrong format.
                    Will be added in the error part of the response message. (Default: "")
                invalid_string {str} -- The result of all actions that are invalid.
                    Will be added in the error part of the response message. (Default: "")

        Raises:
            CommandError -- RedditBot Error which indicates a lack of a command or
                an invalid command action requested
        """
        result_action = {
            "valid_string": "",
            "badformat_string": "",
            "invalid_string": ""
        }

        def condition_sanitize(action):
            sep = self.action_separator
            return (sep in action and action.count(sep) == 1)

        def condition_action(action):
            return (action in self.action_list)

        try:
            if not command:  # Handles empty command
                raise EmptyCommandError(command, cmd=command)

            action_list = command.split(self.cmd_separator)
            # Unproperly formatted actions
            badformat_actions = [a for a in action_list if not condition_sanitize(a)]
            # Handle a fully invalid command
            if len(badformat_actions) == len(action_list):
                raise InvalidCommandError(command, cmd=command)
            # Dealing with valid actions
            invalid_actions_error_message = ""
            invalid_actions = []
            valid_actions = [a for a in action_list if condition_sanitize(a)]
            tuple_split_valid_actions = [(a[0], a[1]) for a in valid_actions]
            # Handle at least 1 valid action
            for action in tuple_split_valid_actions:
                if not condition_action(action[0]):
                    invalid_actions.append(action)
                    invalid_actions_error_message += "\
                    Attempt to use an invalid Action: {0} with value {1}\n".format(
                        action[0], action[1])
                else:
                    # IMPROVEMENT: reorder actions to print in a consistent fashion
                    result_action["valid_string"] += self._execute_action(
                        action=action[0], value=action[1])

            # Dealing with invalid actions
            # TODO
            result_action["invalid_string"] = ""
        except EmptyCommandError as e:
            pass
        except InvalidCommandError as e:
            pass
        except InvalidActionCommandError as e:
            pass
        return result_action

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
