import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Search Companies", page_icon="🔍")

st.title("🔍 Search & Compare Companies")
st.markdown("*Find potential acquisition targets based on industry, size, and financial metrics.*")

st.info("🚧 Coming Soon: Full company search and comparison functionality")

# Create sample data for demonstration
def generate_sample_companies():
    industries = ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail"]
    companies = [
        {"name": "TechCorp Solutions", "industry": "Technology", "revenue": 45, "valuation": 320},
        {"name": "MediHealth Inc", "industry": "Healthcare", "revenue": 78, "valuation": 560},
        {"name": "FinServe Capital", "industry": "Finance", "revenue": 112, "valuation": 890},
        {"name": "Industrial Systems", "industry": "Manufacturing", "revenue": 67, "valuation": 410},
        {"name": "RetailGiant", "industry": "Retail", "revenue": 93, "valuation": 640}
    ]
    return pd.DataFrame(companies)

# Display sample search interface
st.subheader("🔎 Search Filters")
col1, col2 = st.columns(2)

with col1:
    industry = st.selectbox("Industry", ["All Industries", "Technology", "Healthcare", "Finance", "Manufacturing", "Retail"])
    min_revenue = st.slider("Min Revenue ($M)", 0, 200, 25)

with col2:
    keyword = st.text_input("Keyword", placeholder="e.g., AI, cloud, platform")
    max_valuation = st.slider("Max Valuation ($M)", 100, 1000, 500)

st.button("Search Companies", type="primary")

# Display sample results
st.subheader("📈 Sample Results")
df = generate_sample_companies()
st.dataframe(df, use_container_width=True)

# Sample comparison chart
st.subheader("📉 Company Comparison")
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.caption("Revenue Comparison ($M)")
    st.bar_chart(df.set_index('name')['revenue'])

with fig_col2:
    st.caption("Valuation Comparison ($M)")
    st.bar_chart(df.set_index('name')['valuation'])

if st.button("← Back to Home"):
    st.switch_page("app.py")
