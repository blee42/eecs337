import json
import pprint
import nltk
import nominee_scraper

#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];
nominees = []

def read(tweets='../data/goldenglobes2015.json'):
	pp = pprint.PrettyPrinter()
	f = open(tweets, 'r')

	while(1):
		tweet = json.loads(f.readline());
		pp.pprint(tweet)
		raw_input('Hit Enter: ')

	return

def parse(tweets='../data/goldenglobes2015.json'):
	pp = pprint.PrettyPrinter()

	categories = nominee_scraper.main()
	nominees = getNominees(categories)

	f = open(tweets, 'r')

	count = 0
	while(1):
		tweet = json.loads(f.readline())

		tweetString = tweet["text"]

		if "best" in tweetString and isUsefulTweet(tweetString):
 			pp.pprint(tweetString)

			# check if tweet is positive emotion
			# for posString in posStrings:
			# 	if posString in tweetString:		

		if count%1000 == 0:
			print count
		count+=1
	return

def getNominees(categories):
	for category in categories:
		for nominee in category["nominees"]:
			if nominee not in categories:
				# remove "," to remove movie title
				if ", " in nominee:
					nominee = nominee[:nominee.index(",")]
				nominees.append(nominee)
	return nominees

def afterEventStart(time):
	dateArray = time.split(" ")
	return dateArray[0] == "Mon" and  dateArray[3] > "01"

def isUsefulTweet(string):
	if string[:4] == "RT @":
		return False

	for nominee in nominees:
		if nominee in string:
			return True
	return False
