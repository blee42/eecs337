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
                "method": "",
                "method_description": ""
                },
            "presenters": {
                "method": "",
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

for category in winners:
    award = {}
    award["winner"] = category["nominees"][0]["name"].encode('utf-8')
    award["nominees"] = map(lambda x: x["name"].encode('utf-8'), category["nominees"])
    award["presenters"] = []
    result["data"]["structured"][category["category"]] = award

    result["data"]["unstructured"]["winners"].append(award["winner"])
    result["data"]["unstructured"]["awards"].append(category["category"])

    for nominee in award["nominees"]:
        result["data"]["unstructured"]["nominees"].append(nominee)
    
    for presenter in award["presenters"]:
        result["data"]["unstructured"]["presenters"].append(presenter)

with io.open('result.json', 'w', encoding='utf-8') as f:
     f.write(unicode(json.dumps(result)))
