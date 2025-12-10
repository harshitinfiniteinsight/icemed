#!/usr/bin/env python3
"""
Generate sample Excel files with different scenarios using openpyxl directly
"""

from openpyxl import Workbook
from datetime import datetime
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
    """Create a single encounter record as a list"""
    return [
        f"Patient{patient_num:03d}, Test",  # Patient Name
        f"0{(patient_num % 9) + 1}-15-{1950 + (patient_num % 50)}",  # DOB
        date_of_service,  # Date of Service
        type_of_care,  # Type of Care
        "Follow-up" if patient_num % 2 == 0 else "New",  # Type of Visit
        facility,  # Facility
        f"{100 + patient_num}",  # Room
        "I10, E11.9" if has_dx else "",  # Assessment (DX)
        "99213" if has_cpt else "",  # CPT
        "Routine checkup",  # Chief Complaint
        "Established" if patient_num % 3 == 0 else "New",  # Visit Type
        provider,  # Servicing Provider
        "Dr. Johnson",  # Supervising Provider
        "10:00 AM",  # Time
        "Full Code",  # Code Status
        "Stable",  # Observation
        "Completed",  # Encounter Status
        "Normal",  # Status Aux
        datetime.now().strftime("%m-%d-%Y")  # Export Date
    ]

def create_excel_file(filename, encounters):
    """Create an Excel file with encounters"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    # Add header row
    ws.append(COLUMNS)
    
    # Add data rows
    for encounter in encounters:
        ws.append(encounter)
    
    # Save file
    wb.save(filename)
    print(f"Created {filename}")

# 1. Sample Complete - All complete encounters
print("Creating sample_complete.xlsx...")
encounters = []
for i in range(1, 21):
    encounters.append(create_encounter(i, has_dx=True, has_cpt=True))
create_excel_file('data/input/sample_complete.xlsx', encounters)

# 2. Sample Missing DX - Missing diagnosis codes
print("Creating sample_missing_dx.xlsx...")
encounters = []
for i in range(1, 16):
    has_dx = i > 10  # First 10 missing DX
    encounters.append(create_encounter(i, has_dx=has_dx, has_cpt=True))
create_excel_file('data/input/sample_missing_dx.xlsx', encounters)

# 3. Sample Missing CPT - Missing procedure codes
print("Creating sample_missing_cpt.xlsx...")
encounters = []
for i in range(1, 16):
    has_cpt = i > 8  # First 8 missing CPT
    encounters.append(create_encounter(i, has_dx=True, has_cpt=has_cpt))
create_excel_file('data/input/sample_missing_cpt.xlsx', encounters)

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
create_excel_file('data/input/sample_mixed.xlsx', encounters)

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
create_excel_file('data/input/sample_multiple_dates.xlsx', encounters)

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
create_excel_file('data/input/sample_large.xlsx', encounters)

print("\nAll sample files created successfully in data/input/")
print("Files created:")
print("  - sample_complete.xlsx (20 encounters, all complete)")
print("  - sample_missing_dx.xlsx (15 encounters, 10 missing DX)")
print("  - sample_missing_cpt.xlsx (15 encounters, 8 missing CPT)")
print("  - sample_mixed.xlsx (25 encounters, various scenarios)")
print("  - sample_multiple_dates.xlsx (30 encounters, 3 different dates)")
print("  - sample_large.xlsx (150 encounters, mixed scenarios)")
