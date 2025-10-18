"""Document schemas for medical documents"""

from .base import DocumentType
from .prescription import PrescriptionSchema, Medication
from .lab_report import LabReportSchema, LabInfo, TestResult
from .doctor_visit import DoctorVisitSchema, VisitMedication, ClinicInfo
from .diagnostic_results import DiagnosticResultsSchema, FacilityInfo

__all__ = [
    "DocumentType",
    "PrescriptionSchema",
    "Medication",
    "LabReportSchema",
    "LabInfo",
    "TestResult",
    "DoctorVisitSchema",
    "VisitMedication",
    "ClinicInfo",
    "DiagnosticResultsSchema",
    "FacilityInfo",
]

