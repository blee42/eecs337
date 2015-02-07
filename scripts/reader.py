import json
import pprint
import nltk
import gg_scraper

#winStrings = ['win', 'congrats', 'winner', 'winning', 'good job', ' won ', ]
#loseStrings = ['lose', 'losing', 'lost']

negStrings = ["afraid", "angry", "annoyed", "anxious", "arrogant", "ashamed", "awful", "bad", "bewildered", "bored", "concerned", "condemned", "confused", "creepy", "cruel", "dangerous", "defeated", "defiant", "depressed", "disgusted", "disturbed", "doubtful", "eerie", "embarrassed", "envious", "evil", "fierce", "foolish", "frantic", "frightened", "grieving", "guilty", "helpless", "hungry", "hurt", "ill", "jealous", "lonely", "mad", "naughty", "nervous", "obnoxious", "outrageous", "panicky", "repulsive", "safe", "scared", "shy", "sleepy", "sore", "strange", "tense", "terrible", "tired", "troubled", "unusual", "upset", "uptight", "weary", "wicked", "worried"]
posStrings = ["agreeable", "alert", "amused", "brave", "bright", "charming", "cheerful", "comfortable", "cooperative", "courageous", "delightful", "determined", "eager", "elated", "enchanting", "encouraging", "energetic", "enthusiastic", "excited", "exuberant", "faithful", "fantastic", "friendly", "frowning", "funny", "gentle", "glorious", "good", "happy", "healthy", "helpful", "hilarious", "innocent", "jolly", "kind", "lively", "lovely", "lucky", "obedient", "perfect", "proud", "relaxed", "relieved", "silly", "smiling", "splendid", "successful", "thoughtful", "victorious", "vivacious", "well", "witty", "wonderful"];

def main(tweets='data/goldenglobes2015.json'):
	pp = pprint.PrettyPrinter()
	f = open(tweets, 'r')

	while(1):
		tweet = json.loads(f.readline());
		pp.pprint(tweet)
		raw_input('Hit Enter: ')

	return

def parse(tweets='data/goldenglobes2015.json'):
	pp = pprint.PrettyPrinter()

	categories = gg_scraper.main()
	f = open(tweets, 'r')

	while(1):
		tweet = json.loads(f.readline())
		tweetString = tweet["text"]

		if tweet["created_at"] > "Sun Jan 12 00":

			#pp.pprint(tweetString)

			for posString in posStrings:
				if posString in tweetString:
					pp.pprint(tweetString)

			for negString in negStrings:
				if negString in tweetString:
					pp.pprint(tweetString)

					#match tweet to winner

					# for category in categories:
					# 	# TODO make dump of nominees

					# 	for nominee in category["nominees"]:

					# 		#if nominee in tweet:
					# 			print(nominee)
					# 			print(tweet)

	return






