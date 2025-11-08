"""Text chunking module for RAG QA System."""

# split text into chunks

from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class TextChunker:
    
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
     
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
       
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'TextChunker':
     
        chunking_config = config.get('chunking', {})
        chunk_size = chunking_config.get('chunk_size', 1000)
        chunk_overlap = chunking_config.get('chunk_overlap', 200)
        
        return cls(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
