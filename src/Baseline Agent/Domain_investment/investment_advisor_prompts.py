# domain_investment/investment_advisor_prompts.py
"""Investment advisor specific prompts"""

# ============== INVESTMENT LEARNING PROMPTS ==============

INVESTMENT_GLOBAL_PROMPT = """
Analyze this investment advisory interaction.

Query: {task}
Interaction: {execution_data}
Existing: {existing}

Output JSON with EXACT format:
{{
    "procedure": {{
        "strategy_pattern": "investment pattern name",
        "steps": ["step 1", "step 2", "step 3"],
        "segments": ["moderate_risk", "millennials"],
        "confidence": 0.85,
        "domain_metrics": {{"avg_portfolio_performance": 8.5}}
    }}
}}

CRITICAL FORMAT RULES:
- segments: array of simple strings like ["aggressive", "retirees"]
- domain_metrics: dict with float values like {{"returns": 10.5, "sharpe": 1.2}}
- NO complex objects, NO descriptions in arrays
"""

INVESTMENT_USER_PROMPT = """
Analyze user {user_id}'s investment preferences.

Query: {task}
Interaction: {execution_data}

Output JSON:
{{
    "procedure": {{
        "strategy_pattern": "user investment preference",
        "steps": ["personalized step 1", "personalized step 2"],
        "segments": ["user_preference"],
        "confidence": 0.9,
        "domain_metrics": {{}}
    }}
}}

segments must be simple strings, domain_metrics must have numeric values only
"""

INVESTMENT_COMMUNITY_PROMPT = """
Analyze {community_segment} investment patterns.

Interaction: {execution_data}

Output JSON:
{{
    "procedure": {{
        "strategy_pattern": "{community_segment} approach",
        "steps": ["community step 1", "community step 2"],
        "segments": ["{community_segment}"],
        "confidence": 0.87,
        "domain_metrics": {{"avg_returns": 0.0}}
    }}
}}
"""

INVESTMENT_TASK_PROMPT = """
Analyze this {task_type} investment task.

Task Type: {task_type}
Query: {task}
Interaction: {execution_data}

Output JSON:
{{
    "procedure": {{
        "strategy_pattern": "{task_type} investment strategy",
        "steps": ["task step 1", "task step 2"],
        "segments": ["{task_type}"],
        "confidence": 0.88,
        "domain_metrics": {{}}
    }}
}}
"""

