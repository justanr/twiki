"""
    twiki.utils
    ~~~~~~~~~~~
    Home for utility functions
"""

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def encode_term(term):
    "Encodes a search term to be more URL friendly"
    return urlencode({'dummy': term.strip()}).split('dummy=', 1)[1]
