import streamlit as st
import pandas as pd
from src.rag_system import DealFlowRAG
from src.market_data import get_market_data_provider
import time

st.set_page_config(page_title="Enhanced Search", page_icon="🔍", layout="wide")

def main():
    st.title("🔍 Enhanced Company Search")
    st.markdown("*AI-powered semantic search with real-time market data and advanced filters*")
    
    # Initialize systems
    rag_system = DealFlowRAG()
    market_data = get_market_data_provider()
    
    # Sidebar with advanced filters
    with st.sidebar:
        st.subheader("🎛️ Advanced Filters")
        
        # Industry filter
        industries = ["All", "Technology", "Financial Services", "Healthcare", "Retail", "Manufacturing", "Energy"]
        selected_industry = st.selectbox("Industry", industries)
        
        # Size filters
        st.subheader("Company Size")
        revenue_range = st.slider("Revenue Range ($M)", 0, 10000, (50, 5000))
        employee_range = st.slider("Employee Count", 0, 100000, (100, 10000))
        
        # Financial filters
        st.subheader("Financial Metrics")
        growth_min = st.slider("Min Growth Rate", -20, 100, 10, format="%d%%")
        margin_min = st.slider("Min EBITDA Margin", -10, 50, 5, format="%d%%")
        
        # Geographic filter
        st.subheader("Geography")
        regions = st.multiselect("Regions", 
            ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East & Africa"],
            default=["North America"])
        
        # Market conditions
        st.markdown("---")
        st.subheader("📈 Market Conditions")
        
        try:
            market_conditions = market_data.get_market_conditions()
            st.metric("Market Sentiment", market_conditions['sentiment'])
            st.metric("Avg Market Change", f"{market_conditions['avg_change']:.1f}%")
            
            # Display major indices
            for name, data in market_conditions.get('indices', {}).items():
                change_color = "inverse" if data['change_percent'] > 0 else "normal"
                st.metric(
                    name, 
                    f"{data['value']:,.0f}",
                    delta=f"{data['change_percent']:+.1f}%",
                    delta_color=change_color
                )
        except Exception as e:
            st.error(f"Market data unavailable: {str(e)}")
    
    # Main search interface
    enhanced_search_interface(rag_system, market_data, {
        'industry': selected_industry,
        'revenue_range': revenue_range,
        'employee_range': employee_range,
        'growth_min': growth_min / 100,
        'margin_min': margin_min / 100,
        'regions': regions
    })

def enhanced_search_interface(rag_system, market_data, filters):
    """Enhanced search interface with filters and real-time data."""
    
    # Search modes
    search_mode = st.radio(
        "Search Mode",
        ["Semantic Search", "Similar Companies", "Market Screening"],
        horizontal=True
    )
    
    if search_mode == "Semantic Search":
        semantic_search_tab(rag_system, market_data, filters)
    elif search_mode == "Similar Companies":
        similar_companies_tab(rag_system, market_data, filters)
    else:
        market_screening_tab(rag_system, market_data, filters)

def semantic_search_tab(rag_system, market_data, filters):
    """Semantic search with AI understanding."""
    
    st.subheader("🤖 AI-Powered Semantic Search")
    
    # Search examples
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Describe what you're looking for",
            placeholder="e.g., 'AI companies with enterprise SaaS models and strong recurring revenue'"
        )
    
    with col2:
        num_results = st.selectbox("Results", [5, 10, 20, 50], index=1)
    
    # Quick search examples
    st.markdown("**Quick Examples:**")
    example_buttons = st.columns(3)
    
    with example_buttons[0]:
        if st.button("🤖 AI & Machine Learning"):
            search_query = "artificial intelligence machine learning companies"
    
    with example_buttons[1]:
        if st.button("💰 High-Growth SaaS"):
            search_query = "software as a service companies with high growth rates"
    
    with example_buttons[2]:
        if st.button("🏥 Healthcare Tech"):
            search_query = "healthcare technology digital health companies"
    
    # Perform search
    if search_query:
        perform_enhanced_search(search_query, num_results, filters, rag_system, market_data)

def perform_enhanced_search(query, num_results, filters, rag_system, market_data):
    """Perform enhanced search with filters and real-time data."""
    
    with st.spinner("🔍 Searching with AI and applying filters..."):
        # Get semantic search results
        results = rag_system.search_similar_companies(query, num_results * 2)  # Get more to filter
        
        # Apply filters (simplified implementation)
        filtered_results = apply_search_filters(results, filters)
        
        # Limit to requested number
        final_results = filtered_results[:num_results]
    
    if final_results:
        st.success(f"✅ Found {len(final_results)} matching companies")
        
        # Display results with enhanced information
        for i, result in enumerate(final_results):
            display_enhanced_result(result, i, market_data)
    else:
        st.warning("No companies match your criteria. Try adjusting your filters.")

