from threading import Thread
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper
import sys
import os
import sys
import urllib2
import bs4
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display


#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

pp = pprint.PrettyPrinter()

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
wishStrings = ["hope", "hoping", "if", "luck"]
presentStrings = ["presenting", "present", "presented", "presenter"]
punct = ["!", ",", ".", "&", "@", "#", "-", "'"]
nominees = []
categories = nominee_scraper.main()
parties = []
best_dressed = {}
worst_dressed = {}
red_carpet_photos = {}

stop_words = nltk.corpus.stopwords.words('english')

def main():
    thread = run()

    while (1):
        inp = raw_input('Hit Enter for results: \n')
        if inp == 'break':
            break
        get_current_winners()
        # return { 'categories': categories, 'best_dressed': best_dressed, 'parties': parties }

    thread.join()

def run():
    init()
    thread = Thread(target=parse, args={})
    thread.daemon = True
    thread.start()

    return thread

def init():
    global nominees
    nominees = get_nominees(categories)

def read(tweets='data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    while(1):
        tweet = json.loads(f.readline());
        pp.pprint(tweet)
        raw_input('Hit Enter: ')

    return

def parse(tweets='../data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    count = 0
    line = f.readline()
    while(line != ''):
        tweet = json.loads(line)
        tweet_string = tweet["text"]
        
        # nominee = is_useful_tweet(tweet_string)
        # if "Best" in tweet_string and nominee and "wins" in tweet_string:
        #     if not is_wishful_tweet(tweet_string.lower()):
        #         process(nominee)

        # # presenter = is_presenter_tweet(tweet_string)
        # # if  is_presenterList(tweet_string.lower()):
        # #     if presenter in tweet_string:
        # #         pp.pprint(presenter)

        # # RED CARPET
        # if not is_retweet(tweet_string) and is_red_carpet(tweet_string) and is_best_dressed(tweet_string):
        #     tokens = tweet_string.split()
        #     tagged_tokens = nltk.pos_tag(tokens)
        #     get_red_carpet_winners("best", tagged_tokens)

        # if not is_retweet(tweet_string) and is_red_carpet(tweet_string) and is_worst_dressed(tweet_string):
        #     tokens = tweet_string.split()
        #     tagged_tokens = nltk.pos_tag(tokens)
        #     get_red_carpet_winners("worst", tagged_tokens)

        if not is_retweet(tweet_string) and is_red_carpet(tweet_string) and "http:" in tweet_string:
            # print "found one"
            tokens = tweet_string.split()

            for tok in tokens:
                if "http:" in tok:
                    url = tok
                    break
            if url:
                if (url[-1] == '"') or (url[-1] == u'\u201d'):
                    url = url[:-1]
                url = url.encode('utf-8')
                try:
                    hdr = {'User-Agent': 'Mozilla/5.0'}
                    req = urllib2.Request(url, headers=hdr)
                    expanded_url = urllib2.urlopen(req).url

                    if "instagram" in expanded_url:
                        display = Display(visible=0, size=(800, 600))
                        display.start()
                        
                        driver = webdriver.Firefox()
                        driver.get(expanded_url)
                        soup = bs4.BeautifulSoup(driver.page_source)
                        div = soup.find('div', {'id':'iImage_0'})
                        style = div['style']

                        img_url = style[21:-2]

                        print img_url

                        driver.quit()
                        display.stop()

                except urllib2.HTTPError, e:
                    expanded_url = ""
                    pass

            
        # # PARTY
        # if not is_retweet(tweet_string) and is_a_party(tweet_string):
        #     for word in tweet_string.split(" "):
        #         if word[:1] == "@":
        #             if not word == "@" and not word == "@goldenglobes":
        #                 parties.append(word.lower())

        # if count%100000 == 0:
        #     print '\rCount: ',count,
        #     sys.stdout.flush()
        print '\rCount: ',count,
        count+=1

        line = f.readline()

    return

def process(nominee):
    relevant = update_relevant_categories(nominee)

def process_presenters(presenter, category):
     for cat in categories:
        if cat == category:
            cat['presenters'].append(presenter)

def get_current_winners():
    # for category in categories:
    #     print bcolors.HEADER + '[CATEGORY] ' + bcolors.ENDC,
    #     print category['category']
    #     print bcolors.OKBLUE + '[PRESENTERS] ' + bcolors.ENDC,
    #     for presenter in category['presenters']:
    #         print presenter, 
    #     print
    #     category['nominees'].sort(key=lambda nominee: nominee['score'], reverse=True)
    #     print bcolors.OKBLUE + '[WINNER] ' + bcolors.ENDC,
    #     print category['nominees'][0]['name']
    #     print bcolors.OKBLUE + '[SCORE] ' + bcolors.ENDC, 
    #     print category['nominees'][0]['score']
    #     print ''
    return categories

def get_current_red_carpet():
    return { 'best_dressed': best_dressed, 'worst_dressed': worst_dressed }

def get_current_parties():
    return parties

def get_nominees(categories):
    nominees = []
    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] not in categories:
                # remove "," to remove movie title
                if ", " in nominee['name']:
                    nominee['name'] = nominee['name'][:nominee['name'].index(",")]
                nominees.append(nominee['name'])
    return nominees

def get_mentioned_nominees(tweet):
    mentioned = []

    for nominee in nominees:
        if nominee in tweet:
            mentioned.append(nominee)

    return mentioned

def get_red_carpet_winners(category, tagged_tokens):
    for tok in xrange(0,len(tagged_tokens)-1,2):
        flag = False
        for word in stop_words:
            if word == tagged_tokens[tok][0]:
                flag = True

        if (tagged_tokens[tok][0] == "Golden") and (tagged_tokens[tok+1][0] == "Globes" or tagged_tokens[tok+1][0] == "Globe"):
            continue

        if (tagged_tokens[tok][0] == "Red") and (tagged_tokens[tok+1][0] == "Carpet"):
            continue                

        if tagged_tokens[tok][0][0].islower() or tagged_tokens[tok+1][0][0].islower():
            continue

        if tagged_tokens[tok][0].isupper() or tagged_tokens[tok+1][0].isupper():
            continue

        for symbol in punct:
            if symbol in tagged_tokens[tok][0] or symbol in tagged_tokens[tok+1][0]:
                flag = True

        if flag:
            continue

        if tagged_tokens[tok][1] == "NNP" and tagged_tokens[tok+1][1] == "NNP":
            name = tagged_tokens[tok][0] + " " + tagged_tokens[tok+1][0]
            
            if category == "best":
                if name in best_dressed.keys():
                    best_dressed[name] += 1
                else:
                    best_dressed[name] = 1
            else:
                if name in worst_dressed.keys():
                    worst_dressed[name] += 1
                else:
                    worst_dressed[name] = 1
    return

def update_relevant_categories(mentioned):
    relevant = []

    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] in mentioned:
                relevant.append(category)
                nominee['score'] += 1

    return relevant

