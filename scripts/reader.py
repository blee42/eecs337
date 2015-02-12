from threading import Thread
from colors import bcolors
import json
import pprint
import nltk
import nominee_scraper
import os
import sys

#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

pp = pprint.PrettyPrinter()

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
wishStrings = ["hope", "hoping", "if", "luck"]
punct = ["!", ",", ".", "&", "@", "#", "-", "'"]
nominees = []
categories = nominee_scraper.main()
best_dressed = {}


def main():
    init()

    thread = Thread(target = parse, args = {})
    thread.daemon = True
    thread.start()

    while (1):
        raw_input('==========REFRESH ==========')
        # get_current_winners()

        print best_dressed
        # Uncomment to send categories to view
        # return categories

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

       
        # nominee = is_useful_tweet(tweet_string)
        
        # WINNERS
        # if "Best" in tweet_string and nominee and "wins" in tweet_string:
        #     if not is_wishful_tweet(tweet_string.lower()):
        #         process(nominee)

        # PRESENTERS
        # presenter = ''
        # category = ''
        # tokens = tweet_string.lower().split()
        # if "presents" in tokens and nominee:
        #     index_presents = tokens.index("presents")
        #     for tok in tokens[:index_presents]:
        #         if tok.isupper():
        #             presenter = tok
        #     for tok in tokens[index_presents:]:
        #         category = find_category(tokens[index_presents:])
            
        # process_presenters(presenter, category)

        # RED CARPET
        if tweet_string[:4] == "RT @":
            continue
        if "RedCarpet" in tweet_string and "BestDressed" in tweet_string:
            tokens = tweet_string.split()
            # print tweet_string
            # print tokens
            tagged_tokens = nltk.pos_tag(tokens)
            # print tagged_tokens
            for tok in xrange(0,len(tagged_tokens)-1,2):
                if tagged_tokens[tok][0][0].islower() or tagged_tokens[tok+1][0][0].islower():
                    continue

                flag = False
                for symbol in punct:
                    if symbol in tagged_tokens[tok][0] or symbol in tagged_tokens[tok+1][0]:
                        flag = True
                if flag:
                    continue

                if tagged_tokens[tok][1] == "NNP" and tagged_tokens[tok+1][1] == "NNP":
                    name = tagged_tokens[tok][0] + " " + tagged_tokens[tok+1][0]
                    if name in best_dressed.keys():
                        best_dressed[name] += 1
                    else:
                        best_dressed[name] = 1
 
            # print
            # print "========================"

        if count%100000 == 0:
            print '\rCount: ',count,
            sys.stdout.flush()
        count +=1

    return

def process(nominee):
    # mentioned = get_mentioned_nominees(tweet)
    relevant = update_relevant_categories(nominee)

    # print "[MENTIONED] ", mentioned
    # print "[RELEVANT] ", relevant

def process_presenters(presenter, category):
     for cat in categories:
        if cat == category:
            cat['presenters'].append(presenter)

def get_current_winners():
    for category in categories:
        print bcolors.HEADER + '[CATEGORY] ' + bcolors.ENDC,
        print category['category']
        print bcolors.OKBLUE + '[PRESENTERS] ' + bcolors.ENDC,
        for presenter in category['presenters']:
            print presenter, 
        print
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

def find_category(tweet):
    best_category_count = 0
    best_category = ''

    for category in categories:
        for word in category['category'].split():
            count = 0
            if word.lower() in tweet:
                count +=1
        if count > best_category_count:
            best_category_count = count
            best_category = category

    return best_category


def afterEventStart(time):
    date_array = time.split(" ")
    return date_array[0] == "Mon" and  date_array[3] > "01"

