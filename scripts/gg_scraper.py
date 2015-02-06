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
    
def get_categories(soup):
    for category in soup.find_all('strong'): # each strong tag indicates a category
        entry = {}
        entry['category'] = category.contents[0]
        entry['nominees'] = []

        for child in category.parent.next_sibling.next_sibling.children:
            if type(child) is not bs4.element.Tag: # not a <br/>
                entry['nominees'].append(child)

        categories.append(entry)

    return categories



