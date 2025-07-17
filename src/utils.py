import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="DealFlow AI",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def display_sidebar():
    """Display the sidebar with navigation and settings."""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x80?text=DealFlow+AI", width=150)
        st.markdown("## Navigation")
        
        # Check if API key is set
        api_key_set = os.environ.get("OPENAI_API_KEY") is not None
        
        if not api_key_set:
            st.warning("⚠️ OpenAI API key not set")
            with st.expander("Set API Key"):
                api_key = st.text_input("OpenAI API Key", type="password")
                if api_key and st.button("Save API Key"):
                    os.environ["OPENAI_API_KEY"] = api_key
                    st.success("API key set successfully!")
                    st.rerun()
        
        # Display settings
        with st.expander("Settings"):
            st.selectbox(
                "LLM Model",
                ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                index=0
            )
            st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
            st.number_input("Max Tokens", min_value=100, max_value=4000, value=1000, step=100)
        
        # Display collections
        try:
            from src.document_processor import DocumentProcessor
            processor = DocumentProcessor()
            collections = processor.get_collections()
            
            if collections:
                st.markdown("## Collections")
                for collection in collections:
                    st.markdown(f"- {collection}")
        except:
            pass

def format_currency(value):
    """Format a value as currency."""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}M" if value >= 1 else f"${value*1000:,.2f}K"

def create_radar_chart(company_data: Dict[str, Any], metrics: List[str], title: str = "Company Metrics"):
    """
    Create a radar chart for company metrics.
    
    Args:
        company_data: Dictionary with company data
        metrics: List of metrics to include in the chart
        title: Chart title
        
    Returns:
        Plotly figure
    """
    # Normalize values between 0 and 1 for radar chart
    values = []
    for metric in metrics:
        if metric in company_data:
            # Simple normalization - in a real app, you'd want to normalize against industry benchmarks
            if metric == "revenue_millions":
                values.append(min(company_data[metric] / 100, 1))
            elif metric == "employees":
                values.append(min(company_data[metric] / 500, 1))
            elif metric == "growth_rate":
                values.append(min(company_data[metric] / 50, 1))
            else:
                values.append(0.5)  # Default for unknown metrics
        else:
            values.append(0)
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        name=company_data.get("company_name", "Company")
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title=title,
        showlegend=True
    )
    
    return fig

def create_comparison_chart(companies_data: List[Dict[str, Any]], metric: str, title: str = None):
    """
    Create a bar chart comparing companies on a specific metric.
    
    Args:
        companies_data: List of dictionaries with company data
        metric: Metric to compare
        title: Chart title
        
    Returns:
        Plotly figure
    """
    df = pd.DataFrame(companies_data)
    
    if not title:
        title = f"Company Comparison: {metric.replace('_', ' ').title()}"
    
    fig = px.bar(
        df,
        x="company_name",
        y=metric,
        title=title,
        labels={"company_name": "Company", metric: metric.replace('_', ' ').title()},
        color="company_name"
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig

def create_growth_projection(company_data: Dict[str, Any], years: int = 5):
    """
    Create a growth projection chart.
    
    Args:
        company_data: Dictionary with company data
        years: Number of years to project
        
    Returns:
        Plotly figure
    """
    current_revenue = company_data.get("revenue_millions", 50)
    growth_rate = company_data.get("growth_rate", 15) / 100
    
    years_list = list(range(years + 1))
    revenue_projection = [current_revenue * ((1 + growth_rate) ** year) for year in years_list]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years_list,
        y=revenue_projection,
        mode='lines+markers',
        name='Projected Revenue',
        line=dict(color='royalblue', width=4)
    ))
    
    fig.update_layout(
        title=f"Revenue Projection: {company_data.get('company_name', 'Company')}",
        xaxis_title="Years from Now",
        yaxis_title="Revenue ($ Millions)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        yaxis=dict(tickformat="$,.1fM")
    )
    
    return fig

def generate_report_html(company_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """
    Generate an HTML report for a company.
    
    Args:
        company_data: Dictionary with company data
        analysis: Dictionary with analysis data
        
    Returns:
        HTML string
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DealFlow AI Report: {company_data.get('company_name', 'Company')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background-color: #0066CC; color: white; padding: 20px; }}
            .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; }}
            .metric {{ display: inline-block; width: 30%; margin: 10px; text-align: center; }}
            .metric-value {{ font-size: 24px; font-weight: bold; }}
            .metric-label {{ font-size: 14px; color: #666; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>DealFlow AI: Target Analysis Report</h1>
            <h2>{company_data.get('company_name', 'Company')}</h2>
            <p>Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
        </div>
        
        <div class="section">
            <h2>Company Overview</h2>
            <p><strong>Industry:</strong> {company_data.get('industry', 'N/A')}</p>
            <p><strong>Headquarters:</strong> {company_data.get('headquarters', 'N/A')}</p>
            <p><strong>Founded:</strong> {company_data.get('founded_year', 'N/A')}</p>
            <p><strong>Description:</strong> {company_data.get('description', 'N/A')}</p>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{format_currency(company_data.get('revenue_millions', 0))}</div>
                    <div class="metric-label">Annual Revenue</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{company_data.get('employees', 'N/A')}</div>
                    <div class="metric-label">Employees</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{company_data.get('growth_rate', 'N/A')}%</div>
                    <div class="metric-label">Growth Rate</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Financial Analysis</h2>
            <p>{analysis.get('financial_analysis', 'No financial analysis available.')}</p>
        </div>
        
        <div class="section">
            <h2>Strategic Fit</h2>
            <p>{analysis.get('strategic_fit', 'No strategic fit analysis available.')}</p>
        </div>
        
        <div class="section">
            <h2>SWOT Analysis</h2>
            <table>
                <tr>
                    <th>Strengths</th>
                    <th>Weaknesses</th>
                </tr>
                <tr>
                    <td>{analysis.get('strengths', 'No data available.')}</td>
                    <td>{analysis.get('weaknesses', 'No data available.')}</td>
                </tr>
                <tr>
                    <th>Opportunities</th>
                    <th>Threats</th>
                </tr>
                <tr>
                    <td>{analysis.get('opportunities', 'No data available.')}</td>
                    <td>{analysis.get('threats', 'No data available.')}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Valuation Considerations</h2>
            <p>{analysis.get('valuation', 'No valuation analysis available.')}</p>
        </div>
        
        <div class="section">
            <h2>Recommendation</h2>
            <p>{analysis.get('recommendation', 'No recommendation available.')}</p>
        </div>
        
        <div class="footer">
            <p>This report was generated by DealFlow AI. The information contained herein is for informational purposes only.</p>
        </div>
    </body>
    </html>
    """
    
    return html
