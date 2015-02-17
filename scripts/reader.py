from threading import Thread, Event
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper
import sys
import os
import sys
# import urllib2
# import bs4
# import selenium.webdriver as webdriver
# from pyvirtualdisplay import Display
import time
<<<<<<< HEAD
import copy
=======
import timeit
>>>>>>> e04348c21b5eea54f3a80644c7658691d7b6e8ad

#### DEBUG ####
pp = pprint.PrettyPrinter()

#### WEB MODE INTEGRATION ####
MODE = 2015
RUNNING_THREAD = False
INTERRUPT = False

#### KEYWORD STRINGS ####
winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
loseStrings = ['lose', 'losing', 'lost']
negStrings = ["afraid", "angry", "annoyed", "ashamed", "awful", "bad", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "congrats", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
# negStrings = []
# posStrings = []
wishStrings = ["hope", "hoping", "if", "luck"]
presentStrings = ["presenting", "present", "presented", "presenter", "presents"]

#### TOOL LISTS ####
punct = ["!", ",", ".", "&", "@", "#", "-", "'", "("]
stop_words = nltk.corpus.stopwords.words('english')

#### GLOBAL TRACKERS ####
nominees = []
categories = []
parties = []
presenters = []
best_dressed = {}
worst_dressed = {}
sentiments = {}

##############################
######### THREADING ##########
##############################

def run(tweets='data/goldenglobes2015.json'):  
    init(tweets)
    print 'Starting on set {0}.'.format(str(MODE))

    global INTERRUPT
    INTERRUPT = Event()
    thread = Thread(target=parse, args={tweets})
    thread.daemon = True
    thread.start()
    
    global RUNNING_THREAD
    RUNNING_THREAD = thread

    return thread

##############################
##### SETUP ALL GLOBALS ######
##############################

def init(tweets):
    global MODE
    global categories
    global nominees
    global sentiments
    # global negStrings
    # global posStrings
    
    if (INTERRUPT):
        INTERRUPT.set()
        time.sleep(1)

    if tweets[len(tweets) - 6] == '3':
        MODE = 2013
        categories = nominee_scraper.get2013()
    else:
        MODE = 2015
        categories = nominee_scraper.get2015()

    nominees = get_nominees(categories)
    sentiments['upvote'] = 0
    sentiments['downvote'] = 0
    # negStrings = get_strings('scripts/negativewords')
    # posStrings = get_strings('scripts/positivewords')

def get_strings(fn):
    f = open(fn)

    words = []
    for line in f:
        words.append(line.lower().strip('\n'))

    return words

##############################
###### READ DATA STREAMS #####
##############################

def read_stream(tweets):
    thread = run(tweets)

    while (1):
        inp = raw_input('Hit Enter for results: \n')
        if inp == 'break':
            break
        # print_current_winners()
        pp.pprint(categories)
    thread.join()

def read2015(tweets='../data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    while(1):
        tweet = json.loads(f.readline());
        pp.pprint(tweet)
        raw_input('Hit Enter: ')

    return

def read2013(tweets='../data/gg2013.json'):
    f = open(tweets, 'r')
    f = eval(f.readline())

    i = 0
    print 'Corpus length: {0}'.format(len(f))
    while(1):
        tweet = f[i]
        pp.pprint(tweet)
        raw_input('Hit Enter: ')
        i += 1

    return

##############################
###### PARSE ALL TWEETS ######
##############################

def parse(tweets):
    start = timeit.default_timer()
    f = open(tweets, 'r')

    if MODE == 2013:
        f = eval(f.readline())
        sys.stdout.flush()

    count = 0
    for line in f:
        if (INTERRUPT.is_set()):
            break;

        if MODE == 2015:
            tweet = json.loads(line)
            tweet_string = tweet["text"]
        else:
            tweet_string = line["text"]

        # WINNERS
        nominee = is_useful_tweet(tweet_string)
        if "Best" in tweet_string and nominee and "wins" in tweet_string:
            if not is_wishful_tweet(tweet_string.lower()):
                process(nominee)
        

        if not is_retweet(tweet_string) and is_presents(tweet_string):
            tokens = tweet_string.split()
            pos_tokens = copy.deepcopy(tokens)
            if "Best" in tokens:
                index = tokens.index("Best")
                category = tokens[index::3]
                tagged_tokens = nltk.pos_tag(pos_tokens)
                name = get_name("presents", tagged_tokens)
                if name:
                    process_presenters(name, category)
                    # print presenters

        if not is_retweet(tweet_string):
            # RED CARPET
            if is_red_carpet(tweet_string) and is_best_dressed(tweet_string):
                tokens = tweet_string.split()
                tagged_tokens = nltk.pos_tag(tokens)
                get_name("best", tagged_tokens)

            if is_red_carpet(tweet_string) and is_worst_dressed(tweet_string):
                tokens = tweet_string.split()
                tagged_tokens = nltk.pos_tag(tokens)
                get_name("worst", tagged_tokens)

            # PARTY
            if is_a_party(tweet_string):
                for word in tweet_string.split(" "):
                    if word[:1] == "@":
                        if not word == "@" and not word == "@goldenglobes":
                            parties.append(word.lower())

            # SENTIMENT
            if not is_wishful_tweet(tweet_string.lower()):
                if is_happy_tweet(tweet_string.lower()):
                    sentiments['upvote'] += 1
                elif is_sad_tweet(tweet_string.lower()):
                    sentiments['downvote'] += 1

        if count%100000 == 0:
            print '\rCount: ',count,
            sys.stdout.flush()
        count+=1

    print 'Finished parsing all {0} data.'.format(str(MODE))
    print 'Took {0} seconds.'.format(timeit.default_timer() - start)

    while True:
        time.sleep(100000)

##############################
###### PROCESS RESULTS #######
##############################

def process(nominee):
    relevant = update_relevant_categories(nominee)

def process_presenters(presenter_name, category_name):
    present_obj = {}
    present_obj['category'] = ' '.join(category_name)
    present_obj['name'] = presenter_name

    presenters.append(present_obj)

def update_relevant_categories(mentioned):
    relevant = []

    global categories
    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] in mentioned:
                relevant.append(category)
                nominee['score'] += 1

    return relevant

##############################
### RETRIEVE TRACKED DATA ####
##############################

def get_current_winners():
    return categories

def get_current_red_carpet():
    return { 'best_dressed': best_dressed, 'worst_dressed': worst_dressed }

def get_current_parties():
    return parties

def get_current_sentiments():
    return sentiments

def get_nominees(categories):
    nominee_list = []
    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] not in categories:
                # remove "," to remove movie title
                if ", " in nominee['name']:
                    nominee['name'] = nominee['name'][:nominee['name'].index(",")]
                nominee_list.append(nominee['name'])
    return nominee_list

