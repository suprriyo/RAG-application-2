"""Answer generator for creating responses using LLM."""

# generate answers with LLM

from typing import List
from dataclasses import dataclass
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser





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
       
        template = """You are an expert educational tutor specializing in mathematics and science. Your goal is to help students learn through clear, detailed explanations and step-by-step problem solving.

Context from the documents:
{context}

Conversation History:
{chat_history}

Current Question: {question}

CRITICAL INSTRUCTIONS FOR MATH & SCIENCE PROBLEMS:

1. **Problem Identification**: First, identify what type of problem this is (algebra, calculus, physics, chemistry, etc.)

2. **Given Information**: List all given values, variables, and known information clearly

3. **Required**: State what needs to be found or proven

4. **Step-by-Step Solution**:
   - Number each step (Step 1, Step 2, etc.)
   - Show EVERY calculation with actual numbers
   - Explain WHY you're doing each step
   - Write out formulas before substituting values
   - Show intermediate results
   - Never skip steps, even if they seem obvious

5. **Calculations**: 
   - Write: "Formula: [equation]"
   - Write: "Substituting values: [equation with numbers]"
   - Write: "Calculating: [show the arithmetic]"
   - Write: "Result: [answer with units]"

6. **Final Answer**: 
   - Clearly mark the final answer
   - Include proper units (meters, seconds, kg, etc.)
   - Box or highlight the answer if possible

7. **Verification**: If possible, verify the answer makes sense

EXAMPLE FORMAT FOR MATH PROBLEMS:
```
**Given:**
- Value 1 = X
- Value 2 = Y

**Required:** Find Z

**Solution:**

Step 1: Identify the formula
Formula: Z = X + Y

Step 2: Substitute the values
Z = 5 + 3

Step 3: Calculate
Z = 8

**Final Answer: Z = 8 units**
```

FOR CONCEPTUAL QUESTIONS:
- Explain using the context from documents
- Use analogies and examples
- Break down complex concepts into simple parts
- Reference relevant formulas or principles

IMPORTANT RULES:
- Consider conversation history for follow-up questions
- If the question refers to "it", "that", or "the previous answer", use conversation history
- If context doesn't contain relevant information, state: "I cannot find relevant information about this in the uploaded material."
- Do NOT reference chunk numbers
- Always show your work completely
- Be thorough and educational

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
    
    def generate_answer(self, question: str, context: List[Document], chat_history: List[dict] = None) -> Answer:
        """
        Generate an answer to a question using retrieved context and conversation history.
        
        Args:
            question: The current question
            context: Retrieved document chunks
            chat_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            Answer object with text, sources, and confidence
        """
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
            
            # Format context from documents
            formatted_context = self._format_context(context)
            
            # Format chat history for the prompt
            formatted_history = self._format_chat_history(chat_history or [])
            
            # Create the chain
            chain = (
                {
                    "context": lambda x: formatted_context,
                    "chat_history": lambda x: formatted_history,
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
    
    def _format_chat_history(self, chat_history: List[dict]) -> str:
        """Format chat history for the prompt."""
        if not chat_history:
            return "No previous conversation."
        
        # Only include last 5 exchanges to avoid token limits
        recent_history = chat_history[-10:]  # Last 5 Q&A pairs (10 messages)
        
        formatted = []
        for msg in recent_history:
            role = "Student" if msg["role"] == "user" else "Tutor"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
