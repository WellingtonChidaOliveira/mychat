import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')

class CleanTextUseCase:
    def __init__(self, text: str):
        self.text = text

    def execute(text):
        stop_words = set(stopwords.words('portuguese'))
        
        text = re.sub(r'[^a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+', '', text)
        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words and word.isalpha()]
        return words