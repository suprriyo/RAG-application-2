# RAG-Based QA System Design Document

## Overview

This document outlines the design for a Retrieval-Augmented Generation (RAG) Question Answering system built with LangChain. The system processes educational PDF documents, creates vector embeddings, and answers student questions using retrieved context. The architecture follows a modular design with clear separation between document processing, storage, retrieval, and answer generation.

## Architecture

### High-Level Architecture

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     CLI Interface Layer             │
│  - Upload PDFs                      │
│  - Ask Questions                    │
│  - Display Answers                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Application Layer                 │
│  - Document Manager                 │
│  - Query Engine                     │
│  - Session Manager                  │
└──────┬──────────────────┬───────────┘
       │                  │
       ▼                  ▼
┌──────────────┐   ┌─────────────────┐
│   Document   │   │     Query       │
│  Processing  │   │   Processing    │
│   Pipeline   │   │    Pipeline     │
└──────┬───────┘   └────────┬────────┘
       │                    │
       ▼                    ▼
┌─────────────────────────────────────┐
│      LangChain Layer                │
│  - PDF Loaders                      │
│  - Text Splitters                   │
│  - Embeddings                       │
│  - Vector Stores                    │
│  - Retrieval Chains                 │
│  - LLM Integration                  │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Storage Layer                     │
│  - Vector Database (ChromaDB)       │
│  - Document Metadata Store          │
└─────────────────────────────────────┘
```

### Technology Stack

- **Framework**: LangChain (Python)
- **Vector Database**: ChromaDB (local, persistent)
- **Embeddings**: OpenAI embeddings or HuggingFace alternatives
- **LLM**: OpenAI GPT-3.5/4 or Anthropic Claude (configurable)
- **PDF Processing**: PyPDF2 via LangChain loaders
- **CLI**: Python argparse or Click
- **Configuration**: YAML + environment variables

## Components and Interfaces

### 1. Document Processing Pipeline

**Purpose**: Extract, chunk, embed, and store PDF content

**Components**:

- **PDFLoader**: Wraps LangChain's PDF loader
  ```python
  class PDFLoader:
      def load(self, file_path: str) -> List[Document]
      def validate_pdf(self, file_path: str) -> bool
  ```

- **TextChunker**: Splits documents into manageable chunks
  ```python
  class TextChunker:
      def __init__(self, chunk_size: int, chunk_overlap: int)
      def split_documents(self, documents: List[Document]) -> List[Document]
  ```

- **EmbeddingService**: Generates vector embeddings
  ```python
  class EmbeddingService:
      def __init__(self, model_name: str)
      def embed_documents(self, texts: List[str]) -> List[List[float]]
      def embed_query(self, text: str) -> List[float]
  ```

- **VectorStoreManager**: Manages vector database operations
  ```python
  class VectorStoreManager:
      def __init__(self, persist_directory: str)
      def add_documents(self, documents: List[Document], embeddings: List[List[float]])
      def similarity_search(self, query_embedding: List[float], k: int) -> List[Document]
      def get_collection_info(self) -> dict
  ```

### 2. Query Processing Pipeline

**Purpose**: Process questions and generate answers

**Components**:

- **QueryProcessor**: Handles question processing
  ```python
  class QueryProcessor:
      def process_query(self, question: str) -> str
      def retrieve_context(self, question: str, k: int) -> List[Document]
  ```

- **AnswerGenerator**: Generates answers using LLM
  ```python
  class AnswerGenerator:
      def __init__(self, llm_provider: str, model_name: str)
      def generate_answer(self, question: str, context: List[Document]) -> Answer
  ```

- **Answer Model**: Structured answer response
  ```python
  @dataclass
  class Answer:
      text: str
      sources: List[str]
      confidence: float
  ```

### 3. Application Layer

**Purpose**: Orchestrate document and query operations

**Components**:

- **DocumentManager**: Manages document lifecycle
  ```python
  class DocumentManager:
      def upload_pdf(self, file_path: str) -> str
      def list_documents(self) -> List[dict]
      def get_document_stats(self, doc_id: str) -> dict
  ```

- **RAGEngine**: Main orchestrator
  ```python
  class RAGEngine:
      def __init__(self, config: Config)
      def ingest_document(self, file_path: str) -> bool
      def ask_question(self, question: str) -> Answer
      def reset_database(self) -> bool
  ```

### 4. User Interface

**Purpose**: Provide user interaction via Streamlit web app

**Primary Interface - Streamlit Web App**:
- File uploader widget for PDF upload
- Text input for questions
- Chat interface for Q&A with history
- Sidebar for document management and settings
- Progress indicators for processing

**Secondary Interface - CLI** (for development/testing):
- `upload <pdf_path>`: Upload and process a PDF
- `ask "<question>"`: Ask a question
- `list`: List uploaded documents
- `reset`: Clear the vector database

## Data Models

### Document Metadata

```python
{
    "doc_id": "uuid",
    "filename": "textbook.pdf",
    "upload_date": "2025-11-07T10:30:00",
    "page_count": 450,
    "chunk_count": 892,
    "file_size_mb": 45.2
}
```

### Document Chunk

```python
{
    "chunk_id": "uuid",
    "doc_id": "uuid",
    "content": "text content...",
    "page_number": 42,
    "chunk_index": 15,
    "metadata": {
        "source": "textbook.pdf",
        "page": 42
    }
}
```

### Configuration Schema

```yaml
# config.yaml
embedding:
  provider: "openai"  # or "huggingface"
  model: "text-embedding-ada-002"

