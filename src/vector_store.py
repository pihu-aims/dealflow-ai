import chromadb
import streamlit as st
import logging
from typing import List, Dict, Optional
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)

@st.cache(allow_output_mutation=True)
def init_chroma_client():
    """Initialize ChromaDB client with persistent storage."""
    try:
        # Create data directory if it doesn't exist
        db_path = Path("data/vector_db")
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        client = chromadb.PersistentClient(path=str(db_path))
        logger.info("✅ ChromaDB client initialized successfully")
        return client
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize ChromaDB: {str(e)}")
        return None

class VectorStore:
    def __init__(self):
        self.client = init_chroma_client()
        self.collection_name = "company_documents"
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get existing collection."""
        try:
            if self.client is None:
                raise Exception("ChromaDB client not initialized")
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Company documents and embeddings for similarity search"}
            )
            logger.info(f"✅ Collection '{self.collection_name}' ready")
            
        except Exception as e:
            logger.error(f"Error initializing collection: {str(e)}")
            self.collection = None
    
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """Add documents with embeddings to vector store."""
        try:
            if self.collection is None:
                raise Exception("Collection not initialized")
            
            # Prepare data for ChromaDB
            ids = [str(uuid.uuid4()) for _ in documents]
            texts = [doc.get('text', '') for doc in documents]
            metadatas = [
                {
                    'company_name': doc.get('company_name', 'Unknown'),
                    'document_type': doc.get('document_type', 'Unknown'),
                    'filename': doc.get('filename', 'Unknown'),
                    'document_id': str(doc.get('document_id', ''))
                }
                for doc in documents
            ]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✅ Added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    def similarity_search(self, query_embedding: List[float], n_results: int = 5) -> Optional[Dict]:
        """Search for similar documents using vector similarity."""
        try:
            if self.collection is None:
                raise Exception("Collection not initialized")
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return None
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store."""
        try:
            if self.collection is None:
                return {
                    "total_documents": 0, 
                    "total_embeddings": 0,
                    "collections": 1,
                    "status": "Not initialized"
                }
            
            count = self.collection.count()
            return {
                "total_documents": count,
                "total_embeddings": count,  # Each document has one embedding
                "collections": 1,
                "status": "Active",
                "collection_name": self.collection_name
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {
                "total_documents": 0, 
                "total_embeddings": 0,
                "collections": 1,
                "status": "Error"
            }