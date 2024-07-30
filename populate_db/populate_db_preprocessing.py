import csv
import json

INPUT='/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/orignal_text_csv.csv'
OUTPUT='/home/magellan/envs/vericaptcha_prototype_mongodb/project_files/data/orignal_text_json.json'

documents = []

with open(INPUT, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
            documents.append({"sentence": row[1]})

with open(OUTPUT, mode='w') as json_file:
    json.dump(documents, json_file, indent=4)