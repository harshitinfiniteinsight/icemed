#!/usr/bin/env python3
"""
Generate sample Excel files with different scenarios for testing
"""

import pandas as pd
from datetime import datetime, timedelta
import os

# Create data/input directory if it doesn't exist
os.makedirs('data/input', exist_ok=True)

# ICE Export File Column Schema
COLUMNS = [
    "Patient Name", "DOB", "Date of Service", "Type of Care", "Type of Visit",
    "Facility", "Room", "Assessment", "CPT", "Chief Complaint", 
    "Visit Type", "Servicing Provider", "Supervising Provider", 
    "Time", "Code Status", "Observation", "Encounter Status", 
    "Status Aux", "Export Date"
]

def create_encounter(
    patient_num, 
    date_of_service="12-09-2025",
    has_dx=True, 
    has_cpt=True, 
    facility="Hospital A",
    provider="Dr. Smith",
    type_of_care="LTC"
):
    """Create a single encounter record"""
    return {
        "Patient Name": f"Patient{patient_num:03d}, Test",
        "DOB": f"0{(patient_num % 9) + 1}-15-{1950 + (patient_num % 50)}",
        "Date of Service": date_of_service,
        "Type of Care": type_of_care,
        "Type of Visit": "Follow-up" if patient_num % 2 == 0 else "New",
        "Facility": facility,
        "Room": f"{100 + patient_num}",
        "Assessment": "I10, E11.9" if has_dx else "",
        "CPT": "99213" if has_cpt else "",
        "Chief Complaint": "Routine checkup",
        "Visit Type": "Established" if patient_num % 3 == 0 else "New",
        "Servicing Provider": provider,
        "Supervising Provider": "Dr. Johnson",
        "Time": "10:00 AM",
        "Code Status": "Full Code",
        "Observation": "Stable",
        "Encounter Status": "Completed",
        "Status Aux": "Normal",
        "Export Date": datetime.now().strftime("%m-%d-%Y")
    }

# 1. Sample Complete - All complete encounters
print("Creating sample_complete.xlsx...")
encounters = []
for i in range(1, 21):
    encounters.append(create_encounter(i, has_dx=True, has_cpt=True))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_complete.xlsx', index=False, sheet_name='Sheet1')

# 2. Sample Missing DX - Missing diagnosis codes
print("Creating sample_missing_dx.xlsx...")
encounters = []
for i in range(1, 16):
    has_dx = i > 10  # First 10 missing DX
    encounters.append(create_encounter(i, has_dx=has_dx, has_cpt=True))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_missing_dx.xlsx', index=False, sheet_name='Sheet1')

# 3. Sample Missing CPT - Missing procedure codes
print("Creating sample_missing_cpt.xlsx...")
encounters = []
for i in range(1, 16):
    has_cpt = i > 8  # First 8 missing CPT
    encounters.append(create_encounter(i, has_dx=True, has_cpt=has_cpt))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_missing_cpt.xlsx', index=False, sheet_name='Sheet1')

# 4. Sample Mixed - Mix of scenarios
print("Creating sample_mixed.xlsx...")
encounters = []
facilities = ["Hospital A", "Hospital B", "Nursing Home C", "", "Hospital D"]
providers = ["Dr. Smith", "Dr. Jones", "Dr. Wilson", "Dr. Smith", "Dr. Brown"]
types = ["LTC", "Acute", "LTC", "Acute", "LTC"]

for i in range(1, 26):
    if i <= 10:  # Complete
        encounters.append(create_encounter(i, has_dx=True, has_cpt=True))
    elif i <= 15:  # Missing DX
        encounters.append(create_encounter(i, has_dx=False, has_cpt=True))
    elif i <= 20:  # Missing CPT
        encounters.append(create_encounter(i, has_dx=True, has_cpt=False))
    elif i <= 23:  # Invalid facility (empty)
        encounters.append(create_encounter(i, has_dx=True, has_cpt=True, facility=""))
    else:  # Mix with different facilities
        encounters.append(create_encounter(
            i, 
            has_dx=True, 
            has_cpt=True,
            facility=facilities[i % len(facilities)],
            provider=providers[i % len(providers)],
            type_of_care=types[i % len(types)]
        ))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_mixed.xlsx', index=False, sheet_name='Sheet1')

# 5. Sample Multiple Dates - Different dates of service
print("Creating sample_multiple_dates.xlsx...")
encounters = []
dates = ["12-01-2025", "12-02-2025", "12-03-2025"]
facilities = ["Hospital A", "Hospital B", "Hospital C"]

for i in range(1, 31):
    date_idx = i % 3
    has_dx = i % 4 != 0  # Every 4th missing DX
    has_cpt = i % 5 != 0  # Every 5th missing CPT
    
    encounters.append(create_encounter(
        i, 
        date_of_service=dates[date_idx],
        has_dx=has_dx,
        has_cpt=has_cpt,
        facility=facilities[date_idx]
    ))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_multiple_dates.xlsx', index=False, sheet_name='Sheet1')

# 6. Sample Large - 100+ encounters for performance testing
print("Creating sample_large.xlsx...")
encounters = []
for i in range(1, 151):
    # Mix of scenarios
    if i % 7 == 0:
        has_dx = False
        has_cpt = True
    elif i % 11 == 0:
        has_dx = True
        has_cpt = False
    elif i % 13 == 0:
        has_dx = False
        has_cpt = False
    else:
        has_dx = True
        has_cpt = True
    
    encounters.append(create_encounter(
        i,
        has_dx=has_dx,
        has_cpt=has_cpt,
        facility=f"Facility {chr(65 + (i % 5))}",  # A, B, C, D, E
        provider=f"Dr. Provider{(i % 10) + 1}",
        type_of_care="LTC" if i % 2 == 0 else "Acute"
    ))
    
df = pd.DataFrame(encounters)
df.to_excel('data/input/sample_large.xlsx', index=False, sheet_name='Sheet1')

print("\nAll sample files created successfully in data/input/")
print("Files created:")
print("  - sample_complete.xlsx (20 encounters, all complete)")
print("  - sample_missing_dx.xlsx (15 encounters, 10 missing DX)")
print("  - sample_missing_cpt.xlsx (15 encounters, 8 missing CPT)")
print("  - sample_mixed.xlsx (25 encounters, various scenarios)")
print("  - sample_multiple_dates.xlsx (30 encounters, 3 different dates)")
print("  - sample_large.xlsx (150 encounters, mixed scenarios)")
