"""Verify all imports work correctly."""

print("Testing imports...")

try:
    from langchain_core.documents import Document
    print(" langchain_core.documents.Document")
except ImportError as e:
    print(f"langchain_core.documents.Document: {e}")

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print(" langchain_text_splitters.RecursiveCharacterTextSplitter")
except ImportError as e:
    print(f" langchain_text_splitters.RecursiveCharacterTextSplitter: {e}")

try:
    from langchain_core.prompts import ChatPromptTemplate
    print(" langchain_core.prompts.ChatPromptTemplate")
except ImportError as e:
    print(f" langchain_core.prompts.ChatPromptTemplate: {e}")

try:
    from langchain_core.runnables import RunnablePassthrough
    print(" langchain_core.runnables.RunnablePassthrough")
except ImportError as e:
    print(f" langchain_core.runnables.RunnablePassthrough: {e}")

try:
    from langchain_core.output_parsers import StrOutputParser
    print(" langchain_core.output_parsers.StrOutputParser")
except ImportError as e:
    print(f" langchain_core.output_parsers.StrOutputParser: {e}")

print("\nAll imports verified!")
