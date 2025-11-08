"""Query processor for retrieving relevant document chunks."""

# Handles user question

from typing import List
from langchain.schema import Document


class QueryProcessor:
 
    
    def __init__(self, vector_store_manager, config: dict):
      
        self.vector_store_manager = vector_store_manager
        self.config = config
        
        retrieval_config = config.get('retrieval', {})
        self.default_top_k = retrieval_config.get('top_k', 4)
        self.score_threshold = retrieval_config.get('score_threshold')
    
    def retrieve_context(self, question: str, k: int = None) -> List[Document]:
        
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
   
        num_results = k if k is not None else self.default_top_k
        
        try:
          
            documents = self.vector_store_manager.similarity_search(
                query=question,
                k=num_results,
                score_threshold=self.score_threshold
            )
            
            return documents
            
        except Exception as e:
            raise Exception(f"Failed to retrieve context for question: {e}")
