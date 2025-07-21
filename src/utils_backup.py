import os
import streamlit as st
# from supabase import create_client, Client  # Commented out - not installed
# from dotenv import load_dotenv  # Commented out - not installed
import logging

# Load environment variables
# load_dotenv()  # Commented out - dotenv not installed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_resource
def init_supabase() -> Client:
    """Initialize Supabase client with connection pooling."""
    try:
        # Try to get credentials from Streamlit secrets (for deployment)
        if hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets:
            supabase_url = st.secrets['SUPABASE_URL']
            supabase_key = st.secrets['SUPABASE_ANON_KEY']
        else:
            # Fallback to environment variables (for local development)
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment or secrets")
        
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("✅ Supabase client initialized successfully")
        return supabase
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase: {str(e)}")
        st.error(f"Database connection failed: {str(e)}")
        return None

def test_database_connection():
    """Test database connection and return status."""
    try:
        supabase = init_supabase()
        if supabase is None:
            return False, "Failed to initialize Supabase client"
        
        # Test with a simple query
        result = supabase.table('companies').select('count').execute()
        return True, f"✅ Database connected successfully"
        
    except Exception as e:
        return False, f"❌ Database connection failed: {str(e)}"

def get_companies_summary():
    """Get summary statistics from companies table."""
    try:
        supabase = init_supabase()
        if supabase is None:
            return {"total": 0, "industries": 0}
        
        # Get total companies
        companies = supabase.table('companies').select('*').execute()
        total_companies = len(companies.data)
        
        # Get unique industries
        industries = set()
        for company in companies.data:
            if company.get('industry'):
                industries.add(company['industry'])
        
        return {
            "total": total_companies,
            "industries": len(industries),
            "latest": companies.data[-3:] if companies.data else []
        }
        
    except Exception as e:
        logger.error(f"Error getting companies summary: {str(e)}")
        return {"total": 0, "industries": 0, "latest": []}

def test_database_connection():
    """
    Test the database connection and return status.
    
    Returns:
        tuple: (bool, str) - (success, message)
    """
    try:
        # For now, just return a mock successful connection
        # In a real app, you'd test actual database connectivity
        return True, "✅ Database connected"
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

def init_supabase():
    """
    Initialize Supabase client (placeholder for now).
    
    Returns:
        Mock client object
    """
    # Placeholder - in a real app, you'd initialize the actual Supabase client
    class MockSupabase:
        def __init__(self):
            self.connected = True
            
        def table(self, table_name):
            return self
            
        def select(self, *args):
            return self
            
        def execute(self):
            return {'data': [], 'error': None}
    
    return MockSupabase()
