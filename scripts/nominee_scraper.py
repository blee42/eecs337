import bs4
import urllib2

hosts = ['Tina Fey', 'Amy Poehler']
NOMINEES2013_URL = 'http://www.theguardian.com/film/2012/dec/13/golden-globes-2013-nominations-list'
NOMINEES2015_URL = 'http://www.theguardian.com/film/2015/jan/11/2015-golden-globes-full-list-nominations'
categories = []

def read_page(url):
    res = urllib2.urlopen(url)
    return res.read()

def get2015():
    html = read_page(NOMINEES2015_URL)
    soup = bs4.BeautifulSoup(html)

    global categories
    categories = []
    categories = get_2015categories(soup)

    return categories

def get2013():
    html = read_page(NOMINEES2013_URL)
    soup = bs4.BeautifulSoup(html)

    global categories
    categories = []
    categories = get_2013categories(soup)

    return categories
    
def get_2015categories(soup):
    for category in soup.find_all('strong'): # each strong tag indicates a category
        if category.contents[0] == 'Television': # random header halfway down page
            continue
        entry = {}
        entry['category'] = category.contents[0]
        entry['nominees'] = []
        entry['presenters'] = []

        for child in category.parent.next_sibling.next_sibling.children:
            if type(child) is not bs4.element.Tag: # not a <br/>
                nominee = {}
                nominee['name'] = child
                nominee['score'] = 0
                entry['nominees'].append(nominee)

        categories.append(entry)

    return categories

def get_2013categories(soup):
    for category in soup.find_all('h2'): # each strong tag indicates a category
        entry = {}
        entry['category'] = category.contents[0]
        entry['nominees'] = []
        entry['presenters'] = []

        carryover = "{0}"
        category_name = category.contents[0]
        for child in category.next_sibling.next_sibling.children:
            # necessary ugly scrapping details...
            if (category_name == 'Best original song' and type(child) is bs4.element.NavigableString):
                nominee = {}
                nominee['name'] = child.string.split(' (')[0].strip("'")
                nominee['score'] = 0
                entry['nominees'].append(nominee)
            elif child.string == 'Kon-Tiki' or child.string == 'Untouchable':
                nominee = {}
                nominee['name'] = child.string
                nominee['score'] = 0
                entry['nominees'].append(nominee)
            elif type(child) is bs4.element.NavigableString:
                carryover = child.string + "{0})"
            elif len(child.contents) > 0:
                nominee = {}
                line = carryover.format(child.contents[0]).strip(')').split(' (')
                thing = line[0]
                film = line[1] if (len(line) > 1) else 0
                nominee['name'] = thing if (category_name != 'Best screenplay' or category_name != 'Best original score') else film
                nominee['score'] = 0
                entry['nominees'].append(nominee)
                carryover = "{0}"

        categories.append(entry)
        if category_name == 'Best original song':
            break

    return categories

import pprint
p = pprint.PrettyPrinter()
p.pprint(get2013())

def get_names_from_twitter(array):
    base_url = "https://twitter.com/"

    for entry in array:
        twitter_id = entry[0][1:]
        page = base_url + twitter_id

        try:
            html = read_page(page)
        except urllib2.HTTPError:
            print "no such id"
            continue
        except urllib2.URLError:
            print "no host"
            continue
        except UnicodeEncodeError:
            print "unicode char"
            continue

        soup = bs4.BeautifulSoup(html)

        for name_element in soup.find_all("a", { "class" : "ProfileHeaderCard-nameLink" }):
            print twitter_id
            print name_element.getText()
def get_hosts():
    return hosts
