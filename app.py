"""Streamlit web interface for RAG-based QA System."""

import os
import time
from datetime import datetime
from typing import Optional

# Import streamlit
import streamlit as st

# MUST be the first Streamlit command!
st.set_page_config(
    page_title="RAG QA System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== API KEY CONFIGURATION =====
# Now we can safely access st.secrets after set_page_config
try:
    # Try to load from Streamlit secrets (cloud deployment)
    if 'OPENAI_API_KEY' in st.secrets:
        os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
except (FileNotFoundError, AttributeError):
    # Secrets file doesn't exist - running locally
    pass

# Load from .env file for local development
from dotenv import load_dotenv
load_dotenv()

# Verify API key is loaded
if not os.getenv('OPENAI_API_KEY'):
    st.error("⚠️ OpenAI API key not found!")
    st.info("Please configure OPENAI_API_KEY in .env file (local) or Streamlit Cloud secrets (cloud)")
    st.stop()
# ===== END API KEY CONFIGURATION =====

from src.rag_engine import RAGEngine, DocumentInfo
from src.config import Config, ConfigError
from src.answer_generator import Answer

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .source-citation {
        font-size: 0.85rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():

    if 'rag_engine' not in st.session_state:
        try:
            st.session_state.rag_engine = RAGEngine()
            st.session_state.engine_initialized = True
        except ConfigError as e:
            st.session_state.engine_initialized = False
            st.session_state.init_error = str(e)
        except Exception as e:
            st.session_state.engine_initialized = False
            st.session_state.init_error = f"Failed to initialize RAG engine: {e}"
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'uploaded_documents' not in st.session_state:
        st.session_state.uploaded_documents = []
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def display_header():
    """Display the main header."""
    st.markdown('<div class="main-header">📚 RAG Question Answering System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload educational PDFs and ask questions about their content</div>', unsafe_allow_html=True)
    
    # Show storage warning if deployed on Streamlit Cloud
    try:
        if 'OPENAI_API_KEY' in st.secrets:
            st.info("""
                📌 **Demo Mode:** Uploaded documents are temporary and will be reset when the app restarts 
                (typically every 24-48 hours). For production use with permanent storage, please contact support.
            """, icon="ℹ️")
    except (FileNotFoundError, AttributeError):
        # Running locally - no warning needed
        pass


def display_sidebar():
   
    with st.sidebar:
        st.header(" Document Management")
        
      
        if st.session_state.engine_initialized:
            try:
                db_info = st.session_state.rag_engine.get_database_info()
                st.metric("Total Chunks", db_info.get('count', 0))
            except Exception as e:
                st.warning(f"Could not load database info: {e}")
        
        st.divider()
        
       
        st.subheader("Uploaded Documents")
        if st.session_state.uploaded_documents:
            for i, doc in enumerate(st.session_state.uploaded_documents):
                with st.expander(f" {doc['filename']}", expanded=False):
                    st.write(f"**Chunks:** {doc['chunk_count']}")
                    st.write(f"**Size:** {doc['file_size_mb']:.2f} MB")
                    st.write(f"**Uploaded:** {doc['upload_time']}")
        else:
            st.info("No documents uploaded yet")
        
        st.divider()
        
       
        if st.button(" Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.engine_initialized:
                st.session_state.rag_engine.clear_conversation_history()
            st.rerun()
        
       
        if st.button(" Reset Database", use_container_width=True, type="secondary"):
            if st.session_state.engine_initialized:
                try:
                    st.session_state.rag_engine.reset_database()
                    st.session_state.uploaded_documents = []
                    st.session_state.messages = []
                    st.success("Database reset successfully!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to reset database: {e}")
        
        st.divider()
        
      
        st.subheader(" Settings")
        if st.session_state.engine_initialized:
            config = st.session_state.rag_engine.config
            st.write(f"**LLM:** {config.get('llm.model')}")
            st.write(f"**Embedding:** {config.get('embedding.model')}")
            st.write(f"**Retrieval Top-K:** {config.get('retrieval.top_k')}")


def handle_pdf_upload():
  
    st.subheader("📤 Upload PDF Document")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload educational PDFs (textbooks, papers, etc.) up to 100MB"
    )
    
    if uploaded_file is not None:
        if st.button("Process Document", type="primary"):
           
            temp_path = f"temp_{uploaded_file.name}"
            
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Show processing status
                with st.status("Processing document...", expanded=True) as status:
                    st.write(" Loading PDF...")
                    time.sleep(0.5)
                    
                    st.write(" Splitting into chunks...")
                    time.sleep(0.5)
                    
                    st.write("Generating embeddings...")
                    time.sleep(0.5)
                    
                    st.write(" Storing in database...")
                    
                  
                    start_time = time.time()
                    doc_info = st.session_state.rag_engine.ingest_document(
                        temp_path,
                        show_progress=False
                    )
                    processing_time = time.time() - start_time
                    
                    status.update(label=" Document processed successfully!", state="complete")
                
             
                st.session_state.uploaded_documents.append({
                    'filename': uploaded_file.name,
                    'chunk_count': doc_info.chunk_count,
                    'file_size_mb': doc_info.file_size_mb,
                    'upload_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'processing_time': processing_time
                })
                
               
                st.markdown(f"""
                    <div class="success-box">
                        <strong> Success!</strong><br>
                        Document: {uploaded_file.name}<br>
                        Chunks created: {doc_info.chunk_count}<br>
                        Processing time: {processing_time:.2f}s
                    </div>
                """, unsafe_allow_html=True)
                
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.markdown(f"""
                    <div class="error-box">
                        <strong> Error!</strong><br>
                        {str(e)}
                    </div>
                """, unsafe_allow_html=True)
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)


def display_chat_interface():
    
    st.subheader(" Ask Questions")
    
   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
          
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:** {source}")
            
      
            if message["role"] == "assistant" and "generation_time" in message:
                st.caption(f" Generated in {message['generation_time']:.2f}s")
    
  
    if prompt := st.chat_input("Ask a question about your documents..."):
       
        if not st.session_state.uploaded_documents:
            st.warning(" Please upload at least one document before asking questions.")
            st.stop()
        
     
        st.session_state.messages.append({"role": "user", "content": prompt})
        
      
        try:
            start_time = time.time()
            answer = st.session_state.rag_engine.ask_question(prompt)
            generation_time = time.time() - start_time
            
           
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer.text,
                "sources": answer.sources,
                "generation_time": generation_time
            })
            
        except Exception as e:
            error_message = f" Error generating answer: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
        
      
        st.rerun()


