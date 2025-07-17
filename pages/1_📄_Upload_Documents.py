import streamlit as st

st.set_page_config(page_title="Upload Documents", page_icon="📄")

st.title("📄 Upload Company Documents")
st.markdown("*Upload pitch decks, 10-K filings, and research reports to build your company database.*")

st.info("🚧 Coming Soon: Document upload and processing functionality")

# Placeholder for future functionality
st.subheader("📋 Planned Features")
st.write("- Drag & drop file upload")
st.write("- PDF text extraction") 
st.write("- Document chunking and embedding")
st.write("- Vector database storage")

if st.button("← Back to Home"):
    st.switch_page("app.py")
