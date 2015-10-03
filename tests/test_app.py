from twiki.app import (get_pages, _transform_pages, shorten_summary,
                       _transform_tweets)

try:
    from unittest import mock
except ImportError:
    import mock


def test_get_tweets_transforms_results():
    user = mock.Mock()
    user.name = 'fred'  # name is a field for Mock.__init__
    tweets = [mock.Mock(user=user, text='Some text', id=1)]

    assert _transform_tweets(tweets) == [{'user': 'fred', 'text': 'Some text', 'id': 1}]


@mock.patch('twiki.app.wikipedia')
def test_basic_assumption(wikipedia):
    wikipedia.search.return_value = ['page']
    wikipedia.page.return_value = mock.Mock(title='fred', summary='freds', url='fred')

    pages = get_pages('page')

    assert pages == [dict(title='fred', summary='freds', url='fred')]


def test_transform_pages():
    pages = [mock.Mock(title='Fred Fredenheimer', summary='Fred Fredenheimer...',
                       url='Fred_Fredenheimer')]

    transformed = _transform_pages(pages)

    assert transformed == [dict(title='Fred Fredenheimer', url='Fred_Fredenheimer',
                                summary='Fred Fredenheimer...')]


def test_shorten_summary_with_short():
    summary = 'a short summary'

    assert shorten_summary(summary) == summary


def test_shorten_summary_with_no_summary():
    assert shorten_summary('') == ''


def test_shorten_summary_with_long_summary():
    summary = 'a ' * 30
    expected = '{0} ...'.format(' '.join(['a'] * 25))

    assert shorten_summary(summary) == expected
