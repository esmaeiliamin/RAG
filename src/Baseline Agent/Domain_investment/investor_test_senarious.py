"""Test scenarios and data for investment memory hierarchical retrieval demonstration."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from procedural_memory import DomainProcedure

def setup_hierarchy_demo(investment_memory):
    """Setup all test data for hierarchical retrieval demonstration."""
    
    # Community procedures
    investment_memory.community_procedures["moderate_professionals"] = {
        "moderate_prof_strategy": DomainProcedure(
            strategy_pattern="moderate_prof_strategy",
            steps=["Community step 1: Balanced approach", "Community step 2: Diversify"],
            segments=["moderate_professionals"],
            success_rate=0.85,
            scope="community",
            scope_id="moderate_professionals"
        )
    }
    investment_memory.user_communities["user_003"] = ["moderate_professionals"]

    # Task procedures
    investment_memory.task_procedures["rebalancing"] = {
        "rebalancing_specialist": DomainProcedure(
            strategy_pattern="rebalancing_specialist",
            steps=["Task step 1: Analyze drift", "Task step 2: Execute trades"],
            segments=["rebalancing"],
            success_rate=0.88,
            scope="task",
            scope_id="rebalancing"
        )
    }
    
    # Global procedures
    investment_memory.global_procedures["general_investment"] = DomainProcedure(
        strategy_pattern="general_investment",
        steps=["Global step 1: Assess situation", "Global step 2: Provide guidance"],
        segments=["general"],
        success_rate=0.75,
        scope="global"
    )

def get_test_cases():
    """Return test cases for demonstrating retrieval hierarchy."""
    return [
        ("user_001", "I want to rebalance", {"age": 35, "risk_tolerance": "moderate"}, 
         "Should retrieve USER scope (user_001 has personalized strategy)"),
        ("user_003", "Need investment advice", {"age": 45, "risk_tolerance": "moderate"},
         "Should retrieve COMMUNITY scope (user_003 in moderate_professionals)"),
        ("user_004", "Time to rebalance my portfolio", {"age": 50, "risk_tolerance": "conservative"},
         "Should retrieve TASK scope (rebalancing task identified)"),
        ("user_005", "General investment question", {"age": 25, "risk_tolerance": "aggressive"},
         "Should retrieve GLOBAL scope (no specific matches)")
    ]

def get_feedback_rounds():
    """Return feedback rounds for performance testing."""
    return [
        {"client_satisfaction": 9, "returns": 12.5, "goals_achieved": True},   # Good
        {"client_satisfaction": 8, "returns": 8.0, "goals_achieved": True},    # Good
        {"client_satisfaction": 4, "returns": -2.0, "goals_achieved": False},  # Bad
        {"client_satisfaction": 7, "returns": 5.0, "goals_achieved": True},    # OK
    ]
