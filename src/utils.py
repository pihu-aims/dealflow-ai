import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import logging

# Supabase import with graceful fallback
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    try:
        # Try alternative import for newer versions
        from supabase import create_client
        from supabase.client import Client
        SUPABASE_AVAILABLE = True
    except ImportError:
        # If all imports fail, define a dummy Client type
        Client = None
        SUPABASE_AVAILABLE = False
        logging.warning("Supabase not installed - using mock database")

def init_supabase():
    """Initialize Supabase client with connection pooling."""
    if not SUPABASE_AVAILABLE:
        logging.warning("Supabase not available - using mock database")
        return None
        
    try:
        # Try to get credentials from Streamlit secrets first
        if hasattr(st, 'secrets') and 'supabase' in st.secrets:
            supabase_url = st.secrets['supabase']['url']
            supabase_key = st.secrets['supabase']['key']
        else:
            # Fallback to environment variables
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY')

        if not supabase_url or not supabase_key:
            logging.warning("Supabase credentials not found - using mock database")
            return None

        # Create client with minimal parameters to avoid compatibility issues
        supabase = create_client(supabase_url, supabase_key)
        
        # Test the connection with a simple query
        try:
            # Try a simple health check
            result = supabase.table('companies').select('count').limit(1).execute()
            logging.info("✅ Supabase client initialized and tested successfully")
        except Exception as test_error:
            logging.warning(f"⚠️ Supabase client initialized but test failed: {str(test_error)}")
            
        return supabase
        
    except Exception as e:
        logging.error(f"❌ Failed to initialize Supabase: {str(e)}")
        return None

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

def format_currency(value):
    """Format a value as currency."""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}M" if value >= 1 else f"${value*1000:,.2f}K"

def test_database_connection():
    """
    Test the database connection and return status.
    
    Returns:
        tuple: (bool, str) - (success, message)
    """
    try:
        supabase = init_supabase()
        if supabase is None:
            return False, "❌ Supabase not available - using mock database"
        
        # Test connection with a simple query
        result = supabase.table('companies').select('count').execute()
        return True, "✅ Supabase database connected"
        
    except Exception as e:
        return False, f"❌ Database connection failed: {str(e)}"

def get_companies_summary():
    """
    Get summary statistics about companies in the database.
    
    Returns:
        dict: Summary statistics
    """
    try:
        # Mock data for now - in a real app, you'd query the actual database
        return {
            'total': 1247,
            'industries': 23,
            'documents': 3456,
            'recent_additions': 12
        }
    except Exception as e:
        return {
            'total': 0,
            'industries': 0,
            'documents': 0,
            'recent_additions': 0
        }

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
            value = company_data[metric]
            if isinstance(value, (int, float)):
                normalized_value = min(value / 100, 1.0)  # Simple normalization
            else:
                normalized_value = 0.5  # Default for non-numeric values
        else:
            normalized_value = 0.0
        values.append(normalized_value)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=metrics,
        fill='toself',
        name=company_data.get('company_name', 'Company')
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
            <p><strong>Founded:</strong> {company_data.get('founded', 'N/A')}</p>
            <p><strong>Employees:</strong> {company_data.get('employees', 'N/A')}</p>
        </div>
        
        <div class="section">
            <h2>Financial Metrics</h2>
            <div class="metric">
                <div class="metric-value">{format_currency(company_data.get('revenue', 0))}</div>
                <div class="metric-label">Revenue</div>
            </div>
            <div class="metric">
                <div class="metric-value">{format_currency(company_data.get('valuation', 0))}</div>
                <div class="metric-label">Valuation</div>
            </div>
            <div class="metric">
                <div class="metric-value">{company_data.get('growth_rate', 'N/A')}%</div>
                <div class="metric-label">Growth Rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Analysis Summary</h2>
            <p>{analysis.get('summary', 'No analysis available.')}</p>
        </div>
        
        <div class="section">
            <h2>Investment Recommendation</h2>
            <p><strong>Score:</strong> {analysis.get('investment_score', 'N/A')}/10</p>
            <p><strong>Risk Level:</strong> {analysis.get('risk_level', 'N/A')}</p>
            <p><strong>Recommendation:</strong> {analysis.get('recommendation', 'N/A')}</p>
        </div>
    </body>
    </html>
    """
    
    return html