def get_mentioned_nominees(tweet):
    mentioned = []

    for nominee in nominees:
        if nominee in tweet:
            mentioned.append(nominee)

    return mentioned

def get_name(category, tagged_tokens):
    for tok in xrange(0,len(tagged_tokens)-1,2):
        flag = False
        for word in stop_words:
            if word == tagged_tokens[tok][0]:
                flag = True

        if (tagged_tokens[tok][0] == "Golden") and (tagged_tokens[tok+1][0] == "Globes" or tagged_tokens[tok+1][0] == "Globe"):
            continue

        if (tagged_tokens[tok][0] == "Red") and (tagged_tokens[tok+1][0] == "Carpet"):
            continue

        if (tagged_tokens[tok][0] == "Best"):
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
            elif category == "worst":
                if name in worst_dressed.keys():
                    worst_dressed[name] += 1
                else:
                    worst_dressed[name] = 1
            elif category == "presents":
                return name
    return

def update_relevant_categories(mentioned):
    relevant = []

    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] in mentioned:
                relevant.append(category)
                nominee['score'] += 1

    return relevant

##############################
#### TWEET CATEGORIZATION ####
##############################

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
    # for word in wishStrings:
    #     if word in tweet:
    #         return True
    # return False
    if any([i in tweet for i in wishStrings]):
        return True
    return False

def is_happy_tweet(tweet):
    if any([i in tweet for i in posStrings]):
        return True
    return False

def is_sad_tweet(tweet):
    if any([i in tweet for i in negStrings]):
        return True
    return False

def is_a_party(tweet):
    partyStrings = ["parties", "party"];

    if any([i in tweet for i in partyStrings]):
        return True    
    # for partyString in partyStrings:
    #     if partyString in tweet:
    #         return True
            
    return False

def is_presents(tweet):
    for word in presentStrings:
        if word in tweet:
            return True
    return False

def is_red_carpet(tweet):
    redCarpetStrings = ['redcarpet', 'RedCarpet']
    if any([i in tweet for i in redCarpetStrings]):
        return True
    return False

def is_best_dressed(tweet):
    bestDressedStrings = ['bestdressed', 'BestDressed']
    if any([i in tweet for i in bestDressedStrings]):
        return True
    return False

def is_worst_dressed(tweet):
    worstDressedStrings = ['worstdressed', 'WorstDressed']
    if any([i in tweet for i in worstDressedStrings]):
        return True
    return False

##############################
####### PRINT FUNCTIONS ######
##############################

def print_current_winners():
    for category in categories:
        print bcolors.HEADER + '[CATEGORY] ' + bcolors.ENDC,
        print category['category']
        # print bcolors.OKBLUE + '[PRESENTERS] ' + bcolors.ENDC,
        # for presenter in category['presenters']:
        #     print presenter, 
        # print
        category['nominees'].sort(key=lambda nominee: nominee['score'], reverse=True)
        print bcolors.OKBLUE + '[WINNER] ' + bcolors.ENDC,
        print category['nominees'][0]['name']
        print bcolors.OKBLUE + '[SCORE] ' + bcolors.ENDC, 
        print category['nominees'][0]['score']
        print ''
    return categories

def get_current_winners():
    # for category in categories:
    #     category['nominees'].sort(key=lambda nominee: nominee['score'], reverse=True)
    return categories

def get_presenters():
    return presenters

# read_stream('../data/goldenglobes2015.json')

