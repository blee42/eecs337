from threading import Thread, Event
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper
import sys
import os
import sys
import re
from nltk import pos_tag, ne_chunk
from nltk.tokenize import SpaceTokenizer
from nltk.tokenize import TreebankWordTokenizer
import pdb

import time
import timeit
wordTokenizer= TreebankWordTokenizer()

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
presentStrings = ["presenting", "present", "presented", "presenter"]

stopList= ["golden", "globes"  ,"drogo", "best" ,"congrats" , "actor" ,"your", "drama" , "los" , "actress" , "best" , "song" , "film" , "movie" ,"motion", "present" , "award" , "original" , "screenplay", "comedy/musical" , "comedy" , "make" , "wins" , "win"]
goodList= ["Golden Globes" "Best Actor" "Best Actress" , "Best Motion Picture" , "Best Comedy Actress" , "Best Screenplay" , "Best Comedy"]
#### TOOL LISTS ####

punct = ["!", ",", ".", "&", "@", "#", "-", "'"]
stop_words = nltk.corpus.stopwords.words('english')

#### GLOBAL TRACKERS ####
nominees = []
categories = []
parties = []
best_dressed = {}
worst_dressed = {}
sentiments = {}
Dict={}
presentersList=['Benedict Cumberbatch' , 'David Duchovny' 'Jennifer Anisto']
parsing_done=0
##############################
######### THREADING ##########
##############################

def run(tweets='../data/goldenglobes2015.json'):  
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
        INTERRUPT.clear()

    if tweets[len(tweets) - 6] == '3':
        MODE = 2013
        categories = nominee_scraper.get2013()
    else:
        MODE = 2015
        categories = nominee_scraper.get2015()

    # nominees = get_nominees(categories)
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

    # count = 0
    for presenter in presentersList:
        count=0
        for line in f:
            if (INTERRUPT.set()):
                break;

            if MODE == 2015:
                tweet = json.loads(line)
                tweet_string = tweet["text"]
            else:
                tweet_string = line["text"]

                if presenter in tweet_string:

                    cat_match=regexmatch(tweet_string)
                    

                    if cat_match:

                        count+=1

                    else :
                        continue

    print 'Finished parsing all {0} data.'.format(str(MODE))
    print 'Took {0} seconds.'.format(timeit.default_timer() - start)


def regexmatch (tweet):

    for category in categories:

        flag=0
        reg=regexx(category["category"])

            flag=1
            matchObj = re.match( reg, tweet, flag=0)

            if flag==1:
                return category["category"]
            else :
                continue

    if flag==0:
        return False






def regexx(cat):

    cat_words= cat.split()

    return generate(cat_words)


def generate(words):

    if(words =='')

        return reg


    return reg= words[0].* + generate(words[1:])
