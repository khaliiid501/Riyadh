"""
Riyadh - Predictive Real Estate Analytics System

A comprehensive real estate analytics platform that forecasts property values
and market trends based on historical sales data, neighborhood demographics,
economic indicators, and seasonal fluctuations.
"""

__version__ = "1.0.0"
__author__ = "Riyadh Development Team"

from .models import Property, MarketData, Transaction, Neighborhood, PropertyType
from .predictive_engine import PredictiveEngine, PredictionResult
from .analytics import MarketAnalyzer, InvestmentAnalyzer, MarketTrend, InvestmentOpportunity
from .insights import InsightGenerator

__all__ = [
    "Property",
    "MarketData",
    "Transaction",
    "Neighborhood",
    "PropertyType",
    "PredictiveEngine",
    "PredictionResult",
    "MarketAnalyzer",
    "InvestmentAnalyzer",
    "MarketTrend",
    "InvestmentOpportunity",
    "InsightGenerator",
]
