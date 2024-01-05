import json
from NCHU_nlptoolkit.cut import *
from tqdm import tqdm
from math import log

def load_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

def print_data_info(data):
    print(data.keys())
    print(data['409175'].keys())
    print(data['409175']['全文'])
    print(cut_sentence(data['409175']['全文']))

file_path = "AgriData.json"
data = load_data(file_path)
print_data_info(data)


def build_inverted_index(data):
    compact_index = {}
    total_items = len(data.items())
    with tqdm(total=total_items, desc="Building Compact Inverted Index") as pbar:
        for data_id, item in data.items():
            text = item['全文']
            tokens = cut_sentence(text)
            for token in tokens:
                if token not in compact_index:
                    compact_index[token] = []
                compact_index[token].append(data_id)
            pbar.update(1)

    total_items = len(compact_index.items())
    with tqdm(total=total_items, desc="Compacting Inverted Index") as pbar:
        for token, ids in compact_index.items():
            compact_index[token] = [(id, ids.count(id)) for id in set(ids)]
            pbar.update(1)
    
    sorted_index = {token: sorted(ids) for token, ids in compact_index.items()}
    return sorted_index

compact_index = build_inverted_index(data)
print(compact_index['水稻徒長病'])



# Serialize compact_index into a file
with open("compact_index.json", "w") as file:
    json.dump(compact_index, file)



print(compact_index['稻飛蝨'])
print(data['139485']['全文'])

def count_document_frequency(compact_index, token):
    if token in compact_index:
        return len(compact_index[token])
    else:
        return 0

token = '葡萄'
document_frequency = count_document_frequency(compact_index, token)
print(document_frequency)


def remove_single_tokens(compact_index):
    filtered_index = {token: ids for token, ids in compact_index.items() if len(token) > 1}
    return filtered_index

filtered_index = remove_single_tokens(compact_index)
print(filtered_index['水稻徒長病'])



def count_top_tokens(compact_index, n=10):
    token_frequency = {token: len(ids) for token, ids in compact_index.items()}
    sorted_tokens = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)
    top_tokens = sorted_tokens[:n]
    return top_tokens

top_tokens = count_top_tokens(filtered_index, n=100)
print(top_tokens)

def get_term_frequency(compact_index, token, document_id):
    if token in compact_index:
        for id, frequency in compact_index[token]:
            if id == document_id:
                return frequency
    return 0

token = '水稻徒長病'
print(filtered_index[token])
count_document_frequency(filtered_index, token)
get_term_frequency(filtered_index, token, '154525')


def search_documents(compact_index, query_tokens, k):
    document_scores = {}
    N = len(data)  # Total number of documents in the index
    avg_dl = sum(len(data[document_id]['全文']) for document_id, _ in compact_index.values()) / N  # Average document length
    
    for token in query_tokens:
        document_frequency = count_document_frequency(compact_index, token)
        for document_id, _ in compact_index[token]:
            term_frequency = get_term_frequency(compact_index, token, document_id)
            
            # BM25 scoring formula
            k1 = 1.2
            b = 0.75
            dl = len(data[document_id]['全文'])  # Document length
            print(dl)
            idf = log((N - document_frequency + 0.5) / (document_frequency + 0.5))
            tf = ((k1 + 1) * term_frequency) / (k1 * ((1 - b) + b * (dl / avg_dl)) + term_frequency)
            
            score = idf * tf
            
            if document_id in document_scores:
                document_scores[document_id] += score
            else:
                document_scores[document_id] = score
    
    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    top_documents = sorted_documents[:k]
    return top_documents

search_documents(filtered_index, ['水稻徒長病'], 5)
print(data['21632']['全文'])