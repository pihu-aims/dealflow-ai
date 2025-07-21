import streamlit as st
import PyPDF2
import io
from pathlib import Path
import hashlib
from datetime import datetime
from src.utils import init_supabase
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supabase = init_supabase()
        self.supported_types = ['pdf', 'txt', 'docx']
    
    def extract_text_from_pdf(self, uploaded_file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    logger.warning(f"Could not extract text from page {page_num}: {str(e)}")
                    continue
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_from_txt(self, uploaded_file) -> str:
        """Extract text from uploaded TXT file."""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'ascii']:
                try:
                    text = uploaded_file.read().decode(encoding)
                    return text.strip()
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Could not decode text file with any supported encoding")
            
        except Exception as e:
            logger.error(f"Error extracting TXT text: {str(e)}")
            raise Exception(f"Failed to extract text from TXT file: {str(e)}")
    
    def process_document(self, uploaded_file, company_name=None):
        """Process uploaded document and save to database."""
        try:
            if self.supabase is None:
                raise Exception("Database connection not available")
            
            # Get file info
            file_size = uploaded_file.size
            file_type = uploaded_file.type
            filename = uploaded_file.name
            
            # Validate file type
            file_extension = filename.split('.')[-1].lower()
            if file_extension not in self.supported_types:
                raise Exception(f"Unsupported file type: {file_extension}")
            
            # Extract text based on file type
            if file_extension == 'pdf':
                extracted_text = self.extract_text_from_pdf(uploaded_file)
            elif file_extension == 'txt':
                extracted_text = self.extract_text_from_txt(uploaded_file)
            else:
                raise Exception(f"Text extraction not implemented for {file_extension}")
            
            # Basic text validation
            if len(extracted_text) < 50:
                raise Exception("Extracted text is too short (less than 50 characters)")
            
            # Generate document summary (basic for now)
            word_count = len(extracted_text.split())
            summary = self.generate_basic_summary(extracted_text)
            
            # Save to database
            document_data = {
                'filename': filename,
                'file_type': file_type,
                'file_size': file_size,
                'processed': True,
                'processing_status': 'completed',
                'extracted_text': extracted_text[:50000],  # Limit to 50k chars
                'document_summary': summary,
                'key_metrics': {
                    'word_count': word_count,
                    'character_count': len(extracted_text),
                    'pages_processed': extracted_text.count('\n') + 1
                }
            }
            
            # If company name provided, link to company
            if company_name:
                # Try to find existing company
                company_result = self.supabase.table('companies').select('id').eq('name', company_name).execute()
                if company_result.data:
                    document_data['company_id'] = company_result.data[0]['id']
            
            # Insert document record
            result = self.supabase.table('documents').insert(document_data).execute()
            
            return {
                'success': True,
                'document_id': result.data[0]['id'],
                'text_length': len(extracted_text),
                'word_count': word_count,
                'summary': summary
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_basic_summary(self, text: str) -> str:
        """Generate basic summary of document content."""
        try:
            # Simple extractive summary - first paragraph + key metrics
            paragraphs = text.split('\n\n')
            first_paragraph = paragraphs[0] if paragraphs else text[:500]
            
            # Look for common financial keywords
            financial_keywords = ['revenue', 'profit', 'ebitda', 'valuation', 'growth', 'market', 'employees']
            found_keywords = [kw for kw in financial_keywords if kw.lower() in text.lower()]
            
            summary = f"Document contains {len(text.split())} words. "
            if found_keywords:
                summary += f"Key topics: {', '.join(found_keywords)}. "
            
            summary += f"Preview: {first_paragraph[:200]}..."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Summary generation failed."
    
    def get_recent_documents(self, limit=10):
        """Get recently processed documents."""
        try:
            if self.supabase is None:
                return []
            
            result = self.supabase.table('documents')\
                .select('*')\
                .order('upload_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting recent documents: {str(e)}")
            return []