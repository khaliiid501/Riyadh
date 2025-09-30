"""
Example usage of the Riyadh Predictive Real Estate Analytics System.

This script demonstrates how to use the system to:
1. Create property and market data
2. Make predictions on property values
3. Analyze market trends
4. Identify investment opportunities
5. Generate actionable insights for buyers, sellers, and investors
"""

from datetime import datetime, timedelta
from riyadh.models import Property, Transaction, MarketData, Neighborhood, PropertyType
from riyadh.predictive_engine import PredictiveEngine
from riyadh.analytics import MarketAnalyzer, InvestmentAnalyzer
from riyadh.insights import InsightGenerator


def create_sample_data():
    """Create sample data for demonstration."""
    
    # Sample properties
    properties = [
        Property(
            property_id="PROP001",
            location="Downtown",
            property_type=PropertyType.APARTMENT,
            square_footage=1200,
            bedrooms=2,
            bathrooms=2,
            year_built=2018,
            amenities=["Metro Station", "Shopping Mall", "Park", "School"],
            neighborhood="Downtown",
            latitude=24.7136,
            longitude=46.6753
        ),
        Property(
            property_id="PROP002",
            location="Suburbs",
            property_type=PropertyType.VILLA,
            square_footage=3500,
            bedrooms=4,
            bathrooms=3.5,
            year_built=2015,
            amenities=["School", "Park", "Shopping Center"],
            neighborhood="Suburbs",
            latitude=24.7500,
            longitude=46.7000
        )
    ]
    
    # Sample transactions (historical sales data)
    transactions = []
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(50):
        transaction_date = base_date + timedelta(days=i*7)
        
        # Downtown transactions
        transactions.append(Transaction(
            transaction_id=f"TXN{i:03d}",
            property_id=f"PROP{i:03d}",
            sale_price=450000 + (i * 2000),  # Appreciating market
            transaction_date=transaction_date,
            property_type=PropertyType.APARTMENT,
            square_footage=1200 + (i % 200),
            location="Downtown",
            buyer_type="individual"
        ))
        
        # Suburb transactions
        if i % 2 == 0:
            transactions.append(Transaction(
                transaction_id=f"TXN_S{i:03d}",
                property_id=f"PROP_S{i:03d}",
                sale_price=750000 + (i * 3000),
                transaction_date=transaction_date,
                property_type=PropertyType.VILLA,
                square_footage=3400 + (i % 300),
                location="Suburbs",
                buyer_type="individual"
            ))
    
    # Sample market data
    market_data = []
    for i in range(24):  # 24 months of data
        date = datetime.now() - timedelta(days=(24-i)*30)
        
        # Downtown market data
        market_data.append(MarketData(
            area="Downtown",
            date=date,
            median_price=450000 + (i * 5000),
            average_price=470000 + (i * 5200),
            total_sales=45 + (i % 10),
            inventory=120 - (i % 20),
            days_on_market=35 - (i % 10),
            price_per_sqft=375 + (i * 4),
            economic_indicators={
                "unemployment_rate": 4.5 - (i * 0.05),
                "gdp_growth": 2.5 + (i * 0.1),
                "interest_rate": 4.0 - (i * 0.02)
            },
            demographic_data={
                "population_growth": 1.5,
                "median_age": 35
            },
            seasonal_factors={
                "season_adjustment": 1.0 + (0.1 if i % 12 in [4, 5, 6] else 0)
            }
        ))
        
        # Suburbs market data
        market_data.append(MarketData(
            area="Suburbs",
            date=date,
            median_price=750000 + (i * 8000),
            average_price=780000 + (i * 8500),
            total_sales=30 + (i % 8),
            inventory=80 - (i % 15),
            days_on_market=45 - (i % 12),
            price_per_sqft=220 + (i * 2),
            economic_indicators={
                "unemployment_rate": 3.8 - (i * 0.04),
                "gdp_growth": 3.0 + (i * 0.12),
                "interest_rate": 4.0 - (i * 0.02)
            },
            demographic_data={
                "population_growth": 2.5,
                "median_age": 38
            }
        ))
    
    # Sample neighborhoods
    neighborhoods = [
        Neighborhood(
            neighborhood_id="N001",
            name="Downtown",
            population=50000,
            median_income=85000,
            employment_rate=96.0,
            crime_rate=5.2,
            school_rating=8.5,
            amenity_score=9.0,
            walkability_score=85,
            transit_score=90,
            growth_rate=0.08
        ),
        Neighborhood(
            neighborhood_id="N002",
            name="Suburbs",
            population=75000,
            median_income=95000,
            employment_rate=97.5,
            crime_rate=2.8,
            school_rating=9.2,
            amenity_score=7.5,
            walkability_score=65,
            transit_score=60,
            growth_rate=0.12
        )
    ]
    
    return properties, transactions, market_data, neighborhoods


