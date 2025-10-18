"""OpenAI API service"""

import json
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        if not settings.openai_api_key:
            logger.warning("OpenAI API key is not set! API calls will fail.")
            logger.warning("Please set OPENAI_API_KEY environment variable in Railway.")
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.openai_model
    
    async def analyze_image_with_prompt(
        self,
        base64_image: str,
        prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
        max_tokens: int = 2000
    ) -> str:
        """
        Analyze image with a custom prompt
        
        Args:
            base64_image: Base64 encoded image
            prompt: Prompt for analysis
            response_format: Optional JSON schema for structured output
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from OpenAI
        """
        if not self.client:
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable.")
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
            }
            
            # Add response format if provided (for structured output)
            if response_format:
                api_params["response_format"] = response_format
            
            # Make API call
            response = self.client.chat.completions.create(**api_params)
            
            result = response.choices[0].message.content
            logger.info(f"OpenAI API call successful. Tokens used: {response.usage.total_tokens}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def classify_document(self, base64_image: str) -> Dict[str, Any]:
        """
        Classify medical document type
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Dictionary with document_type and confidence
        """
        prompt = """Вы классификатор медицинских документов. Проанализируйте это изображение и определите тип медицинского документа.

Возможные типы документов:
1. prescription - Медицинский рецепт с информацией о пациенте, враче и назначенных лекарствах
2. lab_report - Отчет о лабораторных анализах с результатами тестов и референсными значениями
3. doctor_visit - Заключение врача после визита с диагнозом, процедурами и рекомендациями
4. diagnostic_results - Результаты диагностической визуализации (рентген, МРТ, КТ, УЗИ) с заключениями
5. unknown - Если документ не соответствует ни одному из вышеперечисленных типов

Отвечайте ТОЛЬКО JSON объектом в этом точном формате (ключи на английском, значения reasoning на русском):
{
    "document_type": "один из типов выше",
    "confidence": 0.95,
    "reasoning": "краткое объяснение на русском"
}"""
        
        try:
            response = await self.analyze_image_with_prompt(
                base64_image=base64_image,
                prompt=prompt,
                max_tokens=200
            )
            
            # Clean the response - remove markdown code fences if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]  # Remove ```
            
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON response
            result = json.loads(cleaned_response)
            
            # Validate response
            if "document_type" not in result or "confidence" not in result:
                raise ValueError("Invalid response format from OpenAI")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse classification response: {str(e)}")
            logger.error(f"Response was: {response}")
            return {
                "document_type": "unknown",
                "confidence": 0.0,
                "reasoning": "Failed to parse response"
            }
        except Exception as e:
            logger.error(f"Error classifying document: {str(e)}")
            raise
    
    async def extract_structured_data(
        self,
        base64_image: str,
        document_type: str,
        schema_description: str
    ) -> Dict[str, Any]:
        """
        Extract structured data from document based on its type
        
        Args:
            base64_image: Base64 encoded image
            document_type: Type of document
            schema_description: Description of expected schema
            
        Returns:
            Extracted structured data
        """
        prompt = f"""Вы специалист по извлечению данных из медицинских документов. Проанализируйте этот документ типа {document_type} и извлеките всю соответствующую информацию.

{schema_description}

Извлеките данные и ответьте ТОЛЬКО JSON объектом с извлеченной информацией. Все текстовые значения должны быть на русском языке. Если поле отсутствует или неясно, используйте null для необязательных полей. Будьте точны и извлекайте именно то, что видите в документе.

Формат ответа: Чистый JSON объект без дополнительного текста или объяснений. Названия полей (ключи) должны оставаться на английском, а значения - на русском."""
        
        try:
            response = await self.analyze_image_with_prompt(
                base64_image=base64_image,
                prompt=prompt,
                max_tokens=2000
            )
            
            # Clean the response - remove markdown code fences if present
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]  # Remove ```
            
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON response
            result = json.loads(cleaned_response)
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse extraction response: {str(e)}")
            logger.error(f"Response was: {response}")
            logger.error(f"Cleaned response was: {cleaned_response}")
            raise ValueError(f"Failed to parse structured data: {str(e)}")
        except Exception as e:
            logger.error(f"Error extracting structured data: {str(e)}")
            raise

