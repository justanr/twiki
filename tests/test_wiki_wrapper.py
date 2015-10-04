from twiki.wiki import Wikipedia, WikipediaError
import wikipedia
import pytest
from collections import namedtuple

try:
    from unittest import mock
except ImportError:
    import mock


FakePage = namedtuple('FakePage', ['title', 'url', 'summary'])

@pytest.fixture
def fakewiki():
    return mock.create_autospec(wikipedia)


@pytest.fixture
def fakepage():
    return FakePage(title='Python', url='https://www.wikipedia.org/wiki/Python',
                    summary = 'Python')


def test_convert_wiki_error():
    e = wikipedia.WikipediaException("Something bad happened")
    with pytest.raises(WikipediaError) as excinfo:
        Wikipedia._throw_from_wikipedia_error(e)

    assert excinfo.value.msg == 'Something bad happened' and excinfo.value.code == 500


def test_wikipedia_search_happy_path(fakewiki, fakepage):
    fakewiki.search.return_value = ['Python (Programming Language)']
    wiki = Wikipedia(fakewiki)

    assert wiki.search('python') == [{'title': 'Python (Programming Language)',
                                      'url': 'https://www.wikipedia.org/wiki/Python_(Programming_Language)'}]


def test_wikipedia_search_blows_up(fakewiki):
    fakewiki.search.side_effect = wikipedia.WikipediaException('Whoops..')
    wiki = Wikipedia(fakewiki)

    with pytest.raises(WikipediaError):
        wiki.search('')


def test_transform_page(fakepage):
    wiki = Wikipedia(None)

    assert wiki._transform_page(fakepage) == {'title': 'Python',
                                              'url': 'https://www.wikipedia.org/wiki/Python',
                                              'summary': 'Python'}


def test_wikipedia_get_page_happy_path(fakewiki, fakepage):
    fakewiki.page.return_value = fakepage
    wiki = Wikipedia(fakewiki)

    assert wiki.get_page('Python') == {'title': 'Python',
                                       'url': 'https://www.wikipedia.org/wiki/Python',
                                       'summary': 'Python'}


def test_wikipedia_get_page_blows_up(fakewiki):
    fakewiki.page.side_effect = wikipedia.WikipediaException('...')
    wiki = Wikipedia(fakewiki)

    with pytest.raises(WikipediaError):
        wiki.get_page('')


def test_wikipedia_get_page_receives_disambiguation(fakewiki):
    fakewiki.page.side_effect = wikipedia.DisambiguationError('...', '...')
    wiki = Wikipedia(fakewiki)

    with pytest.raises(WikipediaError) as excinfo:
        wiki.get_page('Whooops...')

    assert excinfo.value.msg == 'This is a disambiguation page'
    assert excinfo.value.code == 301


def test_shorten_summary_with_short():
    summary = 'a short summary'

    assert Wikipedia._shorten_summary(summary) == summary


def test_shorten_summary_with_no_summary():
    assert Wikipedia._shorten_summary('') == ''


def test_shorten_summary_with_long_summary():
    summary = 'a ' * 30
    expected = '{0} ...'.format(' '.join(['a'] * 25))

    assert Wikipedia._shorten_summary(summary) == expected
