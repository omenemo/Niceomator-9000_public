from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

class StanceDetection():
    
    def __init__(self, task):
        assert(task in ["abortion", "atheism", "climate", "feminist", "hillary"])
        self.task = task
        self.MODEL_TAG = f"cardiffnlp/twitter-roberta-base-stance-{self.task}"
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_TAG)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_TAG)
        
        # download label mapping
        self.labels=[]
        mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/stance/mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        self.labels = [row[1] for row in csvreader if len(row) > 1]
       
    
    # Preprocess text (username and link placeholders)
    def preprocess(self, text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def predict(self, text):
        text = self.preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        return {self.labels[ind]: round(i, 4) for ind, i in enumerate(softmax(scores))}