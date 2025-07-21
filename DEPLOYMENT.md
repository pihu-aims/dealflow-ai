# DealFlow AI - Deployment Guide

## Overview
This guide covers deploying DealFlow AI to Streamlit Cloud and other production environments.

## Prerequisites
- Python 3.9.7+
- Streamlit 1.12.0+
- All dependencies from requirements.txt
- API keys for external services

## Streamlit Cloud Deployment

### 1. Repository Setup
```bash
git add .
git commit -m "Deploy DealFlow AI v2.0"
git push origin main
```

### 2. Streamlit Cloud Configuration
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Select branch: `main`
4. Main file path: `app.py`

### 3. Environment Variables
Configure the following secrets in Streamlit Cloud:

```toml
# .streamlit/secrets.toml
[supabase]
url = "your_supabase_url"
key = "your_supabase_anon_key"

[openai]
api_key = "your_openai_api_key"

[alpha_vantage]
api_key = "your_alpha_vantage_api_key"
```

### 4. Required API Keys

#### Supabase (Database)
- Sign up at [supabase.com](https://supabase.com)
- Create new project
- Get URL and anon key from Settings > API

#### OpenAI (AI Models)
- Sign up at [platform.openai.com](https://platform.openai.com)
- Generate API key from API Keys section
- Ensure sufficient credits for GPT-4 usage

#### Alpha Vantage (Market Data)
- Sign up at [alphavantage.co](https://www.alphavantage.co)
- Get free API key (500 requests/day)
- Premium plans available for higher limits

## Local Development

### 1. Environment Setup
```bash
# Clone repository
git clone <your-repo-url>
cd dealflow-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Create secrets file
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit with your actual API keys
```

### 3. Run Application
```bash
streamlit run app.py
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9.7-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
docker build -t dealflow-ai .
docker run -p 8501:8501 dealflow-ai
```

## Production Considerations

### 1. Security
- Use environment variables for all secrets
- Enable HTTPS in production
- Implement rate limiting
- Regular security updates

### 2. Performance
- Enable Streamlit caching
- Optimize database queries
- Use CDN for static assets
- Monitor resource usage

### 3. Monitoring
- Set up application logging
- Monitor API usage and costs
- Track user analytics
- Set up alerts for errors

### 4. Backup & Recovery
- Regular database backups
- Version control for code
- Document recovery procedures
- Test backup restoration

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9.7+
```

#### API Key Issues
- Verify all API keys are correctly set
- Check API key permissions and limits
- Monitor API usage quotas

#### Database Connection
- Verify Supabase URL and key
- Check network connectivity
- Review database permissions

### Performance Issues
- Enable Streamlit caching
- Optimize database queries
- Monitor memory usage
- Check API response times

## Support
For deployment issues, contact the development team or create an issue in the repository.

## Version History
- v2.0.0: Enhanced search, real-time market data, professional reports
- v1.0.0: Initial release with basic functionality
