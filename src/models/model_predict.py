from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
from utils.preprocess import preprocess_text
import torch
def init(model_path: str, tokenizer_path: str):
    """
    init model
    """
    
    tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model

def predict(text: str, model, tokenizer) -> str:
    """
    predict label
    """
    try:
        label_dict = {'Order Status': 0, 
                    'Out of Domain': 1, 
                    'Delivery Time': 2, 
                    'Shipping Issues': 3}
        text = preprocess_text(text)
        inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt",max_length = 64)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        predicted = torch.argmax(logits, dim=1)
        for label, index in label_dict.items():
            if index == predicted:
                return label
    except Exception as e:
        print(e)
        return str(e)
        
    