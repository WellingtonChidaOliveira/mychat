import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')

class CleanTextUseCase:
    def __init__(self):
        pass

    def execute(self, text):
        stop_words = set(stopwords.words('portuguese'))
        
        text = re.sub(r'[^a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+', '', text)
        words = word_tokenize(text)
        words = [word for word in words if word not in stop_words and word.isalpha()]
        return words