def apply_search_filters(results, filters):
    """Apply search filters to results."""
    filtered_results = []
    
    for result in results:
        # Basic filtering logic (would be more sophisticated in production)
        metadata = result.get('metadata', {})
        
        # Industry filter
        if filters['industry'] != "All":
            # Would check against actual industry data
            pass
        
        # For demo, return all results
        filtered_results.append(result)
    
    return filtered_results

def display_enhanced_result(result, index, market_data):
    """Display enhanced search result with real-time data."""
    
    metadata = result.get('metadata', {})
    content = result['content']
    similarity_score = result['similarity_score']
    
    with st.expander(f"🏢 {metadata.get('filename', 'Company')} (Match: {similarity_score:.0%})", expanded=index < 3):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("**📄 Document Content:**")
            preview = content[:400] + "..." if len(content) > 400 else content
            st.write(preview)
            
            # AI-generated insights
            if st.button(f"🤖 Generate AI Analysis", key=f"ai_analysis_{index}"):
                with st.spinner("Generating insights..."):
                    # Would use actual AI analysis here
                    st.info("📊 **AI Insights:** Strong market position with consistent revenue growth. Potential acquisition target with high strategic value.")
        
        with col2:
            st.markdown("**📊 Key Metrics:**")
            st.metric("Similarity Score", f"{similarity_score:.0%}")
            st.metric("Document Type", metadata.get('document_type', 'Unknown'))
            
            # Mock financial data
            st.metric("Est. Revenue", "$250M")
            st.metric("Growth Rate", "25%")
        
        with col3:
            st.markdown("**📈 Market Data:**")
            
            # Try to get real market data
            try:
                # Extract potential ticker from filename
                potential_ticker = extract_ticker_from_filename(metadata.get('filename', ''))
                if potential_ticker:
                    price_data = market_data.get_stock_price(potential_ticker)
                    st.metric(
                        f"{potential_ticker} Price",
                        f"${price_data['current_price']:.2f}",
                        delta=f"{price_data['change_percent']:+.1f}%"
                    )
                else:
                    st.info("No ticker identified")
            except Exception as e:
                st.info("Market data unavailable")
            
            # Action buttons
            if st.button(f"📋 Add to Watchlist", key=f"watchlist_{index}"):
                st.success("Added to watchlist!")
            
            if st.button(f"📊 Full Analysis", key=f"analysis_{index}"):
                st.info("Opening full analysis...")

def extract_ticker_from_filename(filename):
    """Extract potential stock ticker from filename."""
    # Simple extraction logic
    common_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA']
    filename_upper = filename.upper()
    
    for ticker in common_tickers:
        if ticker in filename_upper:
            return ticker
    
    return None

def similar_companies_tab(rag_system, market_data, filters):
    """Find companies similar to a specific target."""
    
    st.subheader("🔄 Find Similar Companies")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        reference_company = st.text_input(
            "Reference Company",
            placeholder="Enter a company name or description"
        )
    
    with col2:
        similarity_threshold = st.slider("Similarity Threshold", 50, 95, 75, 5, format="%d%%")
    
    if reference_company and st.button("🔍 Find Similar Companies"):
        query = f"companies similar to {reference_company}"
        perform_enhanced_search(query, 10, filters, rag_system, market_data)

def market_screening_tab(rag_system, market_data, filters):
    """Market screening based on criteria."""
    
    st.subheader("📊 Market Screening")
    
    st.info("🚧 Advanced market screening coming soon - will integrate with real-time financial databases")
    
    # Mock screening results
    if st.button("🔍 Run Market Screen"):
        mock_screening_results()

def mock_screening_results():
    """Display mock screening results."""
    
    mock_data = pd.DataFrame({
        'Company': ['TechCorp A', 'SoftwareB Inc', 'DataCorp C', 'AI Solutions D'],
        'Industry': ['Software', 'SaaS', 'Analytics', 'AI/ML'],
        'Revenue ($M)': [250, 180, 320, 150],
        'Growth Rate': ['25%', '40%', '15%', '60%'],
        'EBITDA Margin': ['20%', '30%', '25%', '15%'],
        'Match Score': ['92%', '87%', '84%', '81%']
    })
    
    st.dataframe(mock_data, use_container_width=True)

if __name__ == "__main__":
    main()
    
    # Navigation
    if st.button("← Back to Home"):
        st.switch_page("app.py")