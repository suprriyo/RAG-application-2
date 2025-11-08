"""Streamlit web interface for RAG-based QA System."""

import os
import time
from datetime import datetime
from typing import Optional


import streamlit as st


st.set_page_config(
    page_title="RAG QA System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


try:
 
    if 'OPENAI_API_KEY' in st.secrets:
        os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
except (FileNotFoundError, AttributeError):
  
    pass


from dotenv import load_dotenv
load_dotenv()


if not os.getenv('OPENAI_API_KEY'):
    st.error(" OpenAI API key not found!")
    st.info("Please configure OPENAI_API_KEY in .env file (local) or Streamlit Cloud secrets (cloud)")
    st.stop()


from src.rag_engine import RAGEngine, DocumentInfo
from src.config import Config, ConfigError
from src.answer_generator import Answer


st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(120deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 400;
    }
    
    /* Chat styling */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Success and error boxes */
    .success-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.15);
    }
    .error-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(220, 53, 69, 0.15);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #1f77b4;
        border-radius: 12px;
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: #f8f9fa;
        font-weight: 500;
    }
    
    /* Input styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        border-top: 2px solid #e0e0e0;
        padding-top: 1rem;
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
    
    st.markdown('<div class="main-header">📚 RAG Question Answering System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload educational PDFs and get instant answers</div>', unsafe_allow_html=True)
    
    
    with st.expander(" Quick Tips - Click to expand", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **Upload Documents**
            - Support for PDF files
            - Up to 100MB per file
            """)
        with col2:
            st.markdown("""
            ** Ask Questions**
            - Ask specific questions
            """)
        with col3:
            st.markdown("""
            ** View Sources**
            - Click "View Sources" to see references
            """)
    
    
    try:
        if 'OPENAI_API_KEY' in st.secrets:
            st.info(" **Demo Mode:** Uploaded documents are temporary and will be reset when the app restarts.", icon="ℹ️")
    except (FileNotFoundError, AttributeError):
        pass


def display_sidebar():
    
    with st.sidebar:
        st.header(" Dashboard")
        
        
        if st.session_state.engine_initialized:
            try:
                db_info = st.session_state.rag_engine.get_database_info()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Documents", len(st.session_state.uploaded_documents))
                with col2:
                    st.metric(" Chunks", db_info.get('count', 0))
            except Exception as e:
                st.warning(f" Could not load database info: {e}")
        
        st.divider()
        
        
        st.subheader(" Uploaded Documents")
        if st.session_state.uploaded_documents:
            for i, doc in enumerate(st.session_state.uploaded_documents, 1):
                with st.expander(f" {doc['filename']}", expanded=False):
                    st.markdown(f"""
                    - **Chunks:** {doc['chunk_count']}
                    - **Size:** {doc['file_size_mb']:.2f} MB
                    - **Uploaded:** {doc['upload_time']}
                    - **Processing:** {doc.get('processing_time', 0):.2f}s
                    """)
        else:
            st.info(" No documents uploaded yet\n\nGo to the 'Upload Documents' tab to get started!")
        
        st.divider()
        
        
        st.subheader(" Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(" Clear Chat", use_container_width=True, help="Clear conversation history"):
                st.session_state.messages = []
                if st.session_state.engine_initialized:
                    st.session_state.rag_engine.clear_conversation_history()
                st.rerun()
        
        with col2:
            if st.button(" Reset DB", use_container_width=True, type="secondary", help="Delete all documents"):
                if st.session_state.engine_initialized:
                    try:
                        st.session_state.rag_engine.reset_database()
                        st.session_state.uploaded_documents = []
                        st.session_state.messages = []
                        st.success(" Database reset!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f" Failed to reset: {e}")
        
        st.divider()
        
        
        st.subheader(" System Settings")
        if st.session_state.engine_initialized:
            config = st.session_state.rag_engine.config
            st.markdown(f"""
            - **LLM Model:** `{config.get('llm.model')}`
            - **Embedding:** `{config.get('embedding.model')}`
            - **Top-K Results:** `{config.get('retrieval.top_k')}`
            - **Chunk Size:** `{config.get('chunking.chunk_size')}`
            - **Chunk Overlap:** `{config.get('chunking.chunk_overlap')}`
            """)
        
        st.divider()
        
        
        st.caption(" Powered by OpenAI & LangChain")
        st.caption("Your data is processed securely")


def handle_pdf_upload():
 
    st.subheader(" Upload PDF Document")
    
    
    st.info(" **Supported:** PDF files up to 100MB | **Best for:** Textbooks, research papers, study materials", icon="ℹ️")
    
    uploaded_file = st.file_uploader(
        "Drag and drop or click to browse",
        type=['pdf'],
        help="Upload educational PDFs (textbooks, papers, etc.) up to 100MB",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"** File:** {uploaded_file.name}")
        with col2:
            st.write(f"** Size:** {file_size_mb:.2f} MB")
        with col3:
            st.write(f"** Type:** PDF")
        
        st.divider()
        
        if st.button(" Process Document", type="primary", use_container_width=True):
            
            temp_path = f"temp_{uploaded_file.name}"
            
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                
                with st.status(" Processing document...", expanded=True) as status:
                    st.write(" Loading PDF...")
                    time.sleep(0.3)
                    
                    st.write(" Splitting into chunks...")
                    time.sleep(0.3)
                    
                    st.write(" Generating embeddings...")
                    time.sleep(0.3)
                    
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
                        <strong> Success!</strong><br><br>
                         <strong>Document:</strong> {uploaded_file.name}<br>
                         <strong>Chunks created:</strong> {doc_info.chunk_count}<br>
                         <strong>Processing time:</strong> {processing_time:.2f}s<br>
                         <strong>File size:</strong> {doc_info.file_size_mb:.2f} MB
                    </div>
                """, unsafe_allow_html=True)
                
                st.balloons()  # Celebration animation!
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.markdown(f"""
                    <div class="error-box">
                        <strong> Error!</strong><br><br>
                        {str(e)}<br><br>
                        <small>Please check the file and try again.</small>
                    </div>
                """, unsafe_allow_html=True)
            
            finally:
              
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 12px; border: 2px dashed #dee2e6;">
            <h3 style="color: #6c757d;"> No file selected</h3>
            <p style="color: #6c757d;">Upload a PDF document to get started</p>
        </div>
        """, unsafe_allow_html=True)


def display_chat_interface():
    """Display the chat interface for Q&A."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(" Ask Questions")
    with col2:
        if len(st.session_state.messages) > 0:
            st.caption(f"{len(st.session_state.messages)//2} Q&A pairs in memory")
    
   
    if not st.session_state.messages:
        if st.session_state.uploaded_documents:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 2rem;">
                <h2 style="color: white; margin-bottom: 1rem;"> Ready to answer your questions!</h2>
                <p style="font-size: 1.1rem; margin-bottom: 0;">Ask anything about your uploaded documents below</p>
            </div>
            """, unsafe_allow_html=True)
            
           
            st.markdown("** Example questions you can ask:**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - "Explain the concept of..."
                - "What is the formula for..."
                - "Solve this problem step by step..."
                """)
            with col2:
                st.markdown("""
                - "Summarize chapter X"
                - "What are the key points about..."
                - "Give me an example of..."
                """)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background-color: #fff3cd; border-radius: 12px; border-left: 5px solid #ffc107;">
                <h3 style="color: #856404;">📚 No documents uploaded yet</h3>
                <p style="color: #856404; font-size: 1.1rem;">Please upload a PDF document first to start asking questions</p>
            </div>
            """, unsafe_allow_html=True)
            return
    
    # Create a container for chat messages with scrolling
    chat_container = st.container()
    
    # Display chat messages in the container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🧑‍🎓" if message["role"] == "user" else "🤖"):
                st.markdown(message["content"])
                
                # Show sources for assistant messages
                if message["role"] == "assistant" and "sources" in message:
                    if message["sources"]:
                        with st.expander(" View Sources"):
                            for i, source in enumerate(message["sources"], 1):
                                st.markdown(f"**{i}.** {source}")
                
                # Show generation time
                if message["role"] == "assistant" and "generation_time" in message:
                    st.caption(f"⏱ Generated in {message['generation_time']:.2f}s")
    
    # Add some spacing before the chat input
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat input - this persists the query after submission
    # The chat input is fixed at the bottom by Streamlit
    if prompt := st.chat_input(" Ask a question about your documents...", key="chat_input"):
        
        if not st.session_state.uploaded_documents:
            st.warning(" Please upload at least one document before asking questions.")
            st.stop()
        
        # Display user message immediately
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)
        
        # Add to message history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    start_time = time.time()
                    answer = st.session_state.rag_engine.ask_question(prompt)
                    generation_time = time.time() - start_time
                    
                    # Display answer
                    st.markdown(answer.text)
                    
                    # Display sources
                    if answer.sources:
                        with st.expander("📚 View Sources"):
                            for i, source in enumerate(answer.sources, 1):
                                st.markdown(f"**{i}.** {source}")
                    
                    st.caption(f"⏱️ Generated in {generation_time:.2f}s")
                    
                    # Add to message history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer.text,
                        "sources": answer.sources,
                        "generation_time": generation_time
                    })
                    
                except Exception as e:
                    error_message = f" Error generating answer: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })


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
