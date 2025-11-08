"""Answer generator for creating responses using LLM."""

# generate answers with LLM

from typing import List
from dataclasses import dataclass
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser





@dataclass
class Answer:
    
    text: str
    sources: List[str]
    confidence: float = 1.0


class AnswerGenerator:
    """Generates answers to questions using LLM and retrieved context."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-3.5-turbo", 
                 temperature: float = 0.7, max_tokens: int = 500):
       
        self.provider = provider.lower()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._llm = self._initialize_llm()
        self._prompt_template = self._create_prompt_template()
    
    def _initialize_llm(self):
        
        if self.provider == "openai":
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
       
        template = """You are a helpful educational tutor. Your job is to help students learn by both explaining concepts and solving problems step-by-step.

Context from the documents:
{context}

Question: {question}

Instructions:
- If the question asks to solve a problem (math, physics, etc.), provide a complete step-by-step solution
- Show all working steps clearly with explanations
- For math problems: write out each calculation step
- For conceptual questions: explain using the context provided
- Use the information from the context as reference, but apply it to solve the specific problem asked
- If it's a numerical problem, calculate the final answer
- Write in a clear, educational tone that helps students understand
- If the context does not contain relevant information to help answer, clearly state: "I cannot find relevant information about this in the uploaded material."
- Do NOT reference chunk numbers in your answer

Answer:"""
        
        return ChatPromptTemplate.from_template(template)

    def _format_context(self, documents: List[Document]) -> str:
       
        if not documents:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
        
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'Unknown')
            
        
            context_parts.append(
                f"[Source: {source}, Page: {page}]\n{doc.page_content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _extract_sources(self, documents: List[Document]) -> List[str]:
     
        sources = []
        for doc in documents:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'Unknown')
            source_str = f"{source} (Page {page})"
            if source_str not in sources:
                sources.append(source_str)
        
        return sources
    
    def generate_answer(self, question: str, context: List[Document]) -> Answer:
        
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            # Handle case with no relevant context
            if not context:
                return Answer(
                    text="I cannot find relevant information about this in the uploaded material.",
                    sources=[],
                    confidence=0.0
                )
            
        
            formatted_context = self._format_context(context)
            
            # Create the chain
            chain = (
                {
                    "context": lambda x: formatted_context,
                    "question": RunnablePassthrough()
                }
                | self._prompt_template
                | self._llm
                | StrOutputParser()
            )
            
            # Generate answer
            answer_text = chain.invoke(question)
            
            # Extract sources
            sources = self._extract_sources(context)
            
            return Answer(
                text=answer_text,
                sources=sources,
                confidence=1.0 if context else 0.0
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate answer: {e}")
