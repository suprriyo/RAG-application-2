"""Main RAG engine orchestrator for the QA system."""

# orchaestrate everything

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from src.config import Config
from src.pdf_loader import PDFLoader, PDFProcessingError
from src.text_chunker import TextChunker
from src.embedding_service import EmbeddingService
from src.vector_store_manager import VectorStoreManager
from src.query_processor import QueryProcessor
from src.answer_generator import AnswerGenerator, Answer


@dataclass
class DocumentInfo:
   
    filename: str
    chunk_count: int
    file_size_mb: float
    status: str


class RAGEngine:
  
    
    def __init__(self, config: Optional[Config] = None):
      
        
        self.config = config if config is not None else Config()
        
       
        self._initialize_components()
        
    
        self._conversation_history: List[Dict[str, str]] = []
    
    def _initialize_components(self) -> None:
       
        self.pdf_loader = PDFLoader()
        self.text_chunker = TextChunker(
            chunk_size=self.config.get('chunking.chunk_size', 1000),
            chunk_overlap=self.config.get('chunking.chunk_overlap', 200)
        )
        
       
        embedding_config = self.config.get_section('embedding')
        self.embedding_service = EmbeddingService(
            provider=embedding_config.get('provider', 'openai'),
            model=embedding_config.get('model', 'text-embedding-ada-002')
        )
        
        storage_config = self.config.get_section('storage')
        self.vector_store_manager = VectorStoreManager(
            embedding_service=self.embedding_service,
            persist_directory=storage_config.get('persist_directory', './data/chroma_db'),
            collection_name=storage_config.get('collection_name', 'educational_docs')
        )
        
      
        self.query_processor = QueryProcessor(
            vector_store_manager=self.vector_store_manager,
            config=self.config.to_dict()
        )
        
        llm_config = self.config.get_section('llm')
        self.answer_generator = AnswerGenerator(
            provider=llm_config.get('provider', 'openai'),
            model=llm_config.get('model', 'gpt-3.5-turbo'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 500)
        )
    
    def ingest_document(self, file_path: str, show_progress: bool = True) -> DocumentInfo:
        
        try:
            filename = os.path.basename(file_path)
            
            if show_progress:
                print(f"\n Processing document: {filename}")
                print("=" * 60)
            
            
            if show_progress:
                print(" Step 1/4: Loading PDF...")
            
            documents = self.pdf_loader.load(file_path)
            
            if show_progress:
                print(f" Loaded {len(documents)} pages")
            
            
            if show_progress:
                print(" Step 2/4: Splitting into chunks...")
            
            chunks = self.text_chunker.split_documents(documents)
            chunk_count = len(chunks)
            
            if show_progress:
                print(f" Created {chunk_count} chunks")
            
           
            if show_progress:
                print(" Step 3/4: Generating embeddings...")
            
           
            
            if show_progress:
                print(" Embeddings generated")
            
         
            if show_progress:
                print(" Step 4/4: Storing in vector database...")
            
            self.vector_store_manager.add_documents(chunks)
            
            if show_progress:
                print(" Stored in database")
            
            
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            if show_progress:
                print("=" * 60)
                print(f" Document processed successfully!")
                print(f"   Filename: {filename}")
                print(f"   Chunks: {chunk_count}")
                print(f"   Size: {file_size_mb:.2f} MB")
                print()
            
            return DocumentInfo(
                filename=filename,
                chunk_count=chunk_count,
                file_size_mb=file_size_mb,
                status="success"
            )
            
        except PDFProcessingError as e:
            if show_progress:
                print(f"\n PDF Processing Error: {e}\n")
            raise
        except Exception as e:
            if show_progress:
                print(f"\n Error during document ingestion: {e}\n")
            raise Exception(f"Failed to ingest document: {e}")
    
    def ask_question(self, question: str, use_context: bool = True) -> Answer:
        """
        Answer a question using RAG with conversational memory.
        
        Args:
            question: The user's question
            use_context: Whether to use conversation history (default: True)
        
        Returns:
            Answer object with text, sources, and confidence
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            # Retrieve relevant context from documents
            context_documents = self.query_processor.retrieve_context(question)
            
            # Prepare chat history for conversational context
            chat_history = []
            if use_context and self._conversation_history:
                # Convert internal history format to chat format
                for entry in self._conversation_history:
                    chat_history.append({"role": "user", "content": entry['question']})
                    chat_history.append({"role": "assistant", "content": entry['answer']})
            
            # Generate answer with conversation history
            answer = self.answer_generator.generate_answer(
                question, 
                context_documents,
                chat_history=chat_history
            )
            
            # Store in conversation history
            self._conversation_history.append({
                'question': question,
                'answer': answer.text
            })
            
            return answer
            
        except Exception as e:
            raise Exception(f"Failed to answer question: {e}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
       
        return self._conversation_history.copy()
    
    def clear_conversation_history(self) -> None:
      
        self._conversation_history = []
    
    def get_database_info(self) -> Dict[str, Any]:
       
        return self.vector_store_manager.get_collection_info()
    
    def reset_database(self) -> bool:
        
        try:
          
            self.vector_store_manager.clear_all_documents()
            
            # Clear conversation history
            self.clear_conversation_history()
            return True
        except Exception as e:
            raise Exception(f"Failed to reset database: {e}")
