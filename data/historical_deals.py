import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_historical_ma_dataset():
    """Generate realistic historical M&A dataset for model training."""
    
    # Real M&A deals as foundation (publicly available data)
    base_deals = [
        # Tech Acquisitions
        {'acquirer': 'Microsoft', 'target': 'LinkedIn', 'deal_value': 26200, 'year': 2016, 'success': 1, 'industry': 'Technology'},
        {'acquirer': 'Facebook', 'target': 'WhatsApp', 'deal_value': 19000, 'year': 2014, 'success': 1, 'industry': 'Technology'},
        {'acquirer': 'Google', 'target': 'Nest Labs', 'deal_value': 3200, 'year': 2014, 'success': 0, 'industry': 'Technology'},
        {'acquirer': 'Yahoo', 'target': 'Tumblr', 'deal_value': 1100, 'year': 2013, 'success': 0, 'industry': 'Technology'},
        {'acquirer': 'Microsoft', 'target': 'Skype', 'deal_value': 8500, 'year': 2011, 'success': 1, 'industry': 'Technology'},
        {'acquirer': 'Oracle', 'target': 'Sun Microsystems', 'deal_value': 7400, 'year': 2010, 'success': 1, 'industry': 'Technology'},
        {'acquirer': 'HP', 'target': 'Autonomy', 'deal_value': 11100, 'year': 2011, 'success': 0, 'industry': 'Technology'},
        {'acquirer': 'Adobe', 'target': 'Figma', 'deal_value': 20000, 'year': 2022, 'success': 1, 'industry': 'Technology'},
        
        # Financial Services
        {'acquirer': 'JPMorgan', 'target': 'Bear Stearns', 'deal_value': 240, 'year': 2008, 'success': 1, 'industry': 'Financial Services'},
        {'acquirer': 'Wells Fargo', 'target': 'Wachovia', 'deal_value': 15100, 'year': 2008, 'success': 1, 'industry': 'Financial Services'},
        {'acquirer': 'Bank of America', 'target': 'Countrywide', 'deal_value': 4000, 'year': 2008, 'success': 0, 'industry': 'Financial Services'},
        
        # Healthcare
        {'acquirer': 'Pfizer', 'target': 'Wyeth', 'deal_value': 68000, 'year': 2009, 'success': 1, 'industry': 'Healthcare'},
        {'acquirer': 'Johnson & Johnson', 'target': 'Actelion', 'deal_value': 30000, 'year': 2017, 'success': 1, 'industry': 'Healthcare'},
        
        # Retail/Consumer
        {'acquirer': 'Amazon', 'target': 'Whole Foods', 'deal_value': 13700, 'year': 2017, 'success': 1, 'industry': 'Retail'},
        {'acquirer': 'Walmart', 'target': 'Jet.com', 'deal_value': 3300, 'year': 2016, 'success': 0, 'industry': 'Retail'},
    ]
    
    # Generate additional synthetic deals based on patterns
    industries = ['Technology', 'Financial Services', 'Healthcare', 'Retail', 'Manufacturing', 'Energy']
    
    synthetic_deals = []
    for i in range(200):  # Generate 200 synthetic deals
        industry = random.choice(industries)
        
        # Create realistic features based on industry
        if industry == 'Technology':
            revenue_multiple = np.random.normal(6.0, 2.5)
            growth_rate = np.random.normal(0.25, 0.15)
            profit_margin = np.random.normal(0.12, 0.08)
        elif industry == 'Financial Services':
            revenue_multiple = np.random.normal(2.5, 1.0)
            growth_rate = np.random.normal(0.08, 0.05)
            profit_margin = np.random.normal(0.20, 0.10)
        else:
            revenue_multiple = np.random.normal(4.0, 1.5)
            growth_rate = np.random.normal(0.15, 0.10)
            profit_margin = np.random.normal(0.08, 0.05)
        
        # Ensure realistic bounds
        revenue_multiple = max(0.5, min(15.0, revenue_multiple))
        growth_rate = max(-0.2, min(0.8, growth_rate))
        profit_margin = max(-0.1, min(0.4, profit_margin))
        
        # Calculate success probability based on features
        success_prob = 0.3  # Base probability
        if revenue_multiple < 8.0: success_prob += 0.2
        if growth_rate > 0.15: success_prob += 0.2
        if profit_margin > 0.10: success_prob += 0.2
        if industry in ['Technology', 'Healthcare']: success_prob += 0.1
        
        success = 1 if random.random() < success_prob else 0
        
        synthetic_deal = {
            'acquirer': f'Acquirer_{i}',
            'target': f'Target_{i}',
            'deal_value': random.uniform(100, 50000),  # $100M - $50B
            'year': random.randint(2010, 2023),
            'success': success,
            'industry': industry,
            'revenue_multiple': revenue_multiple,
            'growth_rate': growth_rate,
            'profit_margin': profit_margin,
            'market_share': random.uniform(0.01, 0.25),
            'employee_count': random.randint(50, 50000),
            'geography_overlap': random.uniform(0.2, 1.0),
            'technology_fit': random.uniform(0.1, 1.0) if industry == 'Technology' else random.uniform(0.1, 0.6),
            'cultural_fit': random.uniform(0.3, 1.0),
            'integration_complexity': random.uniform(0.2, 0.9)
        }
        synthetic_deals.append(synthetic_deal)
    
    # Combine real and synthetic deals
    all_deals = base_deals + synthetic_deals
    
    # Create DataFrame
    df = pd.DataFrame(all_deals)
    
    # Fill missing values for real deals
    for col in ['revenue_multiple', 'growth_rate', 'profit_margin', 'market_share', 
                'employee_count', 'geography_overlap', 'technology_fit', 'cultural_fit', 'integration_complexity']:
        if col not in df.columns:
            df[col] = np.random.normal(0.5, 0.2, len(df))
        df[col] = df[col].fillna(np.random.normal(0.5, 0.2, df[col].isna().sum()))
    
    return df

def save_historical_dataset():
    """Generate and save the historical M&A dataset."""
    df = generate_historical_ma_dataset()
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data/ml_models', exist_ok=True)
    
    # Save dataset
    df.to_csv('data/ml_models/historical_ma_deals.csv', index=False)
    print(f"✅ Generated {len(df)} historical M&A deals")
    print(f"Success rate: {df['success'].mean():.1%}")
    print("\nDataset saved to: data/ml_models/historical_ma_deals.csv")
    
    return df

if __name__ == "__main__":
    dataset = save_historical_dataset()
    print("\nSample deals:")
    print(dataset.head())