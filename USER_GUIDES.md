# User Guides - Riyadh Real Estate Analytics

## Table of Contents
- [Buyer's Guide](#buyers-guide)
- [Seller's Guide](#sellers-guide)
- [Investor's Guide](#investors-guide)
- [Agent's Guide](#agents-guide)

---

## Buyer's Guide

### Getting Started

As a property buyer, the Riyadh system helps you:
- Determine fair market value of properties
- Assess if asking prices are reasonable
- Identify the best time to buy
- Get negotiation strategies
- Understand future value potential

### Step-by-Step Workflow

#### 1. Property Evaluation

```python
from riyadh import Property, PropertyType, InsightGenerator

# Create property object for the property you're interested in
property = Property(
    property_id="INTERESTED_PROP",
    location="Downtown",
    property_type=PropertyType.APARTMENT,
    square_footage=1200,
    bedrooms=2,
    bathrooms=2,
    year_built=2018,
    amenities=["Metro", "School", "Park"]
)

# Get buyer insights
insights = insight_generator.generate_buyer_insights(
    property=property,
    budget=500000  # Your budget
)
```

#### 2. Understanding Your Results

**Value Assessment:**
- "Excellent value" = Property priced 15%+ below market
- "Good value" = Property priced 5-15% below market  
- "Fair value" = Property priced at market (±5%)
- "Overpriced" = Property priced 5-15% above market
- "Significantly overpriced" = Property priced 15%+ above market

**Budget Fit:**
- "Well within budget" = Property is ≤85% of your budget
- "Within budget" = Property is 85-100% of your budget
- "Slightly over budget" = Property is 100-110% of your budget
- "Over budget" = Property is >110% of your budget

**Market Timing:**
- Score 70+: Excellent time to buy
- Score 55-69: Good time to buy
- Score 45-54: Neutral market
- Score 30-44: Challenging for buyers
- Score <30: Consider waiting

#### 3. Making an Offer

Use the insights to guide your offer:

```python
# Check if you should negotiate
market_heat = insights['market_conditions']['heat_index']

if market_heat < 50:
    print("Low competition - you have negotiating power")
    suggested_offer = insights['predicted_value'] * 0.95  # 5% below value
elif market_heat > 70:
    print("High competition - consider full price offer")
    suggested_offer = insights['predicted_value']
else:
    suggested_offer = insights['predicted_value'] * 0.98  # 2% below value

print(f"Suggested offer: ${suggested_offer:,.0f}")
```

#### 4. Long-Term Planning

Review future projections:

```python
projections = insights['future_projections']

print(f"Current value: ${insights['predicted_value']:,.0f}")
print(f"1-year projection: ${projections['1_year']:,.0f}")
print(f"3-year projection: ${projections['3_year']:,.0f}")
print(f"5-year projection: ${projections['5_year']:,.0f}")

# Calculate expected gain
purchase_price = 480000  # Your negotiated price
five_year_gain = projections['5_year'] - purchase_price
roi = (five_year_gain / purchase_price) * 100

print(f"Expected 5-year appreciation: ${five_year_gain:,.0f} ({roi:.1f}%)")
```

### Common Buyer Scenarios

#### Scenario 1: First-Time Buyer

**Challenge:** Limited budget, need to maximize value

**Strategy:**
1. Set strict budget limit (don't exceed 100% of approved mortgage)
2. Focus on "Good value" or "Excellent value" properties
3. Consider emerging neighborhoods with growth potential
4. Be patient - wait for right opportunity

```python
# Find properties in budget with good value
max_budget = 400000

for prop in available_properties:
    insights = insight_generator.generate_buyer_insights(prop, max_budget)
    
    if (insights['budget_fit'] in ['Within budget', 'Well within budget'] and
        insights['value_assessment'] in ['Good value', 'Excellent value']):
        
        print(f"Good opportunity: {prop.property_id}")
        print(f"  Value: ${insights['predicted_value']:,.0f}")
        print(f"  Assessment: {insights['value_assessment']}")
```

#### Scenario 2: Upgrading Home

**Challenge:** Timing sale of current home with purchase of new home

**Strategy:**
1. Analyze both properties (current and target)
2. Compare market conditions for both neighborhoods
3. Time transactions to avoid double payments or gap

```python
# Analyze your current home
current_home_insights = insight_generator.generate_seller_insights(current_home)

# Analyze target home
target_home_insights = insight_generator.generate_buyer_insights(
    target_home, 
    budget=current_home_insights['market_value']
)

# Compare timing
print("Current home timing:", current_home_insights['timing']['recommendation'])
print("Target home timing:", target_home_insights['timing']['recommendation'])
```

#### Scenario 3: Investment Property

**Challenge:** Need rental income and appreciation

**Strategy:**
1. Calculate total return (rental + appreciation)
2. Assess cash flow requirements
3. Consider tenant demographics in area

```python
report = insight_generator.generate_comprehensive_report(property)

rental_yield = report['investment_metrics']['rental_yield']
roi_projections = report['investment_metrics']['roi_projections']

print(f"Rental yield: {rental_yield:.2f}%")
print(f"5-year total ROI: {roi_projections['total_roi_percent']:.2f}%")
print(f"Annual ROI: {roi_projections['annual_roi_percent']:.2f}%")

# Check if meets investment criteria
if roi_projections['annual_roi_percent'] >= 15:
    print("✓ Meets investment criteria")
```

---

## Seller's Guide

### Getting Started

As a property seller, the Riyadh system helps you:
- Determine optimal listing price
- Identify best time to sell
- Estimate how long property will take to sell
- Develop marketing strategies
- Understand market conditions

### Step-by-Step Workflow

#### 1. Property Valuation

```python
# Create your property
my_property = Property(
    property_id="MY_HOME",
    location="Suburbs",
    property_type=PropertyType.VILLA,
    square_footage=3500,
    bedrooms=4,
    bathrooms=3.5,
    year_built=2015,
    amenities=["School", "Park", "Shopping"]
)

# Get seller insights
insights = insight_generator.generate_seller_insights(
    property=my_property,
    desired_price=1200000  # Optional: your target price
)
```

#### 2. Setting Your Price

```python
pricing = insights['pricing_strategy']

print(f"Market value: ${insights['market_value']:,.0f}")
print(f"Recommended list price: ${pricing['recommended_list_price']:,.0f}")
print(f"Strategy: {pricing['strategy']}")
print()
print(f"Pricing range:")
print(f"  Minimum: ${pricing['pricing_range']['minimum']:,.0f}")
print(f"  Optimal: ${pricing['pricing_range']['optimal']:,.0f}")
print(f"  Maximum: ${pricing['pricing_range']['maximum']:,.0f}")
```

**Pricing Strategies Explained:**

- **"Price at premium"**: Hot market (heat index >70), you can ask 5% over value
- **"Price at market value"**: Balanced market, list at predicted value
- **"Price competitively"**: Cool market (heat index <40), list 5% below value to attract buyers

#### 3. Timing Your Sale

```python
timing = insights['timing']

print(f"Timing score: {timing['score']}/100")
print(f"Recommendation: {timing['recommendation']}")
print()
print("Reasons:")
for reason in timing['reasons']:
    print(f"  • {reason}")
```

**When to Sell:**

Best times (Spring/Early Summer):
- March-June: Peak buyer activity
- Higher prices (8-12% seasonal premium)
- Faster sales

Good times (Fall):
- September-October: Secondary peak
- Moderate activity

Challenging times (Winter):
- November-February: Slower market
- Lower prices (4-8% seasonal discount)
- Longer time on market

Exception: If market trend is strongly up and heat index >70, sell immediately regardless of season

#### 4. Preparing to Sell

```python
marketing_tips = insights['marketing_recommendations']

print("Marketing recommendations:")
for tip in marketing_tips:
    print(f"  • {tip}")

estimated_days = insights['estimated_days_on_market']
print(f"\nEstimated time to sell: {estimated_days} days")
```

### Common Seller Scenarios

#### Scenario 1: Quick Sale Needed

**Challenge:** Need to sell within 30-60 days

**Strategy:**
1. Price aggressively (5-10% below market value)
2. Make property show-ready immediately
3. Consider all reasonable offers
4. Be flexible on closing date

```python
# Price for quick sale
quick_sale_price = insights['market_value'] * 0.92  # 8% below market

print(f"Quick sale strategy price: ${quick_sale_price:,.0f}")
print(f"Expected time: {estimated_days * 0.6:.0f} days")  # 40% faster
```

#### Scenario 2: Maximize Profit

**Challenge:** Want highest possible price, not time-sensitive

**Strategy:**
1. Wait for optimal season (spring/summer)
2. Price at or slightly above market
3. Invest in staging and improvements
4. Be patient for right buyer

```python
# Check if current timing is optimal
if timing['score'] >= 70:
    max_price = insights['market_value'] * 1.05
    print(f"List at premium: ${max_price:,.0f}")
else:
    print(f"Consider waiting {months_to_spring} months for spring market")
    print(f"Expected additional gain: ${insights['market_value'] * 0.08:,.0f}")
```

#### Scenario 3: Inherited Property

**Challenge:** Unfamiliar with property value and market

**Strategy:**
1. Get comprehensive analysis
2. Understand neighborhood trends
3. Consider current market conditions
4. Get professional inspection

```python
# Get full analysis
report = insight_generator.generate_comprehensive_report(inherited_property)

print("Property assessment:")
print(f"  Current value: ${report['valuation']['predicted_value']:,.0f}")
print(f"  Market trend: {report['market_analysis']['trend_direction']}")
print(f"  Area heat: {report['market_analysis']['heat_index']:.0f}/100")

# Decision support
if report['market_analysis']['trend_direction'] == 'up':
    print("\n→ Recommendation: Hold if possible, market appreciating")
else:
    print("\n→ Recommendation: Consider selling now")
```

---

## Investor's Guide

### Getting Started

As a real estate investor, the Riyadh system helps you:
- Identify high-potential investment opportunities
- Calculate expected returns (ROI and rental yield)
- Assess risk levels
- Optimize portfolio allocation
- Track emerging markets

### Step-by-Step Workflow

#### 1. Define Investment Criteria

```python
investment_goals = {
    "min_roi": 15.0,              # Minimum annual ROI
    "risk_tolerance": "medium",    # low, medium, or high
    "time_horizon": "medium",      # short, medium, or long
    "property_types": [PropertyType.APARTMENT, PropertyType.VILLA],
    "max_investment": 1000000      # Per property
}
```

#### 2. Find Investment Opportunities

```python
investor_insights = insight_generator.generate_investor_insights(
    budget=2000000,
    investment_goals=investment_goals
)

# Review top opportunities
for opp in investor_insights['top_opportunities']:
    print(f"\n{opp['location']}:")
    print(f"  Opportunity Score: {opp['opportunity_score']:.1f}/100")
    print(f"  Expected ROI: {opp['predicted_roi']:.2f}%")
    print(f"  Rental Yield: {opp['rental_yield']:.2f}%")
    print(f"  Risk Level: {opp['risk_level']}")
    print(f"  Recommendation: {opp['recommendation']}")
```

#### 3. Analyze Individual Properties

```python
# Deep dive on specific property
property = opportunities[0]  # Top opportunity

# Calculate investment metrics
roi = investment_analyzer.predict_roi(
    property=property,
    purchase_price=800000,
    holding_period_years=5
)

print(f"Investment Analysis for {property.location}:")
print(f"  Purchase Price: $800,000")
print(f"  5-Year Total ROI: {roi['total_roi_percent']:.2f}%")
print(f"  Annual ROI: {roi['annual_roi_percent']:.2f}%")
print(f"  Rental Income (5yr): ${roi['total_rental_income']:,.0f}")
print(f"  Appreciation (5yr): ${roi['total_appreciation']:,.0f}")
print(f"  Total Return: ${roi['total_return']:,.0f}")
```

#### 4. Portfolio Optimization

```python
portfolio_strategy = investor_insights['portfolio_strategy']

print(f"\nPortfolio Strategy: {portfolio_strategy['diversification_strategy']}")
print(f"Expected Portfolio ROI: {portfolio_strategy['expected_portfolio_roi']:.2f}%")
print("\nRecommended Allocation:")

for allocation in portfolio_strategy['recommended_allocation']:
    print(f"  {allocation['location']}:")
    print(f"    Investment: ${allocation['estimated_investment']:,.0f}")
    print(f"    Percentage: {allocation['allocation_percent']:.0f}%")
    print(f"    Expected ROI: {allocation['expected_roi']:.2f}%")
    print(f"    Risk: {allocation['risk_level']}")
```

### Investment Strategies

#### Strategy 1: Income-Focused (Rental Yield)

**Goal:** Maximize monthly cash flow

**Approach:**
```python
# Find properties with highest rental yields
high_yield_properties = []

for prop in available_properties:
    rental_yield = investment_analyzer.calculate_rental_yield(
        property=prop,
        purchase_price=prop.estimated_price
    )
    
    if rental_yield >= 7.0:  # 7%+ yield
        high_yield_properties.append({
            'property': prop,
            'yield': rental_yield
        })

# Sort by yield
high_yield_properties.sort(key=lambda x: x['yield'], reverse=True)

print("Top rental yield opportunities:")
for item in high_yield_properties[:5]:
    print(f"  {item['property'].location}: {item['yield']:.2f}%")
```

#### Strategy 2: Growth-Focused (Appreciation)

**Goal:** Maximize property value appreciation

**Approach:**
```python
# Find emerging markets with high growth
emerging_markets = market_analyzer.identify_emerging_markets(
    min_growth_rate=8.0  # 8%+ annual growth
)

print("High-growth markets:")
for market in emerging_markets:
    trend = market_analyzer.analyze_market_trend(market, period_months=12)
    print(f"  {market}: {trend.price_change_percent:+.2f}% growth")
```

#### Strategy 3: Balanced Portfolio

**Goal:** Mix of income and appreciation

**Approach:**
```python
# Allocate 60% to income, 40% to growth
total_budget = 2000000

income_budget = total_budget * 0.6  # $1.2M
growth_budget = total_budget * 0.4  # $800K

# Income properties (high rental yield, stable areas)
income_properties = find_properties(
    criteria={'min_rental_yield': 6.5, 'market_stability': 'stable'}
)

# Growth properties (emerging areas, high appreciation)
growth_properties = find_properties(
    criteria={'min_price_growth': 8.0, 'emerging_market': True}
)
```

### Risk Management

#### Diversification Rules

1. **Geographic Diversification**
```python
# Don't concentrate in single neighborhood
portfolio_locations = [prop.location for prop in portfolio]
location_counts = {}

for loc in portfolio_locations:
    location_counts[loc] = location_counts.get(loc, 0) + 1

# Alert if >40% in single location
for loc, count in location_counts.items():
    concentration = (count / len(portfolio)) * 100
    if concentration > 40:
        print(f"⚠ Warning: {concentration:.0f}% concentrated in {loc}")
```

2. **Property Type Diversification**
```python
# Mix of apartments, villas, commercial
type_mix = {
    PropertyType.APARTMENT: 0.5,    # 50%
    PropertyType.VILLA: 0.3,        # 30%
    PropertyType.COMMERCIAL: 0.2    # 20%
}
```

3. **Risk Level Distribution**
```python
# Recommended: 50% low risk, 30% medium risk, 20% high risk
risk_distribution = {
    'low': 0.50,
    'medium': 0.30,
    'high': 0.20
}
```

### Performance Tracking

```python
def track_portfolio_performance(portfolio, period_months=12):
    """Track actual vs expected performance"""
    
    total_return = 0
    total_invested = 0
    
    for investment in portfolio:
        # Calculate actual return
        current_value = get_current_valuation(investment.property)
        rental_income = investment.rental_income_collected
        
        actual_return = (current_value - investment.purchase_price + 
                        rental_income)
        actual_roi = (actual_return / investment.purchase_price) * 100
        
        # Compare to expected
        expected_roi = investment.projected_roi
        
        print(f"{investment.property.location}:")
        print(f"  Expected ROI: {expected_roi:.2f}%")
        print(f"  Actual ROI: {actual_roi:.2f}%")
        print(f"  Variance: {actual_roi - expected_roi:+.2f}%")
        
        total_return += actual_return
        total_invested += investment.purchase_price
    
    portfolio_roi = (total_return / total_invested) * 100
    print(f"\nPortfolio ROI: {portfolio_roi:.2f}%")
```

---

## Agent's Guide

### Using Riyadh as a Real Estate Agent

The system can enhance your service to clients:

#### For Buyer Clients

```python
def create_buyer_package(property, client_budget):
    """Create comprehensive buyer package"""
    
    # Get insights
    insights = insight_generator.generate_buyer_insights(property, client_budget)
    
    package = {
        'property_summary': format_property_details(property),
        'valuation': {
            'market_value': insights['predicted_value'],
            'asking_price': property.asking_price,
            'value_assessment': insights['value_assessment']
        },
        'market_analysis': insights['market_conditions'],
        'investment_potential': insights['future_projections'],
        'negotiation_strategy': insights['negotiation_tips'],
        'timing_recommendation': insights['timing']
    }
    
    return package
```

#### For Seller Clients

```python
def create_listing_presentation(property):
    """Create seller listing presentation"""
    
    insights = insight_generator.generate_seller_insights(property)
    
    presentation = {
        'market_value': insights['market_value'],
        'pricing_strategy': insights['pricing_strategy'],
        'market_conditions': insights['market_conditions'],
        'expected_timeline': insights['estimated_days_on_market'],
        'marketing_plan': insights['marketing_recommendations'],
        'comparable_sales': get_comparable_sales(property)
    }
    
    return presentation
```

#### Comparative Market Analysis (CMA)

```python
def generate_cma(property, num_comparables=10):
    """Generate CMA for clients"""
    
    # Find comparable properties
    comparables = predictive_engine._find_comparable_properties(
        property, 
        max_comparables=num_comparables
    )
    
    # Analyze market
    trend = market_analyzer.analyze_market_trend(
        property.location, 
        period_months=6
    )
    
    cma = {
        'subject_property': property,
        'comparable_sales': comparables,
        'market_trend': trend,
        'price_range': calculate_price_range(comparables),
        'recommended_price': predictive_engine.predict_property_value(property)
    }
    
    return cma
```

---

## Additional Resources

- **API Documentation**: See main README.md
- **Prompt Templates**: See PROMPT_TEMPLATE.md
- **Example Code**: See example.py
- **Technical Details**: See individual module docstrings

## Support

For questions or issues:
1. Check the README.md for API reference
2. Review example.py for working code
3. Open an issue on GitHub

## Best Practices

1. **Always use recent data** - Predictions are only as good as the data
2. **Validate assumptions** - Cross-reference with local knowledge
3. **Consider context** - Numbers don't tell the whole story
4. **Update regularly** - Market conditions change
5. **Use as decision support** - Not a replacement for professional judgment
