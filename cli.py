#!/usr/bin/env python3
"""
Command-line interface for Riyadh Real Estate Analytics System.

Usage:
    python cli.py predict --location "Downtown" --type apartment --size 1200
    python cli.py market-trend --location "Downtown" --period 12
    python cli.py opportunities --budget 2000000 --min-roi 15
"""

import argparse
import sys
from datetime import datetime
from riyadh.models import Property, PropertyType
from riyadh.predictive_engine import PredictiveEngine
from riyadh.analytics import MarketAnalyzer, InvestmentAnalyzer
from riyadh.insights import InsightGenerator


def setup_system():
    """Initialize the Riyadh system with basic setup."""
    print("Initializing Riyadh Real Estate Analytics System...")
    
    predictive_engine = PredictiveEngine()
    market_analyzer = MarketAnalyzer()
    investment_analyzer = InvestmentAnalyzer(market_analyzer)
    insight_generator = InsightGenerator(
        predictive_engine,
        market_analyzer,
        investment_analyzer
    )
    
    print("✓ System ready\n")
    return predictive_engine, market_analyzer, investment_analyzer, insight_generator


def predict_value(args, predictive_engine, insight_generator):
    """Predict property value."""
    print("=" * 80)
    print("PROPERTY VALUE PREDICTION")
    print("=" * 80)
    
    # Parse property type
    property_type_map = {
        'apartment': PropertyType.APARTMENT,
        'villa': PropertyType.VILLA,
        'townhouse': PropertyType.TOWNHOUSE,
        'residential': PropertyType.RESIDENTIAL,
        'commercial': PropertyType.COMMERCIAL
    }
    
    prop_type = property_type_map.get(args.type.lower(), PropertyType.RESIDENTIAL)
    
    # Create property
    property = Property(
        property_id=f"CLI_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        location=args.location,
        property_type=prop_type,
        square_footage=args.size,
        bedrooms=args.bedrooms,
        bathrooms=args.bathrooms,
        year_built=args.year_built,
        amenities=args.amenities.split(',') if args.amenities else []
    )
    
    # Get prediction
    prediction = predictive_engine.predict_property_value(property)
    
    print(f"\nProperty Details:")
    print(f"  Location: {property.location}")
    print(f"  Type: {property.property_type.value}")
    print(f"  Size: {property.square_footage} sq ft")
    print(f"  Bedrooms: {property.bedrooms}")
    print(f"  Bathrooms: {property.bathrooms}")
    
    print(f"\nPrediction Results:")
    print(f"  Predicted Value: ${prediction.predicted_value:,.2f}")
    print(f"  Confidence Level: {prediction.confidence_level*100:.1f}%")
    print(f"  Confidence Interval: ${prediction.confidence_interval[0]:,.2f} - ${prediction.confidence_interval[1]:,.2f}")
    print(f"  Market Trend: {prediction.market_trend.upper()}")
    
    # If budget provided, get buyer insights
    if args.budget:
        print(f"\n" + "-" * 80)
        print("BUYER INSIGHTS")
        print("-" * 80)
        
        insights = insight_generator.generate_buyer_insights(property, args.budget)
        
        print(f"\nBudget Analysis:")
        print(f"  Your Budget: ${args.budget:,}")
        print(f"  Property Value: ${insights['predicted_value']:,.2f}")
        print(f"  Budget Fit: {insights['budget_fit']}")
        print(f"  Value Assessment: {insights['value_assessment']}")
        
        print(f"\nMarket Timing:")
        print(f"  {insights['timing']['recommendation']}")
        
        print(f"\nNegotiation Tips:")
        for tip in insights['negotiation_tips']:
            print(f"  • {tip}")


def analyze_market(args, market_analyzer):
    """Analyze market trends."""
    print("=" * 80)
    print("MARKET TREND ANALYSIS")
    print("=" * 80)
    
    trend = market_analyzer.analyze_market_trend(
        args.location,
        period_months=args.period
    )
    
    print(f"\nArea: {trend.area}")
    print(f"Analysis Period: {args.period} months")
    print(f"\nTrend Analysis:")
    print(f"  Direction: {trend.trend_direction.upper()}")
    print(f"  Price Change: {trend.price_change_percent:+.2f}%")
    print(f"  Volume Change: {trend.volume_change_percent:+.2f}%")
    print(f"  Inventory Change: {trend.inventory_change_percent:+.2f}%")
    print(f"  Confidence Score: {trend.confidence_score*100:.1f}%")
    
    # Additional metrics
    heat_index = market_analyzer.calculate_market_heat_index(args.location)
    velocity = market_analyzer.calculate_market_velocity(args.location)
    
    print(f"\nMarket Metrics:")
    print(f"  Heat Index: {heat_index:.1f}/100")
    print(f"  Velocity: {velocity:.1f}/100")
    
    # Market assessment
    print(f"\nMarket Assessment:")
    if heat_index > 70:
        print("  • HOT MARKET - High demand, competitive")
    elif heat_index > 50:
        print("  • WARM MARKET - Moderate activity")
    else:
        print("  • COOL MARKET - Buyer advantage")
    
    if velocity > 70:
        print("  • Properties selling quickly")
    elif velocity < 40:
        print("  • Properties taking longer to sell")


