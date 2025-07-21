import streamlit as st
from sentence_transformers import SentenceTransformer
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

@st.cache(allow_output_mutation=True)
def load_embedding_model():
    """Load free sentence transformer model for embeddings."""
    try:
        # Use free HuggingFace model (alternative to OpenAI)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✅ Embedding model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load embedding model: {str(e)}")
        return None

@st.cache(allow_output_mutation=True)  
def load_text_generation_model():
    """Load free text generation model."""
    try:
        from transformers import pipeline
        # Use free model for text generation
        generator = pipeline(
            'text-generation', 
            model='microsoft/DialoGPT-medium',
            max_length=512,
            pad_token_id=50256
        )
        logger.info("✅ Text generation model loaded successfully")
        return generator
    except Exception as e:
        logger.error(f"❌ Failed to load text generation model: {str(e)}")
        return None

class AIModelManager:
    def __init__(self):
        self.embedding_model = load_embedding_model()
        self.text_generator = load_text_generation_model()
    
    def generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for list of texts."""
        try:
            if self.embedding_model is None:
                raise Exception("Embedding model not loaded")
            
            embeddings = self.embedding_model.encode(texts)
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return None
    
    def generate_text(self, prompt: str, max_length: int = 200) -> str:
        """Generate text using free model."""
        try:
            if self.text_generator is None:
                raise Exception("Text generator not loaded")
            
            result = self.text_generator(
                prompt, 
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7
            )
            
            return result[0]['generated_text']
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return f"Error generating analysis: {str(e)}"