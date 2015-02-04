
def main(tweets='goldenglobes2015.json'):
    f = open(tweets, 'r')

    while (1):
        tweet = f.readline()
        print tweet
        raw_input('Hit Enter: ')

    return