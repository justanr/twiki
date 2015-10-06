"""
    twiki
    ~~~~~
    Unified search client for twitter and wikipedia
"""

from flask import Blueprint, render_template, jsonify
from .exts import twitter, wiki


frontend = Blueprint('frontend', __name__)
backend = Blueprint('backend', __name__)


@frontend.route('/')
def index():
    return render_template('index.html')


@backend.route('/tweets/')
@backend.route('/tweets/<term>')
def tweets(term=None):
    if term is None:
        return jsonify({'msg': 'No search term provided'}), 400

    return jsonify(tweets=twitter.search(term))


@backend.route('/titles/')
@backend.route('/titles/<term>')
def titles(term=None):
    if term is None:
        return jsonify({'msg': 'No search term provided'}), 400

    return jsonify(titles=wiki.search(term))


@backend.route('/page/')
@backend.route('/page/<title>')
def page(title=None):
    if title is None:
        return jsonify({'msg': 'No page title provided'}), 400
    return jsonify(page=wiki.get_page(title))
