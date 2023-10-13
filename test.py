import json
import codecs

# Open the file with the source encoding (e.g., 'utf-16')
with codecs.open('data.json', 'r', encoding='utf-16') as source_file:
    data = json.load(source_file)

# Open the file with the desired encoding (e.g., 'utf-8')
with codecs.open('data.json', 'w', encoding='utf-8') as target_file:
    json.dump(data, target_file, ensure_ascii=False)
