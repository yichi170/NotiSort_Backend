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

import torch
from tqdm import tqdm
import torchshard as ts
import pytorch_lightning as pl
from torch import nn, optim, hub
from torch.nn import functional as F

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

class NN_Indiv(pl.LightningModule):
    
    def __init__(self, dropout, lr):
        super().__init__()
        self.fc = nn.Sequential(
            ts.nn.ParallelLinear(5376, 192),
            nn.GELU(),
            nn.BatchNorm1d(192),
            nn.Dropout(dropout),
            ts.nn.ParallelLinear(192, 192),
        )
    
    def forward(self, x):
        return self.fc(x)

class NN(pl.LightningModule):
    
    def __init__(self, device, lr, dropout):
        super().__init__()
        self.lr = lr
        self.comps = nn.ModuleList(
            NN_Indiv(dropout, lr) for _ in range(8))
        self.en_fc = nn.Sequential(
            nn.GELU(),
            nn.BatchNorm1d(768),
            nn.Dropout(dropout),
            ts.nn.ParallelLinear(768, 384)
        )
        self.zh_fc = nn.Sequential(
            nn.GELU(),
            nn.BatchNorm1d(768),
            nn.Dropout(dropout),
            ts.nn.ParallelLinear(768, 384)
        )
        self.fc = nn.Sequential(
            nn.GELU(),
            nn.BatchNorm1d(768),
            nn.Dropout(dropout),
            ts.nn.ParallelLinear(768, 7)
        )
        self.pos_weights = torch.Tensor(
            [1, .8, .6, .4, .2, 0, -0.2])
        self.pos_weights.requires_grad = False
        self.criterion = hub.load(
            'adeelh/pytorch-multi-class-focal-loss',
            model='FocalLoss',
            gamma=2,
            reduction='mean',
            force_reload=False
        )
    
    def forward(self, x):
        en, zh = torch.tensor_split(
            torch.cat(
                [m(t) for m, t in zip(
                    self.comps, torch.tensor_split(x, 8, dim=1))], dim=1),
            2, dim=1)
        xx = torch.cat((self.en_fc(en), self.zh_fc(zh)), dim=1)
        return self.fc(xx)
    
    def loss_func(self, logits, y, stage):
        class_loss = self.criterion(logits, y)
        _, y_pred = torch.max(logits.data, axis=1)
        report = classification_report(y.detach().cpu(),
                                       y_pred.detach().cpu(), output_dict=True)
        for label in report:
            if label == 'accuracy':
                self.log(f'{stage}_accuracy', report[label])
            else:
                for metric in report[label]:
                    self.log(f'{stage}_{metric}_{label}', report[label][metric])
        weighted_pos = (F.softmax(logits, dim=1) * self.pos_weights).sum(axis=1)
        y_pos = 1 - y / 5
        mse_loss = F.mse_loss(weighted_pos, y_pos)
        l1_loss = F.l1_loss(weighted_pos, y_pos)
        self.log(f'{stage}_class_loss', class_loss)
        self.log(f'{stage}_mse_dis', mse_loss)
        self.log(f'{stage}_L1_dis', l1_loss)
        return class_loss + mse_loss
    
    def training_step(self, batch, idx):
        X, y = batch
        logits = self(X)
        loss = self.loss_func(logits, y, 'train')
        self.log(f'train_loss', loss)
        return loss
    
    def validation_step(self, batch, idx):
        X, y = batch
        logits = self(X)
        loss = self.loss_func(logits, y, 'val')
        self.log(f'val_loss', loss)
        return loss
    
    def sort_notis(self, data,
                   en_tokenizer, en_model, zh_tokenizer, zh_model, output_log=True, output_prob=False):
        idx = [0, 3, 1, 2, 4, 5, 6]
        text = [[row[i] for i in idx] for row in data]
        noti_id = [row[-1] for row in data]
        with torch.no_grad():
            X = torch.stack([torch.cat((
                torch.cat(en_model(
                    **en_tokenizer(
                        row, return_tensors='pt', padding=True, truncation=True
                    ), output_hidden_states=True)[2][-4: ])[:, 0].detach(),
                torch.cat(zh_model(
                    **zh_tokenizer(
                        row, return_tensors='pt', padding=True, truncation=True
                    ), output_hidden_states=True)[2][-4: ])[:, 0].detach(),
                    )) for row in tqdm(text)])
            X = X.view(X.shape[0], 8, -1)
            print(X.shape)
            logits = torch.cat([self(x.view(1, -1)) for x in X])
            _, y_pred = torch.max(logits.data, axis=1)
            weighted_pos = (F.softmax(logits, dim=1) * self.pos_weights).sum(axis=1).cpu().numpy()
            if output_prob:
                print(F.softmax(logits, dim=1))
            text_score = list(zip(text, weighted_pos, noti_id))
            print(text_score)
            text_score.sort(key=lambda x: -x[1])
            if output_log:
                for text, weighted_pos, noti_id in text_score:
                    print(noti_id, weighted_pos, text)
        print([noti[-1] for noti in text_score])
        return list(dict.fromkeys([int(noti[-1]) for noti in text_score]))
    
    @property
    def num_training_steps(self) -> int:
        """Total training steps inferred from datamodule and devices."""
        if self.trainer.max_steps:
            return self.trainer.max_steps

        limit_batches = self.trainer.limit_train_batches
        batches = len(self.train_dataloader())
        batches = min(batches, limit_batches) if isinstance(limit_batches, int) else int(limit_batches * batches)     

        num_devices = max(1, self.trainer.num_gpus, self.trainer.num_processes)
        if self.trainer.tpu_cores:
            num_devices = max(num_devices, self.trainer.tpu_cores)

        effective_accum = self.trainer.accumulate_grad_batches * num_devices
        return (batches // effective_accum) * self.trainer.max_epochs
    
    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, self.num_training_steps)
        return [optimizer], [scheduler]



BUFSIZE = 8192 * 2
HOST = '0.0.0.0'
PORT = 5000

app = FastAPI()

@app.post('/')
async def upload_noti(
    json_noti: dict = Body(
        example={
            "data": [
                ["app1", "title1", "content1",
                 "category", "STILL", "WEEKDAY",
                 "MIDNIGHT", 10000, 1], 
                ["app2", "title2", "content2",
                 "category", "STILL", "WEEKDAY",
                 "MIDNIGHT", 10000, 2], 
                ["app3", "title3", "content3",
                 "category", "STILL", "WEEKDAY",
                 "MIDNIGHT", 10000, 3]
            ]
        }
    )
):
    data = json_noti['data']
    start_time = time.time()
    result = model.sort_notis(data, en_tokenizer, en_model, zh_tokenizer, zh_model)
    end_time = time.time()
    print(f'{end_time - start_time:.5f} seconds')

    message_to_app = json.dumps(result,ensure_ascii=False) #10 第十個放在第一個
    del json_noti
    del data
    del start_time
    del end_time
    gc.collect()
    return message_to_app
    

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

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
