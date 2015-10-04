"""
    twiki.exts
    ~~~~~~~~~~
    Pre-created extensions used in Twiki
"""

from .twitter import Twitter
from .wiki import Wikipedia
import wikipedia


twitter = Twitter()
wiki = Wikipedia(wikipedia)
