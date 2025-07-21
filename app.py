import streamlit as st
import pandas as pd
from pathlib import Path
from src.utils import test_database_connection, get_companies_summary
from src.rag_system import DealFlowRAG  # Enabled - langchain now installed

# Page configuration
st.set_page_config(
    page_title="DealFlow AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (keep existing)
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
    st.markdown('<h1 class="main-header">DealFlow AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent M&A Target Discovery Platform</p>', unsafe_allow_html=True)
    
    # Database connection status
    db_status, db_message = test_database_connection()
    
    # Sidebar
    with st.sidebar:
        st.title(" Navigation")
        
        # Database status
        if db_status:
            st.success(db_message)
        else:
            st.error(db_message)
        
        # Get real stats
        summary = get_companies_summary()
        
        st.markdown("---")
        st.subheader(" Platform Stats")
        st.metric("Companies", summary.get('total', 0), help="Total companies in database")
        st.metric("Industries", summary.get('industries', 0), help="Unique industries tracked")
        st.metric("Documents", "Loading...", help="Documents processed")
        
        # Get RAG system stats
        try:
            rag_system = DealFlowRAG()
            rag_stats = rag_system.get_rag_stats()
            
            st.markdown("---")
            st.subheader("🤖 AI System")
            st.metric("Vector Documents", rag_stats['vector_store']['total_documents'])
            st.metric("Embeddings", rag_stats['vector_store']['total_embeddings'])
            st.metric("Collections", rag_stats['vector_store']['collections'])
            
        except Exception as e:
            st.error(f"RAG System Error: {str(e)}")
        
    # Main navigation (keep existing)
    st.subheader("Getting Started")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(" Upload Documents"):
            st.info(" Navigate to 'Upload Documents' page using the sidebar")
    
    with col2:
        if st.button(" Search Companies"):
            st.info("🔍 Navigate to 'Search Companies' page using the sidebar")
    
    with col3:
        if st.button("Analyze Targets"):
            st.info(" Navigate to 'Analyze Targets' page using the sidebar")
    
    with col4:
        if st.button(" Generate Report"):
            st.info(" Navigate to 'Generate Report' page using the sidebar")
    
    # Show sample companies if database connected
    if db_status and summary.get('latest'):
        st.markdown("---")
        st.subheader("Sample Companies in Database")
        
        for company in summary['latest']:
            with st.expander(f"🏢 {company['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Industry:** {company.get('industry', 'N/A')}")
                    st.write(f"**Location:** {company.get('headquarters', 'N/A')}")
                with col2:
                    st.write(f"**Founded:** {company.get('founded_year', 'N/A')}")
                    st.write(f"**Employees:** {company.get('employee_count', 'N/A'):,}" if company.get('employee_count') else "**Employees:** N/A")
    
    # Features overview (keep existing)
    st.markdown("---")
    st.subheader("🎯 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Document Intelligence
        - Upload pitch decks, 10-K filings, research reports
        - AI-powered text extraction and analysis
        - Semantic search across document database
        """)
        
        st.markdown("""
        ###  Goldman Sachs Integration
        - Industry-standard valuation methodologies
        - Professional financial modeling
        - Risk assessment frameworks
        """)
    
    with col2:
        st.markdown("""
        ### Custom AI Models
        - Acquisition fit scoring algorithms
        - Company similarity matching
        - Investment thesis generation
        """)
        
        st.markdown("""
        ### Advanced Analytics
        - Real-time market intelligence
        - Comparative deal analysis
        - Automated report generation
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit, LangChain, Supabase, and custom ML models*")

if __name__ == "__main__":
    main()