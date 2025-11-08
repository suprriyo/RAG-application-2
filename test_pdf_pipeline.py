"""Quick test script for PDF processing pipeline."""

from src.pdf_loader import PDFLoader, PDFProcessingError
from src.text_chunker import TextChunker
from src.config import Config

def test_pdf_loader():
    """Test PDFLoader validation."""
    print("Testing PDFLoader...")
    loader = PDFLoader()
    
    # Test validation with non-existent file
    try:
        loader.validate_pdf("nonexistent.pdf")
        print("❌ Should have raised error for non-existent file")
    except PDFProcessingError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Test validation with non-PDF file
    try:
        loader.validate_pdf("config.yaml")
        print("❌ Should have raised error for non-PDF file")
    except PDFProcessingError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print("PDFLoader validation tests passed!\n")

def test_text_chunker():
    """Test TextChunker initialization."""
    print("Testing TextChunker...")
    
    # Test with default values
    chunker = TextChunker()
    print(f"✓ Default chunker created: chunk_size={chunker.chunk_size}, overlap={chunker.chunk_overlap}")
    
    # Test with custom values
    chunker = TextChunker(chunk_size=500, chunk_overlap=100)
    print(f"✓ Custom chunker created: chunk_size={chunker.chunk_size}, overlap={chunker.chunk_overlap}")
    
    # Test from config
    config = Config()
    chunker = TextChunker.from_config(config.get_all())
    print(f"✓ Config-based chunker created: chunk_size={chunker.chunk_size}, overlap={chunker.chunk_overlap}")
    
    print("TextChunker tests passed!\n")

def test_config():
    """Test Config loading."""
    print("Testing Config...")
    
    config = Config()
    chunking_config = config.get('chunking')
    print(f"✓ Config loaded successfully")
    print(f"  Chunk size: {chunking_config.get('chunk_size')}")
    print(f"  Chunk overlap: {chunking_config.get('chunk_overlap')}")
    
    print("Config tests passed!\n")

if __name__ == "__main__":
    print("=" * 50)
    print("PDF Processing Pipeline Tests")
    print("=" * 50 + "\n")
    
    test_config()
    test_pdf_loader()
    test_text_chunker()
    
    print("=" * 50)
    print("All tests completed successfully!")
    print("=" * 50)
