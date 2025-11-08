"""Quick test to verify Config and RAGEngine implementation."""

from src.config import Config, ConfigError
from src.rag_engine import RAGEngine

def test_config():
    """Test Config class."""
    print("Testing Config class...")
    
    try:
        # Test loading config
        config = Config()
        print(" Config loaded successfully")
        
        # Test getting values
        embedding_provider = config.get('embedding.provider')
        print(f" Embedding provider: {embedding_provider}")
        
        chunk_size = config.get('chunking.chunk_size')
        print(f" Chunk size: {chunk_size}")
        
        # Test getting section
        llm_config = config.get_section('llm')
        print(f"LLM config: {llm_config}")
        
        print(" Config tests passed!\n")
        return True
        
    except ConfigError as e:
        print(f" Config error: {e}\n")
        return False
    except Exception as e:
        print(f" Unexpected error: {e}\n")
        return False

def test_rag_engine():
    """Test RAGEngine initialization."""
    print("Testing RAGEngine class...")
    
    try:
        # Test initialization
        engine = RAGEngine()
        print(" RAGEngine initialized successfully")
        
        
        db_info = engine.get_database_info()
        print(f"Database info: {db_info}")
        
    
        history = engine.get_conversation_history()
        print(f"Conversation history: {len(history)} items")
        
        print(" RAGEngine tests passed!\n")
        return True
        
    except Exception as e:
        print(f" Error: {e}\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Application Orchestration Layer")
    print("=" * 60)
    print()
    
    config_ok = test_config()
    engine_ok = test_rag_engine()
    
    print("=" * 60)
    if config_ok and engine_ok:
        print(" All tests passed!")
    else:
        print(" Some tests failed")
    print("=" * 60)
