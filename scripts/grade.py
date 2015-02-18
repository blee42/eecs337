from reader import init, parse, get_current_winners
import io, json

tweets='data/goldenglobes2015.json'
init(tweets)
parse(tweets)
winners = get_current_winners()

result = {
    "metadata": {
        "year": 2015,
        "names" : {
            "hosts": {
                "method": "hardcoded",
                "method_description": ""
                },
            "nominees": {
                "method": "scraped",
                "method_description": ""
                },
            "awards": {
                "method": "detected",
                "method_description": ""
                },
            "presenters": {
                "method": "detected",
                "method_description": ""
                }
            },
        "mappings": {
            "nominees": {
                "method": "scraped",
                "method_description": ""
                },
            "presenters": {
                "method": "detected",
                "method_description": ""
                }
            }
        },
    "data": {
        "unstructured": {
            "hosts": ['Tina Fey', 'Amy Poehler'],
            "winners": [],
            "awards": [],
            "presenters": [],
            "nominees": []
        },
        "structured": {
        }
    }
}

converters = {
    'Best original score': {
        'name': 'Best Original Score - Motion Picture',
        'Johann Johannsson': 'The Theory of Everything',
        'Alexandre Desplat': 'The Imitation Game',
        'Trent Reznor & Atticus Ross': 'Gone Girl',
        'Antonio Sanchez': 'Birdman',
        'Hans Zimmer': 'Interstellar'
    },
    'Best original song': {
        'name': 'Best Original Song - Motion Picture',
        'Big Eyes': 'Big Eyes',
        'Glory': 'Selma',
        'Mercy Is': 'Noah',
        'Opportunity': 'Annie',
        'Yellow Flicker Beat': 'The Hunger Games: Mockingjay - Part 1'
    },
    'Best screenplay': {
        'name': 'Best screenplay',
        'Wes Anderson': 'The Grand Budapest Hotel',
        'Gillian Flynn': 'Gone Girl',
        'Alejandro Inarritu Gonzalez': 'Birdman',
        'Richard Linklater': 'Boyhood',
        'Graham Moore': 'The Imitation Game'
    }
}

for category in winners:
    if category['category'] in converters:
        for i in range(len(category['nominees'])):
            category['nominees'][i]['name'] = converters[category['category']][category['nominees'][i]['name']]
        category['category'] = converters[category['category']]['name']

    award = {}
    award["winner"] = category["nominees"][0]["name"].encode('utf-8')
    award["nominees"] = map(lambda x: x["name"].encode('utf-8'), category["nominees"][1:])
    award["presenters"] = []
    result["data"]["structured"][category["category"]] = award

    result["data"]["unstructured"]["winners"].append(award["winner"])
    result["data"]["unstructured"]["awards"].append(category["category"])

    for nominee in award["nominees"]:
        if nominee not in result["data"]["unstructured"]["nominees"]:
            result["data"]["unstructured"]["nominees"].append(nominee)
    
    for presenter in award["presenters"]:
        if presenter not in result["data"]["unstructured"]["presenters"]:
            result["data"]["unstructured"]["presenters"].append(presenter)

with io.open('result.json', 'w', encoding='utf-8') as f:
     f.write(unicode(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))))
