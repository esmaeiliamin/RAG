# domain_investment/investment_advisor_agent.py
import os
import sys
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain_agent import DomainAgent, DomainProcedure
from typing import Dict, List, Optional
from .investment_advisor_prompts import INVESTMENT_PROMPTS

class InvestmentAdvisorAgent(DomainAgent):
    """Investment advisor specific implementation"""
    
    def __init__(self):
        # Set domain-specific paths
        self.domain_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.domain_dir, "investment_advisor_data")
        
        # Use generic "domain_memory_store" name for reusability across domains
        self.memory_dir = os.path.join(self.domain_dir, "domain_memory_store")
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.memory_dir, exist_ok=True)
    
    def get_procedure_class(self) -> type:
        return DomainProcedure

    def get_optimization_prompt(self, prompt_type: str) -> str:
        """Get optimization prompt by type"""
        from .investment_advisor_prompts import get_optimization_prompt
        return get_optimization_prompt(prompt_type)