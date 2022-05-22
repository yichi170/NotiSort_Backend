import os
import gc
import json
import time
import warnings
import numpy as np
import tensorflow
import uvicorn
from tensorflow import keras
from functools import cmp_to_key
from keras.models import load_model
from fastapi import Body, FastAPI
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

# load prediction model

def bertVector( string ):
    if string == '0' or string != string:
        string = '[PAD]'
    if len(string) > 200:
        string = string[:200]

    input_ = tokenizer.encode( string , return_tensors='pt')
    v = np.mean(embedding(input_).last_hidden_state.detach().numpy(), axis=1) # shape (1, 768) 取 mean當作句向量
    
    return v[0]

def wordToBert( notification ):
    bert_vector = bertVector(notification[0])+bertVector(notification[1])+bertVector(notification[2])+bertVector(notification[3])
        
    return bert_vector

def notiPairwiseScore(noti_1, noti_2):
    res1 = model.predict(np.asarray([[noti_1[1], noti_2[1]]]))[0][1]
    res2 = model.predict(np.asarray([[noti_2[1], noti_1[1]]]))[0][1]
    return res1 - res2 + 1, res2 - res1 + 1

def notiPairwiseCompare(noti_1, noti_2):
    if noti_1[2] != noti_2[2]:
        return 1 if noti_1[2] < noti_2[2] else -1
    s1, s2 = notiPairwiseScore(noti_1, noti_2)
    if s1 != s2:
        return 1 if s1 < s2 else -1
    return 1 if noti_1[0] > noti_2[0] else -1

# android_tcp_connection:

BUFSIZE = 8192 * 2
HOST = '0.0.0.0'
PORT = 5000

app = FastAPI()

@app.post('/')
async def upload_noti(json_noti: dict = Body(...)):
    # json_noti = request.get_json()
    data = json_noti['data']
    start_time = time.time()
    indexed_notifications = [[noti_index, wordToBert(ele[: -2]), 0] for noti_index, ele in enumerate(data)]
    n = len(indexed_notifications)
    
    # groups = {groupkey: sorted([noti if noti[-1] == groupkey for noti in data], key = lambda x: x[-2]) for groupkey in set([noti[-1] for noti in data])}
    groups = dict()
    for noti_index, noti in enumerate(data):
        key = int(noti[-1])
        if key not in groups:
            groups[key] = []
        groups[key].append([noti_index, *noti])
    for key in groups.keys():
        groups[key].sort(key=lambda x: x[-2])
    
    for group in groups.keys():
        print(f'{group}:')
        for noti in groups[group]:
            print(noti[3])
    
    for i in range(n):
        for j in range(i + 1, n):
            d_i, d_j = notiPairwiseScore(indexed_notifications[i], indexed_notifications[j])
            indexed_notifications[i][2] += d_i
            indexed_notifications[j][2] += d_j
    indexed_notifications.sort(key=cmp_to_key(notiPairwiseCompare))
    
    result = []

    for top_noti in indexed_notifications:
        noti_index = top_noti[0]
        noti_key = int(data[noti_index][-1]) 
        if len(groups[noti_key]) > 0:
            print(f'GROUP {noti_key}: {top_noti[2] / (n - 1)}')
            for noti in groups[noti_key]:
                print(noti[3])
            groups[noti_key] = []
            result.append(noti_key)

    end_time = time.time()
    print(f'{end_time - start_time:.5f} seconds')
    #sorted_index = [ele[0] for ele in result]
    #sorted_notifications = [data[ele[0]] for ele in result]
    message_to_app = json.dumps(result,ensure_ascii=False) #10 第十個放在第一個
    del json_noti
    del data
    del start_time
    del end_time
    del indexed_notifications
    del n
    del groups
    del result
    gc.collect()
    return message_to_app
    
# running web app in local machine

model = None
tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')
embedding = AutoModel.from_pretrained('bert-base-chinese')
os.system('clear') 
model = load_model("model_1.h5")

if __name__ == '__main__':
    print("Num GPUs Available: ", len(tensorflow.config.list_physical_devices('GPU')))
    uvicorn.run(app, host=HOST, port=PORT)
