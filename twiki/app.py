"""
    twiki
    ~~~~~
    Unified search client for twitter and wikipedia
"""

from flask import Flask, redirect, render_template, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from .auth_keys import AuthKeys
import tweepy
import wikipedia


app = Flask(__name__)
app.config.from_object(AuthKeys)
app.config['SECRET_KEY'] = 'fred'

Bootstrap(app)

tweepy_auth = tweepy.OAuthHandler(app.config['KEY'], app.config['SECRET'])
twitter = tweepy.API(tweepy_auth)


@app.after_request
def allow_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, PUT'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return resp

class SearchForm(Form):
    term = StringField('term', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        term = form.term.data
        anchor = '#/#{0}'.format(term)
        return redirect(url_for('search', term=term) + anchor)
    return render_template('index.html', form=form)


@app.route('/search/')
@app.route('/search/<term>')
def search(term=None):
    if not term:
        flash('Please enter a search term', 'warning')
        return redirect(url_for('index'))

    tweets = []
    pages = []
    return render_template('display_results.html', tweets=tweets, pages=pages, term=term)


@app.route('/tweets/')
@app.route('/tweets/<term>')
def tweets(term=None):
    if term is None:
        return jsonify({'error': 'no search term provided'}), 400

    return jsonify(tweets=get_tweets(term))


@app.route('/pages/')
@app.route('/pages/<term>')
def pages(term=None):
    if term is None:
        return jsonify({'error': 'no search term provided'}), 400

    return jsonify(pages=get_pages(term))


def get_tweets(term):
    return [transform_tweet(tweet) for tweet in twitter.search(term)]


def transform_tweet(t):
    return {'user': t.user.name, 'text': t.text, 'id': t.id}


def get_pages(term):
    pages = (get_page_contents(title) for title in wikipedia.search(term))
    return [transform_page(page) for page in pages if page]


def get_page_contents(title):
    try:
        return wikipedia.page(title)
    except wikipedia.DisambiguationError:
        pass


def transform_page(page):
    summary = shorten_summary(page.summary)
    return {'title': page.title, 'summary': summary, 'url': page.url}


def shorten_summary(summary, word_limit=25):
    if summary.count(' ') <= word_limit:
        return summary

    else:
        cut_off_summary = summary.split()[:word_limit]
        return '{0} ...'.format(' '.join(cut_off_summary))
