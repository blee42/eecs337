#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from scripts import reader, nominee_scraper

TWEET_STREAM = 'data/goldenglobes2015.json'

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
categories = reader.categories
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    context = {}
    
    categories = reader.get_current_winners()
    for category in categories:
        category['nominees'].sort(key=lambda nominee: nominee['score'], reverse=True)

    hosts = nominee_scraper.get_hosts()
    
    context['categories'] = categories
    context['hosts'] = hosts
    context['counter'] = reader.get_current_count()
    return render_template('pages/placeholder.home.html', context=context)

@app.route('/redcarpet')
def red_carpet():
    red_carpet_data = reader.get_current_red_carpet()
    red_carpet_data['counter'] = reader.get_current_count()
    return render_template('pages/placeholder.redcarpet.html', context=red_carpet_data)

@app.route('/parties')
def parties():
    parties = reader.get_current_parties()
    context = [parties, reader.get_current_count()]
    return render_template('pages/placeholder.parties.html', context=context)

@app.route('/presenters')
def presenters():
    presenters = reader.get_presenters()
    return render_template('pages/placeholder.presenters.html', context=presenters)

@app.route('/sentiment')
def sentiments():
    sentiments = reader.get_current_sentiments()
    sentiments[1].sort(key=lambda wordTuple: wordTuple[1], reverse=True)
    sentiments[2].sort(key=lambda wordTuple: wordTuple[1], reverse=True)
    sentiments.append(reader.get_current_count())
    return render_template('pages/placeholder.sentiments.html', context=sentiments)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/dataset/<corpus>')
def dataset(corpus):
    reader.run('data/' + corpus)
    return redirect(url_for('home'))


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

@app.before_first_request
def before_first_request():
    reader.run(TWEET_STREAM)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
