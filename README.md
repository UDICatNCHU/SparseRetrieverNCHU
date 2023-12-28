# SparseRetrieverNCHU


import json
from NCHU_nlptoolkit.cut import *

file_path = "/Users/yaochungfan/SparseRetrieverNCHU/AgriData.json"

with open(file_path) as file:
    data = json.load(file)

print(data.keys())
print(data['409175'].keys())
doc = '首先，對區塊鏈需要的第一個理解是，它是一種「將資料寫錄的技術」。'
cut_sentence(doc, flag=True)
print(data['409175']['全文'])
print(cut_sentence(data['409175']['全文']))

empty_count = 0
for key, value in data.items():
    if value['摘要'] == '':
        empty_count += 1

print(f"Number of items with empty '全文' value: {empty_count}")


def tokenize_data(data):
    tokenized_data = {}
    for data_id, item in data.items():
        text = item['全文']
        tokens = cut_sentence(text)
        for token in tokens:
            if token not in tokenized_data:
                tokenized_data[token] = []
            tokenized_data[token].append(data_id)
    
    sorted_data = {token: sorted(ids) for token, ids in tokenized_data.items()}
    return sorted_data

invert_index = tokenize_data(data)

print(invert_index['水稻徒長病'])

data.items()
