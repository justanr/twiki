from twiki.twitter import Twitter, TwitterError
from tweepy import API, TweepError

try:
    from unittest import mock
except ImportError:
    import mock

import pytest


def test_search_without_config_causes_error():
    twitter = Twitter()

    with pytest.raises(TwitterError) as excinfo:
        twitter.search('')

    assert excinfo.value.msg == "Can't connect to Twitter right now."


def test_transform_tweepy_error():
    e = TweepError("Something bad happened", mock.Mock(status_code=400))

    with pytest.raises(TwitterError) as excinfo:
        Twitter._throw_from_tweepy_error(e)

    assert excinfo.value.msg == "Something bad happened" and excinfo.value.code == 500


def test_transform_tweets():
    tweet = mock.Mock(user=mock.Mock(screen_name='Fred'), text='Some Text', id_str='1')

    assert Twitter()._format(tweet) == {'user': 'Fred', 'text': 'Some Text',
                                        'url': 'https://twitter.com/Fred/status/1'}


def test_twitter_search_happy_path():
    twitter = Twitter()
    api = mock.create_autospec(API)
    api.search.return_value = [mock.Mock(user=mock.Mock(screen_name='Fred'),
                                         text='Some Text', id_str='1')]
    twitter._api = api

    tweets = twitter.search('Fred')

    assert api.search.call_args == mock.call('Fred')
    assert tweets == [{'user': 'Fred', 'text': 'Some Text',
                       'url': 'https://twitter.com/Fred/status/1'}]


def test_twitter_search_throws_error():
    twitter = Twitter()
    api = mock.create_autospec(API)
    api.search.side_effect = TweepError('Something Bad Happened', mock.Mock(status_code=400))
    twitter._api = api

    with pytest.raises(TwitterError):
        twitter.search('Fred')