llm:
  provider: "openai"  # or "anthropic"
  model: "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 500

chunking:
  chunk_size: 1000
  chunk_overlap: 200

retrieval:
  top_k: 4
  score_threshold: 0.7

storage:
  persist_directory: "./data/chroma_db"
  collection_name: "educational_docs"
```

## Error Handling

### Error Categories

1. **PDF Processing Errors**
   - Invalid PDF format
   - Corrupted file
   - File too large
   - Extraction failure

2. **Embedding Errors**
   - API key missing/invalid
   - Rate limiting
   - Network failures
   - Model unavailable

3. **Query Errors**
   - Empty database
   - No relevant results
   - LLM generation failure

### Error Handling Strategy

```python
class RAGException(Exception):
    """Base exception for RAG system"""
    pass

class PDFProcessingError(RAGException):
    """Raised when PDF processing fails"""
    pass

class EmbeddingError(RAGException):
    """Raised when embedding generation fails"""
    pass

class QueryError(RAGException):
    """Raised when query processing fails"""
    pass
```

**Approach**:
- Log all errors with context
- Provide user-friendly error messages
- Implement retry logic for transient failures (API calls)
- Graceful degradation where possible
- Validate inputs before processing

## Testing Strategy

### Unit Tests

- Test PDF loading with valid/invalid files
- Test text chunking with various sizes
- Test embedding generation (mocked API)
- Test vector store operations
- Test answer generation logic

### Integration Tests

- Test end-to-end document ingestion
- Test end-to-end question answering
- Test with sample educational PDFs
- Test error scenarios

### Test Data

- Sample math textbook PDF (10-20 pages)
- Sample science textbook PDF (10-20 pages)
- Corrupted PDF file
- Oversized PDF file
- Set of test questions with expected answers

## Implementation Considerations

### Performance

- **Batch Processing**: Process multiple chunks in parallel where possible
- **Caching**: Cache embeddings to avoid regeneration
- **Lazy Loading**: Load vector store only when needed
- **Streaming**: Stream LLM responses for better UX

### Security

- Validate file paths to prevent directory traversal
- Sanitize user inputs
- Store API keys in environment variables
- Implement rate limiting for API calls

### Scalability

- Use persistent vector store for large document collections
- Support incremental document addition
- Implement document deletion/update capabilities
- Consider cloud vector databases for production (Pinecone, Weaviate)

### User Experience

- Show progress indicators during PDF processing
- Display processing time and chunk count
- Provide clear feedback on errors
- Support conversation history in interactive mode
- Allow follow-up questions with context

## Deployment

### Local Development

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with API keys

# Run Streamlit App
streamlit run app.py

# Or use CLI
python main.py upload textbook.pdf
python main.py ask "What is Newton's first law?"
```

### Streamlit Cloud Deployment (Free)

1. Push code to GitHub repository
2. Go to share.streamlit.io
3. Connect GitHub account
4. Select repository and branch
5. Add secrets (API keys) in Streamlit dashboard
6. Deploy with one click
7. Share the public URL with your client

**Advantages**:
- Free hosting for public apps
- Automatic HTTPS
- Easy updates via git push
- Built-in secrets management
- No server maintenance required

### Dependencies

```
langchain>=0.1.0
chromadb>=0.4.0
openai>=1.0.0
pypdf2>=3.0.0
python-dotenv>=1.0.0
pyyaml>=6.0
streamlit>=1.28.0
click>=8.0.0
```

## Future Enhancements

- Multi-user support with authentication
- Document versioning
- Advanced citation with page numbers and highlights
- Support for other document formats (DOCX, EPUB)
- Fine-tuned embeddings for educational content
- Question history and analytics
- Export Q&A sessions
- Mobile-responsive design improvements
