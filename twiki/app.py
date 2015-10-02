"""
    twiki
    ~~~~~
    Unified search client for twitter and wiki
"""

from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from .auth_keys import AuthKeys
import tweepy
import wikipedia
from collections import namedtuple

Tweet = namedtuple('Tweet', ['user', 'text', 'id'])
WikiPage = namedtuple('WikiPage', ['title', 'summary', 'url'])

app = Flask(__name__)
app.config.from_object(AuthKeys)
app.config['SECRET_KEY'] = 'fred'

Bootstrap(app)

tweepy_auth = tweepy.OAuthHandler(app.config['KEY'], app.config['SECRET'])
twitter = tweepy.API(tweepy_auth)


class SearchForm(Form):
    term = StringField('term', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('search', term=form.term.data))
    return render_template('index.html', form=form)


@app.route('/search/<term>/')
def search(term=None):
    if not term:
        return 'Please enter a search term'

    tweets = [Tweet(t.user.name, t.text, t.id) for t in twitter.search('#' + term)]
    pages = []

    for page in wikipedia.search(term):
        try:
            page = wikipedia.page(page)
        except wikipedia.DisambiguationError:
            pass
        else:
            pages.append(WikiPage(page.title, page.summary, page.url))

    return render_template('display_results.html', tweets=tweets, pages=pages, term=term)
