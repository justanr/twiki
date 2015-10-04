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
            self._throw_from_tweepy_error(e, "Sorry, we're having trouble with Twitter right now.")

    def _format(self, tweet):
        return {'user': tweet.user.screen_name,
                'text': tweet.text,
                'url': self._build_url(tweet.user.screen_name, tweet.id_str)
                }

    @staticmethod
    def _build_url(username, status_id):
        return 'https://twitter.com/{0}/status/{1}'.format(username, status_id)

    @staticmethod
    def _throw_from_tweepy_error(e, msg=None):
        "Converts a tweepy error into an application specific error"
        if msg is None:
            msg = e.reason

        raise TwitterError(msg, 500)
