import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="DealFlow AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 DealFlow AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent M&A Target Discovery Platform</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("🚀 Navigation")
        st.info("Welcome to DealFlow AI - Your intelligent M&A assistant")
        
        # Status indicator
        st.success("🟢 System Online")
        st.caption("All services operational")
        
        # Quick stats
        st.markdown("---")
        st.subheader("📊 Quick Stats")
        st.metric("Companies", "0", help="Total companies analyzed")
        st.metric("Documents", "0", help="Documents processed")
        st.metric("Analyses", "0", help="AI analyses completed")
    
    # Main content area
    st.subheader("🚀 Getting Started")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Upload Documents", use_container_width=True):
            st.switch_page("pages/1_📄_Upload_Documents.py")
    
    with col2:
        if st.button("🔍 Search Companies", use_container_width=True):
            st.switch_page("pages/2_🔍_Search_Companies.py")
    
    with col3:
        if st.button("📊 Analyze Targets", use_container_width=True):
            st.switch_page("pages/3_📊_Analyze_Targets.py")
    
    with col4:
        if st.button("📋 Generate Report", use_container_width=True):
            st.switch_page("pages/4_📋_Generate_Report.py")
    
    # Features overview
    st.markdown("---")
    st.subheader("🎯 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📄 Document Intelligence
        - Upload pitch decks, 10-K filings, research reports
        - AI-powered text extraction and analysis
        - Semantic search across document database
        """)
        
        st.markdown("""
        ### 🏦 Goldman Sachs Integration
        - Industry-standard valuation methodologies
        - Professional financial modeling
        - Risk assessment frameworks
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 Custom AI Models
        - Acquisition fit scoring algorithms
        - Company similarity matching
        - Investment thesis generation
        """)
        
        st.markdown("""
        ### 📊 Advanced Analytics
        - Real-time market intelligence
        - Comparative deal analysis
        - Automated report generation
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit, LangChain, and custom ML models*")

if __name__ == "__main__":
    main()
