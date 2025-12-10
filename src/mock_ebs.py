"""
Mock EBS Integration - Simulates billing evaluation business rules
"""

from typing import List
from .models import Encounter, BillingResult


class MockEBS:
    """
    Mock EBS class that simulates billing evaluation
    Returns billing results based on business rules without actual EBS integration
    """
    
    def __init__(self):
        """Initialize mock EBS"""
        self.call_count = 0
    
    def evaluate_encounter(self, encounter: Encounter) -> BillingResult:
        """
        Evaluate a single encounter and return billing result
        
        Business Rules Simulation:
        - Missing DX (Assessment) → "Missing DX"
        - Missing CPT → "Missing CPT"
        - Empty Facility → "Invalid Facility"
        - Missing Servicing Provider → "Provider Mismatch"
        - Otherwise → Success
        """
        self.call_count += 1
        encounter_key = encounter.generate_key()
        
        # Check for missing diagnosis code (Assessment)
        if not encounter.assessment or encounter.assessment.strip() == "":
            return BillingResult(
                encounter_key=encounter_key,
                success=False,
                reason="Missing DX"
            )
        
        # Check for missing CPT code
        if not encounter.cpt or encounter.cpt.strip() == "":
            return BillingResult(
                encounter_key=encounter_key,
                success=False,
                reason="Missing CPT"
            )
        
        # Check for invalid/empty facility
        if not encounter.facility or encounter.facility.strip() == "":
            return BillingResult(
                encounter_key=encounter_key,
                success=False,
                reason="Invalid Facility"
            )
        
        # Check for missing servicing provider
        if not encounter.servicing_provider or encounter.servicing_provider.strip() == "":
            return BillingResult(
                encounter_key=encounter_key,
                success=False,
                reason="Provider Mismatch"
            )
        
        # Check for missing supervising provider
        if not encounter.supervising_provider or encounter.supervising_provider.strip() == "":
            return BillingResult(
                encounter_key=encounter_key,
                success=False,
                reason="Provider Mismatch"
            )
        
        # All checks passed - billing successful
        return BillingResult(
            encounter_key=encounter_key,
            success=True,
            reason="",
            claim_id=f"CLAIM-{self.call_count:06d}"
        )
    
    def batch_evaluate(self, encounters: List[Encounter]) -> List[BillingResult]:
        """
        Evaluate multiple encounters in batch
        Returns list of billing results in same order as input
        """
        results = []
        for encounter in encounters:
            result = self.evaluate_encounter(encounter)
            results.append(result)
        
        return results
    
    def get_stats(self) -> dict:
        """Get statistics about EBS calls"""
        return {
            "total_calls": self.call_count
        }
