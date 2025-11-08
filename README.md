# RAG-Based Question Answering System

A Retrieval-Augmented Generation (RAG) system for educational content that allows students to upload PDF textbooks and ask questions about their content.

**🌐 Live Demo:** [Deploy to Streamlit Cloud](https://share.streamlit.io)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## Features

-  **PDF Upload**: Upload educational PDFs (textbooks, papers, etc.)
-  **Interactive Chat**: Ask questions and get answers based on uploaded content
-  **Source Citations**: View which parts of the documents were used to generate answers
-  **Multi-Document Support**: Upload multiple PDFs and query across all documents
-  **Performance Metrics**: See answer generation time
-  **Document Management**: View uploaded documents and manage the database

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd rag-qa-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional: ANTHROPIC_API_KEY, HUGGINGFACE_API_KEY
```

### 3. Run the Application

#### Web Interface (Streamlit)

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

#### Command Line Interface (CLI)

```bash
# Upload a document
python main.py upload path/to/textbook.pdf

# Ask a question
python main.py ask "What is Newton's first law?"

# List uploaded documents
python main.py list

# Reset database
python main.py reset
```

## Usage Guide

### Uploading Documents

1. Go to the "Upload Documents" tab
2. Click "Choose a PDF file" and select your document
3. Click "Process Document"
4. Wait for processing to complete (you'll see progress updates)

### Asking Questions

1. Go to the "Chat" tab
2. Type your question in the chat input
3. Press Enter or click Send
4. View the answer along with source citations
5. Click "View Sources" to see which parts of the document were used

### Managing Documents

- View uploaded documents in the sidebar
- See document statistics (chunks, size, upload time)
- Clear conversation history with "Clear Conversation" button
- Reset entire database with "Reset Database" button

## Configuration

Edit `config.yaml` to customize:

- **Embedding Model**: Choose between OpenAI or HuggingFace embeddings
- **LLM Provider**: Use OpenAI GPT or Anthropic Claude
- **Chunk Size**: Adjust text chunking parameters
- **Retrieval Settings**: Configure how many relevant chunks to retrieve

Example configuration:

```yaml
embedding:
  provider: "openai"
  model: "text-embedding-ada-002"

llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 500

chunking:
  chunk_size: 1000
  chunk_overlap: 200

retrieval:
  top_k: 4
  score_threshold: 0.7
```

## Deployment to Streamlit Cloud

### Prerequisites

- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add your API keys:
     ```toml
     OPENAI_API_KEY = "your_key_here"
     ```

4. **Share Your App**
   - Your app will be available at: `https://share.streamlit.io/[username]/[repo]/[branch]/app.py`
   - Share this URL with users

## Architecture

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Streamlit Web Interface         │
│  - Upload PDFs                      │
│  - Chat Interface                   │
│  - Document Management              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   RAG Engine (Orchestrator)         │
│  - Document Processing              │
│  - Query Processing                 │
│  - Session Management               │
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
│  - Vector Stores (ChromaDB)         │
│  - LLM Integration                  │
└─────────────────────────────────────┘
```

## Technology Stack

- **Framework**: LangChain (Python)
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI / HuggingFace
- **LLM**: OpenAI GPT / Anthropic Claude
- **PDF Processing**: PyPDF2
- **Web Interface**: Streamlit
- **CLI**: Click

## Troubleshooting

### API Key Errors

If you see "Missing required API key" errors:
- Check that your `.env` file exists and contains valid API keys
- Ensure the `.env` file is in the project root directory
- Restart the application after updating `.env`

### PDF Processing Errors

If PDF upload fails:
- Ensure the PDF is not corrupted
- Check that the file size is under 100MB
- Verify the PDF contains extractable text (not just images)

### Database Issues

If you encounter database errors:
- Try resetting the database using the "Reset Database" button
- Delete the `data/chroma_db` directory and restart the app
- Check that you have write permissions in the project directory

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.


---

## 🚀 Deployment to Streamlit Cloud

### Quick Deploy

1. **Fork/Clone this repository**
2. **Push to your GitHub**
3. **Go to** [share.streamlit.io](https://share.streamlit.io)
4. **Click** "New app" and select your repo
5. **Add secrets:**
   ```toml
   OPENAI_API_KEY = "your-key-here"
   ```
6. **Deploy!**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### ⚠️ Important Note

Streamlit Cloud has ephemeral storage. Uploaded documents are temporary and will be lost when the app restarts. For production use, consider:
- Pinecone (free tier available)
- AWS S3 for persistent storage
- PostgreSQL for user management

---

## 📁 Project Structure

```
rag-qa-system/
├── app.py                      # Main Streamlit application
├── src/                        # Core RAG components
│   ├── rag_engine.py          # Main orchestrator
│   ├── pdf_loader.py          # PDF processing
│   ├── text_chunker.py        # Text splitting
│   ├── embedding_service.py   # Embeddings generation
│   ├── vector_store_manager.py # ChromaDB management
│   ├── query_processor.py     # Query handling
│   ├── answer_generator.py    # LLM answer generation
│   └── config.py              # Configuration management
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Secrets template
├── config.yaml                # App configuration
├── requirements.txt           # Python dependencies
├── packages.txt              # System dependencies
├── .gitignore                # Git ignore rules
├── DEPLOYMENT.md             # Deployment guide
└── README.md                 # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [LangChain](https://langchain.com)
- Vector storage by [ChromaDB](https://www.trychroma.com)
- LLM by [OpenAI](https://openai.com)

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for education**
