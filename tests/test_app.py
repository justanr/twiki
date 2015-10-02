from twiki.app import get_tweets

try:
    from unittest import mock
except ImportError:
    import mock


@mock.patch('twiki.app.twitter')
def test_get_tweets_formats_term(twitter):
    twitter.search.return_value = []

    get_tweets('flask')

    assert twitter.search.call_args == mock.call('#flask')


@mock.patch('twiki.app.twitter')
def test_get_tweets_transforms_results(twitter):
    user = mock.Mock()
    user.name = 'fred'  # name is a field for Mock.__init__
    twitter.search.return_value = [mock.Mock(user=user,
                                             text='Some text', id=1)]

    tweets = get_tweets('something')

    assert tweets == [{'user': 'fred', 'text': 'Some text', 'id': 1}]
