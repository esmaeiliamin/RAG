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


def process_baseline_conversations(full_agent, conversations, num_baseline=30):
    """Process baseline conversations and return learning summary."""
    from collections import defaultdict
    
    baseline_conversations = conversations[:num_baseline]
    learning_summary = defaultdict(int)
    processed = defaultdict(set)
    facts_extracted = 0
    extraction_errors = 0
    
    for i, conv in enumerate(baseline_conversations):
        user_id = str(conv['user_id'])
        messages = [(msg['role'], msg['content']) for msg in conv['messages']]
        
        # Store episodic memory
        full_agent.store_episodic_memory(
            conversation_id=conv['conversation_id'],
            messages=messages,
            summary=f"Investment discussion - satisfaction: {conv['feedback']['satisfaction_score']}/5.0"
        )
        
        # Extract semantic facts
        try:
            facts = full_agent.extract_semantic_facts(messages)
            if facts:
                facts_extracted += full_agent.store_semantic_facts(facts, user_id=user_id)
        except Exception:
            extraction_errors += 1
        
        # Learn from successful conversations
        if conv['feedback']['success'] and conv['feedback']['satisfaction_score'] >= 4.0:
            communities, user_profile = identify_user_community(conv)

            # Assign user to community
            for community in communities:
                if user_id not in full_agent.procedural_memory.user_communities:
                    full_agent.procedural_memory.user_communities[user_id] = []
                if community not in full_agent.procedural_memory.user_communities[user_id]:
                    full_agent.procedural_memory.user_communities[user_id].append(community)
                    full_agent.procedural_memory.community_members[community].add(user_id)
                    processed['communities'].add(community)

            # Learn patterns
            learning_result = full_agent.procedural_memory.learn_from_interaction(
                query=conv['messages'][0]['content'],
                interaction_data={
                    'messages': conv['messages'],
                    'success': True,
                    'client_satisfaction': conv['feedback']['satisfaction_score'],
                    'query_type': conv['metadata'].get('query_type', 'unknown')
                },
                user_id=user_id,
                user_profile=user_profile
            )
            # Track learning
            for key in ['global_learned', 'user_learned', 'community_learned', 'task_learned']:
                if learning_result.get(key):
                    scope = key.replace('_learned', '')
                    learning_summary[scope] += 1
                    if scope == 'user':
                        processed['users'].add(user_id)
                    elif scope == 'task':
                        task = full_agent.procedural_memory._identify_task_type(conv['messages'][0]['content'])
                        processed['tasks'].add(task)
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(baseline_conversations)}...")
    
    return {
        'baseline_count': len(baseline_conversations),
        'facts_extracted': facts_extracted,
        'extraction_errors': extraction_errors,
        'learning_summary': dict(learning_summary),
        'processed': {k: len(v) for k, v in processed.items()}
    }
