"""Vector store manager for ChromaDB operations."""

# store or search vectors


from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document


class VectorStoreManager:
   
    
    def __init__(self, embedding_service, persist_directory: str = "./data/chroma_db", 
                 collection_name: str = "educational_docs"):
      
        self.embedding_service = embedding_service
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self._vector_store = None
    
    def _get_vector_store(self) -> Chroma:
        
        if self._vector_store is None:
            self._vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_service._embeddings,
                persist_directory=self.persist_directory
            )
        return self._vector_store
    
    def add_documents(self, documents: List[Document]) -> List[str]:
       
        try:
            vector_store = self._get_vector_store()
            ids = vector_store.add_documents(documents)
            return ids
        except Exception as e:
            raise Exception(f"Failed to add documents to vector store: {e}")
    
    def similarity_search(self, query: str, k: int = 4, 
                         score_threshold: Optional[float] = None) -> List[Document]:
        
        try:
            vector_store = self._get_vector_store()
            
            # ChromaDB uses distance metrics where lower is better
           
            documents = vector_store.similarity_search(query, k=k)
            
            return documents
        except Exception as e:
            raise Exception(f"Failed to perform similarity search: {e}")

    def get_collection_info(self) -> dict:
      
        try:
            vector_store = self._get_vector_store()
            collection = vector_store._collection
            
            return {
                "name": self.collection_name,
                "count": collection.count(),
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {
                "name": self.collection_name,
                "count": 0,
                "persist_directory": self.persist_directory,
                "error": str(e)
            }
    
    def clear_all_documents(self) -> bool:
       
        try:
            vector_store = self._get_vector_store()
            collection = vector_store._collection
            
           
            all_ids = collection.get()['ids']
            
           
            if all_ids:
                collection.delete(ids=all_ids)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to clear documents: {e}")
    
    def delete_collection(self) -> bool:
        
        try:
            if self._vector_store is not None:
                self._vector_store.delete_collection()
                self._vector_store = None
            return True
        except Exception as e:
            raise Exception(f"Failed to delete collection: {e}")
