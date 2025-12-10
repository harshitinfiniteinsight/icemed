"""
Data models for ICE Reconciliation System
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import hashlib


@dataclass
class Encounter:
    """Represents a patient encounter from ICE export file"""
    patient_name: str
    dob: str
    date_of_service: str
    type_of_care: str
    type_of_visit: str
    facility: str
    room: str
    assessment: str  # DX codes
    cpt: str  # CPT code
    chief_complaint: str
    visit_type: str
    servicing_provider: str
    supervising_provider: str
    time: str
    code_status: str
    observation: str
    encounter_status: str
    status_aux: str
    export_date: str
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Encounter from dictionary"""
        return cls(
            patient_name=str(data.get("Patient Name", "")),
            dob=str(data.get("DOB", "")),
            date_of_service=str(data.get("Date of Service", "")),
            type_of_care=str(data.get("Type of Care", "")),
            type_of_visit=str(data.get("Type of Visit", "")),
            facility=str(data.get("Facility", "")),
            room=str(data.get("Room", "")),
            assessment=str(data.get("Assessment", "")),
            cpt=str(data.get("CPT", "")),
            chief_complaint=str(data.get("Chief Complaint", "")),
            visit_type=str(data.get("Visit Type", "")),
            servicing_provider=str(data.get("Servicing Provider", "")),
            supervising_provider=str(data.get("Supervising Provider", "")),
            time=str(data.get("Time", "")),
            code_status=str(data.get("Code Status", "")),
            observation=str(data.get("Observation", "")),
            encounter_status=str(data.get("Encounter Status", "")),
            status_aux=str(data.get("Status Aux", "")),
            export_date=str(data.get("Export Date", ""))
        )
    
    def generate_key(self) -> str:
        """Generate unique encounter key using SHA-256 hash"""
        # Normalize components
        patient = self._normalize_string(self.patient_name)
        dob = self._normalize_date(self.dob)
        dos = self._normalize_date(self.date_of_service)
        facility = self._normalize_string(self.facility)
        cpt = self._normalize_string(self.cpt)
        
        # Create key string
        key_string = f"{patient}_{dob}_{dos}_{facility}_{cpt}"
        
        # Generate SHA-256 hash
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    @staticmethod
    def _normalize_string(value: Optional[str]) -> str:
        """Normalize string: trim, uppercase, collapse whitespace"""
        if not value:
            return ""
        return " ".join(value.strip().upper().split())
    
    @staticmethod
    def _normalize_date(date_value: str) -> str:
        """Normalize date to YYYY-MM-DD format"""
        if not date_value:
            return ""
        
        # Try common date formats
        formats = ["%m-%d-%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(str(date_value).strip(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If all formats fail, return as is
        return str(date_value).strip()


@dataclass
class BillingResult:
    """Result of billing evaluation for an encounter"""
    encounter_key: str
    success: bool
    reason: str = ""  # Empty if success=True
    claim_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "encounter_key": self.encounter_key,
            "success": self.success,
            "reason": self.reason,
            "claim_id": self.claim_id,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ReconciliationData:
    """Data for General Reconciliation output"""
    encounter: Encounter
    billed: str  # "Yes" or "No"
    reason_for_not_billed: str = ""
    
    def to_dict(self):
        """Convert to dictionary for Excel output"""
        data = self.encounter.to_dict()
        data["Billed"] = self.billed
        data["Reason for not billed"] = self.reason_for_not_billed
        return data


@dataclass
class MasterMissingRecord:
    """Record for Master Missing file (historical ledger)"""
    patient_name: str
    dob: str
    date_of_service: str
    type_of_care: str
    type_of_visit: str
    facility: str
    last_attempt_to_process: str
    billed: str = "No"  # Always "No" in Master Missing
    reason_for_not_billed: str = ""
    encounter_key: str = ""
    
    def to_dict(self):
        """Convert to dictionary for Excel output"""
        return {
            "Patient Name": self.patient_name,
            "DOB": self.dob,
            "Date of Service": self.date_of_service,
            "Type of Care": self.type_of_care,
            "Type of Visit": self.type_of_visit,
            "Facility": self.facility,
            "Last Attempt to Process": self.last_attempt_to_process,
            "Billed": self.billed,
            "Reason for not billed": self.reason_for_not_billed
        }
    
    @classmethod
    def from_encounter(cls, encounter: Encounter, reason: str, execution_date: str):
        """Create MasterMissingRecord from Encounter"""
        return cls(
            patient_name=encounter.patient_name,
            dob=encounter.dob,
            date_of_service=encounter.date_of_service,
            type_of_care=encounter.type_of_care,
            type_of_visit=encounter.type_of_visit,
            facility=encounter.facility,
            last_attempt_to_process=execution_date,
            billed="No",
            reason_for_not_billed=reason,
            encounter_key=encounter.generate_key()
        )


@dataclass
class ExecutionSummary:
    """Summary of reconciliation execution"""
    total_encounters: int = 0
    billed_count: int = 0
    not_billed_count: int = 0
    success_rate: float = 0.0
    execution_date: str = ""
    input_file: str = ""
    general_reconciliation_file: str = ""
    master_missing_file: str = ""
    master_missing_added: int = 0
    master_missing_updated: int = 0
    master_missing_removed: int = 0
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