def find_opportunities(args, investment_analyzer):
    """Find investment opportunities."""
    print("=" * 80)
    print("INVESTMENT OPPORTUNITIES")
    print("=" * 80)
    
    opportunities = investment_analyzer.identify_investment_opportunities(
        max_opportunities=args.max_results,
        min_roi=args.min_roi
    )
    
    print(f"\nInvestment Criteria:")
    print(f"  Budget: ${args.budget:,}")
    print(f"  Minimum ROI: {args.min_roi}%")
    print(f"\nFound {len(opportunities)} opportunities:\n")
    
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp.location}")
        print(f"   Opportunity Score: {opp.opportunity_score:.1f}/100")
        print(f"   Predicted ROI: {opp.predicted_roi:.2f}%")
        print(f"   Rental Yield: {opp.rental_yield:.2f}%")
        print(f"   Risk Level: {opp.risk_level.upper()}")
        print(f"   Time Horizon: {opp.time_horizon}")
        print(f"   Recommendation: {opp.recommendation}")
        
        if opp.key_factors:
            print(f"   Key Factors:")
            for factor in opp.key_factors[:3]:
                print(f"     • {factor}")
        print()


def seller_analysis(args, insight_generator):
    """Analyze property for selling."""
    print("=" * 80)
    print("SELLER ANALYSIS")
    print("=" * 80)
    
    # Parse property type
    property_type_map = {
        'apartment': PropertyType.APARTMENT,
        'villa': PropertyType.VILLA,
        'townhouse': PropertyType.TOWNHOUSE,
        'residential': PropertyType.RESIDENTIAL,
        'commercial': PropertyType.COMMERCIAL
    }
    
    prop_type = property_type_map.get(args.type.lower(), PropertyType.RESIDENTIAL)
    
    # Create property
    property = Property(
        property_id=f"SELL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        location=args.location,
        property_type=prop_type,
        square_footage=args.size,
        bedrooms=args.bedrooms,
        bathrooms=args.bathrooms,
        year_built=args.year_built,
        amenities=args.amenities.split(',') if args.amenities else []
    )
    
    # Get seller insights
    insights = insight_generator.generate_seller_insights(
        property,
        desired_price=args.desired_price
    )
    
    print(f"\nProperty Details:")
    print(f"  Location: {property.location}")
    print(f"  Type: {property.property_type.value}")
    print(f"  Size: {property.square_footage} sq ft")
    
    print(f"\nValuation:")
    print(f"  Market Value: ${insights['market_value']:,.2f}")
    
    if args.desired_price:
        diff = args.desired_price - insights['market_value']
        pct = (diff / insights['market_value']) * 100
        print(f"  Your Target: ${args.desired_price:,}")
        print(f"  Difference: ${diff:+,.0f} ({pct:+.1f}%)")
    
    print(f"\nPricing Strategy:")
    strategy = insights['pricing_strategy']
    print(f"  Recommended List Price: ${strategy['recommended_list_price']:,.2f}")
    print(f"  Strategy: {strategy['strategy']}")
    print(f"  Price Range: ${strategy['pricing_range']['minimum']:,.0f} - ${strategy['pricing_range']['maximum']:,.0f}")
    
    print(f"\nMarket Timing:")
    print(f"  {insights['timing']['recommendation']}")
    
    print(f"\nExpectations:")
    print(f"  Estimated Days on Market: {insights['estimated_days_on_market']} days")
    
    print(f"\nMarketing Tips:")
    for tip in insights['marketing_recommendations']:
        print(f"  • {tip}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Riyadh Real Estate Analytics - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict property value')
    predict_parser.add_argument('--location', required=True, help='Property location')
    predict_parser.add_argument('--type', required=True, 
                              choices=['apartment', 'villa', 'townhouse', 'residential', 'commercial'],
                              help='Property type')
    predict_parser.add_argument('--size', type=float, required=True, help='Square footage')
    predict_parser.add_argument('--bedrooms', type=int, default=2, help='Number of bedrooms')
    predict_parser.add_argument('--bathrooms', type=float, default=2, help='Number of bathrooms')
    predict_parser.add_argument('--year-built', type=int, default=2018, help='Year built')
    predict_parser.add_argument('--amenities', default='', help='Comma-separated amenities')
    predict_parser.add_argument('--budget', type=float, help='Your budget (optional, for buyer insights)')
    
    # Market trend command
    market_parser = subparsers.add_parser('market', help='Analyze market trends')
    market_parser.add_argument('--location', required=True, help='Area to analyze')
    market_parser.add_argument('--period', type=int, default=12, help='Analysis period in months')
    
    # Opportunities command
    opp_parser = subparsers.add_parser('opportunities', help='Find investment opportunities')
    opp_parser.add_argument('--budget', type=float, required=True, help='Investment budget')
    opp_parser.add_argument('--min-roi', type=float, default=15.0, help='Minimum ROI (%)')
    opp_parser.add_argument('--max-results', type=int, default=5, help='Maximum results')
    
    # Seller command
    seller_parser = subparsers.add_parser('sell', help='Analyze property for selling')
    seller_parser.add_argument('--location', required=True, help='Property location')
    seller_parser.add_argument('--type', required=True,
                              choices=['apartment', 'villa', 'townhouse', 'residential', 'commercial'],
                              help='Property type')
    seller_parser.add_argument('--size', type=float, required=True, help='Square footage')
    seller_parser.add_argument('--bedrooms', type=int, default=2, help='Number of bedrooms')
    seller_parser.add_argument('--bathrooms', type=float, default=2, help='Number of bathrooms')
    seller_parser.add_argument('--year-built', type=int, default=2018, help='Year built')
    seller_parser.add_argument('--amenities', default='', help='Comma-separated amenities')
    seller_parser.add_argument('--desired-price', type=float, help='Your desired price')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize system
    predictive_engine, market_analyzer, investment_analyzer, insight_generator = setup_system()
    
    # Route to appropriate handler
    if args.command == 'predict':
        predict_value(args, predictive_engine, insight_generator)
    elif args.command == 'market':
        analyze_market(args, market_analyzer)
    elif args.command == 'opportunities':
        find_opportunities(args, investment_analyzer)
    elif args.command == 'sell':
        seller_analysis(args, insight_generator)
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
