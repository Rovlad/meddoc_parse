"""Document classification service"""

import logging
from typing import Tuple
from app.schemas.base import DocumentType
from app.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)


class DocumentClassifier:
    """Service for classifying medical documents"""
    
    def __init__(self, openai_service: OpenAIService):
        """
        Initialize classifier
        
        Args:
            openai_service: OpenAI service instance
        """
        self.openai_service = openai_service
    
    async def classify(self, base64_image: str) -> Tuple[DocumentType, float]:
        """
        Classify document type from image
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Tuple of (document_type, confidence)
        """
        try:
            # Call OpenAI to classify
            result = await self.openai_service.classify_document(base64_image)
            
            # Extract document type and confidence
            doc_type_str = result.get("document_type", "unknown").lower()
            confidence = result.get("confidence", 0.0)
            
            # Convert string to DocumentType enum
            try:
                document_type = DocumentType(doc_type_str)
            except ValueError:
                logger.warning(f"Unknown document type returned: {doc_type_str}")
                document_type = DocumentType.UNKNOWN
                confidence = 0.0
            
            logger.info(f"Classified document as {document_type.value} with confidence {confidence}")
            
            return document_type, confidence
            
        except Exception as e:
            logger.error(f"Error classifying document: {str(e)}")
            # Return unknown on error
            return DocumentType.UNKNOWN, 0.0

