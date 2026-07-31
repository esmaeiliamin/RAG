# investment_advisor_data.py (updated version with original content)
"""
Enhanced synthesized data for Investment Advisor Agent with realistic conversation structure
All content is original and conversational
"""

import os
import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

class QueryType(Enum):
    """Types of queries users make"""
    PERFORMANCE_ANALYSIS = "performance_analysis"
    EXPOSURE_ANALYSIS = "exposure_analysis"
    COMPOSITION_ANALYSIS = "composition_analysis"
    RANKING_ANALYSIS = "ranking_analysis"
    REBALANCING = "rebalancing"
    TAX_PLANNING = "tax_planning"
    RISK_ASSESSMENT = "risk_assessment"
    MARKET_OUTLOOK = "market_outlook"

class Topic(Enum):
    """Main topics in conversations"""
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    MARKET_CONDITIONS = "market_conditions"
    INVESTMENT_STRATEGY = "investment_strategy"
    TAX_OPTIMIZATION = "tax_optimization"
    RISK_MANAGEMENT = "risk_management"

@dataclass
class RealisticMessage:
    """Message structure matching real data"""
    role: str
    content: str

@dataclass
class BehavioralSignals:
    """Behavioral signals from conversation"""
    provided_specific_data: bool
    used_retrieval: bool
    personalized_response: bool
    asked_clarification: bool
    error_occurred: bool
    sorted_results: bool
    showed_empathy: bool = False
    explained_jargon: bool = False
    referenced_context: bool = False

@dataclass
class ConversationData:
    """Complete conversation data structure matching real format"""
    conversation_id: str
    user_id: int
    timestamp: str
    messages: List[Dict[str, str]]
    feedback: Dict[str, Any]
    behavioral_signals: Dict[str, bool]
    metadata: Dict[str, Any]

class EnhancedInvestmentAdvisorDataGenerator:
    """Generate realistic investment advisor conversations matching real data structure"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.base_date = datetime(2025, 8, 1)
        
        # Set domain directory
        self.domain_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Real portfolio data templates
        self.portfolio_templates = {
            "conservative": {
                "holdings": ["BND", "AGG", "VCIT", "TLT", "IEF", "SPY", "VTI"],
                "allocation": {"bonds": 0.7, "stocks": 0.3},
                "avg_yield": 0.04
            },
            "moderate": {
                "holdings": ["SPY", "QQQ", "BND", "VTI", "VXUS", "GLD", "VCIT"],
                "allocation": {"stocks": 0.6, "bonds": 0.3, "alternatives": 0.1},
                "avg_yield": 0.025
            },
            "aggressive": {
                "holdings": ["NVDA", "TSLA", "QQQ", "ARKK", "SPY", "TQQQ", "AMD"],
                "allocation": {"stocks": 0.9, "alternatives": 0.1},
                "avg_yield": 0.01
            },
            "income_focused": {
                "holdings": ["VNQ", "DGRO", "VCIT", "DIV", "VYM", "SCHD", "REZ"],
                "allocation": {"dividend_stocks": 0.5, "bonds": 0.5},
                "avg_yield": 0.06
            }
        }
        # Original response templates - completely different from provided data
        self.response_templates = {
            "performance_success": [
                "Looking at your investments from {start_date} through {end_date}, you've seen a {percent}% {gain_loss}. That translates to about ${amount} in actual dollars. The standout winner has been {top_gainer} which contributed ${gainer_amount} to your returns. On the flip side, {top_loser} has been weighing things down a bit with a ${loser_amount} decline. Keep in mind these numbers reflect your current positions.",
                "Hey, quick update on your investments - you're {direction} {percent}% as of now, which means you've {gained_lost} about ${amount}. {top_holding} is really carrying the team today with a {holding_percent}% gain. Not bad at all!",
                "So I've run the numbers for you. Since {start_date}, your investments have moved {percent}% {direction}, putting you {gain_loss} ${amount}. What's interesting is that {top_gainer} alone accounts for ${gainer_amount} of that movement. Meanwhile, {top_loser} has been a bit of a drag, but that's pretty normal market behavior."
            ],
            "exposure_success": [
                "I can see you've got {percent}% of your money in {sector} right now. Most of that comes from three main positions: {holding1} makes up {percent1}%, then {holding2} at {percent2}%, and {holding3} at {percent3}%. This makes {sector} your {rank} biggest area of investment.",
                "Let me break down your {category} exposure for you - it's sitting at {percent}% of your total investments. The main contributors here are {holdings_list}. This seems pretty reasonable given your overall strategy.",
                "Your {sector} allocation is currently {percent}%. The heavy lifters in this category are {holding1} and {holding2}, which together make up most of that exposure. Is this level comfortable for you?"
            ],
            "error_response": [
                "Hmm, I'm running into a technical hiccup trying to pull that information. Mind giving me another moment?",
                "Something's not quite right with my data connection. Let me try a different approach to get you that answer.",
                "I'm having trouble accessing those specific details right now. Can we try looking at this from a different angle?"
            ],
            "clarification_needed": [
                "Just to make sure I give you the most useful information - are you asking about {clarification}?",
                "I want to make sure I understand correctly. Are you interested in {option1} or {option2}?",
                "Before I dive in, let me clarify - you're looking for information about {topic}, right?"
            ]
        }
        # Tool combinations based on query types
        self.tool_patterns = {
            QueryType.PERFORMANCE_ANALYSIS: ["get_portfolio", "get_attribute", "calculate_returns"],
            QueryType.EXPOSURE_ANALYSIS: ["get_portfolio", "factor_contribution", "filter"],
            QueryType.COMPOSITION_ANALYSIS: ["get_portfolio", "aggregate", "filter"],
            QueryType.RANKING_ANALYSIS: ["get_portfolio", "get_attribute", "sort", "filter"],
            QueryType.REBALANCING: ["get_portfolio", "optimize", "calculate_trades"],
            QueryType.TAX_PLANNING: ["get_transactions", "calculate_tax", "filter"],
            QueryType.RISK_ASSESSMENT: ["get_portfolio", "calculate_var", "stress_test"],
            QueryType.MARKET_OUTLOOK: ["get_market_data", "analyze_trends"]
        }
        