def is_retweet(tweet):
    if tweet[:4] == "RT @":
        return True
    return False

def is_useful_tweet(tweet):
    if is_retweet(tweet):
        return False

    for nominee in nominees:
        if nominee in tweet:
            return nominee
    return False

def is_wishful_tweet(tweet):
    for word in wishStrings:
        if word in tweet:
            return True
    return False

def is_a_party(tweet):
    partyStrings = ["parties", "party"];
    
    for partyString in partyStrings:
        if partyString in tweet:
            return True
            
    return False

def is_presenter_tweet(tweet):
    if is_retweet(tweet):
        return False

    for presenter in presenters:
        if presenter in tweet:
            return presenter
    return False

def is_presenterList(tweet):
    for word in presentStrings:
        if word in tweet:
            return True
    return False

def is_red_carpet(tweet):
    redCarpetStrings = ['redcarpet', 'RedCarpet']
    for word in redCarpetStrings:
        if word in tweet:
            return True
    return False

def is_best_dressed(tweet):
    bestDressedStrings = ['bestdressed', 'BestDressed']
    for word in bestDressedStrings:
        if word in tweet:
            return True
    return False

def is_worst_dressed(tweet):
    worstDressedStrings = ['worstdressed', 'WorstDressed']
    for word in worstDressedStrings:
        if word in tweet:
            return True
    return False

def afterEventStart(time):
    date_array = time.split(" ")
    return date_array[0] == "Mon" and  date_array[3] > "01"

