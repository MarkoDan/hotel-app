import json 

with open('data.json', 'r', encoding='utf-8') as fixture_file:
    try:
        data = json.load(fixture_file)
        print('')