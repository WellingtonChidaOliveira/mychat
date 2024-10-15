import PyPDF2
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import faiss
import pandas as pd

# Download de recursos do NLTK
nltk.download('stopwords')

# Função para extrair texto de um PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Função para pré-processar o texto
def preprocess_text(text):
    # Tokenização, remoção de stop words e outras etapas de pré-processamento
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in words if word not in stop_words]
    return words

# Carregar os PDFs e extrair o texto
file_paths = ['C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-adaptacao-climatica-nacional.pdf',
              'C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-climatica-agro.pdf']
texts = [extract_text_from_pdf(file_path) for file_path in file_paths]

# Pré-processar os textos
processed_texts = [preprocess_text(text) for text in texts]

# Criar a matriz TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_texts)

# Clustering (K-means como exemplo)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

# Criar o índice FAISS
index = faiss.IndexFlatL2(X.shape[1])
index.add(X.toarray())

# Associar os clusters aos níveis de aplicação (manualmente neste exemplo)
# Uma abordagem mais sofisticada seria usar técnicas de classificação para determinar o nível automaticamente
cluster_labels = kmeans.labels_
levels = ['nacional', 'agro']

# Criar um DataFrame para facilitar a análise
df = pd.DataFrame({'text': processed_texts, 'cluster': cluster_labels, 'level': levels})

# Exibir os resultados
print(df)

# Para realizar uma busca:
query = 'mudanças climáticas no setor agrícola'
query_vec = vectorizer.transform([query])
D, I = index.search(query_vec, k=1)
print(df.iloc[I[0]])