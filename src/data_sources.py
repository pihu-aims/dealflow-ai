import os
import json
import pandas as pd
import requests
from typing import List, Dict, Any, Optional
import streamlit as st

class DataSources:
    """Class for handling various data sources for company information."""
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize the DataSources class.
        
        Args:
            data_dir: Directory to store data
        """
        self.data_dir = data_dir
        self.sample_data_dir = os.path.join(data_dir, "sample_data")
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.sample_data_dir, exist_ok=True)
    
    def load_sample_companies(self) -> pd.DataFrame:
        """
        Load sample company data or create if it doesn't exist.
        
        Returns:
            DataFrame with sample company data
        """
        sample_file = os.path.join(self.sample_data_dir, "sample_companies.csv")
        
        if os.path.exists(sample_file):
            return pd.read_csv(sample_file)
        else:
            # Create sample data
            data = {
                "company_name": [
                    "TechInnovate Solutions", "GreenEnergy Systems", 
                    "HealthPlus Analytics", "FinSecure Technologies",
                    "DataMesh Networks", "CloudScale Infrastructure",
                    "BioGenetics Research", "SmartRetail Solutions",
                    "IndustrialAutomation Inc.", "CyberDefense Systems"
                ],
                "industry": [
                    "Software", "Renewable Energy", 
                    "Healthcare", "Financial Technology",
                    "Telecommunications", "Cloud Computing",
                    "Biotechnology", "Retail Technology",
                    "Manufacturing", "Cybersecurity"
                ],
                "revenue_millions": [
                    45.2, 78.5, 32.1, 65.8,
                    28.7, 92.3, 41.6, 53.9,
                    87.2, 39.5
                ],
                "employees": [
                    250, 420, 180, 310,
                    150, 480, 220, 290,
                    520, 210
                ],
                "founded_year": [
                    2015, 2010, 2017, 2012,
                    2018, 2011, 2016, 2014,
                    2008, 2019
                ],
                "headquarters": [
                    "San Francisco, CA", "Austin, TX", 
                    "Boston, MA", "New York, NY",
                    "Seattle, WA", "Denver, CO",
                    "Cambridge, MA", "Chicago, IL",
                    "Detroit, MI", "Raleigh, NC"
                ],
                "growth_rate": [
                    32.5, 28.7, 41.2, 24.8,
                    45.6, 22.3, 36.9, 19.7,
                    15.2, 38.4
                ]
            }
            
            df = pd.DataFrame(data)
            df.to_csv(sample_file, index=False)
            return df
    
    def search_companies(self, query: str, filters: Dict = None) -> pd.DataFrame:
        """
        Search for companies based on query and filters.
        
        Args:
            query: Search query
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with search results
        """
        # For now, just use the sample data
        df = self.load_sample_companies()
        
        if query:
            # Simple search across all string columns
            mask = df.apply(
                lambda row: any(
                    str(query).lower() in str(val).lower() 
                    for val in row if isinstance(val, str)
                ),
                axis=1
            )
            df = df[mask]
        
        if filters:
            # Apply filters
            for col, value in filters.items():
                if col in df.columns:
                    if isinstance(value, list) and len(value) == 2:  # Range filter
                        df = df[(df[col] >= value[0]) & (df[col] <= value[1])]
                    elif isinstance(value, str):  # String filter
                        df = df[df[col].str.contains(value, case=False, na=False)]
                    else:  # Exact match
                        df = df[df[col] == value]
        
        return df
    
    def get_company_details(self, company_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific company.
        
        Args:
            company_name: Name of the company
            
        Returns:
            Dictionary with company details
        """
        # For now, use the sample data
        df = self.load_sample_companies()
        company_data = df[df["company_name"] == company_name]
        
        if len(company_data) == 0:
            return {"error": f"Company '{company_name}' not found"}
        
        # Convert to dictionary
        company_dict = company_data.iloc[0].to_dict()
        
        # Add some additional mock data for demonstration
        company_dict["description"] = f"{company_name} is a leading provider in the {company_dict['industry']} industry, founded in {company_dict['founded_year']}."
        company_dict["key_products"] = ["Product A", "Product B", "Service C"]
        company_dict["competitors"] = ["Competitor 1", "Competitor 2", "Competitor 3"]
        company_dict["recent_news"] = [
            {"date": "2023-06-15", "title": f"{company_name} Announces New Product Line"},
            {"date": "2023-04-22", "title": f"{company_name} Reports Q1 Earnings"},
            {"date": "2023-02-10", "title": f"{company_name} Expands to European Market"}
        ]
        
        return company_dict
    
    def save_company_data(self, company_data: Dict[str, Any]) -> bool:
        """
        Save company data to the database.
        
        Args:
            company_data: Dictionary with company data
            
        Returns:
            Boolean indicating success
        """
        try:
            # For now, just append to the sample data
            df = self.load_sample_companies()
            
            # Check if company already exists
            if company_data["company_name"] in df["company_name"].values:
                # Update existing company
                df.loc[df["company_name"] == company_data["company_name"]] = company_data
            else:
                # Add new company
                df = pd.concat([df, pd.DataFrame([company_data])], ignore_index=True)
            
            # Save to CSV
            df.to_csv(os.path.join(self.sample_data_dir, "sample_companies.csv"), index=False)
            return True
        except Exception as e:
            st.error(f"Error saving company data: {str(e)}")
            return False
    
    def get_market_data(self, industry: str) -> Dict[str, Any]:
        """
        Get market data for a specific industry.
        
        Args:
            industry: Industry to get data for
            
        Returns:
            Dictionary with market data
        """
        # Mock market data
        market_data = {
            "industry": industry,
            "market_size_billions": round(50 + hash(industry) % 200, 1),
            "growth_rate": round(5 + hash(industry) % 20, 1),
            "top_players": [
                {"name": "Company A", "market_share": round(10 + hash("A" + industry) % 30, 1)},
                {"name": "Company B", "market_share": round(10 + hash("B" + industry) % 25, 1)},
                {"name": "Company C", "market_share": round(5 + hash("C" + industry) % 20, 1)},
                {"name": "Company D", "market_share": round(5 + hash("D" + industry) % 15, 1)},
                {"name": "Others", "market_share": round(10 + hash("Others" + industry) % 30, 1)}
            ],
            "trends": [
                "Digital transformation accelerating adoption",
                "Increasing focus on sustainability",
                "Rising competition from startups",
                "Consolidation through M&A activity"
            ]
        }
        
        return market_data
