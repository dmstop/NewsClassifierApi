import torch
from transformers import RobertaTokenizer
import logging

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        self.model = torch.load("predictor_model/roberta_predictor.pth", map_location=self.device)
        self.model.to(self.device)
        self.model.eval()
        self.classes = ['Fake', 'Real']
        self.max_length = 512
        logger.info("Model successfully loaded")

    def predict(self, text: str):
        inputs = self.tokenizer(text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors="pt")
        vec, mask = inputs['input_ids'].to(self.device), inputs['attention_mask'].to(self.device)
        with torch.inference_mode():
            pred = self.model(vec, attention_mask=mask)        
        probs = torch.softmax(pred.logits, dim=1)
        label_id = torch.argmax(probs, dim=1)
        label = self.classes[label_id]

        return label, probs.squeeze()[label_id].item()

news_classifier = Predictor()