# baseline_agent.py
"""
CoALA Baseline Agent with Semantic and Episodic Memory.
Provides foundation for adding procedural memory.
"""

from datetime import datetime
from typing import List, Dict, TypedDict, Annotated, Sequence, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

class SemanticFact(BaseModel):
    """Structure for semantic memory facts"""
    subject: str = Field(description="Entity or topic")
    predicate: str = Field(description="Relationship or property")
    object: str = Field(description="Value or related entity")
    confidence: float = Field(description="Confidence score 0-1")
    source: str = Field(description="Source: user or assistant")

class AgentState(TypedDict):
    """State structure for the agent workflow"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    working_memory: dict
    episodic_recall: list
    semantic_facts: dict
    user_id: str
    conversation_id: str

class CoALABaselineAgent:
    """Baseline agent with semantic and episodic memory"""
    
    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
        temperature: float = 0,
        persist_directory: str = "./memory_store"
    ):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.embeddings = OpenAIEmbeddings()
        self.output_parser = StrOutputParser()
        
        self.vector_store = Chroma(
            collection_name="agent_memory",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
        self.current_user_id = "default"
        self.current_conversation_id = None