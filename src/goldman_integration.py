import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import logging

# Note: GS Quant requires Goldman Sachs API access for full functionality
# For MVP, we'll implement the methodologies without requiring API access

logger = logging.getLogger(__name__)

class GoldmanSachsAnalyzer:
    """
    Goldman Sachs financial analysis methodologies
    Implements industry-standard valuation and risk assessment frameworks
    """
    
    def __init__(self):
        self.risk_free_rate = 0.045  # Current 10-year Treasury rate
        self.market_risk_premium = 0.06  # Historical equity risk premium
        
    def calculate_dcf_valuation(self, company_financials):
        """
        Calculate DCF valuation using Goldman Sachs methodology
        """
        try:
            # Extract financial data
            revenue = company_financials.get('revenue', 100_000_000)
            growth_rate = company_financials.get('growth_rate', 0.15)
            ebitda_margin = company_financials.get('ebitda_margin', 0.20)
            tax_rate = company_financials.get('tax_rate', 0.21)
            capex_rate = company_financials.get('capex_rate', 0.03)
            
            # Goldman Sachs DCF Parameters
            projection_years = 5
            terminal_growth_rate = 0.025  # Long-term GDP growth
            
            # Project cash flows
            cash_flows = []
            current_revenue = revenue
            
            for year in range(1, projection_years + 1):
                # Revenue growth (declining over time)
                year_growth = growth_rate * (0.85 ** (year - 1))  # Declining growth
                current_revenue *= (1 + year_growth)
                
                # EBITDA
                ebitda = current_revenue * ebitda_margin
                
                # EBIT (assuming D&A is 3% of revenue)
                ebit = ebitda - (current_revenue * 0.03)
                
                # Taxes
                taxes = ebit * tax_rate
                
                # NOPAT
                nopat = ebit - taxes
                
                # CapEx
                capex = current_revenue * capex_rate
                
                # Free Cash Flow
                fcf = nopat - capex
                cash_flows.append(fcf)
            
            # Terminal value
            terminal_fcf = cash_flows[-1] * (1 + terminal_growth_rate)
            terminal_value = terminal_fcf / (self.calculate_wacc(company_financials) - terminal_growth_rate)
            
            # Discount cash flows
            wacc = self.calculate_wacc(company_financials)
            present_values = []
            
            for i, fcf in enumerate(cash_flows):
                pv = fcf / ((1 + wacc) ** (i + 1))
                present_values.append(pv)
            
            # Terminal value present value
            terminal_pv = terminal_value / ((1 + wacc) ** projection_years)
            
            # Enterprise value
            enterprise_value = sum(present_values) + terminal_pv
            
            return {
                'enterprise_value': enterprise_value,
                'dcf_per_share': enterprise_value / company_financials.get('shares_outstanding', 100_000_000),
                'wacc': wacc,
                'terminal_value': terminal_value,
                'cash_flows': cash_flows,
                'methodology': 'Goldman Sachs DCF Model'
            }
            
        except Exception as e:
            logger.error(f"Error in DCF calculation: {str(e)}")
            return {'error': str(e)}
    
    def calculate_wacc(self, company_financials):
        """Calculate Weighted Average Cost of Capital using Goldman methodology"""
        # Company-specific inputs
        beta = company_financials.get('beta', 1.2)
        debt_to_equity = company_financials.get('debt_to_equity', 0.3)
        tax_rate = company_financials.get('tax_rate', 0.21)
        
        # Cost of equity (CAPM)
        cost_of_equity = self.risk_free_rate + (beta * self.market_risk_premium)
        
        # Cost of debt (risk-free rate + credit spread)
        credit_spread = self.estimate_credit_spread(company_financials)
        cost_of_debt = self.risk_free_rate + credit_spread
        after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)
        
        # Weight calculations
        weight_equity = 1 / (1 + debt_to_equity)
        weight_debt = debt_to_equity / (1 + debt_to_equity)
        
        # WACC calculation
        wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_of_debt)
        
        return wacc
    
    def estimate_credit_spread(self, company_financials):
        """Estimate credit spread based on company fundamentals"""
        # Simple credit scoring model
        revenue = company_financials.get('revenue', 100_000_000)
        ebitda_margin = company_financials.get('ebitda_margin', 0.20)
        debt_to_equity = company_financials.get('debt_to_equity', 0.3)
        
        # Base spread
        base_spread = 0.02  # 200bps
        
        # Adjustments
        if revenue > 1_000_000_000:  # Large company
            base_spread -= 0.005
        elif revenue < 100_000_000:  # Small company
            base_spread += 0.01
        
        if ebitda_margin > 0.25:  # High profitability
            base_spread -= 0.005
        elif ebitda_margin < 0.10:  # Low profitability
            base_spread += 0.01
        
        if debt_to_equity > 0.5:  # High leverage
            base_spread += 0.01
        
        return max(0.005, base_spread)  # Minimum 50bps spread
    
    def calculate_comparable_valuation(self, company_financials, industry_multiples):
        """Calculate valuation using comparable company analysis"""
        try:
            revenue = company_financials.get('revenue', 100_000_000)
            ebitda = revenue * company_financials.get('ebitda_margin', 0.20)
            
            # Industry multiples (would be real data in production)
            ev_revenue_multiple = industry_multiples.get('ev_revenue', 4.0)
            ev_ebitda_multiple = industry_multiples.get('ev_ebitda', 15.0)
            
            # Valuation calculations
            ev_by_revenue = revenue * ev_revenue_multiple
            ev_by_ebitda = ebitda * ev_ebitda_multiple
            
            # Average of methodologies
            average_ev = (ev_by_revenue + ev_by_ebitda) / 2
            
            return {
                'ev_revenue_valuation': ev_by_revenue,
                'ev_ebitda_valuation': ev_by_ebitda,
                'average_valuation': average_ev,
                'methodology': 'Goldman Sachs Comparable Analysis'
            }
            
        except Exception as e:
            logger.error(f"Error in comparable valuation: {str(e)}")
            return {'error': str(e)}
    
    def assess_acquisition_risks(self, acquirer_profile, target_profile):
        """Goldman Sachs risk assessment framework"""
        risks = []
        risk_score = 0
        
        # Integration risk
        if abs(acquirer_profile.get('employee_count', 1000) - target_profile.get('employee_count', 500)) > 10000:
            risks.append("High integration complexity due to size difference")
            risk_score += 0.2
        
        # Cultural fit
        culture_score = target_profile.get('cultural_fit', 0.5)
        if culture_score < 0.4:
            risks.append("Low cultural alignment may impact integration")
            risk_score += 0.15
        
        # Market overlap
        market_overlap = target_profile.get('geography_overlap', 0.5)
        if market_overlap < 0.3:
            risks.append("Limited market synergies due to geographic dispersion")
            risk_score += 0.1
        
        # Financial risk
        debt_to_equity = target_profile.get('debt_to_equity', 0.3)
        if debt_to_equity > 0.6:
            risks.append("High leverage increases financial risk")
            risk_score += 0.2
        
        # Technology risk
        tech_fit = target_profile.get('technology_fit', 0.5)
        if tech_fit < 0.4:
            risks.append("Technology integration challenges expected")
            risk_score += 0.15
        
        # Overall risk assessment
        if risk_score < 0.3:
            risk_level = "Low"
        elif risk_score < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'risk_factors': risks,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'methodology': 'Goldman Sachs Risk Framework'
        }
    
    def generate_investment_recommendation(self, dcf_valuation, comparable_valuation, 
                                         risk_assessment, market_price=None):
        """Generate Goldman Sachs style investment recommendation"""
        
        # Average valuation
        avg_valuation = (dcf_valuation['enterprise_value'] + comparable_valuation['average_valuation']) / 2
        
        # Risk adjustment
        risk_discount = risk_assessment['risk_score'] * 0.15  # Max 15% discount for risk
        risk_adjusted_valuation = avg_valuation * (1 - risk_discount)
        
        # Recommendation logic
        if market_price:
            upside = (risk_adjusted_valuation - market_price) / market_price
            if upside > 0.20:
                recommendation = "BUY"
                rating = 5
            elif upside > 0.10:
                recommendation = "OVERWEIGHT"
                rating = 4
            elif upside > -0.10:
                recommendation = "NEUTRAL"
                rating = 3
            elif upside > -0.20:
                recommendation = "UNDERWEIGHT"
                rating = 2
            else:
                recommendation = "SELL"
                rating = 1
        else:
            recommendation = "BUY" if risk_assessment['risk_level'] == "Low" else "HOLD"
            rating = 4 if risk_assessment['risk_level'] == "Low" else 3
        
        return {
            'recommendation': recommendation,
            'rating': rating,
            'target_valuation': risk_adjusted_valuation,
            'risk_adjusted_discount': risk_discount,
            'methodology': 'Goldman Sachs Investment Framework'
        }

@st.cache(allow_output_mutation=True)
def get_goldman_analyzer():
    """Get cached Goldman Sachs analyzer instance."""
    return GoldmanSachsAnalyzer()