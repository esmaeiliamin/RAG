# coala_agent.py
"""
Full CoALA Agent with Episodic, Semantic, and Procedural Memory.
Uses LangMem for procedural memory extraction and optimization.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, TypedDict, Annotated, Sequence

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from Domain_agent import DomainAgent, DomainProcedure
from procedural_memory import ProceduralMemory

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
    procedural_strategy: dict
    user_id: str
    conversation_id: str


class CoALAAgent:
    """Full CoALA agent with all three memory types powered by LangMem"""
    
    def __init__(
        self,
        domain_agent: DomainAgent,
        model_name: str = "gpt-4.1-mini",
        temperature: float = 0,
        persist_directory: str = None,
        optimization_algorithm: str = "prompt_memory"
    ):
        self.domain_agent = domain_agent
        
        if persist_directory is None and hasattr(domain_agent, 'memory_dir'):
            persist_directory = domain_agent.memory_dir
        elif persist_directory is None:
            persist_directory = "./memory_store"
        
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.embeddings = OpenAIEmbeddings()
        self.output_parser = StrOutputParser()
        
        self.vector_store = Chroma(
            collection_name="agent_memory",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        self.procedural_memory = ProceduralMemory(
            llm=self.llm,
            domain_agent=domain_agent,
            optimization_algorithm=optimization_algorithm
        )
        
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
        self.current_user_id = "default"
        self.current_conversation_id = None

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        workflow.add_node("memory_agent", self._unified_memory_agent)
        workflow.set_entry_point("memory_agent")
        workflow.add_edge("memory_agent", END)
        return workflow
    
    def store_episodic_memory(self, conversation_id: str, messages: List, summary: Optional[str] = None) -> str:
        if not summary and messages:
            first_msg = messages[0]
            if isinstance(first_msg, tuple):
                summary = f"Discussion: {first_msg[1][:100]}..."
            else:
                summary = f"Discussion: {first_msg.content[:100]}..."
        
        metadata = {
            "type": "episodic",
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "message_count": len(messages),
            "user_id": self.current_user_id
        }
        
        conversation_text = self._format_messages(messages)
        self.vector_store.add_documents([Document(page_content=conversation_text, metadata=metadata)])
        return conversation_id