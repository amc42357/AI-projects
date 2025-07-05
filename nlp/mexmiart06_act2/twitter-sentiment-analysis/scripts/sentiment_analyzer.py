from transformers import pipeline
import numpy as np

class SentimentAnalyzer:
    def __init__(self, model_name="finiteautomata/beto-sentiment-analysis"):
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
            tokenizer=model_name
        )
    
    def predict_sentiment(self, text):
        if not text.strip():
            return "NEU"
        
        try:
            result = self.classifier(text[:512])  # Limitar a longitud máxima de BERT
            return result[0]['label']
        except Exception as e:
            print(f"Error en análisis de sentimiento: {e}")
            return "NEU"
    
    def predict_batch(self, texts):
        return [self.predict_sentiment(text) for text in texts]
    
    def predict_probabilities(self, text):
        result = self.classifier(text[:512], return_all_scores=True)
        return {item['label']: item['score'] for item in result[0]}
