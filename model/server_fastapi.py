import torch
from modelfile import NN
from transformers import AutoTokenizer, AutoModel

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
from transformers import AutoTokenizer, AutoModel

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

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
    result = model.sort_notis(
        data, en_tokenizer, en_model, zh_tokenizer, zh_model)
    end_time = time.time()
    print(f'{end_time - start_time:.5f} seconds')
    #sorted_index = [ele[0] for ele in result]
    #sorted_notifications = [data[ele[0]] for ele in result]
    message_to_app = json.dumps(result,ensure_ascii=False) #10 第十個放在第一個
    del json_noti
    del data
    del start_time
    del end_time
    gc.collect()
    return message_to_app
    
# running web app in local machine

model = None

if __name__ == '__main__':

    print("Num GPUs Available: ", len(tensorflow.config.list_physical_devices('GPU')))
    en_tokenizer = AutoTokenizer.from_pretrained(
        "bert-base-uncased", output_hidden_states=True)
    en_model = AutoModel.from_pretrained(
        "bert-base-uncased", output_hidden_states=True)
    zh_tokenizer = AutoTokenizer.from_pretrained(
        "bert-base-chinese", output_hidden_states=True)
    zh_model = AutoModel.from_pretrained(
        "bert-base-chinese", output_hidden_states=True)
    
    os.system('clear') 
    
    BATCH_SIZE = 32
    DROPOUT = 0.5
    LEARNING_RATE = 3e-4
    DEVICE = "cpu"
    
    model = NN(DEVICE, LEARNING_RATE, DROPOUT)
    model.load_state_dict(torch.load('sevenclass.pt'))
    model.eval()
    uvicorn.run(app, host=HOST, port=PORT)
