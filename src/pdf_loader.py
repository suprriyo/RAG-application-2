"""PDF loading and validation module for RAG QA System."""

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document


class PDFProcessingError(Exception):
    
    pass


class PDFLoader:
   
    
    MAX_FILE_SIZE_MB = 100
    
    def __init__(self):
       
        pass
    
    def validate_pdf(self, file_path: str) -> bool:
       
        if not os.path.exists(file_path):
            raise PDFProcessingError(f"File not found: {file_path}")
        
       
        if not os.path.isfile(file_path):
            raise PDFProcessingError(f"Path is not a file: {file_path}")
        
     
        if not file_path.lower().endswith('.pdf'):
            raise PDFProcessingError(f"File is not a PDF: {file_path}")
        
     
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise PDFProcessingError(
                f"File size ({file_size_mb:.2f}MB) exceeds maximum allowed size "
                f"({self.MAX_FILE_SIZE_MB}MB)"
            )
        
        return True
    
    def load(self, file_path: str) -> List[Document]:
       
        try:
          
            self.validate_pdf(file_path)
            
         
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            if not documents:
                raise PDFProcessingError(f"No content extracted from PDF: {file_path}")
            
            return documents
            
        except PDFProcessingError:
          
            raise
        except Exception as e:
           
            raise PDFProcessingError(
                f"Failed to load PDF '{file_path}': {str(e)}"
            ) from e
