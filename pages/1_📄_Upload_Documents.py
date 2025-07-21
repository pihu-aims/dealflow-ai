import streamlit as st
import pandas as pd
from src.document_processor import DocumentProcessor
from src.utils import get_companies_summary
import time

st.set_page_config(page_title="Upload Documents", page_icon="📄", layout="wide")

# Initialize document processor
doc_processor = DocumentProcessor()

def main():
    st.title("📄 Upload Company Documents")
    st.markdown("Upload pitch decks, 10-K filings, and research reports to build your company database.")
    
    # Check database connection
    if doc_processor.supabase is None:
        st.error("⚠️ Database connection failed. Please check configuration.")
        return
    
    # File uploader
    st.subheader("📁 Upload Documents")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'txt'],
            help="Supported formats: PDF, TXT (Max 200MB per file)"
        )
    
    with col2:
        # Optional company name
        company_name = st.text_input(
            "Company Name (Optional)",
            help="Link this document to a specific company"
        )
    
    # Process uploaded files
    if uploaded_files:
        st.subheader(f"📋 Processing {len(uploaded_files)} file(s)...")
        
        for i, uploaded_file in enumerate(uploaded_files):
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**File size:** {uploaded_file.size:,} bytes")
                    st.write(f"**File type:** {uploaded_file.type}")
                    if company_name:
                        st.write(f"**Company:** {company_name}")
                
                with col2:
                    if st.button(f"Process Document", key=f"process_{i}"):
                        process_document(uploaded_file, company_name)

def process_document(uploaded_file, company_name):
    """Process a single document with progress indicators."""
    try:
        # Show processing steps
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Extract text
        status_text.text("📄 Extracting text from document...")
        progress_bar.progress(25)
        time.sleep(0.5)  # Small delay for UX
        
        # Step 2: Process with AI
        status_text.text("🤖 Processing with AI...")
        progress_bar.progress(50)
        
        # Process document
        result = doc_processor.process_document(uploaded_file, company_name)
        progress_bar.progress(75)
        
        # Step 3: Save to database
        status_text.text("💾 Saving to database...")
        progress_bar.progress(100)
        
        # Show results
        if result['success']:
            st.success("✅ Document processed successfully!")
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", f"{result['word_count']:,}")
            with col2:
                st.metric("Characters", f"{result['text_length']:,}")
            with col3:
                st.metric("Document ID", result['document_id'])
            
            # Show preview
            if result.get('summary'):
                st.markdown("**Summary:**")
                st.info(result['summary'])
                
        else:
            st.error(f"❌ Error processing document: {result['error']}")
            
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
    
    finally:
        # Clean up progress indicators
        progress_bar.empty()
        status_text.empty()

# Display recent uploads
def show_recent_uploads():
    st.markdown("---")
    st.subheader("📋 Recent Uploads")
    
    try:
        recent_docs = doc_processor.get_recent_documents(10)
        
        if recent_docs:
            # Convert to DataFrame for better display
            df_data = []
            for doc in recent_docs:
                df_data.append({
                    'Filename': doc['filename'],
                    'Upload Date': doc['upload_date'][:10],  # Just date part
                    'Status': '✅ Processed' if doc['processed'] else '⏳ Processing',
                    'Size': f"{doc.get('file_size', 0):,} bytes",
                    'Words': doc.get('key_metrics', {}).get('word_count', 'N/A')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
        else:
            st.info("No documents uploaded yet. Upload your first document above!")
            
    except Exception as e:
        st.error(f"Error loading recent uploads: {str(e)}")

# Sidebar with stats
def show_sidebar_stats():
    with st.sidebar:
        st.title("📊 Database Stats")
        
        # Get company summary
        summary = get_companies_summary()
        
        st.metric("Total Companies", summary.get('total', 0))
        st.metric("Industries", summary.get('industries', 0))
        
        # Show latest companies
        if summary.get('latest'):
            st.markdown("**Latest Companies:**")
            for company in summary['latest']:
                st.write(f"• {company['name']}")

if __name__ == "__main__":
    show_sidebar_stats()
    main()
    show_recent_uploads()
    
    # Navigation
    if st.button("← Back to Home"):
        st.switch_page("app.py")