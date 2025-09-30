"""
Predictive engine for forecasting property values and market trends.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .models import Property, Transaction, MarketData


@dataclass
class PredictionResult:
    """
    Results from a property value prediction.
    
    Attributes:
        predicted_value: Predicted property value
        confidence_interval: Tuple of (lower_bound, upper_bound)
        confidence_level: Confidence level (0-1)
        contributing_factors: Dictionary of factors and their impact
        market_trend: Predicted market trend (up, down, stable)
        prediction_date: Date of prediction
    """
    predicted_value: float
    confidence_interval: Tuple[float, float]
    confidence_level: float
    contributing_factors: Dict[str, float]
    market_trend: str
    prediction_date: datetime


class PredictiveEngine:
    """
    Advanced predictive engine for real estate analytics.
    
    This engine uses multiple algorithms to forecast property values:
    - Historical trend analysis
    - Seasonal adjustment
    - Neighborhood comparison
    - Economic indicator integration
    - Feature-based valuation
    """
    
    def __init__(self):
        """Initialize the predictive engine."""
        self.historical_data: List[Transaction] = []
        self.market_data: List[MarketData] = []
        self.seasonal_weights = self._initialize_seasonal_weights()
        
    def _initialize_seasonal_weights(self) -> Dict[int, float]:
        """
        Initialize seasonal adjustment weights by month.
        
        Returns:
            Dictionary mapping month (1-12) to weight factor
        """
        # Spring and early summer are typically strong markets
        return {
            1: 0.92,   # January - slower
            2: 0.94,   # February - slower
            3: 1.02,   # March - picking up
            4: 1.08,   # April - strong
            5: 1.12,   # May - peak
            6: 1.10,   # June - strong
            7: 1.05,   # July - moderate
            8: 1.03,   # August - moderate
            9: 1.06,   # September - picking up
            10: 1.04,  # October - moderate
            11: 0.98,  # November - slowing
            12: 0.96,  # December - slower
        }
    
    def add_historical_data(self, transactions: List[Transaction]):
        """Add historical transaction data for training."""
        self.historical_data.extend(transactions)
        self.historical_data.sort(key=lambda x: x.transaction_date)
    
    def add_market_data(self, market_data: List[MarketData]):
        """Add market data for analysis."""
        self.market_data.extend(market_data)
        self.market_data.sort(key=lambda x: x.date)
    
    def predict_property_value(
        self,
        property: Property,
        prediction_date: Optional[datetime] = None
    ) -> PredictionResult:
        """
        Predict the value of a property.
        
        Args:
            property: Property to evaluate
            prediction_date: Date for prediction (default: now)
            
        Returns:
            PredictionResult with predicted value and details
        """
        if prediction_date is None:
            prediction_date = datetime.now()
        
        # Get comparable properties
        comparables = self._find_comparable_properties(property)
        
        # Calculate base value from comparables
        base_value = self._calculate_base_value(property, comparables)
        
        # Apply location adjustment
        location_factor = self._calculate_location_factor(property.location)
        
        # Apply property-specific adjustments
        property_factor = self._calculate_property_factor(property)
        
        # Apply seasonal adjustment
        seasonal_factor = self.seasonal_weights.get(prediction_date.month, 1.0)
        
        # Apply market trend adjustment
        trend_factor = self._calculate_trend_factor(property.location, prediction_date)
        
        # Calculate final predicted value
        predicted_value = (
            base_value * 
            location_factor * 
            property_factor * 
            seasonal_factor * 
            trend_factor
        )
        
        # Calculate confidence interval
        confidence_level = self._calculate_confidence(len(comparables))
        margin = predicted_value * (1 - confidence_level) * 0.5
        confidence_interval = (predicted_value - margin, predicted_value + margin)
        
        # Determine market trend
        market_trend = self._determine_market_trend(trend_factor)
        
        # Contributing factors
        contributing_factors = {
            "base_value": base_value,
            "location_adjustment": location_factor,
            "property_features": property_factor,
            "seasonal_adjustment": seasonal_factor,
            "market_trend": trend_factor,
        }
        
        return PredictionResult(
            predicted_value=predicted_value,
            confidence_interval=confidence_interval,
            confidence_level=confidence_level,
            contributing_factors=contributing_factors,
            market_trend=market_trend,
            prediction_date=prediction_date
        )
    
    def forecast_market_trend(
        self,
        location: str,
        months_ahead: int = 12
    ) -> Dict[datetime, float]:
        """
        Forecast market trends for a location.
        
        Args:
            location: Location to forecast
            months_ahead: Number of months to forecast
            
        Returns:
            Dictionary mapping dates to predicted median prices
        """
        forecast = {}
        current_date = datetime.now()
        
        # Get historical market data for location
        location_data = [
            md for md in self.market_data 
            if md.area.lower() == location.lower()
        ]
        
        if not location_data:
            return forecast
        
        # Calculate trend from historical data
        prices = [md.median_price for md in location_data[-12:]]
        if len(prices) < 2:
            return forecast
        
        # Simple linear trend with seasonal adjustment
        trend = (prices[-1] - prices[0]) / len(prices)
        
        current_price = prices[-1]
        for i in range(months_ahead):
            future_date = current_date + timedelta(days=30 * i)
            seasonal_factor = self.seasonal_weights.get(future_date.month, 1.0)
            predicted_price = current_price + (trend * i) * seasonal_factor
            forecast[future_date] = max(predicted_price, 0)
        
        return forecast
    
    def _find_comparable_properties(
        self,
        property: Property,
        max_comparables: int = 10
    ) -> List[Transaction]:
        """Find comparable recent transactions."""
        comparables = []
        
        # Filter by property type and similar size
        for transaction in self.historical_data:
            if transaction.property_type != property.property_type:
                continue
            
            # Size should be within 30%
            size_diff = abs(transaction.square_footage - property.square_footage)
            if size_diff / property.square_footage > 0.3:
                continue
            
            # Location match (simplified - could use geographic distance)
            if transaction.location.lower() != property.location.lower():
                continue
            
            comparables.append(transaction)
        
        # Return most recent comparables
        comparables.sort(key=lambda x: x.transaction_date, reverse=True)
        return comparables[:max_comparables]
    
    def _calculate_base_value(
        self,
        property: Property,
        comparables: List[Transaction]
    ) -> float:
        """Calculate base property value from comparables."""
        if not comparables:
            # Fallback: use market average if available
            if self.market_data:
                avg_price_per_sqft = np.mean([
                    md.price_per_sqft for md in self.market_data[-6:]
                ])
                return property.square_footage * avg_price_per_sqft
            return property.square_footage * 150  # Default fallback
        
        # Weight comparables by recency and similarity
        weighted_prices = []
        weights = []
        
        for comp in comparables:
            # Recency weight (more recent = higher weight)
            days_ago = (datetime.now() - comp.transaction_date).days
            recency_weight = 1.0 / (1.0 + days_ago / 365)
            
            # Size similarity weight
            size_diff = abs(comp.square_footage - property.square_footage)
            size_weight = 1.0 - (size_diff / property.square_footage)
            
            total_weight = recency_weight * size_weight
            price_per_sqft = comp.price_per_sqft()
            
            weighted_prices.append(price_per_sqft * total_weight)
            weights.append(total_weight)
        
        # Calculate weighted average price per sqft
        avg_price_per_sqft = sum(weighted_prices) / sum(weights)
        return property.square_footage * avg_price_per_sqft
    
    def _calculate_location_factor(self, location: str) -> float:
        """Calculate location-based adjustment factor."""
        # Get recent market data for location
        location_data = [
            md for md in self.market_data
            if md.area.lower() == location.lower()
        ]
        
        if not location_data:
            return 1.0
        
        # Compare to overall market
        recent_location = location_data[-1] if location_data else None
        if not recent_location:
            return 1.0
        
        overall_avg = np.mean([md.average_price for md in self.market_data[-6:]])
        location_avg = recent_location.average_price
        
        return location_avg / overall_avg if overall_avg > 0 else 1.0
    
    def _calculate_property_factor(self, property: Property) -> float:
        """Calculate property-specific adjustment factor."""
        factor = 1.0
        
        # Age adjustment
        age = property.calculate_age()
        if age is not None:
            if age < 5:
                factor *= 1.10  # New construction premium
            elif age > 30:
                factor *= 0.90  # Older property discount
        
        # Amenities adjustment (0.5% per amenity, up to 10%)
        amenity_bonus = min(len(property.amenities) * 0.005, 0.10)
        factor *= (1.0 + amenity_bonus)
        
        return factor
    
    def _calculate_trend_factor(self, location: str, date: datetime) -> float:
        """Calculate market trend adjustment factor."""
        # Get historical trend
        location_data = [
            md for md in self.market_data
            if md.area.lower() == location.lower()
        ]
        
        if len(location_data) < 2:
            return 1.0
        
        # Calculate year-over-year change
        recent = location_data[-1]
        year_ago = location_data[-12] if len(location_data) >= 12 else location_data[0]
        
        yoy_change = (recent.median_price - year_ago.median_price) / year_ago.median_price
        
        # Project trend forward
        months_forward = (date.year - datetime.now().year) * 12
        months_forward += (date.month - datetime.now().month)
        
        # Apply trend with dampening (trends don't continue forever)
        trend_factor = 1.0 + (yoy_change * months_forward / 12) * 0.7
        
        return trend_factor
    
    def _calculate_confidence(self, num_comparables: int) -> float:
        """Calculate confidence level based on available data."""
        # More comparables = higher confidence
        base_confidence = min(num_comparables / 10, 0.85)
        
        # Factor in amount of market data
        data_confidence = min(len(self.market_data) / 24, 0.95)
        
        return (base_confidence + data_confidence) / 2
    
    def _determine_market_trend(self, trend_factor: float) -> str:
        """Determine market trend direction."""
        if trend_factor > 1.03:
            return "up"
        elif trend_factor < 0.97:
            return "down"
        else:
            return "stable"
