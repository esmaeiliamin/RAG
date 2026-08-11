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