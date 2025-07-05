import re
import spacy
import emoji
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

class TwitterPreprocessor:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")
        self.stopwords = set(stopwords.words('spanish') + ["pues", "oye", "eh", "bueno", "vale"])
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
    
    def clean_tweet(self, tweet):
        # Eliminar URLs y menciones
        tweet = re.sub(r"http\S+|www\S+|@\w+", "", tweet)
        
        # Convertir emojis a texto
        tweet = emoji.demojize(tweet, delimiters=(" ", " "))
        
        # Eliminar caracteres especiales (conservar hashtags)
        tweet = re.sub(r"[^\w\s#]", " ", tweet)
        
        # Tokenización y lematización
        doc = self.nlp(tweet)
        tokens = [token.lemma_.lower() for token in doc 
                 if not token.is_stop and token.lemma_ not in self.stopwords and len(token.lemma_) > 2]
        
        return " ".join(tokens)
    
    def tokenize(self, text):
        return [token.text for token in self.nlp(text)]
