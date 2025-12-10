"""
Encounter Key Generator - Utility functions for generating encounter keys
Note: The key generation logic is now in Encounter.generate_key() in models.py
This module provides utility functions for batch operations
"""

from typing import List
from .models import Encounter


def generate_encounter_keys(encounters: List[Encounter]) -> List[str]:
    """
    Generate encounter keys for a list of encounters
    
    Args:
        encounters: List of Encounter objects
    
    Returns:
        List of encounter keys (SHA-256 hashes)
    """
    return [encounter.generate_key() for encounter in encounters]


def create_encounter_map(encounters: List[Encounter]) -> dict:
    """
    Create a dictionary mapping encounter keys to encounters
    
    Args:
        encounters: List of Encounter objects
    
    Returns:
        Dictionary {encounter_key: Encounter}
    """
    return {encounter.generate_key(): encounter for encounter in encounters}
