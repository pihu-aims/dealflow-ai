# 🎯 DealFlow AI - Intelligent M&A Target Discovery Platform

[![Python](https://img.shields.io/badge/Python-3.9.7-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.12.0-red.svg)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-2.17.0-green.svg)](https://supabase.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.0.350-purple.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Database Schema](#database-schema)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

DealFlow AI is a sophisticated M&A (Mergers & Acquisitions) target discovery platform that leverages artificial intelligence, real-time market data, and advanced document processing to identify, analyze, and evaluate potential acquisition targets. Built with modern technologies including Streamlit, LangChain, Supabase, and custom ML models.

### 🎯 Key Objectives

- **Intelligent Target Discovery**: AI-powered company search with semantic matching
- **Document Intelligence**: RAG (Retrieval-Augmented Generation) system for processing 10-K filings, pitch decks, and research reports
- **Real-Time Market Analysis**: Live market data integration with professional-grade analytics
- **Professional Reporting**: Automated generation of investment memos and due diligence reports
- **Goldman Sachs Integration**: Industry-standard valuation methodologies and risk assessment

## ✨ Features

### 🔍 Advanced Company Search
- **Semantic Search**: Natural language queries to find companies
- **Advanced Filters**: Industry, revenue, location, and growth stage filtering
- **Similar Company Discovery**: AI-powered similarity matching algorithms
- **Market Screening**: Real-time market cap and financial metrics filtering

### 📄 Document Intelligence System
- **Multi-Format Support**: PDF, DOCX, TXT document processing
- **AI-Powered Extraction**: Automatic text extraction and analysis
- **Semantic Search**: Query documents using natural language
- **Vector Database**: ChromaDB-powered document storage and retrieval

### 📊 Real-Time Market Data
- **Live Stock Prices**: Real-time market data via Alpha Vantage API
- **Financial Metrics**: P/E ratios, market cap, trading volumes
- **Market Sentiment**: AI-powered sentiment analysis
- **Historical Data**: Comprehensive historical price and volume data

### 📋 Professional Report Generation
- **Executive Summaries**: AI-generated investment summaries
- **Investment Memos**: Detailed investment thesis documents
- **Due Diligence Reports**: Comprehensive company analysis
- **Interactive Dashboards**: Professional visualizations with Plotly

### 🤖 AI & ML Capabilities
- **Custom ML Models**: Acquisition fit scoring algorithms
- **Embedding Models**: Sentence transformers for semantic search
- **Text Generation**: AI-powered content generation
- **Risk Assessment**: Automated risk scoring and analysis

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  LangChain RAG  │    │  Supabase DB    │
│                 │◄──►│                 │◄──►│                 │
│ • Multi-page    │    │ • Document      │    │ • Companies     │
│ • Interactive   │    │   Processing    │    │ • Documents     │
│ • Responsive    │    │ • Vector Store  │    │ • Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Models     │    │  Market Data    │    │  External APIs  │
│                 │    │                 │    │                 │
│ • Embeddings    │    │ • Alpha Vantage │    │ • Goldman Sachs │
│ • Text Gen      │    │ • yfinance      │    │ • OpenAI        │
│ • Transformers  │    │ • Real-time     │    │ • HuggingFace   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Frontend**: Streamlit 1.12.0 (Python 3.9.7 compatible)
- **Backend**: Python with FastAPI-style architecture
- **Database**: Supabase (PostgreSQL) with real-time capabilities
- **Vector Store**: ChromaDB for document embeddings
- **AI/ML**: LangChain, Transformers, Sentence Transformers
- **Market Data**: Alpha Vantage API, yfinance
- **Visualization**: Plotly, Altair, Matplotlib

## 🚀 Installation

### Prerequisites

- Python 3.9.7 (required for Streamlit 1.12.0 compatibility)
- pip package manager
- Git for version control
- Supabase account and project
- Alpha Vantage API key (free tier available)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/dealflow-ai.git
cd dealflow-ai
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Additional Requirements (if needed)

```bash
# For torch security fix (CVE-2025-32434)
pip install "torch>=2.6.0"

# For better performance
pip install watchdog
```

### Step 5: Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
python -c "import supabase; print('Supabase installed successfully')"
```

## ⚙️ Configuration

### 1. Supabase Setup

1. **Create Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note your project URL and anon key

2. **Database Tables**:
   ```sql
   -- Companies table
   CREATE TABLE companies (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     industry VARCHAR(100),
     revenue BIGINT,
     location VARCHAR(100),
     description TEXT,
     created_at TIMESTAMP DEFAULT NOW()
   );

   -- Documents table
   CREATE TABLE documents (
     id SERIAL PRIMARY KEY,
     company_id INTEGER REFERENCES companies(id),
     filename VARCHAR(255),
     content TEXT,
     document_type VARCHAR(50),
     uploaded_at TIMESTAMP DEFAULT NOW()
   );
   ```

### 2. Environment Configuration

Create `.streamlit/secrets.toml`:

```toml
# Supabase Configuration
[supabase]
url = "https://your-project-id.supabase.co"
key = "your-supabase-anon-key"

# OpenAI Configuration (optional)
[openai]
api_key = "your-openai-api-key"

# Alpha Vantage Configuration
[alpha_vantage]
api_key = "your-alpha-vantage-key"

# Goldman Sachs Configuration (optional)
[goldman_sachs]
client_id = "your-gs-client-id"
client_secret = "your-gs-client-secret"
```

### 3. API Keys Setup

#### Alpha Vantage (Free Tier)
1. Visit [alphavantage.co](https://www.alphavantage.co/support/#api-key)
2. Get free API key (500 requests/day)
3. Add to secrets.toml

#### OpenAI (Optional)
1. Visit [platform.openai.com](https://platform.openai.com/api-keys)
2. Create API key
3. Add to secrets.toml for enhanced AI features

## 🎮 Usage

### Starting the Application

```bash
cd dealflow-ai
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Core Workflows

#### 1. Document Upload & Processing
```python
# Navigate to "Upload Documents" page
# 1. Select PDF/DOCX files
# 2. Choose company association
# 3. Upload and process
# 4. Documents are automatically vectorized
```

#### 2. Company Search
```python
# Navigate to "Search Companies" page
# 1. Use natural language queries
# 2. Apply advanced filters
# 3. View similar companies
# 4. Export results
```

#### 3. Target Analysis
```python
# Navigate to "Analyze Targets" page
# 1. Select companies for analysis
# 2. Generate AI-powered insights
# 3. View market data and metrics
# 4. Create comparison reports
```

#### 4. Report Generation
```python
# Navigate to "Generate Report" page
# 1. Choose report type (Executive Summary, Investment Memo, Due Diligence)
# 2. Select target companies
# 3. Generate professional reports
# 4. Export as PDF/HTML
```

### Advanced Features

#### Semantic Search
```python
# Example queries:
"Find SaaS companies with recurring revenue models"
"Show me fintech startups in Series B funding"
"Companies similar to Stripe in payment processing"
```

#### Market Data Integration
```python
# Real-time data available for:
# - Stock prices and volumes
# - Market capitalization
# - P/E ratios and financial metrics
# - Historical performance data
```

## 🔌 API Integration

### Market Data APIs

#### Alpha Vantage Integration
```python
from src.market_data import MarketDataProvider

provider = MarketDataProvider()
data = provider.get_stock_data("AAPL")
```

#### yfinance Integration
```python
import yfinance as yf

ticker = yf.Ticker("MSFT")
info = ticker.info
history = ticker.history(period="1y")
```

### Database Operations

#### Supabase Queries
```python
from src.utils import init_supabase

supabase = init_supabase()
result = supabase.table('companies').select('*').execute()
```

#### Vector Store Operations
```python
from src.vector_store import VectorStore

vector_store = VectorStore()
results = vector_store.similarity_search("AI companies", k=5)
```

## 🗄️ Database Schema

### Companies Table
```sql
CREATE TABLE companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  industry VARCHAR(100),
  revenue BIGINT,
  location VARCHAR(100),
  description TEXT,
  website VARCHAR(255),
  employee_count INTEGER,
  funding_stage VARCHAR(50),
  market_cap BIGINT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Documents Table
```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  filename VARCHAR(255) NOT NULL,
  content TEXT,
  document_type VARCHAR(50),
  file_size INTEGER,
  upload_user VARCHAR(100),
  processing_status VARCHAR(20) DEFAULT 'pending',
  uploaded_at TIMESTAMP DEFAULT NOW()
);
```

### Analytics Table
```sql
CREATE TABLE analytics (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  metric_name VARCHAR(100),
  metric_value DECIMAL,
  metric_date DATE,
  data_source VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 🛠️ Development

### Project Structure
```
dealflow-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
├── .streamlit/
│   └── secrets.toml      # Configuration secrets
├── src/
│   ├── __init__.py
│   ├── utils.py          # Utility functions
│   ├── rag_system.py     # RAG implementation
│   ├── vector_store.py   # Vector database operations
│   ├── ai_models.py      # AI model management
│   ├── market_data.py    # Market data integration
│   ├── report_generator.py # Report generation
│   └── ml_models.py      # Custom ML models
├── pages/
│   ├── 1_📄_Upload_Documents.py
│   ├── 2_🔍_Search_Companies.py
│   ├── 3_📊_Analyze_Targets.py
│   └── 4_📋_Generate_Report.py
├── tests/
│   ├── __init__.py
│   ├── test_core_functionality.py
│   └── test_api_integration.py
└── data/
    ├── sample_companies.json
    └── mock_data/
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core_functionality.py

# Run with coverage
python -m pytest tests/ --cov=src/
```

### Code Quality
```bash
# Format code
black src/ pages/ tests/

# Lint code
flake8 src/ pages/ tests/

# Type checking
mypy src/
```

### Adding New Features

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Implement Feature**:
   - Add code to appropriate modules
   - Write comprehensive tests
   - Update documentation

3. **Test Thoroughly**:
   ```bash
   python -m pytest tests/
   streamlit run app.py  # Manual testing
   ```

4. **Submit Pull Request**:
   - Ensure all tests pass
   - Update README if needed
   - Request code review

## 🐛 Troubleshooting

### Common Issues

#### 1. Streamlit Version Compatibility
```bash
# Error: AttributeError: module 'streamlit' has no attribute 'switch_page'
# Solution: Using Streamlit 1.12.0 for Python 3.9.7 compatibility
pip install streamlit==1.12.0
```

#### 2. Torch Security Vulnerability
```bash
# Error: CVE-2025-32434 vulnerability in torch.load
# Solution: Upgrade torch
pip install "torch>=2.6.0"
```

#### 3. Supabase Connection Issues
```bash
# Error: Failed to initialize Supabase: Invalid URL
# Solution: Check secrets.toml configuration
# Ensure URL and key are correctly formatted
```

#### 4. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'altair.vegalite.v4'
# Solution: Downgrade Altair for compatibility
pip install "altair>=3.2.0,<5.0.0"
```

### Performance Optimization

#### 1. Caching Configuration
```python
# Use appropriate caching for different data types
@st.cache_data  # For data/DataFrames
@st.cache(allow_output_mutation=True)  # For objects (Streamlit 1.12.0)
```

#### 2. Database Query Optimization
```python
# Use indexed queries
supabase.table('companies').select('*').eq('industry', 'Technology').execute()

# Limit results for large datasets
supabase.table('companies').select('*').limit(100).execute()
```

#### 3. Vector Store Performance
```python
# Optimize embedding batch size
vector_store.add_documents(documents, batch_size=50)

# Use appropriate similarity search parameters
results = vector_store.similarity_search(query, k=10, score_threshold=0.7)
```

### Debugging Tips

#### 1. Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 2. Streamlit Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

#### 3. Database Connection Testing
```python
from src.utils import test_database_connection
success, message = test_database_connection()
print(f"Database status: {message}")
```

## 🤝 Contributing

We welcome contributions to DealFlow AI! Please follow these guidelines:

### Development Workflow

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature with tests
4. **Run Tests**: Ensure all tests pass
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push to Branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**: Submit PR with detailed description

### Code Standards

- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Add docstrings to all functions
- **Testing**: Write tests for new functionality
- **Type Hints**: Use type annotations where appropriate

### Reporting Issues

When reporting issues, please include:
- Python version and OS
- Streamlit version
- Complete error traceback
- Steps to reproduce
- Expected vs actual behavior

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team** - For the amazing web app framework
- **LangChain Community** - For RAG system capabilities
- **Supabase Team** - For the excellent database platform
- **HuggingFace** - For transformer models and embeddings
- **Alpha Vantage** - For real-time market data API
- **Open Source Community** - For the incredible tools and libraries

## 📞 Support

For support and questions:

- **Documentation**: Check this README and [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: contact@dealflow-ai.com (if applicable)

---

**Built with ❤️ by the DealFlow AI Team**

*Empowering intelligent M&A decisions through AI and data science.*
