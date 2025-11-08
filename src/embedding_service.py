"""Embedding service for generating vector embeddings."""

# convert text to vectors

import time
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:

    
    def __init__(self, provider: str = "openai", model: str = "text-embedding-ada-002"):
     
        self.provider = provider.lower()
        self.model = model
        self._embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
       
        if self.provider == "openai":
            return OpenAIEmbeddings(model=self.model)
        elif self.provider == "huggingface":
            return HuggingFaceEmbeddings(model_name=self.model)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
    
    def embed_documents(self, texts: List[str], max_retries: int = 3) -> List[List[float]]:
       
        for attempt in range(max_retries):
            try:
                embeddings = self._embeddings.embed_documents(texts)
                return embeddings
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt 
                    print(f"Embedding attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to generate embeddings after {max_retries} attempts: {e}")
    
    def embed_query(self, text: str, max_retries: int = 3) -> List[float]:
       
        for attempt in range(max_retries):
            try:
                embedding = self._embeddings.embed_query(text)
                return embedding
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt 
                    print(f"Query embedding attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to generate query embedding after {max_retries} attempts: {e}")
