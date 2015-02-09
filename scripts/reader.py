from threading import Thread
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper

#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

pp = pprint.PrettyPrinter()

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
nominees = []
categories = nominee_scraper.main()

def main():
    init()

    thread = Thread(target = parse, args = {})
    thread.daemon = True
    thread.start()

    while (1):
        raw_input('Hit Enter for results: ')
        get_current_winners()

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

def parse(tweets='../data/goldenglobes2015.json'):
    f = open(tweets, 'r')

    count = 0
    while(1):
        tweet = json.loads(f.readline())

        tweet_string = tweet["text"]

        if "best" in tweet_string and is_useful_tweet(tweet_string):
            # pp.pprint(tweet_string)
            process(tweet_string)

            # check if tweet is positive emotion
            # for posString in posStrings:
            #   if posString in tweet_string:        

        # if count%1000 == 0:
        #     print count
        count+=1
    return

def process(tweet):
    mentioned = get_mentioned_nominees(tweet)
    relevant = update_relevant_categories(mentioned)

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
            return True
    return False

def afterEventStart(time):
    date_array = time.split(" ")
    return date_array[0] == "Mon" and  date_array[3] > "01"