def demonstrate_system():
    """Demonstrate the Riyadh system capabilities."""
    
    print("=" * 80)
    print("RIYADH - Predictive Real Estate Analytics System")
    print("=" * 80)
    print()
    
    # Create sample data
    print("Loading sample data...")
    properties, transactions, market_data, neighborhoods = create_sample_data()
    print(f"✓ Loaded {len(properties)} properties")
    print(f"✓ Loaded {len(transactions)} transactions")
    print(f"✓ Loaded {len(market_data)} market data points")
    print(f"✓ Loaded {len(neighborhoods)} neighborhoods")
    print()
    
    # Initialize system components
    print("Initializing analytics engine...")
    predictive_engine = PredictiveEngine()
    predictive_engine.add_historical_data(transactions)
    predictive_engine.add_market_data(market_data)
    
    market_analyzer = MarketAnalyzer()
    market_analyzer.add_market_data(market_data)
    market_analyzer.add_transactions(transactions)
    
    investment_analyzer = InvestmentAnalyzer(market_analyzer)
    investment_analyzer.add_neighborhoods(neighborhoods)
    
    insight_generator = InsightGenerator(
        predictive_engine,
        market_analyzer,
        investment_analyzer
    )
    print("✓ System initialized successfully")
    print()
    
    # Example 1: Property Value Prediction
    print("-" * 80)
    print("EXAMPLE 1: Property Value Prediction")
    print("-" * 80)
    property = properties[0]
    prediction = predictive_engine.predict_property_value(property)
    
    print(f"Property: {property.property_id}")
    print(f"Location: {property.location}")
    print(f"Type: {property.property_type.value}")
    print(f"Size: {property.square_footage} sq ft")
    print(f"Bedrooms: {property.bedrooms}")
    print()
    print(f"Predicted Value: ${prediction.predicted_value:,.2f}")
    print(f"Confidence Level: {prediction.confidence_level*100:.1f}%")
    print(f"Confidence Interval: ${prediction.confidence_interval[0]:,.2f} - ${prediction.confidence_interval[1]:,.2f}")
    print(f"Market Trend: {prediction.market_trend}")
    print()
    print("Contributing Factors:")
    for factor, value in prediction.contributing_factors.items():
        print(f"  - {factor}: {value:.4f}")
    print()
    
    # Example 2: Market Trend Analysis
    print("-" * 80)
    print("EXAMPLE 2: Market Trend Analysis")
    print("-" * 80)
    trend = market_analyzer.analyze_market_trend("Downtown", period_months=12)
    
    print(f"Area: {trend.area}")
    print(f"Trend Direction: {trend.trend_direction.upper()}")
    print(f"Price Change: {trend.price_change_percent:+.2f}%")
    print(f"Volume Change: {trend.volume_change_percent:+.2f}%")
    print(f"Inventory Change: {trend.inventory_change_percent:+.2f}%")
    print(f"Confidence Score: {trend.confidence_score*100:.1f}%")
    print()
    
    heat_index = market_analyzer.calculate_market_heat_index("Downtown")
    velocity = market_analyzer.calculate_market_velocity("Downtown")
    
    print(f"Market Heat Index: {heat_index:.1f}/100")
    print(f"Market Velocity: {velocity:.1f}/100")
    print()
    
    # Example 3: Investment Opportunities
    print("-" * 80)
    print("EXAMPLE 3: Investment Opportunity Analysis")
    print("-" * 80)
    opportunities = investment_analyzer.identify_investment_opportunities(
        max_opportunities=5,
        min_roi=10.0
    )
    
    print(f"Found {len(opportunities)} investment opportunities:")
    print()
    
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp.location}")
        print(f"   Opportunity Score: {opp.opportunity_score:.1f}/100")
        print(f"   Predicted ROI: {opp.predicted_roi:.2f}%")
        print(f"   Rental Yield: {opp.rental_yield:.2f}%")
        print(f"   Risk Level: {opp.risk_level}")
        print(f"   Recommendation: {opp.recommendation}")
        print(f"   Key Factors: {', '.join(opp.key_factors[:3])}")
        print()
    
    # Example 4: Buyer Insights
    print("-" * 80)
    print("EXAMPLE 4: Buyer Insights")
    print("-" * 80)
    buyer_budget = 500000
    buyer_insights = insight_generator.generate_buyer_insights(
        properties[0],
        buyer_budget
    )
    
    print(f"Budget: ${buyer_budget:,}")
    print(f"Property Value: ${buyer_insights['predicted_value']:,.2f}")
    print(f"Budget Fit: {buyer_insights['budget_fit']}")
    print(f"Value Assessment: {buyer_insights['value_assessment']}")
    print()
    print(f"Market Conditions:")
    print(f"  - Trend: {buyer_insights['market_conditions']['trend']}")
    print(f"  - Heat Index: {buyer_insights['market_conditions']['heat_index']:.1f}/100")
    print()
    print(f"Timing: {buyer_insights['timing']['recommendation']}")
    print()
    print("Negotiation Tips:")
    for tip in buyer_insights['negotiation_tips']:
        print(f"  • {tip}")
    print()
    print("Key Insights:")
    for insight in buyer_insights['key_insights']:
        print(f"  • {insight}")
    print()
    
    # Example 5: Seller Insights
    print("-" * 80)
    print("EXAMPLE 5: Seller Insights")
    print("-" * 80)
    seller_insights = insight_generator.generate_seller_insights(properties[1])
    
    print(f"Market Value: ${seller_insights['market_value']:,.2f}")
    print()
    print("Pricing Strategy:")
    strategy = seller_insights['pricing_strategy']
    print(f"  - Recommended List Price: ${strategy['recommended_list_price']:,.2f}")
    print(f"  - Strategy: {strategy['strategy']}")
    print(f"  - Pricing Range: ${strategy['pricing_range']['minimum']:,.0f} - ${strategy['pricing_range']['maximum']:,.0f}")
    print()
    print(f"Estimated Days on Market: {seller_insights['estimated_days_on_market']} days")
    print()
    print(f"Timing: {seller_insights['timing']['recommendation']}")
    print()
    print("Marketing Recommendations:")
    for tip in seller_insights['marketing_recommendations']:
        print(f"  • {tip}")
    print()
    
    # Example 6: Investor Insights
    print("-" * 80)
    print("EXAMPLE 6: Investor Portfolio Insights")
    print("-" * 80)
    investment_goals = {
        "min_roi": 15.0,
        "risk_tolerance": "medium",
        "time_horizon": "medium"
    }
    
    investor_insights = insight_generator.generate_investor_insights(
        budget=2000000,
        investment_goals=investment_goals
    )
    
    print(f"Investment Budget: ${investor_insights['budget']:,}")
    print(f"Risk Tolerance: {investment_goals['risk_tolerance']}")
    print(f"Minimum ROI Target: {investment_goals['min_roi']}%")
    print()
    print("Portfolio Strategy:")
    portfolio = investor_insights['portfolio_strategy']
    print(f"  {portfolio['diversification_strategy']}")
    print(f"  Expected Portfolio ROI: {portfolio['expected_portfolio_roi']:.2f}%")
    print()
    print("Recommended Allocations:")
    for allocation in portfolio['recommended_allocation']:
        print(f"  • {allocation['location']}: ${allocation['estimated_investment']:,.0f} "
              f"({allocation['allocation_percent']:.0f}%) - ROI: {allocation['expected_roi']:.1f}%")
    print()
    
    if investor_insights['emerging_markets']:
        print("Emerging Markets to Watch:")
        for market in investor_insights['emerging_markets']:
            print(f"  • {market}")
        print()
    
    # Example 7: Comprehensive Report
    print("-" * 80)
    print("EXAMPLE 7: Comprehensive Property Report")
    print("-" * 80)
    report = insight_generator.generate_comprehensive_report(properties[0])
    
    print("Property Details:")
    prop_info = report['property']
    print(f"  ID: {prop_info['id']}")
    print(f"  Location: {prop_info['location']}")
    print(f"  Type: {prop_info['type']}")
    print(f"  Size: {prop_info['square_footage']} sq ft")
    print(f"  Bedrooms: {prop_info['bedrooms']} | Bathrooms: {prop_info['bathrooms']}")
    print(f"  Age: {prop_info['age']} years")
    print()
    
    print("Valuation:")
    valuation = report['valuation']
    print(f"  Predicted Value: ${valuation['predicted_value']:,.2f}")
    print(f"  Confidence: {valuation['confidence_level']*100:.1f}%")
    print(f"  Market Trend: {valuation['market_trend']}")
    print()
    
    print("Market Analysis:")
    market = report['market_analysis']
    print(f"  Trend: {market['trend_direction']}")
    print(f"  Price Change: {market['price_change_percent']:+.2f}%")
    print(f"  Heat Index: {market['heat_index']:.1f}/100")
    print()
    
    print("Investment Metrics:")
    metrics = report['investment_metrics']
    print(f"  Rental Yield: {metrics['rental_yield']:.2f}%")
    roi = metrics['roi_projections']
    print(f"  5-Year ROI: {roi['total_roi_percent']:.2f}%")
    print(f"  Annual ROI: {roi['annual_roi_percent']:.2f}%")
    print()
    
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    print()
    
    # Market Forecast
    print("-" * 80)
    print("EXAMPLE 8: Market Forecast")
    print("-" * 80)
    forecast = predictive_engine.forecast_market_trend("Downtown", months_ahead=12)
    
    print("12-Month Price Forecast for Downtown:")
    print()
    for i, (date, price) in enumerate(sorted(forecast.items())[:6]):
        print(f"  {date.strftime('%B %Y')}: ${price:,.0f}")
    print("  ...")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_system()
