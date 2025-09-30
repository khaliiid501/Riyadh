"""
Data models for real estate properties, transactions, and market data.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class PropertyType(Enum):
    """Types of properties."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    LAND = "land"
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"


@dataclass
class Property:
    """
    Represents a real estate property with all relevant attributes.
    
    Attributes:
        property_id: Unique identifier for the property
        location: Geographic location (coordinates or address)
        property_type: Type of property (residential, commercial, etc.)
        square_footage: Total area in square feet
        bedrooms: Number of bedrooms (if applicable)
        bathrooms: Number of bathrooms (if applicable)
        year_built: Year the property was constructed
        amenities: List of nearby amenities
        neighborhood: Neighborhood name or identifier
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        features: Additional property features
    """
    property_id: str
    location: str
    property_type: PropertyType
    square_footage: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    year_built: Optional[int] = None
    amenities: List[str] = field(default_factory=list)
    neighborhood: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    features: Dict[str, any] = field(default_factory=dict)
    
    def calculate_age(self) -> Optional[int]:
        """Calculate the age of the property."""
        if self.year_built:
            return datetime.now().year - self.year_built
        return None
    
    def has_amenity(self, amenity: str) -> bool:
        """Check if property has a specific amenity nearby."""
        return amenity.lower() in [a.lower() for a in self.amenities]


@dataclass
class Transaction:
    """
    Represents a real estate transaction.
    
    Attributes:
        transaction_id: Unique identifier for the transaction
        property_id: Associated property identifier
        sale_price: Sale price of the property
        transaction_date: Date of the transaction
        property_type: Type of property
        square_footage: Property area
        location: Property location
        buyer_type: Type of buyer (individual, investor, corporation)
        financing_type: Type of financing used
    """
    transaction_id: str
    property_id: str
    sale_price: float
    transaction_date: datetime
    property_type: PropertyType
    square_footage: float
    location: str
    buyer_type: str = "individual"
    financing_type: str = "conventional"
    
    def price_per_sqft(self) -> float:
        """Calculate price per square foot."""
        if self.square_footage > 0:
            return self.sale_price / self.square_footage
        return 0.0


@dataclass
class MarketData:
    """
    Represents market data for a specific area and time period.
    
    Attributes:
        area: Geographic area identifier
        date: Date of the market data
        median_price: Median property price in the area
        average_price: Average property price in the area
        total_sales: Total number of sales
        inventory: Number of properties available
        days_on_market: Average days properties stay on market
        price_per_sqft: Average price per square foot
        economic_indicators: Economic indicators for the area
        demographic_data: Demographic information
        seasonal_factors: Seasonal adjustment factors
    """
    area: str
    date: datetime
    median_price: float
    average_price: float
    total_sales: int
    inventory: int
    days_on_market: float
    price_per_sqft: float
    economic_indicators: Dict[str, float] = field(default_factory=dict)
    demographic_data: Dict[str, any] = field(default_factory=dict)
    seasonal_factors: Dict[str, float] = field(default_factory=dict)
    
    def calculate_absorption_rate(self) -> float:
        """
        Calculate the market absorption rate.
        
        Returns:
            Monthly absorption rate (sales/inventory)
        """
        if self.inventory > 0:
            return self.total_sales / self.inventory
        return 0.0
    
    def is_sellers_market(self, threshold: float = 0.2) -> bool:
        """
        Determine if it's a seller's market based on absorption rate.
        
        Args:
            threshold: Absorption rate threshold for seller's market
            
        Returns:
            True if seller's market, False otherwise
        """
        return self.calculate_absorption_rate() > threshold


@dataclass
class Neighborhood:
    """
    Represents neighborhood demographics and characteristics.
    
    Attributes:
        neighborhood_id: Unique identifier
        name: Neighborhood name
        population: Total population
        median_income: Median household income
        employment_rate: Employment rate percentage
        crime_rate: Crime rate per 1000 residents
        school_rating: Average school rating (1-10)
        amenity_score: Score based on nearby amenities
        walkability_score: Walkability score (1-100)
        transit_score: Public transit score (1-100)
        growth_rate: Population/economic growth rate
    """
    neighborhood_id: str
    name: str
    population: int
    median_income: float
    employment_rate: float
    crime_rate: float
    school_rating: float
    amenity_score: float
    walkability_score: float
    transit_score: float
    growth_rate: float
    
    def calculate_desirability_score(self) -> float:
        """
        Calculate overall neighborhood desirability score.
        
        Returns:
            Desirability score (0-100)
        """
        # Weighted scoring of various factors
        income_score = min(self.median_income / 1000, 50)  # Cap at 50
        safety_score = max(0, 20 - self.crime_rate)  # Lower crime = higher score
        education_score = self.school_rating * 2  # Scale to 20
        location_score = (self.walkability_score + self.transit_score) / 10
        
        total_score = (
            income_score * 0.25 +
            safety_score * 0.25 +
            education_score * 0.20 +
            location_score * 0.15 +
            self.amenity_score * 0.15
        )
        
        return min(total_score, 100)
