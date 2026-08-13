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
    
    def retrieve_episodic_memories(self, query: str, k: int = 3) -> List[Document]:
        return self.vector_store.similarity_search(query=query, k=k, filter={"type": {"$eq": "episodic"}})
    
    def extract_semantic_facts(self, messages: List) -> List[SemanticFact]:
        extraction_prompt_template = self.domain_agent.get_semantic_extraction_prompt()
        extraction_prompt = PromptTemplate.from_template(extraction_prompt_template)
        
        conversation_text = self._format_messages(messages)
        
        try:
            chain = extraction_prompt | self.llm | JsonOutputParser()
            result = chain.invoke({"conversation": conversation_text})
            
            facts = []
            for fact_dict in result.get("facts", []):
                if "source" in fact_dict:
                    if isinstance(fact_dict["source"], bool):
                        fact_dict["source"] = "assistant" if fact_dict["source"] else "user"
                    elif fact_dict["source"] not in ["user", "assistant"]:
                        fact_dict["source"] = "assistant"
                
                for field in ["subject", "predicate", "object"]:
                    if field in fact_dict and not isinstance(fact_dict[field], str):
                        fact_dict[field] = str(fact_dict[field])
                
                try:
                    facts.append(SemanticFact(**fact_dict))
                except Exception:
                    continue
                    
            return facts
        except Exception as e:
            print(f"Fact extraction error: {e}")
            return []
    
    def store_semantic_facts(self, facts: List[SemanticFact], user_id: Optional[str] = None) -> int:
        if user_id is None:
            user_id = self.current_user_id
            
        documents = []
        for fact in facts:
            documents.append(Document(
                page_content=f"{fact.subject} {fact.predicate} {fact.object}",
                metadata={
                    "type": "semantic",
                    "user_id": user_id,
                    "subject": fact.subject,
                    "predicate": fact.predicate,
                    "object": fact.object,
                    "confidence": fact.confidence,
                    "timestamp": datetime.now().isoformat()
                }
            ))
        
        if documents:
            self.vector_store.add_documents(documents)
        return len(documents)
    
    def retrieve_semantic_facts(self, query: str, user_id: Optional[str] = None, k: int = 5) -> List[Dict]:
        if user_id is None:
            user_id = self.current_user_id
            
        results = self.vector_store.similarity_search(
            query=query,
            k=k,
            filter={"$and": [{"type": {"$eq": "semantic"}}, {"user_id": {"$eq": user_id}}]}
        )
        
        return [{
            "subject": doc.metadata.get("subject"),
            "predicate": doc.metadata.get("predicate"),
            "object": doc.metadata.get("object"),
            "confidence": doc.metadata.get("confidence", 1.0)
        } for doc in results]
    
    def _format_messages(self, messages: List) -> str:
        conversation_text = ""
        for msg in messages:
            if isinstance(msg, tuple):
                conversation_text += f"{msg[0]}: {msg[1]}\n"
            elif isinstance(msg, BaseMessage):
                conversation_text += f"{msg.type}: {msg.content}\n"
            else:
                conversation_text += str(msg) + "\n"
        return conversation_text
    
    