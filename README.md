# Golden Globes Tweet Parser

Project by Kevin Chen, Brittany Lee, Kevin Broh-Kahn, and Bhavita Jaiswal.

This project is built off of a Flask boilerplate - [https://github.com/mjhea0/flask-boilerplate/](https://github.com/mjhea0/flask-boilerplate)

## Quick Start
1. Clone the repo
  ```
  $ git clone git@github.com:blee42/eecs337.git
  $ cd flask-boilerplate
  ```

2. Make a virtual environment.  We are using the virtualenvwrapper; if you have not used it before the installation docs can be seen [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](here).
  ```
  $ mkvirtualenv env
  $ workon env
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

  The dependent libraries include:
  * Fabric==1.8.2
  * Flask==0.10.1
  * Flask-SQLAlchemy==1.0
  * Jinja2==2.7.2
  * MarkupSafe==0.18
  * SQLAlchemy==0.9.3
  * Werkzeug==0.9.4
  * coverage==3.7.1
  * ecdsa==0.10
  * itsdangerous==0.23
  * paramiko==1.12.2
  * pycrypto==2.6.1
  * wsgiref==0.1.2
  * Flask-WTF==0.9.4
  * beautifulsoup4==4.3.2
  * nltk==3.0
  * numpy

4. Ensure that the data jsons are in the data folder.

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

If you see errors involving not having the correct nltk resources, then open up a python window and run:
  ```
  >>> import nltk
  >>> nltk.download()
  ```
This will open a window called the 'NLTK Downloader'. Make sure you have the following installed:
  Corpora -> stopwords and Models -> maxent_treebank_pos


If you want to debug and run one script, use the following procedures.
  ```
  $ python -i [filename]
  $ >>> [function name]
  ```

## Future Adaptability
To ensure that our application will work for future Golden Globes ceremonies, we did not hardcode any date or time information into our analysis.  We also strucutred our analysis to be able to take in a stream of tweets to simulate real-time analysis during future ceremonies.  The one area that needs be changed each year, is adjustments to the web scraper which gets the nominee and category information.  Tweaks to the website that we are pulling from may change in future years.

