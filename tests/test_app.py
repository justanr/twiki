from twiki.factory import create_app
from tweepy import TweepError
from wikipedia import WikipediaException
import pytest
import json
import sys

PY3 = sys.version_info[0] > 2


try:
    from unittest import mock
except ImportError:
    import mock


def make_json(data):
    if PY3:
        return json.loads(data.decode())
    else:
        return json.loads(data)


@pytest.fixture(scope='session')
def app():
    return create_app('test')


@pytest.yield_fixture
def client(app):
    with app.test_client() as c:
        yield c


def test_provide_no_tweet_search(client):
    resp = client.get('/api/tweets/')

    jsoned = make_json(resp.data)

    assert 'No search term provided' == jsoned['msg']
    assert resp.status_code == 400


def test_twitter_error_handling(client):
    api = mock.Mock()
    api.search.side_effect = TweepError('Whoops...')

    with mock.patch('twiki.exts.twitter._api', api):
        resp = client.get('/api/tweets/whoops')

    jsoned = make_json(resp.data)

    assert "Sorry, we're having trouble with Twitter right now." == jsoned['msg']
    assert resp.status_code == 500


def test_process_twitter_response(client):
    tweets = [mock.Mock(user=mock.Mock(screen_name='Fred'), text='Some Text', id_str='1')]

    with mock.patch('twiki.app.twitter._search', return_value=tweets):
        resp = client.get('/api/tweets/Fred')

    jsoned = make_json(resp.data)

    assert jsoned['tweets'] == [{'user': 'Fred', 'text': 'Some Text',
                                 'url': 'https://twitter.com/Fred/status/1'}]


def test_provide_no_wiki_search(client):
    resp = client.get('/api/titles/')

    jsoned = make_json(resp.data)

    assert 'No search term provided' == jsoned['msg']
    assert resp.status_code == 400


def test_wiki_error_handling(client):
    wiki = mock.Mock()
    wiki.search.side_effect = WikipediaException('Whoops...')

    with mock.patch('twiki.exts.wiki._wikipedia', wiki):
        resp = client.get('/api/titles/whoops')

    jsoned = make_json(resp.data)

    assert "Sorry, we're having trouble with Wikipedia right now." == jsoned['msg']
    assert resp.status_code == 500


def test_process_wiki_response(client):
    titles = ['Python']

    with mock.patch('twiki.app.wiki._search', return_value=titles):
        resp = client.get('/api/titles/Python')

    jsoned = make_json(resp.data)

    assert jsoned['titles'] == [{'title': 'Python', 'url': 'https://www.wikipedia.org/wiki/Python'}]
