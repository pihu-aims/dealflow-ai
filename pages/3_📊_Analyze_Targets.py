# Add this to the end of the run_complete_analysis function:

# Report generation section
st.markdown("---")
st.subheader("📋 Professional Investment Report")

col1, col2 = st.columns([2, 1])

with col1:
    report_type = st.selectbox(
        "Report Type",
        ["Executive Summary", "Full Investment Memo", "Due Diligence Report"]
    )
    
    include_charts = st.checkbox("Include Charts & Visualizations", value=True)
    include_appendix = st.checkbox("Include Technical Appendix", value=True)

with col2:
    if st.button("📄 Generate Report", type="primary"):
        generate_professional_report(
            company_name, company_financials, ml_result, 
            dcf_result, risk_result, report_type
        )

def generate_professional_report(company_name, financials, ml_result, dcf_result, risk_result, report_type):
    """Generate and display professional investment report."""
    
    from src.report_generator import get_report_generator
    
    report_gen = get_report_generator()
    
    # Prepare analysis data
    analysis_data = {
        'company_name': company_name,
        'industry': 'Technology',  # Would be actual data
        'revenue': financials['revenue'] / 1_000_000,
        'employees': financials['employee_count'],
        'ml_probability': ml_result.get('success_probability', 0.75),
        'ml_confidence': ml_result.get('confidence', 'High'),
        'dcf_value': dcf_result.get('enterprise_value', 500_000_000) / 1_000_000,
        'dcf_per_share': dcf_result.get('dcf_per_share', 50),
        'wacc': dcf_result.get('wacc', 0.12),
        'risk_level': risk_result.get('risk_level', 'Medium'),
        'risk_factors': risk_result.get('risk_factors', []),
        'recommendation': 'BUY',  # Would be calculated
        'revenue_multiple': 4.5,  # Would be calculated
        'growth_rate': financials.get('growth_rate', 0.25),
        'ebitda_margin': financials.get('ebitda_margin', 0.20)
    }
    
    # Create dashboard
    report_gen.create_dashboard_summary(analysis_data)
    
    # Generate report text
    with st.spinner("📝 Generating professional report..."):
        report_markdown = report_gen.generate_investment_memo(analysis_data)
    
    # Display report
    st.markdown("---")
    st.subheader(f"📄 {report_type}")
    
    # Report content in expandable section
    with st.expander("📖 View Full Report", expanded=True):
        st.markdown(report_markdown)
    
    # Download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📥 Download Markdown",
            data=report_markdown,
            file_name=f"{company_name.replace(' ', '_')}_investment_memo.md",
            mime="text/markdown"
        )
    
    with col2:
        # Convert to text for simple download
        text_report = report_markdown.replace('#', '').replace('*', '')
        st.download_button(
            label="📥 Download Text",
            data=text_report,
            file_name=f"{company_name.replace(' ', '_')}_report.txt",
            mime="text/plain"
        )
    
    with col3:
        if st.button("📧 Email Report"):
            st.success("📧 Email functionality coming soon!")
    
    st.success("✅ Professional investment report generated successfully!")