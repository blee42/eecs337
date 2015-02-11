from reader import init, parse, get_current_winners

init()
parse()
winners = get_current_winners()

result = {
    "metadata": {
        "year": 2015,
        "hosts": {
            "method": "Hardcoded",
            "method_description": ""
            },
        "nominees": {
            "method": "Scraped",
            "method_description": ""
            },
        "awards": {
            "method": "",
            "method_description": ""
            },
        "presenters": {
            "method": "",
            "method_description": ""
            }
        },
    "data": {
        "unstructured": {
            "hosts": [],
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
    result["data"]["structured"][category["category"]] = award

f = open('result.json', 'w')
print str(result) >> f
f.close()















