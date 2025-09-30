"""
Insight generator for producing actionable recommendations.
"""

from typing import List, Dict, Optional
from datetime import datetime

from .models import Property, PropertyType
from .predictive_engine import PredictiveEngine, PredictionResult
from .analytics import MarketAnalyzer, InvestmentAnalyzer, InvestmentOpportunity


class InsightGenerator:
    """
    Generates actionable insights for buyers, sellers, and investors.
    """
    
    def __init__(
        self,
        predictive_engine: PredictiveEngine,
        market_analyzer: MarketAnalyzer,
        investment_analyzer: InvestmentAnalyzer
    ):
        """
        Initialize the insight generator.
        
        Args:
            predictive_engine: PredictiveEngine instance
            market_analyzer: MarketAnalyzer instance
            investment_analyzer: InvestmentAnalyzer instance
        """
        self.predictive_engine = predictive_engine
        self.market_analyzer = market_analyzer
        self.investment_analyzer = investment_analyzer
    
    def generate_buyer_insights(
        self,
        property: Property,
        budget: float
    ) -> Dict[str, any]:
        """
        Generate insights for potential buyers.
        
        Args:
            property: Property being considered
            budget: Buyer's budget
            
        Returns:
            Dictionary containing buyer insights
        """
        # Get property prediction
        prediction = self.predictive_engine.predict_property_value(property)
        
        # Get market analysis
        trend = self.market_analyzer.analyze_market_trend(property.location)
        heat_index = self.market_analyzer.calculate_market_heat_index(property.location)
        
        # Determine if it's a good time to buy
        timing_recommendation = self._assess_buying_timing(trend, heat_index)
        
        # Calculate value assessment
        value_assessment = self._assess_property_value(
            prediction.predicted_value, 
            budget
        )
        
        # Generate negotiation insights
        negotiation_tips = self._generate_negotiation_tips(
            prediction, trend, heat_index
        )
        
        # Calculate affordability metrics
        affordability = self._calculate_affordability(budget, prediction.predicted_value)
        
        # Generate future value projection
        future_value = self._project_future_value(property, prediction)
        
        return {
            "property_id": property.property_id,
            "predicted_value": prediction.predicted_value,
            "confidence_interval": prediction.confidence_interval,
            "confidence_level": prediction.confidence_level,
            "value_assessment": value_assessment,
            "budget_fit": affordability,
            "market_conditions": {
                "trend": trend.trend_direction,
                "heat_index": heat_index,
                "price_change_6m": trend.price_change_percent
            },
            "timing": timing_recommendation,
            "negotiation_tips": negotiation_tips,
            "future_projections": future_value,
            "key_insights": self._generate_buyer_key_insights(
                prediction, trend, value_assessment, affordability
            )
        }
    
    def generate_seller_insights(
        self,
        property: Property,
        desired_price: Optional[float] = None
    ) -> Dict[str, any]:
        """
        Generate insights for potential sellers.
        
        Args:
            property: Property being sold
            desired_price: Seller's desired price (optional)
            
        Returns:
            Dictionary containing seller insights
        """
        # Get property prediction
        prediction = self.predictive_engine.predict_property_value(property)
        
        # Get market analysis
        trend = self.market_analyzer.analyze_market_trend(property.location)
        heat_index = self.market_analyzer.calculate_market_heat_index(property.location)
        velocity = self.market_analyzer.calculate_market_velocity(property.location)
        
        # Determine if it's a good time to sell
        timing_recommendation = self._assess_selling_timing(trend, heat_index, velocity)
        
        # Price recommendations
        price_strategy = self._generate_pricing_strategy(
            prediction, desired_price, heat_index
        )
        
        # Estimate time to sell
        estimated_days_on_market = self._estimate_time_to_sell(
            property.location, price_strategy["recommended_list_price"], 
            prediction.predicted_value
        )
        
        # Generate marketing recommendations
        marketing_tips = self._generate_marketing_tips(property, trend)
        
        return {
            "property_id": property.property_id,
            "market_value": prediction.predicted_value,
            "confidence_interval": prediction.confidence_interval,
            "confidence_level": prediction.confidence_level,
            "market_conditions": {
                "trend": trend.trend_direction,
                "heat_index": heat_index,
                "velocity": velocity,
                "price_change_6m": trend.price_change_percent
            },
            "timing": timing_recommendation,
            "pricing_strategy": price_strategy,
            "estimated_days_on_market": estimated_days_on_market,
            "marketing_recommendations": marketing_tips,
            "key_insights": self._generate_seller_key_insights(
                prediction, trend, heat_index, timing_recommendation
            )
        }
    
    def generate_investor_insights(
        self,
        budget: float,
        investment_goals: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Generate insights for investors.
        
        Args:
            budget: Investment budget
            investment_goals: Dictionary with goals (min_roi, risk_tolerance, etc.)
            
        Returns:
            Dictionary containing investor insights
        """
        # Get investment opportunities
        min_roi = investment_goals.get("min_roi", 15.0)
        opportunities = self.investment_analyzer.identify_investment_opportunities(
            max_opportunities=10,
            min_roi=min_roi
        )
        
        # Filter by risk tolerance
        risk_tolerance = investment_goals.get("risk_tolerance", "medium")
        filtered_opportunities = self._filter_by_risk(opportunities, risk_tolerance)
        
        # Get emerging markets
        emerging_markets = self.market_analyzer.identify_emerging_markets()
        
        # Generate portfolio recommendations
        portfolio_strategy = self._generate_portfolio_strategy(
            filtered_opportunities, budget, investment_goals
        )
        
        return {
            "budget": budget,
            "investment_goals": investment_goals,
            "top_opportunities": [
                self._format_opportunity(opp) 
                for opp in filtered_opportunities[:5]
            ],
            "emerging_markets": emerging_markets,
            "portfolio_strategy": portfolio_strategy,
            "market_overview": self._generate_market_overview(),
            "key_insights": self._generate_investor_key_insights(
                filtered_opportunities, emerging_markets
            )
        }
    
    def generate_comprehensive_report(
        self,
        property: Property,
        analysis_type: str = "all"
    ) -> Dict[str, any]:
        """
        Generate comprehensive property analysis report.
        
        Args:
            property: Property to analyze
            analysis_type: Type of analysis ('buyer', 'seller', 'investor', 'all')
            
        Returns:
            Comprehensive analysis report
        """
        # Get core predictions
        prediction = self.predictive_engine.predict_property_value(property)
        
        # Get market analysis
        trend = self.market_analyzer.analyze_market_trend(property.location)
        heat_index = self.market_analyzer.calculate_market_heat_index(property.location)
        
        # Calculate rental metrics
        rental_yield = self.investment_analyzer.calculate_rental_yield(
            property, prediction.predicted_value
        )
        
        roi_projection = self.investment_analyzer.predict_roi(
            property, prediction.predicted_value, holding_period_years=5
        )
        
        report = {
            "property": {
                "id": property.property_id,
                "location": property.location,
                "type": property.property_type.value,
                "square_footage": property.square_footage,
                "bedrooms": property.bedrooms,
                "bathrooms": property.bathrooms,
                "age": property.calculate_age()
            },
            "valuation": {
                "predicted_value": prediction.predicted_value,
                "confidence_interval": prediction.confidence_interval,
                "confidence_level": prediction.confidence_level,
                "market_trend": prediction.market_trend,
                "contributing_factors": prediction.contributing_factors
            },
            "market_analysis": {
                "area": property.location,
                "trend_direction": trend.trend_direction,
                "price_change_percent": trend.price_change_percent,
                "volume_change_percent": trend.volume_change_percent,
                "heat_index": heat_index,
                "market_velocity": self.market_analyzer.calculate_market_velocity(
                    property.location
                )
            },
            "investment_metrics": {
                "rental_yield": rental_yield,
                "roi_projections": roi_projection
            },
            "recommendations": self._generate_comprehensive_recommendations(
                property, prediction, trend, heat_index
            )
        }
        
        return report
    
    def _assess_buying_timing(self, trend, heat_index: float) -> Dict[str, any]:
        """Assess if it's a good time to buy."""
        score = 50  # Neutral starting point
        recommendation = "Neutral"
        reasons = []
        
        # Market trending down is good for buyers
        if trend.trend_direction == "down":
            score += 20
            reasons.append("Market prices declining - buyer's market")
        elif trend.trend_direction == "up":
            score -= 15
            reasons.append("Market prices rising - act quickly")
        
        # Lower heat index is better for buyers
        if heat_index < 40:
            score += 15
            reasons.append("Low market competition")
        elif heat_index > 70:
            score -= 20
            reasons.append("High market competition - expect bidding wars")
        
        # Determine recommendation
        if score >= 70:
            recommendation = "Excellent time to buy"
        elif score >= 55:
            recommendation = "Good time to buy"
        elif score >= 45:
            recommendation = "Neutral - market is balanced"
        elif score >= 30:
            recommendation = "Challenging market for buyers"
        else:
            recommendation = "Consider waiting for better conditions"
        
        return {
            "score": score,
            "recommendation": recommendation,
            "reasons": reasons
        }
    
    def _assess_selling_timing(self, trend, heat_index: float, velocity: float) -> Dict[str, any]:
        """Assess if it's a good time to sell."""
        score = 50  # Neutral starting point
        recommendation = "Neutral"
        reasons = []
        
        # Market trending up is good for sellers
        if trend.trend_direction == "up":
            score += 20
            reasons.append("Market prices rising - seller's market")
        elif trend.trend_direction == "down":
            score -= 15
            reasons.append("Market prices declining - consider waiting")
        
        # Higher heat index is better for sellers
        if heat_index > 70:
            score += 20
            reasons.append("High market demand")
        elif heat_index < 40:
            score -= 15
            reasons.append("Low market demand")
        
        # High velocity means faster sales
        if velocity > 70:
            score += 10
            reasons.append("Properties selling quickly")
        elif velocity < 40:
            score -= 10
            reasons.append("Properties taking longer to sell")
        
        # Determine recommendation
        if score >= 70:
            recommendation = "Excellent time to sell"
        elif score >= 55:
            recommendation = "Good time to sell"
        elif score >= 45:
            recommendation = "Neutral - market is balanced"
        elif score >= 30:
            recommendation = "Challenging market for sellers"
        else:
            recommendation = "Consider waiting for better conditions"
        
        return {
            "score": score,
            "recommendation": recommendation,
            "reasons": reasons
        }
    
    def _assess_property_value(
        self, 
        predicted_value: float, 
        asking_price: float
    ) -> str:
        """Assess if property is fairly priced."""
        ratio = predicted_value / asking_price
        
        if ratio > 1.15:
            return "Excellent value - priced well below market"
        elif ratio > 1.05:
            return "Good value - priced below market"
        elif ratio > 0.95:
            return "Fair value - priced at market"
        elif ratio > 0.85:
            return "Overpriced - above market value"
        else:
            return "Significantly overpriced - well above market"
    
    def _generate_negotiation_tips(
        self, 
        prediction: PredictionResult,
        trend,
        heat_index: float
    ) -> List[str]:
        """Generate negotiation tips for buyers."""
        tips = []
        
        if heat_index < 50:
            tips.append("Low competition - you have negotiating power")
            tips.append("Consider offering 5-10% below asking price")
        else:
            tips.append("High competition - be prepared to act quickly")
            tips.append("Consider offering close to asking price")
        
        if trend.trend_direction == "down":
            tips.append("Declining market - use recent comparables in negotiation")
        
        if prediction.confidence_level > 0.8:
            tips.append(f"Strong data supports value of ${prediction.predicted_value:,.0f}")
        
        return tips
    
    def _calculate_affordability(self, budget: float, price: float) -> str:
        """Calculate affordability assessment."""
        ratio = price / budget
        
        if ratio <= 0.85:
            return "Well within budget"
        elif ratio <= 1.0:
            return "Within budget"
        elif ratio <= 1.1:
            return "Slightly over budget"
        else:
            return "Over budget"
    
    def _project_future_value(
        self, 
        property: Property, 
        prediction: PredictionResult
    ) -> Dict[str, float]:
        """Project future property values."""
        current_value = prediction.predicted_value
        
        # Get market forecast
        forecast = self.predictive_engine.forecast_market_trend(
            property.location, months_ahead=36
        )
        
        if not forecast:
            # Use simple appreciation if no forecast available
            return {
                "1_year": current_value * 1.03,
                "3_year": current_value * 1.09,
                "5_year": current_value * 1.15
            }
        
        # Use forecast data
        forecast_dates = sorted(forecast.keys())
        
        return {
            "1_year": forecast.get(forecast_dates[11], current_value * 1.03) if len(forecast_dates) > 11 else current_value * 1.03,
            "3_year": forecast.get(forecast_dates[-1], current_value * 1.09) if len(forecast_dates) > 0 else current_value * 1.09,
            "5_year": current_value * 1.15  # Conservative 5-year estimate
        }
    
    def _generate_pricing_strategy(
        self,
        prediction: PredictionResult,
        desired_price: Optional[float],
        heat_index: float
    ) -> Dict[str, any]:
        """Generate pricing strategy for sellers."""
        market_value = prediction.predicted_value
        
        # Adjust based on market conditions
        if heat_index > 70:
            # Hot market - can price higher
            recommended_price = market_value * 1.05
            strategy = "Price at premium due to high demand"
        elif heat_index < 40:
            # Cold market - price competitively
            recommended_price = market_value * 0.95
            strategy = "Price competitively to attract buyers"
        else:
            recommended_price = market_value
            strategy = "Price at market value"
        
        return {
            "market_value": market_value,
            "recommended_list_price": recommended_price,
            "strategy": strategy,
            "pricing_range": {
                "minimum": market_value * 0.90,
                "optimal": recommended_price,
                "maximum": market_value * 1.10
            }
        }
    
    def _estimate_time_to_sell(
        self, 
        location: str, 
        list_price: float, 
        market_value: float
    ) -> int:
        """Estimate days on market."""
        # Get market velocity
        velocity = self.market_analyzer.calculate_market_velocity(location)
        
        # Base days from velocity
        base_days = int(100 - velocity)
        
        # Adjust for pricing
        price_ratio = list_price / market_value
        if price_ratio > 1.1:
            base_days = int(base_days * 1.5)
        elif price_ratio < 0.95:
            base_days = int(base_days * 0.7)
        
        return max(base_days, 7)  # Minimum 7 days
    
    def _generate_marketing_tips(self, property: Property, trend) -> List[str]:
        """Generate marketing tips for sellers."""
        tips = []
        
        tips.append("Professional photos are essential")
        tips.append("Stage the property to highlight its best features")
        
        if property.amenities:
            tips.append(f"Highlight proximity to {', '.join(property.amenities[:3])}")
        
        if trend.trend_direction == "up":
            tips.append("Emphasize market appreciation in marketing materials")
        
        if property.calculate_age() and property.calculate_age() < 5:
            tips.append("Emphasize modern construction and features")
        
        return tips
    
    def _filter_by_risk(
        self, 
        opportunities: List[InvestmentOpportunity], 
        risk_tolerance: str
    ) -> List[InvestmentOpportunity]:
        """Filter opportunities by risk tolerance."""
        if risk_tolerance == "low":
            return [opp for opp in opportunities if opp.risk_level == "low"]
        elif risk_tolerance == "medium":
            return [opp for opp in opportunities if opp.risk_level in ["low", "medium"]]
        else:  # high
            return opportunities
    
    def _generate_portfolio_strategy(
        self,
        opportunities: List[InvestmentOpportunity],
        budget: float,
        goals: Dict[str, any]
    ) -> Dict[str, any]:
        """Generate investment portfolio strategy."""
        strategy = {
            "recommended_allocation": [],
            "diversification_strategy": "",
            "expected_portfolio_roi": 0.0
        }
        
        if not opportunities:
            strategy["diversification_strategy"] = "Insufficient opportunities at current criteria"
            return strategy
        
        # Diversification recommendation
        if budget > 1000000:
            strategy["diversification_strategy"] = "Diversify across 3-5 properties in different areas"
            allocation_count = min(5, len(opportunities))
        elif budget > 500000:
            strategy["diversification_strategy"] = "Consider 2-3 properties for diversification"
            allocation_count = min(3, len(opportunities))
        else:
            strategy["diversification_strategy"] = "Focus on 1-2 high-quality properties"
            allocation_count = min(2, len(opportunities))
        
        # Allocate budget
        per_property = budget / allocation_count
        total_roi = 0
        
        for i, opp in enumerate(opportunities[:allocation_count]):
            strategy["recommended_allocation"].append({
                "location": opp.location,
                "allocation_percent": 100 / allocation_count,
                "estimated_investment": per_property,
                "expected_roi": opp.predicted_roi,
                "risk_level": opp.risk_level
            })
            total_roi += opp.predicted_roi
        
        strategy["expected_portfolio_roi"] = total_roi / allocation_count
        
        return strategy
    
    def _generate_market_overview(self) -> Dict[str, any]:
        """Generate overall market overview."""
        return {
            "overall_trend": "Data-driven analysis based on available market data",
            "recommendation": "Review individual opportunities for specific insights"
        }
    
    def _format_opportunity(self, opp: InvestmentOpportunity) -> Dict[str, any]:
        """Format opportunity for output."""
        return {
            "location": opp.location,
            "opportunity_score": round(opp.opportunity_score, 2),
            "predicted_roi": round(opp.predicted_roi, 2),
            "rental_yield": round(opp.rental_yield, 2),
            "risk_level": opp.risk_level,
            "time_horizon": opp.time_horizon,
            "key_factors": opp.key_factors,
            "recommendation": opp.recommendation
        }
    
    def _generate_buyer_key_insights(
        self, 
        prediction, 
        trend, 
        value_assessment, 
        affordability
    ) -> List[str]:
        """Generate key insights for buyers."""
        insights = []
        
        insights.append(f"Property valued at ${prediction.predicted_value:,.0f} with {prediction.confidence_level*100:.0f}% confidence")
        insights.append(f"Value assessment: {value_assessment}")
        insights.append(f"Affordability: {affordability}")
        insights.append(f"Market trend: {trend.trend_direction}")
        
        return insights
    
    def _generate_seller_key_insights(
        self, 
        prediction, 
        trend, 
        heat_index, 
        timing
    ) -> List[str]:
        """Generate key insights for sellers."""
        insights = []
        
        insights.append(f"Market value: ${prediction.predicted_value:,.0f}")
        insights.append(f"Market conditions: {trend.trend_direction} market")
        insights.append(f"Market heat index: {heat_index:.0f}/100")
        insights.append(f"Timing: {timing['recommendation']}")
        
        return insights
    
    def _generate_investor_key_insights(
        self,
        opportunities: List[InvestmentOpportunity],
        emerging_markets: List[str]
    ) -> List[str]:
        """Generate key insights for investors."""
        insights = []
        
        if opportunities:
            top = opportunities[0]
            insights.append(f"Top opportunity: {top.location} with {top.opportunity_score:.0f}/100 score")
            insights.append(f"Expected ROI: {top.predicted_roi:.1f}%")
        
        if emerging_markets:
            insights.append(f"Emerging markets: {', '.join(emerging_markets[:3])}")
        
        insights.append("Diversification recommended for risk management")
        
        return insights
    
    def _generate_comprehensive_recommendations(
        self,
        property: Property,
        prediction: PredictionResult,
        trend,
        heat_index: float
    ) -> List[str]:
        """Generate comprehensive recommendations."""
        recommendations = []
        
        # Value recommendation
        recommendations.append(
            f"Property is valued at ${prediction.predicted_value:,.0f} "
            f"with {prediction.market_trend} market trend"
        )
        
        # Market condition recommendation
        if heat_index > 70:
            recommendations.append("High market demand - competitive environment")
        elif heat_index < 40:
            recommendations.append("Lower market demand - negotiation opportunities")
        
        # Timing recommendation
        if trend.trend_direction == "up":
            recommendations.append("Appreciation expected - good for sellers, buyers should act quickly")
        elif trend.trend_direction == "down":
            recommendations.append("Market softening - good for buyers, sellers may want to wait")
        
        return recommendations
