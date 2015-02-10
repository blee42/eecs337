import bs4
import urllib2

hosts = ['Tina Fey', 'Amy Poehler']
NOMINEES_URL = 'http://www.theguardian.com/film/2015/jan/11/2015-golden-globes-full-list-nominations'
categories = []

def read_page(url):
    res = urllib2.urlopen(url)
    return res.read()

def main():
    html = read_page(NOMINEES_URL)
    soup = bs4.BeautifulSoup(html)

    categories = get_categories(soup)

    return categories
    
def get_categories(soup):
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


