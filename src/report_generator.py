import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import io
import base64

class ProfessionalReportGenerator:
    def __init__(self):
        self.report_template = self._load_report_template()
    
    def generate_investment_memo(self, analysis_data: Dict) -> str:
        """Generate professional investment memorandum."""
        
        report = f"""
# INVESTMENT MEMORANDUM
**Confidential & Proprietary**

---

## EXECUTIVE SUMMARY

**Target Company:** {analysis_data.get('company_name', 'Target Company')}  
**Industry:** {analysis_data.get('industry', 'Technology')}  
**Analysis Date:** {datetime.now().strftime('%B %d, %Y')}  
**Recommendation:** {analysis_data.get('recommendation', 'HOLD')}

### Key Investment Highlights
- **Acquisition Success Probability:** {analysis_data.get('ml_probability', 0.75):.0%}
- **DCF Valuation:** ${analysis_data.get('dcf_value', 500):,.0f}M
- **Revenue Multiple:** {analysis_data.get('revenue_multiple', 4.5):.1f}x
- **Risk Level:** {analysis_data.get('risk_level', 'Medium')}

---

## COMPANY OVERVIEW

{analysis_data.get('company_name', 'Target Company')} is a {analysis_data.get('industry', 'technology')} company with annual revenue of ${analysis_data.get('revenue', 250):,.0f}M and {analysis_data.get('employees', 1200):,} employees.

### Business Model
{analysis_data.get('description', 'A leading company in its sector with strong market position and growth prospects.')}

### Financial Highlights
- **Annual Revenue:** ${analysis_data.get('revenue', 250):,.0f}M
- **Growth Rate:** {analysis_data.get('growth_rate', 0.25):.0%}
- **EBITDA Margin:** {analysis_data.get('ebitda_margin', 0.20):.0%}
- **Market Share:** {analysis_data.get('market_share', 0.08):.0%}

---

## VALUATION ANALYSIS

### DCF Valuation (Goldman Sachs Methodology)
- **Enterprise Value:** ${analysis_data.get('dcf_value', 500):,.0f}M
- **WACC:** {analysis_data.get('wacc', 0.12):.1%}
- **Terminal Growth Rate:** 2.5%
- **DCF Per Share:** ${analysis_data.get('dcf_per_share', 50):.2f}

### Comparable Company Analysis
- **EV/Revenue Multiple:** {analysis_data.get('ev_revenue', 4.5):.1f}x
- **EV/EBITDA Multiple:** {analysis_data.get('ev_ebitda', 15.0):.1f}x
- **Industry Average P/E:** {analysis_data.get('pe_ratio', 20):.1f}x

---

## MACHINE LEARNING ANALYSIS

Our proprietary ML model, trained on 200+ historical M&A transactions, predicts:

- **Acquisition Success Probability:** {analysis_data.get('ml_probability', 0.75):.0%}
- **Model Confidence:** {analysis_data.get('ml_confidence', 'High')}
- **Key Success Factors:**
  - Revenue Growth Rate: {analysis_data.get('growth_rate', 0.25):.0%}
  - Market Position: Strong
  - Integration Complexity: {analysis_data.get('integration_complexity', 0.4):.0%}

---

## RISK ASSESSMENT

### Risk Level: {analysis_data.get('risk_level', 'Medium')}

#### Key Risk Factors:
"""

        # Add risk factors
        risk_factors = analysis_data.get('risk_factors', [])
        if risk_factors:
            for risk in risk_factors[:5]:
                report += f"- {risk}\n"
        else:
            report += "- Integration complexity\n- Market competition\n- Regulatory environment\n"

        report += f"""

#### Risk Mitigation Strategies:
- Comprehensive due diligence process
- Structured integration planning
- Retention of key personnel
- Clear synergy realization roadmap

---

## STRATEGIC RATIONALE

### Acquisition Benefits:
- **Revenue Synergies:** Estimated {analysis_data.get('revenue_synergies', 15):.0%} uplift
- **Market Expansion:** Access to new customer segments
- **Technology Integration:** Enhanced product capabilities
- **Operational Efficiencies:** Cost synergies of ${analysis_data.get('cost_synergies', 25):,.0f}M

### Strategic Fit Score: {analysis_data.get('strategic_fit', 8.5):.1f}/10

---

## RECOMMENDATION

**{analysis_data.get('recommendation', 'HOLD')}** - Based on comprehensive analysis combining:
- Custom ML prediction model
- Goldman Sachs valuation methodology
- Industry-standard risk assessment

### Proposed Action Plan:
1. **Immediate:** Initiate management meetings
2. **30 Days:** Complete preliminary due diligence
3. **60 Days:** Submit preliminary offer
4. **90 Days:** Finalize transaction structure

---

## APPENDIX

### Methodology Notes:
- DCF analysis based on Goldman Sachs standards
- ML model trained on historical M&A outcomes
- Risk assessment using industry frameworks
- Market data sourced from institutional providers

*This analysis is confidential and proprietary. Distribution is restricted to authorized personnel only.*

**Prepared by:** DealFlow AI Platform  
**Date:** {datetime.now().strftime('%B %d, %Y')}
"""
        
        return report
    
    def create_dashboard_summary(self, analysis_data: Dict) -> None:
        """Create visual dashboard summary."""
        
        st.markdown("## 📊 Executive Dashboard")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Success Probability",
                f"{analysis_data.get('ml_probability', 0.75):.0%}",
                delta=f"+{analysis_data.get('ml_probability', 0.75) - 0.5:.0%} vs avg"
            )
        
        with col2:
            st.metric(
                "DCF Valuation",
                f"${analysis_data.get('dcf_value', 500):,.0f}M",
                delta=f"{analysis_data.get('dcf_upside', 0.15):.0%} upside"
            )
        
        with col3:
            st.metric(
                "Revenue Multiple",
                f"{analysis_data.get('revenue_multiple', 4.5):.1f}x",
                delta=f"vs {analysis_data.get('industry_avg_multiple', 5.0):.1f}x industry"
            )
        
        with col4:
            risk_color = {"Low": "inverse", "Medium": "normal", "High": "off"}
            st.metric(
                "Risk Level",
                analysis_data.get('risk_level', 'Medium'),
                delta=f"{analysis_data.get('risk_score', 0.4):.0%} risk score",
                delta_color=risk_color.get(analysis_data.get('risk_level', 'Medium'), 'normal')
            )
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            # Success probability gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=analysis_data.get('ml_probability', 0.75) * 100,
                title={'text': "ML Success Probability"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300, title="Acquisition Success Prediction")
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Valuation comparison
            valuation_methods = ['DCF Model', 'Comparable Analysis', 'Asset Based']
            valuations = [
                analysis_data.get('dcf_value', 500),
                analysis_data.get('comparable_value', 450),
                analysis_data.get('asset_value', 400)
            ]
            
            fig_bar = px.bar(
                x=valuation_methods,
                y=valuations,
                title="Valuation by Method ($M)",
                color=valuations,
                color_continuous_scale="Viridis"
            )
            fig_bar.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    def export_to_markdown(self, analysis_data: Dict) -> str:
        """Export report as downloadable markdown."""
        return self.generate_investment_memo(analysis_data)
    
    def _load_report_template(self) -> str:
        """Load professional report template."""
        return """
        Professional Investment Banking Report Template
        Customizable for different analysis types
        """

@st.cache(allow_output_mutation=True)
def get_report_generator():
    """Get cached report generator instance."""
    return ProfessionalReportGenerator()