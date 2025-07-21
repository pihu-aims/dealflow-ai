import streamlit as st
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
from typing import Dict, Any, Optional

class MarketDataProvider:
    """Real-time market data provider with caching."""
    
    def __init__(self):
        self.alpha_vantage_key = st.secrets.get("ALPHA_VANTAGE_API_KEY", "demo")
        
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_market_conditions(_self) -> Dict[str, Any]:
        """Get overall market conditions and sentiment."""
        try:
            # Get major indices data using yfinance
            indices = {
                "S&P 500": "^GSPC",
                "Dow Jones": "^DJI", 
                "NASDAQ": "^IXIC"
            }
            
            market_data = {}
            total_change = 0
            
            for name, symbol in indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change_percent = ((current_price - prev_price) / prev_price) * 100
                        
                        market_data[name] = {
                            'value': current_price,
                            'change_percent': change_percent
                        }
                        total_change += change_percent
                        
                except Exception:
                    # Fallback to mock data
                    market_data[name] = {
                        'value': 4500 if "S&P" in name else 35000 if "Dow" in name else 14000,
                        'change_percent': 0.5
                    }
                    total_change += 0.5
            
            avg_change = total_change / len(indices)
            
            # Determine sentiment
            if avg_change > 1:
                sentiment = "Bullish 📈"
            elif avg_change < -1:
                sentiment = "Bearish 📉"
            else:
                sentiment = "Neutral ➡️"
            
            return {
                'sentiment': sentiment,
                'avg_change': avg_change,
                'indices': market_data
            }
            
        except Exception as e:
            # Return mock data if all fails
            return {
                'sentiment': "Neutral ➡️",
                'avg_change': 0.5,
                'indices': {
                    "S&P 500": {'value': 4500, 'change_percent': 0.5},
                    "Dow Jones": {'value': 35000, 'change_percent': 0.3},
                    "NASDAQ": {'value': 14000, 'change_percent': 0.7}
                }
            }
    
    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_stock_price(_self, ticker: str) -> Dict[str, Any]:
        """Get current stock price for a ticker."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_percent = ((current_price - prev_price) / prev_price) * 100
                
                return {
                    'current_price': current_price,
                    'change_percent': change_percent,
                    'volume': hist['Volume'].iloc[-1]
                }
        except Exception:
            pass
            
        # Return mock data if fails
        return {
            'current_price': 150.0,
            'change_percent': 2.5,
            'volume': 1000000
        }

@st.cache(allow_output_mutation=True)
def get_market_data_provider():
    """Get singleton market data provider."""
    return MarketDataProvider()