def display_evaluation_interface():
   
    st.subheader(" System Evaluation & Debugging")
    
    if not st.session_state.uploaded_documents:
        st.info(" Upload documents first to see evaluation metrics")
        return
    
   
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("###  Chunk Analysis")
        
     
        config = st.session_state.rag_engine.config
        chunk_size = config.get('chunking.chunk_size')
        chunk_overlap = config.get('chunking.chunk_overlap')
        
        st.write(f"**Chunk Size:** {chunk_size} characters")
        st.write(f"**Chunk Overlap:** {chunk_overlap} characters")
        
       
        try:
            db_info = st.session_state.rag_engine.get_database_info()
            total_chunks = db_info.get('count', 0)
            st.metric("Total Chunks in Database", total_chunks)
        except Exception as e:
            st.error(f"Error getting database info: {e}")
            return
        
       
        st.markdown("####  Sample Chunks")
        num_samples = st.slider("Number of samples to view", 1, 10, 3)
        
        if st.button("View Random Chunks"):
            try:
             
                sample_query = "the"
                chunks = st.session_state.rag_engine.query_processor.retrieve_context(
                    sample_query, k=num_samples
                )
                
                for i, chunk in enumerate(chunks, 1):
                    with st.expander(f"Chunk {i} - {len(chunk.page_content)} chars"):
                        st.text(chunk.page_content)
                        st.caption(f"Source: {chunk.metadata.get('source', 'Unknown')} | Page: {chunk.metadata.get('page', 'Unknown')}")
            except Exception as e:
                st.error(f"Error retrieving chunks: {e}")
    
    with col2:
        st.markdown("### Retrieval Testing")
        
     
        test_query = st.text_input("Enter a test query:", placeholder="e.g., What is machine learning?")
        top_k = st.slider("Number of chunks to retrieve", 1, 10, 4)
        
        if st.button("Test Retrieval") and test_query:
            try:
                with st.spinner("Retrieving relevant chunks..."):
                    start_time = time.time()
                    chunks = st.session_state.rag_engine.query_processor.retrieve_context(
                        test_query, k=top_k
                    )
                    retrieval_time = time.time() - start_time
                
                st.success(f"Retrieved {len(chunks)} chunks in {retrieval_time:.3f}s")
                
                if chunks:
                    for i, chunk in enumerate(chunks, 1):
                        with st.expander(f"Result {i} - Relevance Rank #{i}"):
                            st.markdown(f"**Content ({len(chunk.page_content)} chars):**")
                            st.text(chunk.page_content[:500] + "..." if len(chunk.page_content) > 500 else chunk.page_content)
                            st.caption(f" Source: {chunk.metadata.get('source', 'Unknown')} | Page: {chunk.metadata.get('page', 'Unknown')}")
                else:
                    st.warning("No chunks retrieved for this query")
                    
            except Exception as e:
                st.error(f"Error during retrieval: {e}")
    
   
    st.divider()
    st.markdown("###  Answer Quality Test")
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        eval_question = st.text_area(
            "Test Question:",
            placeholder="Enter a question to test the full pipeline...",
            height=100
        )
    
    with col4:
        expected_answer = st.text_area(
            "Expected Answer (optional):",
            placeholder="What should the answer contain?",
            height=100
        )
    
    if st.button("Generate & Evaluate Answer", type="primary") and eval_question:
        try:
            with st.spinner("Processing..."):
                
                start_retrieval = time.time()
                chunks = st.session_state.rag_engine.query_processor.retrieve_context(eval_question)
                retrieval_time = time.time() - start_retrieval
                
                
                start_generation = time.time()
                answer = st.session_state.rag_engine.answer_generator.generate_answer(
                    eval_question, chunks
                )
                generation_time = time.time() - start_generation
            
            
            col5, col6 = st.columns([1, 1])
            
            with col5:
                st.markdown("####  Generated Answer")
                st.write(answer.text)
                st.caption(f"⏱️ Retrieval: {retrieval_time:.3f}s | Generation: {generation_time:.3f}s")
                
                if answer.sources:
                    st.markdown("**Sources:**")
                    for source in answer.sources:
                        st.caption(f"- {source}")
            
            with col6:
                st.markdown("####  Evaluation Metrics")
                st.metric("Chunks Retrieved", len(chunks))
                st.metric("Total Time", f"{retrieval_time + generation_time:.3f}s")
                
                if expected_answer:
                   
                    expected_words = set(expected_answer.lower().split())
                    answer_words = set(answer.text.lower().split())
                    overlap = len(expected_words & answer_words)
                    coverage = (overlap / len(expected_words) * 100) if expected_words else 0
                    
                    st.metric("Keyword Coverage", f"{coverage:.1f}%")
                    
                    if coverage > 70:
                        st.success(" Good coverage of expected content")
                    elif coverage > 40:
                        st.warning(" Partial coverage of expected content")
                    else:
                        st.error(" Low coverage of expected content")
                
        except Exception as e:
            st.error(f"Error during evaluation: {e}")


def main():
   
    initialize_session_state()
    
   
    if not st.session_state.engine_initialized:
        st.error("Failed to initialize RAG engine")
        st.error(st.session_state.get('init_error', 'Unknown error'))
        st.info("Please check your configuration and API keys in the .env file")
        st.stop()
    
 
    display_header()
    

    display_sidebar()
    
  
    tab1, tab2, tab3 = st.tabs([" Chat", " Upload Documents", " Evaluation"])
    
    with tab1:
        display_chat_interface()
    
    with tab2:
        handle_pdf_upload()
    
    with tab3:
        display_evaluation_interface()


if __name__ == "__main__":
    main()
