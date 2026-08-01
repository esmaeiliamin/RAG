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

def run_performance_feedback(investment_memory, domain_agent, strategy_key="general_investment"):
    """Run performance feedback demonstration with the given strategy."""
    test_strategy = investment_memory.global_procedures[strategy_key]
    initial_success = test_strategy.success_rate
    initial_metrics = test_strategy.domain_metrics.copy()
    
    print(f"\nInitial state of '{strategy_key}' strategy:")
    print(f"  Success rate: {initial_success:.0%}")
    print(f"  Domain metrics: {initial_metrics}")
    print(f"  Adaptations: {len(test_strategy.adaptations)}")
    
    print("\n📈 Applying feedback rounds:")
    for i, feedback in enumerate(get_feedback_rounds(), 1):
        expected_score = domain_agent.calculate_success_score(feedback)
        old_rate = test_strategy.success_rate
        
        result = investment_memory.update_from_performance(
            strategy=strategy_key,
            performance_data=feedback,
            scope="global"
        )
        
        print(f"\nRound {i}: Satisfaction={feedback['client_satisfaction']}, "
              f"Returns={feedback['returns']:+.1f}%")
        print(f"  Success score: {expected_score:.0%}")
        
        if result.get('updated'):
            print(f"  Success rate: {old_rate:.0%} → {result['new_success_rate']:.0%}")
            print(f"  Trend: {result['performance_trend']}")
            
            if 'avg_portfolio_performance' in test_strategy.domain_metrics:
                print(f"  Avg portfolio: {test_strategy.domain_metrics['avg_portfolio_performance']:.1f}%")
        else:
            print(f"  ✗ Strategy not found for update")

    # Show adaptation history
    print(f"\n📚 Adaptation History:")
    print(f"  Total adaptations: {len(test_strategy.adaptations)}")
    if test_strategy.adaptations:
        for i, adaptation in enumerate(test_strategy.adaptations[-2:], 1):
            print(f"\n  Adaptation {i}:")
            print(f"    Time: {adaptation['timestamp'][:19]}")
            print(f"    Old rate: {adaptation['old_rate']:.0%}")
            print(f"    New rate: {adaptation['new_rate']:.0%}")
            print(f"    Success score: {adaptation['success_score']:.0%}")
    
def identify_user_community(conv):
    """Identify user's community from metadata."""
    metadata = conv.get('metadata', {})
    age = metadata.get('client_age', 35)
    risk = metadata.get('risk_tolerance', 'moderate')
    
    if age >= 60 and risk == "conservative":
        community = "conservative_retirees"
    elif age <= 40 and risk == "aggressive":
        community = "aggressive_millennials"
    else:
        community = "moderate_professionals"
    
    return [community], {"age": age, "risk_tolerance": risk}
