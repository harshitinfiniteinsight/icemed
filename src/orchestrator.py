"""
Reconciliation Orchestrator - Coordinates the complete reconciliation workflow
"""

import json
import os
from datetime import datetime
from typing import Tuple
import logging

from .models import ExecutionSummary
from .file_parser import ExcelFileParser
from .mock_ebs import MockEBS
from .reconciliation_generator import GeneralReconciliationGenerator
from .master_missing_manager import MasterMissingManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReconciliationOrchestrator:
    """
    Orchestrates the complete ICE reconciliation workflow
    
    Workflow:
    1. Parse input Excel file
    2. Generate encounter keys
    3. Evaluate billing (Mock EBS)
    4. Generate General Reconciliation file
    5. Update Master Missing file
    6. Generate execution summary
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize orchestrator with configuration"""
        # Store base directory (where config file is located)
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.parser = ExcelFileParser(self.config.get("input", {}))
        self.mock_ebs = MockEBS()
        self.reconciliation_gen = GeneralReconciliationGenerator(self.config.get("output", {}))
        
        # Initialize master missing manager with absolute path
        master_missing_config = self.config.get("masterMissing", {}).copy()
        master_missing_config["folderPath"] = self._resolve_path(
            master_missing_config.get("folderPath", "data/output")
        )
        self.master_missing_mgr = MasterMissingManager(master_missing_config)
        
        # Create output directories if they don't exist (may fail in read-only environments like Vercel)
        output_folder = self._resolve_path(self.config.get("output", {}).get("folderPath", "data/output"))
        try:
            os.makedirs(output_folder, exist_ok=True)
        except (OSError, PermissionError) as e:
            # In read-only filesystems (like Vercel), we can't create directories
            # This is OK - we'll use /tmp for output files instead
            logger.warning(f"Cannot create output directory {output_folder}: {e}. Will use /tmp for outputs.")
            # Don't fail - we'll handle this in file writing
    
    def run(self, input_file_path: str) -> Tuple[ExecutionSummary, dict]:
        """
        Execute complete reconciliation workflow
        
        Args:
            input_file_path: Path to ICE export Excel file
        
        Returns:
            Tuple of (ExecutionSummary, output_files_dict)
        """
        logger.info("="*60)
        logger.info("Starting ICE Reconciliation Process")
        logger.info("="*60)
        
        start_time = datetime.now()
        execution_date = start_time.strftime("%m-%d-%Y")
        
        # Initialize summary
        summary = ExecutionSummary(
            execution_date=execution_date,
            input_file=input_file_path
        )
        
        try:
            # Step 1: Parse input file
            logger.info(f"Step 1: Parsing input file: {input_file_path}")
            encounters, parse_errors = self.parser.parse_file(input_file_path)
            
            if parse_errors:
                logger.warning(f"Found {len(parse_errors)} parsing errors")
                for error in parse_errors[:5]:  # Show first 5
                    logger.warning(f"  {error}")
            
            summary.total_encounters = len(encounters)
            logger.info(f"Parsed {len(encounters)} encounters")
            
            if not encounters:
                logger.error("No encounters to process")
                return summary, {}
            
            # Step 2: Evaluate billing (Mock EBS)
            logger.info(f"Step 2: Evaluating billing for {len(encounters)} encounters")
            billing_results = self.mock_ebs.batch_evaluate(encounters)
            
            # Count results
            summary.billed_count = sum(1 for r in billing_results if r.success)
            summary.not_billed_count = len(billing_results) - summary.billed_count
            summary.success_rate = (summary.billed_count / summary.total_encounters * 100) if summary.total_encounters > 0 else 0
            
            logger.info(f"Billing Results: {summary.billed_count} billed, {summary.not_billed_count} not billed ({summary.success_rate:.1f}% success)")
            
            # Step 3: Generate General Reconciliation file
            logger.info("Step 3: Generating General Reconciliation file")
            
            reconciliation_filename = f"General Reconciliation {execution_date}.xlsx"
            output_folder = self._resolve_path(self.config.get("output", {}).get("folderPath", "data/output"))
            reconciliation_path = os.path.join(output_folder, reconciliation_filename)
            
            # Generate file and get actual path (may be /tmp if read-only)
            actual_reconciliation_path = self.reconciliation_gen.generate(encounters, billing_results, reconciliation_path, execution_date)
            summary.general_reconciliation_file = actual_reconciliation_path
            logger.info(f"Created: {actual_reconciliation_path}")
            
            # Step 4: Update Master Missing file
            logger.info("Step 4: Updating Master Missing file")
            
            # Load previous Master Missing
            previous_master_missing = self.master_missing_mgr.load_previous_file()
            logger.info(f"Loaded {len(previous_master_missing)} previous Master Missing records")
            
            # Update with current results
            updated_master_missing, stats = self.master_missing_mgr.update_with_results(
                previous_master_missing,
                encounters,
                billing_results,
                execution_date
            )
            
            summary.master_missing_added = stats["added"]
            summary.master_missing_updated = stats["updated"]
            summary.master_missing_removed = stats["removed"]
            
            # Write updated Master Missing file
            master_missing_filename = f"Master Missing to {execution_date}.xlsx"
            master_missing_folder = self._resolve_path(self.config.get("masterMissing", {}).get("folderPath", "data/output"))
            master_missing_path = os.path.join(master_missing_folder, master_missing_filename)
            
            # Write file and get actual path (may be /tmp if read-only)
            actual_master_missing_path = self.master_missing_mgr.write_file(updated_master_missing, master_missing_path, execution_date)
            summary.master_missing_file = actual_master_missing_path
            logger.info(f"Created: {actual_master_missing_path}")
            logger.info(f"Master Missing: {len(updated_master_missing)} total records (Added: {stats['added']}, Updated: {stats['updated']}, Removed: {stats['removed']})")
            
            # Step 5: Generate execution summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("="*60)
            logger.info("Reconciliation Process Complete")
            logger.info(f"Total encounters: {summary.total_encounters}")
            logger.info(f"Billed: {summary.billed_count} ({summary.success_rate:.1f}%)")
            logger.info(f"Not billed: {summary.not_billed_count}")
            logger.info(f"Execution time: {duration:.2f} seconds")
            logger.info("="*60)
            
            # Use actual paths (may be /tmp if read-only filesystem)
            output_files = {
                "general_reconciliation": summary.general_reconciliation_file,
                "master_missing": summary.master_missing_file
            }
            logger.info(f"Returning output files with actual paths: {output_files}")
            
            return summary, output_files
            
        except Exception as e:
            logger.error(f"Error during reconciliation: {e}", exc_info=True)
            raise
    
    def _resolve_path(self, path: str) -> str:
        """Resolve relative path to absolute path based on base directory"""
        if os.path.isabs(path):
            return path
        return os.path.join(self.base_dir, path)
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {
                "input": {"folderPath": "data/input", "sheetName": "Sheet1"},
                "output": {"folderPath": "data/output", "dateFormat": "MM-dd-yyyy"},
                "masterMissing": {"folderPath": "data/output", "fileNamePattern": "Master Missing to {date}.xlsx"}
            }
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
