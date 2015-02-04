import json
import pprint

def main(tweets='goldenglobes2015.json'):
	pp = pprint.PrettyPrinter()
	f = open(tweets, 'r')

	while(1):
		tweet = json.loads(f.readline());
		pp.pprint(tweet)
		raw_input('Hit Enter: ')

	return