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
  Corpora -> stopwords
  Models -> maxent_treebank_pos


If you want to debug and run one script, use the following procedures.
  ```
  $ python -i [filename]
  $ >>> [function name]
  ```

## Team Notes
2/6/2015 Update:
Added scraper ("/scripts/gg_scraper.py") for all categories and nominees. `get_categories` will return data in this form:

```python
[
    {
        'category': 'award1',
        'nominees': 
            [
                {
                    'name': 'nominee1',
                    'score': 0
                },
                {
                    'name': 'nominee2',
                    'score': 0
                },
                '...'
            ],
        'presenters':
            [
                {
                  'name': 'presenter1', # populated as we go along
                  'score': 0
                },
                '...'
            ],
        '...'
    },

    {
        'category': 'award2',
        'nominees': 
            [
                {
                    'name': 'nominee1',
                    'score': 0
                },
                {
                    'name': 'nominee2',
                    'score': 0
                },
                '...'
            ],
        'presenters':
            [
                {
                  'name': 'presenter1',
                  'score': 0
                },
                '...'
            ],
        '...'
    },

    '...'
]
```

2/4/15 Update:
Added reader function ("/scripts/reader.py") that prints each tweet object.