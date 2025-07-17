import os
import tempfile
from typing import List, Dict, Any, Optional
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    CSVLoader,
    TextLoader
)
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import streamlit as st

class DocumentProcessor:
    """Class for processing various document types and creating vector embeddings."""
    
    def __init__(self, vector_db_path: str = "./data/vector_db"):
        """
        Initialize the DocumentProcessor.
        
        Args:
            vector_db_path: Path to store the vector database
        """
        self.vector_db_path = vector_db_path
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Ensure vector DB directory exists
        os.makedirs(vector_db_path, exist_ok=True)
    
    def process_file(self, file, file_type: str) -> List[Dict[str, Any]]:
        """
        Process a file based on its type and extract text content.
        
        Args:
            file: The file to process
            file_type: The type of the file (pdf, docx, pptx, csv, txt)
            
        Returns:
            List of document chunks with text and metadata
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
            tmp_file.write(file.getvalue())
            file_path = tmp_file.name
        
        try:
            if file_type == "pdf":
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_type == "docx":
                loader = Docx2txtLoader(file_path)
                documents = loader.load()
            elif file_type == "pptx":
                loader = UnstructuredPowerPointLoader(file_path)
                documents = loader.load()
            elif file_type == "csv":
                loader = CSVLoader(file_path)
                documents = loader.load()
            elif file_type in ["txt", "json", "md"]:
                loader = TextLoader(file_path)
                documents = loader.load()
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Add metadata about the source file
            for doc in documents:
                doc.metadata["source"] = file.name
                doc.metadata["file_type"] = file_type
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            return chunks
        finally:
            # Clean up the temporary file
            os.unlink(file_path)
    
    def add_to_vector_db(self, chunks: List, collection_name: str) -> None:
        """
        Add document chunks to the vector database.
        
        Args:
            chunks: List of document chunks
            collection_name: Name of the collection to store the vectors
        """
        # Create or get the vector store
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.vector_db_path
        )
        
        # Add documents to the vector store
        vector_store.add_documents(chunks)
        vector_store.persist()
        
        return vector_store
    
    def extract_metadata(self, chunks: List) -> pd.DataFrame:
        """
        Extract metadata from document chunks.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            DataFrame with metadata
        """
        metadata_list = []
        for chunk in chunks:
            metadata = chunk.metadata.copy()
            metadata["text_preview"] = chunk.page_content[:100] + "..."
            metadata_list.append(metadata)
        
        return pd.DataFrame(metadata_list)
    
    def get_collections(self) -> List[str]:
        """
        Get all available collections in the vector database.
        
        Returns:
            List of collection names
        """
        if not os.path.exists(self.vector_db_path):
            return []
        
        # Get subdirectories in the vector DB path which represent collections
        collections = [d for d in os.listdir(self.vector_db_path) 
                      if os.path.isdir(os.path.join(self.vector_db_path, d))]
        return collections
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics about a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection statistics
        """
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.vector_db_path
        )
        
        # Get collection stats
        count = vector_store._collection.count()
        
        # Get unique sources
        metadatas = vector_store.get()["metadatas"]
        sources = set()
        file_types = set()
        
        for metadata in metadatas:
            if metadata and "source" in metadata:
                sources.add(metadata["source"])
            if metadata and "file_type" in metadata:
                file_types.add(metadata["file_type"])
        
        return {
            "document_count": count,
            "unique_sources": len(sources),
            "file_types": list(file_types),
            "sources": list(sources)
        }
