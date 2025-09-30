"""
Analytics modules for market analysis and investment insights.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .models import Property, Transaction, MarketData, Neighborhood, PropertyType


@dataclass
class MarketTrend:
    """Market trend analysis results."""
    area: str
    trend_direction: str  # 'up', 'down', 'stable'
    price_change_percent: float
    volume_change_percent: float
    inventory_change_percent: float
    analysis_period: Tuple[datetime, datetime]
    confidence_score: float


@dataclass
class InvestmentOpportunity:
    """Represents an investment opportunity."""
    location: str
    opportunity_score: float  # 0-100
    predicted_roi: float  # Expected return on investment
    predicted_appreciation: float  # Expected property appreciation
    rental_yield: float  # Expected rental yield
    risk_level: str  # 'low', 'medium', 'high'
    time_horizon: str  # 'short', 'medium', 'long'
    key_factors: List[str]
    recommendation: str


class MarketAnalyzer:
    """
    Analyzes market trends and conditions.
    """
    
    def __init__(self):
        """Initialize the market analyzer."""
        self.market_data: List[MarketData] = []
        self.transactions: List[Transaction] = []
    
    def add_market_data(self, market_data: List[MarketData]):
        """Add market data for analysis."""
        self.market_data.extend(market_data)
        self.market_data.sort(key=lambda x: x.date)
    
    def add_transactions(self, transactions: List[Transaction]):
        """Add transaction data for analysis."""
        self.transactions.extend(transactions)
        self.transactions.sort(key=lambda x: x.transaction_date)
    
    def analyze_market_trend(
        self,
        area: str,
        period_months: int = 12
    ) -> MarketTrend:
        """
        Analyze market trends for a specific area.
        
        Args:
            area: Geographic area to analyze
            period_months: Number of months to analyze
            
        Returns:
            MarketTrend object with analysis results
        """
        # Filter data for the area
        area_data = [
            md for md in self.market_data 
            if md.area.lower() == area.lower()
        ]
        
        if len(area_data) < 2:
            return MarketTrend(
                area=area,
                trend_direction="unknown",
                price_change_percent=0.0,
                volume_change_percent=0.0,
                inventory_change_percent=0.0,
                analysis_period=(datetime.now(), datetime.now()),
                confidence_score=0.0
            )
        
        # Get data for the specified period
        end_date = area_data[-1].date
        start_date = end_date - timedelta(days=period_months * 30)
        period_data = [
            md for md in area_data 
            if md.date >= start_date
        ]
        
        if len(period_data) < 2:
            period_data = area_data[-2:]
        
        # Calculate changes
        start = period_data[0]
        end = period_data[-1]
        
        price_change = ((end.median_price - start.median_price) / start.median_price) * 100
        volume_change = ((end.total_sales - start.total_sales) / max(start.total_sales, 1)) * 100
        inventory_change = ((end.inventory - start.inventory) / max(start.inventory, 1)) * 100
        
        # Determine trend direction
        if price_change > 3:
            trend_direction = "up"
        elif price_change < -3:
            trend_direction = "down"
        else:
            trend_direction = "stable"
        
        # Calculate confidence based on data availability
        confidence_score = min(len(period_data) / period_months, 1.0)
        
        return MarketTrend(
            area=area,
            trend_direction=trend_direction,
            price_change_percent=price_change,
            volume_change_percent=volume_change,
            inventory_change_percent=inventory_change,
            analysis_period=(start.date, end.date),
            confidence_score=confidence_score
        )
    
    def calculate_market_velocity(self, area: str) -> float:
        """
        Calculate market velocity (how fast properties are selling).
        
        Args:
            area: Geographic area
            
        Returns:
            Velocity score (0-100, higher = faster market)
        """
        area_data = [
            md for md in self.market_data 
            if md.area.lower() == area.lower()
        ]
        
        if not area_data:
            return 50.0  # Neutral
        
        recent = area_data[-1]
        
        # Lower days on market = higher velocity
        velocity_score = max(0, 100 - recent.days_on_market)
        
        # Factor in absorption rate
        absorption = recent.calculate_absorption_rate()
        absorption_score = min(absorption * 100, 50)
        
        return (velocity_score * 0.6) + (absorption_score * 0.4)
    
    def identify_emerging_markets(
        self,
        min_growth_rate: float = 5.0
    ) -> List[str]:
        """
        Identify emerging markets with strong growth potential.
        
        Args:
            min_growth_rate: Minimum price growth rate (%)
            
        Returns:
            List of area names showing strong growth
        """
        emerging = []
        
        # Group data by area
        areas = set(md.area for md in self.market_data)
        
        for area in areas:
            trend = self.analyze_market_trend(area, period_months=6)
            
            # Look for areas with strong price growth
            if (trend.price_change_percent >= min_growth_rate and 
                trend.volume_change_percent > 0):
                emerging.append(area)
        
        return emerging
    
    def calculate_market_heat_index(self, area: str) -> float:
        """
        Calculate a market heat index (0-100).
        Higher values indicate a hotter market.
        
        Args:
            area: Geographic area
            
        Returns:
            Heat index score
        """
        area_data = [
            md for md in self.market_data 
            if md.area.lower() == area.lower()
        ]
        
        if not area_data:
            return 50.0
        
        recent = area_data[-1]
        
        # Calculate components
        velocity = self.calculate_market_velocity(area)
        absorption = min(recent.calculate_absorption_rate() * 100, 100)
        
        # Price trend (positive trend increases heat)
        trend = self.analyze_market_trend(area, period_months=6)
        trend_score = min(max(trend.price_change_percent * 5, 0), 100)
        
        # Inventory level (lower inventory = hotter market)
        inventory_score = max(0, 100 - (recent.inventory / max(recent.total_sales, 1)) * 20)
        
        # Weighted combination
        heat_index = (
            velocity * 0.30 +
            absorption * 0.25 +
            trend_score * 0.25 +
            inventory_score * 0.20
        )
        
        return min(heat_index, 100)


class InvestmentAnalyzer:
    """
    Analyzes investment opportunities and calculates ROI projections.
    """
    
    def __init__(self, market_analyzer: MarketAnalyzer):
        """
        Initialize the investment analyzer.
        
        Args:
            market_analyzer: MarketAnalyzer instance for market data
        """
        self.market_analyzer = market_analyzer
        self.neighborhoods: List[Neighborhood] = []
    
    def add_neighborhoods(self, neighborhoods: List[Neighborhood]):
        """Add neighborhood data for analysis."""
        self.neighborhoods.extend(neighborhoods)
    
    def calculate_rental_yield(
        self,
        property: Property,
        purchase_price: float,
        estimated_monthly_rent: Optional[float] = None
    ) -> float:
        """
        Calculate expected rental yield for a property.
        
        Args:
            property: Property to analyze
            purchase_price: Purchase price of the property
            estimated_monthly_rent: Estimated monthly rent (if known)
            
        Returns:
            Annual rental yield as percentage
        """
        if estimated_monthly_rent is None:
            # Estimate rent based on property characteristics
            estimated_monthly_rent = self._estimate_monthly_rent(property)
        
        annual_rent = estimated_monthly_rent * 12
        rental_yield = (annual_rent / purchase_price) * 100
        
        return rental_yield
    
    def _estimate_monthly_rent(self, property: Property) -> float:
        """Estimate monthly rent for a property."""
        # Base rent per square foot varies by property type
        rent_per_sqft_map = {
            PropertyType.APARTMENT: 1.5,
            PropertyType.VILLA: 1.8,
            PropertyType.TOWNHOUSE: 1.6,
            PropertyType.RESIDENTIAL: 1.5,
            PropertyType.COMMERCIAL: 2.0,
        }
        
        base_rent_per_sqft = rent_per_sqft_map.get(
            property.property_type, 
            1.5
        )
        
        base_rent = property.square_footage * base_rent_per_sqft
        
        # Adjust for amenities
        amenity_bonus = len(property.amenities) * 0.02  # 2% per amenity
        base_rent *= (1.0 + amenity_bonus)
        
        return base_rent
    
    def predict_roi(
        self,
        property: Property,
        purchase_price: float,
        holding_period_years: int = 5,
        expected_appreciation_rate: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Predict return on investment for a property.
        
        Args:
            property: Property to analyze
            purchase_price: Purchase price
            holding_period_years: Investment time horizon
            expected_appreciation_rate: Expected annual appreciation (%)
            
        Returns:
            Dictionary with ROI projections
        """
        # Calculate rental yield
        rental_yield = self.calculate_rental_yield(property, purchase_price)
        
        # Estimate appreciation rate
        if expected_appreciation_rate is None:
            trend = self.market_analyzer.analyze_market_trend(
                property.location, 
                period_months=12
            )
            # Use historical trend but apply dampening
            expected_appreciation_rate = trend.price_change_percent * 0.7
        
        # Calculate total return
        annual_rental_income = purchase_price * (rental_yield / 100)
        total_rental_income = annual_rental_income * holding_period_years
        
        appreciation = purchase_price * (
            (1 + expected_appreciation_rate/100) ** holding_period_years - 1
        )
        
        total_return = total_rental_income + appreciation
        roi_percent = (total_return / purchase_price) * 100
        annual_roi = roi_percent / holding_period_years
        
        return {
            "total_roi_percent": roi_percent,
            "annual_roi_percent": annual_roi,
            "rental_yield_percent": rental_yield,
            "appreciation_percent": (appreciation / purchase_price) * 100,
            "total_rental_income": total_rental_income,
            "total_appreciation": appreciation,
            "total_return": total_return
        }
    
    def identify_investment_opportunities(
        self,
        max_opportunities: int = 5,
        min_roi: float = 15.0
    ) -> List[InvestmentOpportunity]:
        """
        Identify high-potential investment areas.
        
        Args:
            max_opportunities: Maximum number of opportunities to return
            min_roi: Minimum acceptable ROI (%)
            
        Returns:
            List of investment opportunities ranked by score
        """
        opportunities = []
        
        # Analyze each neighborhood
        for neighborhood in self.neighborhoods:
            area = neighborhood.name
            
            # Get market metrics
            trend = self.market_analyzer.analyze_market_trend(area)
            heat_index = self.market_analyzer.calculate_market_heat_index(area)
            velocity = self.market_analyzer.calculate_market_velocity(area)
            
            # Calculate opportunity score
            opportunity_score = self._calculate_opportunity_score(
                neighborhood, trend, heat_index, velocity
            )
            
            # Estimate ROI
            predicted_roi = self._estimate_area_roi(area, trend)
            
            if predicted_roi < min_roi:
                continue
            
            # Determine risk level
            risk_level = self._assess_risk_level(
                trend, heat_index, neighborhood
            )
            
            # Generate key factors
            key_factors = self._identify_key_factors(
                neighborhood, trend, heat_index
            )
            
            # Create recommendation
            recommendation = self._generate_recommendation(
                opportunity_score, predicted_roi, risk_level
            )
            
            opportunity = InvestmentOpportunity(
                location=area,
                opportunity_score=opportunity_score,
                predicted_roi=predicted_roi,
                predicted_appreciation=trend.price_change_percent,
                rental_yield=self._estimate_rental_yield_for_area(area),
                risk_level=risk_level,
                time_horizon=self._determine_time_horizon(trend),
                key_factors=key_factors,
                recommendation=recommendation
            )
            
            opportunities.append(opportunity)
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return opportunities[:max_opportunities]
    
    def _calculate_opportunity_score(
        self,
        neighborhood: Neighborhood,
        trend: MarketTrend,
        heat_index: float,
        velocity: float
    ) -> float:
        """Calculate investment opportunity score (0-100)."""
        # Neighborhood desirability
        desirability = neighborhood.calculate_desirability_score()
        
        # Market conditions
        market_score = (heat_index + velocity) / 2
        
        # Growth potential
        growth_score = min(max(trend.price_change_percent * 5, 0), 50)
        
        # Economic factors
        economic_score = (
            min(neighborhood.employment_rate, 50) +
            min(neighborhood.growth_rate * 10, 25)
        )
        
        # Weighted combination
        opportunity_score = (
            desirability * 0.30 +
            market_score * 0.25 +
            growth_score * 0.25 +
            economic_score * 0.20
        )
        
        return min(opportunity_score, 100)
    
    def _estimate_area_roi(self, area: str, trend: MarketTrend) -> float:
        """Estimate average ROI for an area."""
        # Base ROI from appreciation
        appreciation_roi = trend.price_change_percent * 5  # 5-year projection
        
        # Add rental yield estimate
        rental_roi = self._estimate_rental_yield_for_area(area) * 5
        
        return appreciation_roi + rental_roi
    
    def _estimate_rental_yield_for_area(self, area: str) -> float:
        """Estimate typical rental yield for an area."""
        # Simplified estimation - could be enhanced with actual rental data
        return 6.0  # Default 6% annual yield
    
    def _assess_risk_level(
        self,
        trend: MarketTrend,
        heat_index: float,
        neighborhood: Neighborhood
    ) -> str:
        """Assess investment risk level."""
        risk_factors = 0
        
        # High volatility
        if abs(trend.price_change_percent) > 15:
            risk_factors += 1
        
        # Overheated market
        if heat_index > 80:
            risk_factors += 1
        
        # High crime rate
        if neighborhood.crime_rate > 10:
            risk_factors += 1
        
        # Low confidence in data
        if trend.confidence_score < 0.5:
            risk_factors += 1
        
        if risk_factors >= 3:
            return "high"
        elif risk_factors >= 1:
            return "medium"
        else:
            return "low"
    
    def _identify_key_factors(
        self,
        neighborhood: Neighborhood,
        trend: MarketTrend,
        heat_index: float
    ) -> List[str]:
        """Identify key investment factors."""
        factors = []
        
        if trend.price_change_percent > 5:
            factors.append("Strong price appreciation")
        
        if neighborhood.growth_rate > 0.05:
            factors.append("High population growth")
        
        if neighborhood.school_rating > 8:
            factors.append("Excellent schools")
        
        if heat_index > 70:
            factors.append("Hot market with high demand")
        
        if neighborhood.walkability_score > 70:
            factors.append("High walkability")
        
        if neighborhood.median_income > 75000:
            factors.append("High-income area")
        
        return factors[:5]  # Top 5 factors
    
    def _determine_time_horizon(self, trend: MarketTrend) -> str:
        """Determine recommended investment time horizon."""
        if trend.price_change_percent > 10:
            return "short"  # Fast appreciation
        elif trend.price_change_percent > 3:
            return "medium"
        else:
            return "long"
    
    def _generate_recommendation(
        self,
        opportunity_score: float,
        predicted_roi: float,
        risk_level: str
    ) -> str:
        """Generate investment recommendation."""
        if opportunity_score > 75 and predicted_roi > 25:
            return "Strong Buy - High opportunity with excellent returns"
        elif opportunity_score > 60 and predicted_roi > 15:
            return "Buy - Good opportunity with solid returns"
        elif opportunity_score > 45 and predicted_roi > 10:
            return "Consider - Moderate opportunity, suitable for diversification"
        elif risk_level == "high":
            return "Caution - High risk, recommend thorough due diligence"
        else:
            return "Hold - Limited opportunity at current market conditions"
