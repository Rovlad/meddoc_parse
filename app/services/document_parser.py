"""Document parsing service"""

import logging
from typing import Dict, Any, Optional
from app.schemas.base import DocumentType
from app.schemas import (
    PrescriptionSchema,
    LabReportSchema,
    DoctorVisitSchema,
    DiagnosticResultsSchema
)
from app.services.openai_service import OpenAIService
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class DocumentParser:
    """Service for parsing medical documents"""
    
    # Schema descriptions for each document type
    SCHEMA_DESCRIPTIONS = {
        DocumentType.PRESCRIPTION: """
Извлеките следующие поля:
- summary (обязательно): Краткое описание документа в одном предложении (например: "Рецепт на антибиотик Амоксициллин для лечения бактериальной инфекции на 7 дней")
- patient_name (обязательно): Полное имя пациента
- patient_age (необязательно): Возраст пациента
- patient_contact (необязательно): Контактный номер или email пациента
- doctor_name (обязательно): Полное имя врача, выписавшего рецепт
- doctor_specialty (необязательно): Медицинская специальность врача
- doctor_contact (необязательно): Контактные данные врача
- visit_date (необязательно): Дата, когда пациент ФИЗИЧЕСКИ ПОСЕТИЛ клинику/врача (формат YYYY-MM-DD). ВАЖНО: Это дата визита к врачу, обычно совпадает с датой выписки рецепта.
- prescription_date (обязательно): Дата выписки рецепта (формат YYYY-MM-DD)
- validity_date (необязательно): Дата истечения срока действия рецепта (формат YYYY-MM-DD)
- medications (обязательно): Массив лекарств, каждое с полями:
  - name (обязательно): Название лекарства
  - dosage (обязательно): Дозировка
  - frequency (обязательно): Как часто принимать
  - duration (обязательно): Как долго принимать
  - instructions (необязательно): Дополнительные инструкции
- diagnosis (необязательно): Диагноз или состояние
- notes (необязательно): Любые дополнительные заметки
""",
        DocumentType.LAB_REPORT: """
Извлеките следующие поля:
- summary (обязательно): Краткое описание результатов анализа в одном предложении (например: "Общий анализ крови с нормальным уровнем гемоглобина и слегка повышенным содержанием глюкозы")
- patient_name (обязательно): Полное имя пациента
- patient_age (необязательно): Возраст пациента
- patient_id (необязательно): ID пациента или регистрационный номер
- visit_date (необязательно): Дата, когда пациент ФИЗИЧЕСКИ ПОСЕТИЛ клинику/лабораторию для сдачи анализов (формат YYYY-MM-DD). ВАЖНО: Это должна быть дата визита пациента в медучреждение, обычно совпадает с датой сбора/взятия образцов, а НЕ дата создания отчета.
- report_date (обязательно): Дата создания/выдачи отчета (формат YYYY-MM-DD)
- collection_date (необязательно): Дата сбора образцов или дата регистрации материала (формат YYYY-MM-DD). ВНИМАНИЕ: Ищите эту дату в документе под различными названиями, такими как "Дата регистрации", "Дата сбора", "Дата взятия материала", "Дата забора", "Дата/время регистрации". Извлекайте только дату, игнорируйте время. ВАЖНО: visit_date обычно совпадает с collection_date.
- lab_info (обязательно): Объект с полями:
  - lab_name (обязательно): Название лаборатории
  - lab_location (необязательно): Адрес или местоположение лаборатории
  - lab_contact (необязательно): Контактный номер или email лаборатории
- doctor_name (необязательно): Имя направившего врача
- test_results (обязательно): МАССИВ результатов тестов. ОЧЕНЬ ВАЖНО: Извлеките ВСЕ анализы из документа! Каждый анализ должен быть отдельным объектом в массиве с полями:
  - test_name (обязательно): Название теста (например, "Гемоглобин", "Эритроциты", "Лейкоциты")
  - result_value (обязательно): Значение результата теста
  - unit (необязательно): Единица измерения (например, "г/л", "10^9/л")
  - reference_range (необязательно): Референсный диапазон нормы (например, "120-160")
  - status (необязательно): Статус - используйте "normal", "abnormal", или "critical"
  
  Пример структуры test_results:
  [
    {"test_name": "Гемоглобин", "result_value": "145", "unit": "г/л", "reference_range": "120-160", "status": "normal"},
    {"test_name": "Эритроциты", "result_value": "4.5", "unit": "10^12/л", "reference_range": "4.0-5.5", "status": "normal"}
  ]
  
- notes (необязательно): Любые дополнительные заметки или комментарии
""",
        DocumentType.DOCTOR_VISIT: """
Извлеките следующие поля:
- summary (обязательно): Краткое описание визита в одном предложении (например: "Кардиологический прием по поводу гипертонии с корректировкой медикаментов и рекомендациями по образу жизни")
- patient_name (обязательно): Полное имя пациента
- patient_age (необязательно): Возраст пациента
- patient_contact (необязательно): Контактный номер или email пациента
- visit_date (обязательно): Дата, когда пациент ФИЗИЧЕСКИ ПОСЕТИЛ клинику/врача (формат YYYY-MM-DD). ВАЖНО: Это дата реального визита пациента в медучреждение.
- clinic_info (необязательно): Объект с информацией о клинике:
  - clinic_name (обязательно): Название клиники или медицинского учреждения
  - clinic_location (необязательно): Адрес или местоположение клиники
  - clinic_contact (необязательно): Контактный номер или email клиники
- doctor_name (обязательно): Полное имя врача
- doctor_specialty (необязательно): Специальность врача
- diagnosis (обязательно): Диагноз или выявленное состояние
- procedures (необязательно): Массив процедур, выполненных во время визита
- medications (необязательно): Массив назначенных лекарств, каждое с полями:
  - name (обязательно): Название лекарства
  - dosage (обязательно): Дозировка
  - frequency (обязательно): Как часто принимать
  - duration (обязательно): Как долго принимать
- recommendations (необязательно): Массив рекомендаций врача
- follow_up (необязательно): Инструкции по последующему наблюдению или следующему приему
- notes (необязательно): Любые дополнительные заметки
""",
        DocumentType.DIAGNOSTIC_RESULTS: """
Извлеките следующие поля:
- summary (обязательно): Краткое описание результатов диагностики в одном предложении (например: "МРТ поясничного отдела позвоночника показывает незначительную дегенерацию диска без острых отклонений")
- patient_name (обязательно): Полное имя пациента
- patient_age (необязательно): Возраст пациента
- patient_id (необязательно): ID пациента или регистрационный номер
- diagnostic_type (обязательно): Тип диагностического исследования (ultrasound, x-ray, mri, или ct)
- visit_date (необязательно): Дата, когда пациент ФИЗИЧЕСКИ ПОСЕТИЛ диагностический центр для прохождения исследования (формат YYYY-MM-DD). ВАЖНО: Это дата визита пациента, обычно совпадает с датой проведения исследования.
- study_date (обязательно): Дата проведения исследования (формат YYYY-MM-DD)
- facility_info (обязательно): Объект с полями:
  - facility_name (обязательно): Название диагностического центра
  - facility_location (необязательно): Адрес или местоположение центра
  - facility_contact (необязательно): Контактный номер или email центра
- referring_physician (необязательно): Имя направившего врача
- radiologist_name (необязательно): Имя радиолога, проводившего исследование
- body_part_examined (необязательно): Исследуемая часть тела или область
- findings_summary (обязательно): Краткое изложение результатов диагностического исследования
- impression (необязательно): Заключение или вывод радиолога
- recommendations (необязательно): Рекомендации по последующему наблюдению или дополнительным исследованиям
- notes (необязательно): Любые дополнительные заметки или технические детали
"""
    }
    
    # Schema classes for validation
    SCHEMA_CLASSES = {
        DocumentType.PRESCRIPTION: PrescriptionSchema,
        DocumentType.LAB_REPORT: LabReportSchema,
        DocumentType.DOCTOR_VISIT: DoctorVisitSchema,
        DocumentType.DIAGNOSTIC_RESULTS: DiagnosticResultsSchema,
    }
    
    def __init__(self, openai_service: OpenAIService):
        """
        Initialize parser
        
        Args:
            openai_service: OpenAI service instance
        """
        self.openai_service = openai_service
    
    async def parse(
        self,
        base64_image: str,
        document_type: DocumentType
    ) -> Optional[Dict[str, Any]]:
        """
        Parse document and extract structured data
        
        Args:
            base64_image: Base64 encoded image
            document_type: Type of document to parse
            
        Returns:
            Parsed data dictionary or None if parsing fails
        """
        # Unknown documents can't be parsed
        if document_type == DocumentType.UNKNOWN:
            logger.warning("Cannot parse unknown document type")
            return None
        
        # Get schema description
        schema_description = self.SCHEMA_DESCRIPTIONS.get(document_type)
        if not schema_description:
            logger.error(f"No schema description found for {document_type}")
            return None
        
        try:
            # Extract structured data using OpenAI
            logger.info(f"Starting extraction for {document_type.value} document")
            raw_data = await self.openai_service.extract_structured_data(
                base64_image=base64_image,
                document_type=document_type.value,
                schema_description=schema_description
            )
            
            logger.info(f"Raw data extracted: {str(raw_data)[:200]}...")
            
            # Validate data against Pydantic schema
            schema_class = self.SCHEMA_CLASSES.get(document_type)
            if schema_class:
                try:
                    validated_data = schema_class(**raw_data)
                    logger.info(f"Successfully parsed and validated {document_type.value} document")
                    return validated_data.model_dump()
                except ValidationError as e:
                    logger.error(f"Validation errors for {document_type.value}: {str(e)}")
                    logger.error(f"Raw data that failed validation: {raw_data}")
                    # Return raw data even if validation fails
                    logger.info("Returning raw data despite validation errors")
                    return raw_data
            else:
                return raw_data
            
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}", exc_info=True)
            return None

