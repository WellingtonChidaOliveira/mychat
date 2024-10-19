from nltk.tokenize import word_tokenize

class SplitTextIntoChunksUseCase:
    def __init__(self):
        pass

    # Function to split text into chunks for vectorization
    def execute(self, text, chunk_size=800, chunk_overlap=80):
        words = word_tokenize(text)
        chunks = []
        current_chunk_words = []
        for word in words:
            current_chunk_words.append(word)
            if len(current_chunk_words) >= chunk_size:
                chunks.append(' '.join(current_chunk_words[:-chunk_overlap]))
                current_chunk_words = current_chunk_words[-chunk_overlap:]
        if current_chunk_words:
            chunks.append(' '.join(current_chunk_words))
        return chunks