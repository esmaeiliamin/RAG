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

