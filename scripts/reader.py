from threading import Thread
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper
import sys
import os

#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

pp = pprint.PrettyPrinter()

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
wishStrings = ["hope", "hoping", "if", "luck"]
nominees = []
categories = nominee_scraper.main()

def test():
    return "hello world"


def main():
    init()

    thread = Thread(target = parse, args = {})
    thread.daemon = True
    thread.start()

    while (1):
        inp = raw_input('Hit Enter for results: \n')
        if inp == 'break':
            break
        get_current_winners()
        return categories

    thread.join()

def init():
    global nominees
    nominees = get_nominees(categories)

def read(tweets='../data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    while(1):
        tweet = json.loads(f.readline());
        pp.pprint(tweet)
        raw_input('Hit Enter: ')

    return

def parse(tweets='data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    count = 0
    line = f.readline()
    while(line != ''):
        tweet = json.loads(line)
        tweet_string = tweet["text"]
        nominee = is_useful_tweet(tweet_string)
        if "Best" in tweet_string and nominee and "wins" in tweet_string:
            if not is_wishful_tweet(tweet_string.lower()):
                process(nominee)

        # if count%1000 == 0:
        print '\rCount: ',count,
        sys.stdout.flush()
        count+=1

        line = f.readline()
    return

def process(nominee):
    # mentioned = get_mentioned_nominees(tweet)
    relevant = update_relevant_categories(nominee)

    # print "[MENTIONED] ", mentioned
    # print "[RELEVANT] ", relevant

def get_current_winners():
    for category in categories:
        print bcolors.HEADER + '[CATEGORY] ' + bcolors.ENDC,
        print category['category']
        category['nominees'].sort(key=lambda nominee: nominee['score'], reverse=True)
        print bcolors.OKBLUE + '[WINNER] ' + bcolors.ENDC,
        print category['nominees'][0]['name']
        print bcolors.OKBLUE + '[SCORE] ' + bcolors.ENDC, 
        print category['nominees'][0]['score']
        print ''
    return

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

def update_relevant_categories(mentioned):
    relevant = []

    for category in categories:
        for nominee in category["nominees"]:
            if nominee['name'] in mentioned:
                relevant.append(category)
                nominee['score'] += 1

    return relevant

def is_useful_tweet(tweet):
    if tweet[:4] == "RT @":
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

def afterEventStart(time):
    date_array = time.split(" ")
    return date_array[0] == "Mon" and  date_array[3] > "01"

