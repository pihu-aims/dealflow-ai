from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import streamlit as st
import logging
from typing import List, Dict, Optional
from src.ai_models import AIModelManager
from src.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Handle supabase import gracefully
try:
    from src.utils import init_supabase
except ImportError:
    def init_supabase():
        logger.warning("Supabase not available - using mock database")
        return None

class DealFlowRAG:
    def __init__(self):
        self.ai_manager = AIModelManager()
        self.vector_store = VectorStore()
        self.supabase = init_supabase()
        
        # Text splitter for chunking documents (Video 11)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_and_embed_documents(self) -> bool:
        """Process all documents from database and create embeddings."""
        try:
            if self.supabase is None:
                raise Exception("Database not connected")
            
            # Get all processed documents from database
            result = self.supabase.table('documents')\
                .select('*')\
                .eq('processed', True)\
                .execute()
            
            if not result.data:
                logger.info("No documents found to process")
                return True
            
            all_chunks = []
            all_embeddings = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, doc in enumerate(result.data):
                status_text.text(f"Processing document {i+1}/{len(result.data)}: {doc['filename']}")
                
                # Split document into chunks (Video 11)
                text = doc.get('extracted_text', '')
                if not text:
                    continue
                
                # Create LangChain documents
                langchain_doc = Document(
                    page_content=text,
                    metadata={
                        'filename': doc['filename'],
                        'document_id': doc['id'],
                        'company_id': doc.get('company_id')
                    }
                )
                
                # Split into chunks
                chunks = self.text_splitter.split_documents([langchain_doc])
                
                # Prepare chunk data
                for chunk in chunks:
                    chunk_data = {
                        'text': chunk.page_content,
                        'company_name': 'Unknown',  # We'll enhance this later
                        'document_type': doc['file_type'],
                        'filename': doc['filename'],
                        'document_id': doc['id']
                    }
                    all_chunks.append(chunk_data)
                
                progress_bar.progress((i + 1) / len(result.data))
            
            # Generate embeddings for all chunks
            if all_chunks:
                status_text.text("🤖 Generating AI embeddings...")
                
                chunk_texts = [chunk['text'] for chunk in all_chunks]
                embeddings = self.ai_manager.generate_embeddings(chunk_texts)
                
                if embeddings:
                    # Add to vector store
                    status_text.text("💾 Saving to vector database...")
                    success = self.vector_store.add_documents(all_chunks, embeddings)
                    
                    if success:
                        status_text.text("✅ All documents processed successfully!")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            st.error(f"Error: {str(e)}")
            return False
        
        finally:
            # Clean up progress indicators
            if 'progress_bar' in locals():
                progress_bar.empty()
            if 'status_text' in locals():
                status_text.empty()
    
    def search_similar_companies(self, query: str, n_results: int = 5) -> Optional[List[Dict]]:
        """Search for similar companies based on query."""
        try:
            # Generate embedding for query
            query_embedding = self.ai_manager.generate_embeddings([query])
            if not query_embedding:
                raise Exception("Failed to generate query embedding")
            
            # Search vector store
            results = self.vector_store.similarity_search(
                query_embedding[0], 
                n_results=n_results
            )
            
            if not results:
                return []
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                result = {
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'filename': results['metadatas'][0][i].get('filename', 'Unknown')
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
    
    def generate_investment_analysis(self, company_info: str, similar_companies: List[Dict]) -> str:
        """Generate investment analysis using AI."""
        try:
            # Construct analysis prompt
            prompt = f"""
            Analyze this company for potential acquisition:
            
            Company Information:
            {company_info[:500]}
            
            Similar Companies Found:
            """
            
            for comp in similar_companies[:3]:  # Limit to top 3
                prompt += f"- {comp['filename']}: {comp['content'][:200]}...\n"
            
            prompt += """
            
            Based on this information, provide:
            1. Investment Thesis (2-3 sentences)
            2. Key Strengths (3 bullet points)
            3. Potential Risks (2 bullet points)
            4. Acquisition Recommendation (Buy/Hold/Pass)
            """
            
            # Generate analysis using AI
            analysis = self.ai_manager.generate_text(prompt, max_length=400)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating investment analysis: {str(e)}")
            return "Error generating analysis. Please try again."
    
    def get_rag_stats(self) -> Dict:
        """Get RAG system statistics."""
        return {
            "vector_store": self.vector_store.get_collection_stats(),
            "ai_models": {
                "embedding_model": "✅ Loaded" if self.ai_manager.embedding_model else "❌ Not loaded",
                "text_generator": "✅ Loaded" if self.ai_manager.text_generator else "❌ Not loaded"
            }
        }