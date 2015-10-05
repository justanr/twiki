"""
    twiki.wikipedia
    ~~~~~~~~~~~~~~~
    Wikipedia API wrapper
"""

import wikipedia


class WikipediaError(Exception):
    def __init__(self, msg, code=500):
        self.msg = msg
        self.code = code
        super(WikipediaError, self).__init__(msg, code)


class Wikipedia(object):
    """Wraps around wikipedia API wrapper for ease of use in stripping down
    massive wikipedia pages to basic information and for easier error handling
    """
    def __init__(self, wikipedia=wikipedia):
        self._wikipedia = wikipedia

    def search(self, term):
        "Finds wikipedia page titles and returns dictionaries of title and url."
        return [self._build_basic_info(title) for title in self._search(term)]

    def get_page(self, title):
        """Finds a wikipedia page and returns a dictionary of title, url and
        shortened summary.
        """
        return self._transform_page(self._get_page(title))

    def _search(self, term):
        "Attempts to search wikipedia for potentially matching pages"
        try:
            return self._wikipedia.search(term)
        except wikipedia.WikipediaException as e:
            self._throw_from_wikipedia_error(e, "Sorry, we're having trouble with Wikipedia right now.")

    def _build_basic_info(self, title):
        return {'title': title, 'url': self._build_url(title)}

    def _get_page(self, title):
        """Attempts to retrieve a fully wikipedia page and throws a WikipediaError
        if it can't."""
        try:
            return self._wikipedia.page(title)
        except wikipedia.DisambiguationError as e:
            self._throw_from_wikipedia_error(e, "This is a disambiguation page", 301)
        except wikipedia.WikipediaException as e:
            self._throw_from_wikipedia_error(e, "Couldn't find wikipedia page")

    def _transform_page(self, page):
        summary = self._shorten_summary(page.summary)
        return {'title': page.title, 'summary': summary, 'url': page.url}

    @staticmethod
    def _shorten_summary(summary, word_limit=25):
        """Shortens a potentially long summary into a shorter summary."""
        if summary.count(' ') <= word_limit:
            return summary
        else:
            cut_off_summary = summary.split()[:word_limit]
            return '{0} ...'.format(' '.join(cut_off_summary))

    @staticmethod
    def _build_url(title):
        url = 'https://www.wikipedia.org/wiki/{0}'
        return url.format(title.replace(' ', '_'))

    @staticmethod
    def _throw_from_wikipedia_error(e, msg=None, code=500):
        """Raises an application specific error from either the provided message
        or the error passed to it
        """
        if msg is None:
            msg = e.error
        raise WikipediaError(msg, code)
