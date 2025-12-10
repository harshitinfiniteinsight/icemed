#!/usr/bin/env python3
"""
Test backend processing directly without web server
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from src.orchestrator import ReconciliationOrchestrator

def test_sample_file(filename):
    """Test processing a sample file"""
    print(f"\n{'='*60}")
    print(f"Testing: {filename}")
    print(f"{'='*60}\n")
    
    try:
        orchestrator = ReconciliationOrchestrator("config.json")
        file_path = os.path.join("data/input", filename)
        
        summary, output_files = orchestrator.run(file_path)
        
        print(f"\n{'='*60}")
        print("Test Results:")
        print(f"{'='*60}")
        print(f"Total Encounters: {summary.total_encounters}")
        print(f"Billed: {summary.billed_count} ({summary.success_rate:.1f}%)")
        print(f"Not Billed: {summary.not_billed_count}")
        print(f"\nMaster Missing Updates:")
        print(f"  Added: {summary.master_missing_added}")
        print(f"  Updated: {summary.master_missing_updated}")
        print(f"  Removed: {summary.master_missing_removed}")
        print(f"\nOutput Files:")
        print(f"  General Reconciliation: {summary.general_reconciliation_file}")
        print(f"  Master Missing: {summary.master_missing_file}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Test with sample_complete.xlsx
    print("Testing Backend Processing Logic")
    print("="*60)
    
    test_files = [
        "sample_complete.xlsx",
        "sample_missing_dx.xlsx",
        "sample_mixed.xlsx"
    ]
    
    results = {}
    for filename in test_files:
        success = test_sample_file(filename)
        results[filename] = "PASS" if success else "FAIL"
    
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    for filename, result in results.items():
        print(f"{filename}: {result}")
    print("="*60)
