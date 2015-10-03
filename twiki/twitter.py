"""
    twiki.twitter
    ~~~~~~~~~~~~~
    Basic Tweepy wrapper for Flask app
"""

from tweepy import OAuthHandler, API, TweepError


class TwitterError(Exception):
    def __init__(self, msg, code=500):
        self.msg = msg
        self.code = code
        super(TwitterError, self).__init__(msg, code)


class Twitter(object):
    """Thin wrapper around Tweepy to configure the OAuth from a import Flask app
    to make it a little easier to deal with, such as throwing application specific
    exceptions rather than TweepyError and configuring from a passed application.
    """
    def __init__(self, app=None):
        self._api = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        self._api = API(OAuthHandler(app.config['TWITTER_KEY'],
                        app.config['TWITTER_SECRET']))

    def search(self, term):
        if self._api is None:
            raise TwitterError("Can't connect to Twitter right now.")

        return [self._format(tweet) for tweet in self._search(term)]

    def _search(self, term):
        "Attempts to search twitter and raises a TwitterError if it fails."
        try:
            return self._api.search(term)
        except TweepError as e:
            self._throw_from_tweepy_error(e)

    @staticmethod
    def _format(tweet):
        return {'user': tweet.user.screen_name,
                'text': tweet.text,
                'id': tweet.id_str}

    @staticmethod
    def _throw_from_tweepy_error(e):
        "Converts a tweepy error into an application specific error"
        raise TwitterError(e.reason, e.response.status_code)
