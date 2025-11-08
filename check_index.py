"""Quick script to check ChromaDB indexing configuration."""

from src.rag_engine import RAGEngine

# Initialize engine
engine = RAGEngine()

# Get the vector store
vector_store = engine.vector_store_manager._get_vector_store()

# Get collection metadata
collection = vector_store._collection

print("=" * 60)
print("ChromaDB Collection Information")
print("=" * 60)
print(f"Collection Name: {collection.name}")
print(f"Total Documents: {collection.count()}")
print("\nMetadata:")
print(collection.metadata)
print("=" * 60)
