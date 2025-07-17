from typing import List, Dict, Any, Optional
import os
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

class RAGSystem:
    """
    Retrieval-Augmented Generation (RAG) system for querying documents
    and generating insights about potential M&A targets.
    """
    
    def __init__(self, vector_db_path: str = "./data/vector_db"):
        """
        Initialize the RAG system.
        
        Args:
            vector_db_path: Path to the vector database
        """
        self.vector_db_path = vector_db_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    
    def get_vector_store(self, collection_name: str):
        """
        Get a vector store for a specific collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Chroma vector store
        """
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.vector_db_path
        )
    
    def query_documents(self, query: str, collection_name: str, k: int = 5) -> Dict[str, Any]:
        """
        Query documents in a collection and return relevant results.
        
        Args:
            query: The query string
            collection_name: Name of the collection to search
            k: Number of results to return
            
        Returns:
            Dictionary with query results
        """
        vector_store = self.get_vector_store(collection_name)
        results = vector_store.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": score
            })
        
        return {
            "query": query,
            "results": formatted_results
        }
    
    def generate_company_analysis(self, company_name: str, collection_name: str) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis of a company based on available documents.
        
        Args:
            company_name: Name of the company to analyze
            collection_name: Name of the collection to search
            
        Returns:
            Dictionary with analysis results
        """
        vector_store = self.get_vector_store(collection_name)
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        
        # Create analysis prompt
        analysis_prompt = PromptTemplate.from_template("""
        You are a financial analyst specializing in M&A target evaluation.
        Based on the provided documents about {company_name}, create a comprehensive analysis.
        
        Context documents:
        {context}
        
        Please provide the following analysis:
        1. Company Overview: Brief description of the company, its industry, and main products/services
        2. Financial Analysis: Key financial metrics, growth trends, and profitability
        3. Market Position: Competitive landscape, market share, and growth potential
        4. Strengths and Weaknesses: Key advantages and challenges
        5. Strategic Fit: How this company might fit as an acquisition target
        6. Risk Factors: Key risks to consider
        7. Valuation Considerations: Factors that might affect valuation
        
        Your analysis should be detailed, balanced, and backed by information from the documents.
        """)
        
        # Create document chain
        document_chain = create_stuff_documents_chain(self.llm, analysis_prompt)
        
        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Run the chain
        response = retrieval_chain.invoke({"company_name": company_name})
        
        return {
            "company_name": company_name,
            "analysis": response["answer"],
            "source_documents": response["context"]
        }
    
    def generate_investment_thesis(self, company_name: str, collection_name: str) -> Dict[str, str]:
        """
        Generate an investment thesis for a potential acquisition target.
        
        Args:
            company_name: Name of the company
            collection_name: Name of the collection to search
            
        Returns:
            Dictionary with the investment thesis
        """
        vector_store = self.get_vector_store(collection_name)
        retriever = vector_store.as_retriever(search_kwargs={"k": 8})
        
        # Create thesis prompt
        thesis_prompt = PromptTemplate.from_template("""
        You are an M&A advisor creating an investment thesis for acquiring {company_name}.
        Based on the provided documents, create a compelling investment thesis.
        
        Context documents:
        {context}
        
        Your investment thesis should include:
        1. Strategic Rationale: Why this acquisition makes strategic sense
        2. Value Creation: How this acquisition would create value
        3. Synergy Opportunities: Potential synergies (cost, revenue, operational)
        4. Integration Considerations: Key factors for successful integration
        5. ROI Projection: Expected return on investment and timeline
        
        Make your thesis concise, compelling, and supported by information from the documents.
        """)
        
        # Create document chain
        document_chain = create_stuff_documents_chain(self.llm, thesis_prompt)
        
        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Run the chain
        response = retrieval_chain.invoke({"company_name": company_name})
        
        return {
            "company_name": company_name,
            "investment_thesis": response["answer"]
        }
    
    def generate_due_diligence_questions(self, company_name: str, collection_name: str) -> Dict[str, Any]:
        """
        Generate due diligence questions for a potential acquisition target.
        
        Args:
            company_name: Name of the company
            collection_name: Name of the collection to search
            
        Returns:
            Dictionary with due diligence questions
        """
        vector_store = self.get_vector_store(collection_name)
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        # Create due diligence prompt
        dd_prompt = PromptTemplate.from_template("""
        You are an M&A due diligence specialist reviewing {company_name} as a potential acquisition target.
        Based on the provided documents, generate key due diligence questions.
        
        Context documents:
        {context}
        
        Generate 3-5 critical due diligence questions for each of these categories:
        1. Financial: Questions about financial statements, projections, and accounting practices
        2. Legal: Questions about legal issues, contracts, and compliance
        3. Operational: Questions about operations, supply chain, and key processes
        4. Commercial: Questions about customers, market position, and competitive landscape
        5. Technology: Questions about technology stack, IP, and technical capabilities
        6. Human Resources: Questions about team, culture, and organizational structure
        
        For each question, provide a brief explanation of why it's important to address.
        """)
        
        # Create document chain
        document_chain = create_stuff_documents_chain(self.llm, dd_prompt)
        
        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Run the chain
        response = retrieval_chain.invoke({"company_name": company_name})
        
        return {
            "company_name": company_name,
            "due_diligence_questions": response["answer"]
        }
