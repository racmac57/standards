# 2025-12-22-16-00-00
# CAD_Data_Cleaning_Engine/enhanced_esri_output_generator_COMPLETE.py
# Author: R. A. Carucci
# Purpose: Complete ESRI output generator with all domain normalizations (Disposition, How Reported, Incident) and parallel processing

#!/usr/bin/env python
"""
Complete Enhanced ESRI Output Generator
========================================
Generates draft and polished ESRI outputs with comprehensive normalization:
1. Disposition normalization (30+ mappings)
2. How Reported normalization (25+ mappings)
3. Incident normalization (637 mappings from reference file)
4. Strict column ordering
5. Parallel processing for large datasets

Author: R. A. Carucci
Date: 2025-12-22
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Required ESRI column order (must match sample exactly)
ESRI_REQUIRED_COLUMNS = [
    'ReportNumberNew',
    'Incident',
    'How Reported',
    'FullAddress2',
    'Grid',
    'ZoneCalc',
    'Time of Call',
    'cYear',
    'cMonth',
    'Hour_Calc',
    'DayofWeek',
    'Time Dispatched',
    'Time Out',
    'Time In',
    'Time Spent',
    'Time Response',
    'Officer',
    'Disposition',
    'latitude',
    'longitude'
]

# Disposition normalization mapping
DISPOSITION_MAPPING = {
    # Uppercase variants -> Title case standard
    'COMPLETE': 'Complete',
    'ADVISED': 'Advised',
    'ARREST': 'Arrest',
    'ASSISTED': 'Assisted',
    'CANCELED': 'Canceled',
    'CANCELLED': 'Canceled',
    'UNFOUNDED': 'Unfounded',
    
    # Abbreviations -> Full names
    'GOA': 'G.O.A.',
    'G.O.A': 'G.O.A.',
    'UTL': 'Unable to Locate',
    'UTL - UNABLE TO LOCATE': 'Unable to Locate',
    'UNABLE TO LOCATE': 'Unable to Locate',
    
    # Variations
    'CHECKED OK': 'Checked OK',
    'CHECKED': 'Checked OK',
    'OK': 'Checked OK',
    'CURBSIDE WARNING': 'Curbside Warning',
    'CURBSIDE': 'Curbside Warning',
    'DISPERSED': 'Dispersed',
    'FIELD CONTACT': 'Field Contact',
    'FIELD': 'Field Contact',
    'ISSUED': 'Issued',
    'RECORD ONLY': 'Record Only',
    'RECORD': 'Record Only',
    'SEE REPORT': 'See Report',
    'SEE SUPPLEMENT': 'See Supplement',
    'SUPPLEMENT': 'See Supplement',
    'TEMP. SETTLED': 'Temp. Settled',
    'TEMP SETTLED': 'Temp. Settled',
    'TEMPORARILY SETTLED': 'Temp. Settled',
    'TRANSPORTED': 'Transported',
    'TRANSPORT': 'Transported',
    
    # Special cases
    'SEE OCA# (IN NOTES)': 'Other - See Notes',
    'SEE OCA# (IN NOTES)': 'Other - See Notes',  # Case variation
    'SEE OCA#': 'Other - See Notes',
    'SEE OCA# (IN NOTES)': 'Other - See Notes',  # Mixed case
    'OCA#': 'Other - See Notes',
    'OTHER': 'Other - See Notes',
    'OTHER - SEE NOTES': 'Other - See Notes',
    'TOT - SEE NOTES': 'TOT - See Notes',
    'TOT': 'TOT - See Notes',
    
    # Edge cases discovered post-deployment
    'CLEARED': 'Complete',
    'CLOSED': 'Complete',
    'DONE': 'Complete',
    'FINISHED': 'Complete',
    'UNFOUNDED/ GOA': 'Unfounded',
    'UNFOUNDED/GOA': 'Unfounded',
    'UNFOUNDED / GOA': 'Unfounded',
    'GOA/UNFOUNDED': 'G.O.A.',
    'UNFOUNDED/G.O.A.': 'Unfounded',
    'GOA/UNFOUNDED': 'G.O.A.',
    
    # Additional variations
    'REFERRED': 'Other - See Notes',
    'REFERRED TO': 'Other - See Notes',
    'FOLLOW UP': 'Other - See Notes',
    'FOLLOW-UP': 'Other - See Notes',
    'PENDING': 'Other - See Notes',
    'IN PROGRESS': 'Other - See Notes',
    'INVESTIGATION': 'Other - See Notes',
    'ACTIVE': 'Other - See Notes',
}

# How Reported normalization mapping
HOW_REPORTED_MAPPING = {
    '911': '9-1-1',
    '9-1-1': '9-1-1',
    '9/1/1': '9-1-1',
    '9 1 1': '9-1-1',
    'E911': '9-1-1',
    'E-911': '9-1-1',
    'EMERGENCY 911': '9-1-1',
    'EMERGENCY-911': '9-1-1',
    'EMERGENCY/911': '9-1-1',
    
    'WALK IN': 'Walk-In',
    'WALK-IN': 'Walk-In',
    'WALKIN': 'Walk-In',
    'IN PERSON': 'Walk-In',
    
    'PHONE': 'Phone',
    'TEL': 'Phone',
    'TELEPHONE': 'Phone',
    
    'SELF INITIATED': 'Self-Initiated',
    'SELF-INITIATED': 'Self-Initiated',
    'OFFICER INITIATED': 'Self-Initiated',
    'OI': 'Self-Initiated',
    'SI': 'Self-Initiated',
    
    'RADIO': 'Radio',
    'FAX': 'Fax',
    
    'EMAIL': 'eMail',
    'E-MAIL': 'eMail',
    
    'MAIL': 'Mail',
    'POST': 'Mail',
    
    'VIRTUAL PATROL': 'Virtual Patrol',
    
    'CANCELED': 'Canceled Call',
    'CANCELLED': 'Canceled Call',
    'CANCELED CALL': 'Canceled Call',
    'CANCELLED CALL': 'Canceled Call',
    
    'TELETYPE': 'Teletype',
    
    'OTHER - SEE NOTES': 'Other - See Notes',
    'OTHER': 'Other - See Notes',
    
    # Edge cases discovered post-deployment (typos and abbreviations)
    'RS': 'Radio',
    'SR': 'Radio',
    'RE': 'Radio',
    'RR': 'Radio',
    'RP': 'Radio',
    'R': 'Radio',
    'RQ': 'Radio',
    'RT': 'Radio',
    'RF': 'Radio',
    'RLK': 'Radio',
    'RQQ': 'Radio',
    'RQA': 'Radio',
    'RAQ': 'Radio',
    'QR': 'Radio',
    'RARE': 'Radio',
    'RADIOHACK': 'Radio',
    'RRADIO': 'Radio',
    'RADIO': 'Radio',
    'RADIO19': 'Radio',
    'RADIO160': 'Radio',
    'RA9DIO': 'Radio',
    'RAD9-1-1IO': 'Radio',
    'RADISELF-INITIATEDO': 'Radio',
    'RHOME': 'Radio',
    'RFOSC': 'Radio',
    'RVETER': 'Radio',
    'WALK-IR': 'Walk-In',
    'WALK IN': 'Walk-In',
    'WALKIN': 'Walk-In',
    'WAK': 'Walk-In',
    'WALKL': 'Walk-In',
    'WR': 'Walk-In',
    'E': 'eMail',
    'S': 'Self-Initiated',
    'SELF-INIT': 'Self-Initiated',
    'SELF INITIATED': 'Self-Initiated',
    'SELF-INTIATED': 'Self-Initiated',
    'SELF-INITIATE': 'Self-Initiated',
    'SELF REPORTED': 'Self-Initiated',
    'P': 'Phone',
    'PP': 'Phone',
    'PPP': 'Phone',
    'PW': 'Phone',
    'PQ': 'Phone',
    'PHON': 'Phone',
    'PHOME': 'Phone',
    'PHNE': 'Phone',
    'PHB': 'Phone',
    'PCENTRAL': 'Phone',
    'P190': 'Phone',
    'P.O. CHR': 'Phone',
    'PLITO': 'Phone',
    'TELEPHONE': 'Phone',
    'W': 'Walk-In',
    'EMIAL': 'eMail',
    'EMAIL.': 'eMail',
    'EMAIL9': 'eMail',
    # Single character and number patterns
    '0': 'Phone',  # Default for numbers
    '8': 'Phone',
    '10': 'Phone',
    '15': 'Phone',
    '407': 'Phone',
    '9': '9-1-1',
    '91': '9-1-1',
    '99': '9-1-1',
    '9155': '9-1-1',
    '9-1-1.': '9-1-1',  # Remove trailing period
    '9-1-19': '9-1-1',
    '9*': '9-1-1',
    'Y789': '9-1-1',
    # Special characters
    '[': 'Phone',
    ']': 'Phone',
    '(': 'Phone',
    ')': 'Phone',
    '{': 'Phone',
    '{P': 'Phone',
    '}': 'Phone',
    '\\': 'Phone',
    '/': 'Phone',
    '.': 'Phone',
    '+': 'Phone',
    '\\R': 'Phone',
    # Concatenated typos (will be handled by advanced normalization, but add common ones)
    'PHONRADIOE': 'Phone',  # Prefer Phone over Radio
    'RADIOPHONEO': 'Radio',  # Prefer Radio over Phone
    'TELETYPERADIO': 'Teletype',
    'SERADIOLF-INITIATED': 'Self-Initiated',
    'TELETYRADIOPE': 'Teletype',
    'PHORADIONE': 'Phone',
    'PHONE9-1-1': 'Phone',
    'EMAILOTHER - SEE NOTESAIL': 'eMail',
    # Unknown abbreviations (default to Phone)
    'TR': 'Phone',
    'TAR': 'Phone',
    'T-3': 'Phone',
    'MV': 'Phone',
    'ARE': 'Phone',
    'WAS': 'Phone',
    'HEAD': 'Phone',
    'HAC': 'Phone',
    'IOI': 'Phone',
    'MED': 'Phone',
    'BREAK': 'Phone',
    'SPEN': 'Phone',
    'COLUMBUS': 'Phone',
    'JP': 'Phone',
    'LR': 'Phone',
    'U': 'Phone',
    'OH': 'Phone',
    'DET.': 'Phone',
}


def normalize_chunk(
    chunk: pd.DataFrame,
    field: str,
    mapping: Dict[str, str],
    valid_values: Optional[List[str]] = None,
    default_value: Optional[str] = None
) -> pd.Series:
    """
    Normalize domain values for a chunk (for parallel processing).
    
    Args:
        chunk: DataFrame chunk
        field: Field name to normalize
        mapping: Normalization mapping dictionary
        valid_values: List of valid values for validation (optional)
        default_value: Default value if no mapping found (optional)
        
    Returns:
        Series with normalized values
    """
    if field not in chunk.columns:
        return pd.Series([], dtype=str)
    
    series = chunk[field].copy()
    
    # Convert to string and uppercase for matching
    upper_series = series.astype(str).str.strip().str.upper()
    
    # Apply direct mapping first
    normalized = upper_series.replace(mapping)
    
    # Handle nulls and empty strings
    normalized = normalized.replace(['NAN', 'NONE', ''], np.nan)
    
    # Find unmapped values (values not in mapping dictionary)
    mask_unmapped = ~upper_series.isin(mapping.keys())
    unmapped_series = series[mask_unmapped].copy()
    
    if len(unmapped_series) > 0:
        # Apply advanced normalization for unmapped values
        if field == 'Disposition':
            normalized[mask_unmapped] = _normalize_disposition_advanced(unmapped_series, valid_values, default_value)
        elif field == 'How Reported':
            normalized[mask_unmapped] = _normalize_how_reported_advanced(unmapped_series, valid_values, default_value)
        else:
            # For other fields, preserve original if no mapping found
            normalized[mask_unmapped] = unmapped_series
    
    # Handle any remaining NaN values (shouldn't happen after advanced normalization)
    mask_nan = normalized.isna()
    if mask_nan.any():
        if field == 'Disposition' and default_value:
            normalized[mask_nan] = default_value
        elif field == 'How Reported' and default_value:
            normalized[mask_nan] = default_value
        else:
            normalized[mask_nan] = series[mask_nan]
    
    return normalized


def _normalize_disposition_advanced(
    series: pd.Series,
    valid_values: Optional[List[str]] = None,
    default_value: str = 'Complete'
) -> pd.Series:
    """
    Advanced Disposition normalization for edge cases.
    
    Handles:
    - Concatenated values (e.g., "DispersedComplete" → "Dispersed")
    - Values with inserted text (e.g., "Other -G.O.A. See Notes" → "Other - See Notes")
    - Blank/empty values → default
    - Partial matches and abbreviations
    - Defaults to 'Complete' if no match found
    """
    if valid_values is None:
        valid_values = [
            'Advised', 'Arrest', 'Assisted', 'Checked OK', 'Canceled', 'Cleared',
            'Complete', 'Curbside Warning', 'Dispersed', 'Field Contact', 'G.O.A.',
            'Issued', 'Other - See Notes', 'Record Only', 'See Report', 'See Supplement',
            'TOT - See Notes', 'Temp. Settled', 'Transported', 'Unable to Locate', 'Unfounded'
        ]
    
    # Create uppercase lookup for valid values (sorted by length descending for longest match first)
    valid_upper = {v.upper(): v for v in sorted(valid_values, key=len, reverse=True)}
    
    # Create keyword mappings for partial matches
    keyword_mappings = {
        'COMPLETE': 'Complete',
        'ADVISED': 'Advised',
        'ARREST': 'Arrest',
        'ASSISTED': 'Assisted',
        'CANCEL': 'Canceled',
        'UNFOUNDED': 'Unfounded',
        'GOA': 'G.O.A.',
        'UNABLE': 'Unable to Locate',
        'UTL': 'Unable to Locate',
        'CHECKED': 'Checked OK',
        'OK': 'Checked OK',
        'CURBSIDE': 'Curbside Warning',
        'WARNING': 'Curbside Warning',
        'DISPERSED': 'Dispersed',
        'FIELD': 'Field Contact',
        'CONTACT': 'Field Contact',
        'ISSUED': 'Issued',
        'RECORD': 'Record Only',
        'REPORT': 'See Report',
        'SUPPLEMENT': 'See Supplement',
        'TEMP': 'Temp. Settled',
        'SETTLED': 'Temp. Settled',
        'TRANSPORT': 'Transported',
        'OTHER': 'Other - See Notes',
        'NOTES': 'Other - See Notes',
        'TOT': 'TOT - See Notes',
    }
    
    result = pd.Series(index=series.index, dtype=object)
    
    for idx, value in series.items():
        if pd.isna(value) or str(value).strip() == '':
            # Blank values default to 'Complete'
            result[idx] = default_value
            continue
        
        value_str = str(value).strip()
        value_upper = value_str.upper()
        
        # Check if already valid
        if value_upper in valid_upper:
            result[idx] = valid_upper[value_upper]
            continue
        
        # Special handling for "See OCA#" variations (case-insensitive)
        if 'OCA#' in value_upper or 'OCA' in value_upper:
            if 'SEE' in value_upper or 'NOTES' in value_upper:
                result[idx] = 'Other - See Notes'
                continue
        
        # Special handling for "Other - See Notes" with inserted text
        # Example: "Other -G.O.A. See Notes" → "Other - See Notes"
        if 'OTHER' in value_upper and ('SEE NOTES' in value_upper or 'NOTES' in value_upper):
            # Remove common inserted patterns
            cleaned = value_upper.replace('G.O.A.', '').replace('GOA', '').replace('  ', ' ').strip()
            if 'OTHER' in cleaned and ('SEE NOTES' in cleaned or 'NOTES' in cleaned):
                result[idx] = 'Other - See Notes'
                continue
        
        # Try keyword matching for partial matches
        found_match = False
        for keyword, mapped_value in keyword_mappings.items():
            if keyword in value_upper:
                # Prefer longer keywords (more specific matches)
                if len(keyword) >= 4 or value_upper.startswith(keyword):
                    result[idx] = mapped_value
                    found_match = True
                    break
        
        if found_match:
            continue
        
        # Try to extract first valid value from concatenated string
        # Example: "DispersedComplete" → "Dispersed" (first half that matches)
        for valid_upper_key, valid_value in valid_upper.items():
            # Check if value starts with valid key (handles concatenated values)
            if value_upper.startswith(valid_upper_key):
                result[idx] = valid_value
                found_match = True
                break
            
            # Check if valid key appears at the beginning of a word boundary
            # This handles cases like "AdvisedAssisted" where we want "Advised"
            if len(value_upper) >= len(valid_upper_key):
                # Check if first part matches
                if value_upper[:len(valid_upper_key)] == valid_upper_key:
                    result[idx] = valid_value
                    found_match = True
                    break
            
            # Check if valid key is contained in value (handles partial matches)
            if valid_upper_key in value_upper and len(valid_upper_key) >= 5:
                result[idx] = valid_value
                found_match = True
                break
        
        # If no match found, use default
        if not found_match:
            result[idx] = default_value
    
    return result


def _normalize_how_reported_advanced(
    series: pd.Series,
    valid_values: Optional[List[str]] = None,
    default_value: str = 'Phone'
) -> pd.Series:
    """
    Advanced How Reported normalization for edge cases.
    
    Handles:
    - Concatenated values (e.g., "9-1-1 Walk-In" → "9-1-1" - first value that matches dictionary)
    - Pattern matching: starts with "R"/"r" → "Radio", "P"/"p" → "Phone", starts with "9" → "9-1-1"
    - Special characters like "[" → "Phone"
    - Defaults to 'Phone' if no match found
    """
    if valid_values is None:
        valid_values = [
            '9-1-1', 'Walk-In', 'Phone', 'Self-Initiated', 'Radio', 'Teletype',
            'Fax', 'Other - See Notes', 'eMail', 'Mail', 'Virtual Patrol', 'Canceled Call'
        ]
    
    # Create uppercase lookup for valid values (sorted by length descending for longest match first)
    valid_upper = {v.upper(): v for v in sorted(valid_values, key=len, reverse=True)}
    
    result = pd.Series(index=series.index, dtype=object)
    
    for idx, value in series.items():
        if pd.isna(value) or str(value).strip() == '':
            # Empty values default to 'Phone'
            result[idx] = default_value
            continue
        
        value_str = str(value).strip()
        
        # Handle multi-line values - split and take first valid value
        if '\n' in value_str or '\r' in value_str:
            lines = value_str.replace('\r', '\n').split('\n')
            for line in lines:
                line_clean = line.strip()
                if line_clean:
                    value_str = line_clean
                    break
        
        value_upper = value_str.upper()
        
        # Check if already valid
        if value_upper in valid_upper:
            result[idx] = valid_upper[value_upper]
            continue
        
        # Pattern matching rules (in priority order)
        # 1. Remove trailing periods and special characters
        value_clean = value_str.rstrip('.')
        
        # 2. Values starting with "9" → "9-1-1"
        if value_clean and value_clean[0] == '9':
            result[idx] = '9-1-1'
            continue
        
        # 3. Values starting with "R" or "r" → "Radio" (but check for exceptions)
        if value_clean and value_clean[0].upper() == 'R':
            # Exception: single 'R' might be ambiguous, but pattern matching handles it
            if len(value_clean) == 1:
                result[idx] = 'Radio'
            elif value_upper.startswith('RADIO') or any(x in value_upper for x in ['RADIO', 'RAD']):
                result[idx] = 'Radio'
            else:
                result[idx] = 'Radio'  # Default for R-starting values
            continue
        
        # 4. Single character "P" or "p" → "Phone"
        if value_upper in ['P', 'P ']:
            result[idx] = 'Phone'
            continue
        
        # 5. Special characters like "[" → "Phone"
        if value_str in ['[', ']', '(', ')', '{', '}', '\\', '/', '.', '+', '`']:
            result[idx] = 'Phone'
            continue
        
        # 6. Handle concatenated values by extracting valid patterns
        # Look for common concatenations like "PhonRadioe" → extract "Phone" or "Radio"
        concatenated_patterns = [
            ('9-1-1', '9-1-1'),  # Check most specific first
            ('SELF-INITIATED', 'Self-Initiated'),
            ('WALK-IN', 'Walk-In'),
            ('TELEPHONE', 'Phone'),
            ('TELE', 'Teletype'),
            ('PHONE', 'Phone'),
            ('RADIO', 'Radio'),
            ('WALK', 'Walk-In'),
            ('SELF', 'Self-Initiated'),
            ('EMAIL', 'eMail'),
        ]
        
        found_concatenated = False
        for pattern, mapped_value in concatenated_patterns:
            if pattern in value_upper:
                # Prefer patterns that appear early in the string
                pattern_pos = value_upper.find(pattern)
                if pattern_pos >= 0 and pattern_pos < 5:  # Within first 5 chars
                    result[idx] = mapped_value
                    found_concatenated = True
                    break
        
        if found_concatenated:
            continue
        
        # 7. Try to extract first valid value from concatenated string
        # Example: "9-1-1 Walk-In" → "9-1-1" (first value that matches dictionary)
        found_match = False
        for valid_upper_key, valid_value in valid_upper.items():
            # Check if value starts with valid key (handles concatenated values)
            if value_upper.startswith(valid_upper_key):
                result[idx] = valid_value
                found_match = True
                break
            
            # Check if valid key appears at the beginning
            if len(value_upper) >= len(valid_upper_key):
                if value_upper[:len(valid_upper_key)] == valid_upper_key:
                    result[idx] = valid_value
                    found_match = True
                    break
            
            # For multi-word values, check if first word matches
            # Example: "9-1-1 Walk-In" should match "9-1-1" first
            if ' ' in valid_upper_key:
                first_word = valid_upper_key.split()[0]
                if value_upper.startswith(first_word):
                    result[idx] = valid_value
                    found_match = True
                    break
        
        # If no match found, use default
        if not found_match:
            result[idx] = default_value
    
    return result


class CompleteESRIOutputGenerator:
    """
    Complete ESRI output generator with all normalizations.
    
    Features:
    - Disposition normalization (30+ mappings)
    - How Reported normalization (25+ mappings)
    - Incident normalization (637 mappings from reference file)
    - Parallel processing for large datasets
    - Strict column ordering
    - Comprehensive validation and reporting
    """
    
    def __init__(
        self,
        incident_mapping_path: Optional[Path] = None,
        zonecalc_source: str = 'PDZone',
        n_workers: int = 4,
        enable_parallel: bool = True,
        enable_rms_backfill: bool = True,
        rms_dir: Optional[Path] = None
    ):
        """
        Initialize generator.
        
        Args:
            incident_mapping_path: Path to CallType_Categories_clean.csv
            zonecalc_source: Source for ZoneCalc ('PDZone' or 'Grid')
            n_workers: Number of parallel workers
            enable_parallel: Enable parallel processing for large datasets
            enable_rms_backfill: Enable RMS backfill for missing PDZone/Grid
            rms_dir: Path to RMS data directory
        """
        self.zonecalc_source = zonecalc_source
        self.n_workers = n_workers
        self.enable_parallel = enable_parallel
        self.enable_rms_backfill = enable_rms_backfill
        self.rms_dir = rms_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.stats = {
            'generator_version': '3.0_COMPLETE',
            'timestamp': self.timestamp,
            'normalization_applied': [],
            'rms_backfill_applied': False,
            'pdzone_backfilled': 0,
            'grid_backfilled': 0,
            'existing_pdzone_preserved': 0,
            'existing_grid_preserved': 0
        }
        
        # Load incident mapping
        self.incident_mapping = self._load_incident_mapping(incident_mapping_path)
    
    def _load_incident_mapping(
        self,
        path: Optional[Path] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        Load incident mapping from CallType_Categories_clean.csv.
        
        Args:
            path: Path to mapping file
            
        Returns:
            Dict mapping incident to normalized info
        """
        if path is None:
            # Try default locations
            possible_paths = [
                Path('ref/call_types/CallType_Categories_clean.csv'),
                Path('ref/CallType_Categories_clean.csv'),
                Path('CallType_Categories_clean.csv'),
            ]
            
            for p in possible_paths:
                if p.exists():
                    path = p
                    break
        
        if path is None or not path.exists():
            logger.warning("Incident mapping file not found, skipping incident normalization")
            return {}
        
        try:
            df = pd.read_csv(path)
            logger.info(f"Loaded incident mapping: {len(df)} entries from {path}")
            
            # Build mapping dict: uppercase incident -> normalized info
            mapping = {}
            for _, row in df.iterrows():
                incident = str(row['Incident']).strip()
                if incident and incident.upper() != 'NAN':
                    mapping[incident.upper()] = {
                        'Incident_Norm': str(row.get('Incident_Norm', incident)),
                        'Category_Type': str(row.get('Category_Type', '')),
                        'Response_Type': str(row.get('Response_Type', ''))
                    }
            
            self.stats['incident_mappings_loaded'] = len(mapping)
            return mapping
            
        except Exception as e:
            logger.error(f"Error loading incident mapping: {e}")
            return {}
    
    def _normalize_incident_vectorized(
        self,
        series: pd.Series,
        use_parallel: bool = False
    ) -> pd.Series:
        """
        Normalize Incident values using incident mapping with case-insensitive fallback.
        
        Args:
            series: Series to normalize
            use_parallel: Use parallel processing for large series
            
        Returns:
            Normalized series
        """
        if len(series) == 0 or not self.incident_mapping:
            return series
        
        # Create uppercase mapping for matching
        incident_map_upper = {
            k: v['Incident_Norm'] 
            for k, v in self.incident_mapping.items()
        }
        
        # Also create a reverse lookup: normalized value (uppercase) -> normalized value (proper case)
        # This helps with case-insensitive matching
        normalized_lookup = {}
        for norm_value in set(incident_map_upper.values()):
            normalized_lookup[norm_value.upper()] = norm_value
        
        # Convert to uppercase for matching
        upper_series = series.astype(str).str.strip().str.upper()
        
        # Apply direct mapping first
        normalized = upper_series.replace(incident_map_upper)
        
        # Handle nulls
        normalized = normalized.replace(['NAN', 'NONE', ''], np.nan)
        
        # For unmapped values, try case-insensitive matching against normalized values
        # This handles cases like "targeted Area Patrol" -> "Targeted Area Patrol"
        mask_unmapped = ~upper_series.isin(incident_map_upper.keys()) & (normalized == upper_series)
        if mask_unmapped.any():
            # Try to find case-insensitive match in normalized values
            unmapped_values = upper_series[mask_unmapped]
            for idx, val in unmapped_values.items():
                # First try exact uppercase match in normalized lookup
                if val in normalized_lookup:
                    normalized[idx] = normalized_lookup[val]
                    continue
                
                # Try title case normalization for common patterns
                # Handle "targeted Area Patrol" -> "Targeted Area Patrol"
                original_val = series[idx]
                if isinstance(original_val, str) and len(original_val) > 0:
                    # Try title case on first word
                    words = original_val.split()
                    if len(words) > 0:
                        # Capitalize first letter of first word
                        title_case = ' '.join([words[0].capitalize()] + words[1:])
                        title_upper = title_case.upper()
                        if title_upper in normalized_lookup:
                            normalized[idx] = normalized_lookup[title_upper]
                            continue
                        # Also try if title case matches any normalized value directly
                        if title_upper in incident_map_upper:
                            normalized[idx] = incident_map_upper[title_upper]
                            continue
                
                # Try fuzzy matching: check if any normalized value contains this value or vice versa
                # This handles partial matches and case variations
                for norm_upper, norm_proper in normalized_lookup.items():
                    # Exact match (already handled above, but check again)
                    if val == norm_upper:
                        normalized[idx] = norm_proper
                        break
                    # Check if value is contained in normalized (handles abbreviations)
                    elif val in norm_upper or norm_upper in val:
                        # Prefer longer match
                        if len(norm_upper) >= len(val) * 0.8:  # At least 80% match
                            normalized[idx] = norm_proper
                            break
        
        # Preserve original if still no mapping found
        mask_final = normalized == upper_series
        normalized[mask_final] = series[mask_final]
        
        return normalized
    
    def _normalize_disposition_vectorized(
        self,
        series: pd.Series,
        use_parallel: bool = False
    ) -> pd.Series:
        """
        Normalize Disposition values using vectorized operations.
        
        Args:
            series: Series to normalize
            use_parallel: Use parallel processing for large series
            
        Returns:
            Normalized series
        """
        if len(series) == 0:
            return series
        
        # For large datasets, use parallel processing
        if use_parallel and len(series) > 50000 and self.enable_parallel:
            df = pd.DataFrame({'Disposition': series})
            chunk_size = max(10000, len(df) // self.n_workers)
            chunks = [df.iloc[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
            
            results = []
            with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
                valid_dispositions = [
                    'Advised', 'Arrest', 'Assisted', 'Checked OK', 'Canceled', 'Cleared',
                    'Complete', 'Curbside Warning', 'Dispersed', 'Field Contact', 'G.O.A.',
                    'Issued', 'Other - See Notes', 'Record Only', 'See Report', 'See Supplement',
                    'TOT - See Notes', 'Temp. Settled', 'Transported', 'Unable to Locate', 'Unfounded'
                ]
                futures = {
                    executor.submit(
                        normalize_chunk,
                        chunk,
                        'Disposition',
                        DISPOSITION_MAPPING,
                        valid_dispositions,
                        'Complete'
                    ): i for i, chunk in enumerate(chunks)
                }
                
                for future in as_completed(futures):
                    results.append(future.result())
            
            return pd.concat(results)
        
        # Single-threaded normalization
        valid_dispositions = [
            'Advised', 'Arrest', 'Assisted', 'Checked OK', 'Canceled', 'Cleared',
            'Complete', 'Curbside Warning', 'Dispersed', 'Field Contact', 'G.O.A.',
            'Issued', 'Other - See Notes', 'Record Only', 'See Report', 'See Supplement',
            'TOT - See Notes', 'Temp. Settled', 'Transported', 'Unable to Locate', 'Unfounded'
        ]
        return normalize_chunk(
            pd.DataFrame({'Disposition': series}),
            'Disposition',
            DISPOSITION_MAPPING,
            valid_values=valid_dispositions,
            default_value='Complete'
        )
    
    def _normalize_how_reported_vectorized(
        self,
        series: pd.Series,
        use_parallel: bool = False
    ) -> pd.Series:
        """
        Normalize How Reported values using vectorized operations.
        
        Args:
            series: Series to normalize
            use_parallel: Use parallel processing for large series
            
        Returns:
            Normalized series
        """
        if len(series) == 0:
            return series
        
        # For large datasets, use parallel processing
        if use_parallel and len(series) > 50000 and self.enable_parallel:
            df = pd.DataFrame({'How Reported': series})
            chunk_size = max(10000, len(df) // self.n_workers)
            chunks = [df.iloc[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
            
            results = []
            with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
                valid_how_reported = [
                    '9-1-1', 'Walk-In', 'Phone', 'Self-Initiated', 'Radio', 'Teletype',
                    'Fax', 'Other - See Notes', 'eMail', 'Mail', 'Virtual Patrol', 'Canceled Call'
                ]
                futures = {
                    executor.submit(
                        normalize_chunk,
                        chunk,
                        'How Reported',
                        HOW_REPORTED_MAPPING,
                        valid_how_reported,
                        'Phone'
                    ): i for i, chunk in enumerate(chunks)
                }
                
                for future in as_completed(futures):
                    results.append(future.result())
            
            return pd.concat(results)
        
        # Single-threaded normalization
        valid_how_reported = [
            '9-1-1', 'Walk-In', 'Phone', 'Self-Initiated', 'Radio', 'Teletype',
            'Fax', 'Other - See Notes', 'eMail', 'Mail', 'Virtual Patrol', 'Canceled Call'
        ]
        return normalize_chunk(
            pd.DataFrame({'How Reported': series}),
            'How Reported',
            HOW_REPORTED_MAPPING,
            valid_values=valid_how_reported,
            default_value='Phone'
        )
    
    def _create_zonecalc(self, df: pd.DataFrame) -> pd.Series:
        """Create ZoneCalc column from PDZone or Grid."""
        if 'PDZone' in df.columns:
            zonecalc = df['PDZone'].copy()
            zonecalc = zonecalc.astype(str).replace('nan', '').replace('None', '')
            zonecalc = zonecalc.replace('', np.nan)
            zonecalc = pd.to_numeric(zonecalc, errors='coerce')
            self.stats['zonecalc_source'] = 'PDZone'
            return zonecalc
        elif 'Grid' in df.columns and self.zonecalc_source == 'Grid':
            zonecalc = df['Grid'].copy()
            self.stats['zonecalc_source'] = 'Grid'
            return zonecalc
        else:
            return pd.Series([np.nan] * len(df), index=df.index)
    
    def _prepare_polished_output(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare polished ESRI output with strict column order and normalization.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Polished DataFrame with ESRI column order
        """
        logger.info("Preparing polished ESRI output...")
        polished = pd.DataFrame(index=df.index)
        
        # Determine if parallel processing should be used
        use_parallel = len(df) > 50000 and self.enable_parallel
        
        # Required columns in exact order
        for col in ESRI_REQUIRED_COLUMNS:
            if col == 'ZoneCalc':
                polished[col] = self._create_zonecalc(df)
            
            elif col == 'Incident':
                if 'Incident' in df.columns and self.incident_mapping:
                    logger.info("Normalizing Incident values...")
                    polished[col] = self._normalize_incident_vectorized(
                        df['Incident'],
                        use_parallel=False  # Incident mapping is lookup, not compute intensive
                    )
                    self.stats['normalization_applied'].append('Incident')
                elif 'Incident' in df.columns:
                    polished[col] = df['Incident']
                else:
                    polished[col] = np.nan
            
            elif col == 'Disposition':
                if 'Disposition' in df.columns:
                    logger.info("Normalizing Disposition values...")
                    polished[col] = self._normalize_disposition_vectorized(
                        df['Disposition'],
                        use_parallel=use_parallel
                    )
                    self.stats['normalization_applied'].append('Disposition')
                else:
                    polished[col] = np.nan
            
            elif col == 'How Reported':
                if 'How Reported' in df.columns:
                    logger.info("Normalizing How Reported values...")
                    polished[col] = self._normalize_how_reported_vectorized(
                        df['How Reported'],
                        use_parallel=use_parallel
                    )
                    self.stats['normalization_applied'].append('How Reported')
                else:
                    polished[col] = np.nan
            
            elif col == 'Hour_Calc':
                if 'Time of Call' in df.columns:
                    # Get Time of Call column - check if already datetime, otherwise convert
                    time_col_raw = df['Time of Call']
                    if pd.api.types.is_datetime64_any_dtype(time_col_raw):
                        time_col = time_col_raw
                    else:
                        # Convert to datetime if not already
                        time_col = pd.to_datetime(time_col_raw, errors='coerce')
                    # Extract hour as integer 0-23 per Notion documentation
                    # Type: Integer, Format: 0-23, for numeric analysis
                    polished[col] = time_col.dt.hour.astype('float64')
                else:
                    polished[col] = np.nan
            
            else:
                # Direct mapping from input
                if col in df.columns:
                    polished[col] = df[col]
                else:
                    polished[col] = np.nan
        
        # Ensure column order matches ESRI exactly
        polished = polished[ESRI_REQUIRED_COLUMNS]
        
        self.stats['polished_rows'] = len(polished)
        self.stats['polished_columns'] = len(polished.columns)
        
        return polished
    
    def _prepare_draft_output(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare draft output with all columns."""
        logger.info("Preparing draft output (all columns)...")
        draft = df.copy()
        self.stats['draft_rows'] = len(draft)
        self.stats['draft_columns'] = len(draft.columns)
        return draft
    
    def _generate_normalization_report(
        self,
        df_before: pd.DataFrame,
        df_after: pd.DataFrame,
        output_dir: Path
    ) -> Path:
        """Generate detailed normalization report."""
        report_path = output_dir / f"normalization_report_{self.timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Complete Domain Normalization Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Records**: {len(df_before):,}\n")
            f.write(f"**Normalizations Applied**: {', '.join(self.stats['normalization_applied'])}\n\n")
            
            # Incident analysis
            if 'Incident' in df_before.columns and 'Incident' in df_after.columns and self.incident_mapping:
                f.write("## Incident Normalization\n\n")
                
                before_counts = df_before['Incident'].value_counts()
                after_counts = df_after['Incident'].value_counts()
                
                f.write("### Before Normalization (Top 20)\n\n")
                for val, count in before_counts.head(20).items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write("\n### After Normalization (Top 20)\n\n")
                for val, count in after_counts.head(20).items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write(f"\n**Unique values before**: {len(before_counts)}\n")
                f.write(f"**Unique values after**: {len(after_counts)}\n")
                f.write(f"**Reduction**: {len(before_counts) - len(after_counts)} values standardized\n\n")
            
            # Disposition analysis
            if 'Disposition' in df_before.columns and 'Disposition' in df_after.columns:
                f.write("## Disposition Normalization\n\n")
                
                before_counts = df_before['Disposition'].value_counts()
                after_counts = df_after['Disposition'].value_counts()
                
                f.write("### Before Normalization (Top 20)\n\n")
                for val, count in before_counts.head(20).items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write("\n### After Normalization (Top 20)\n\n")
                for val, count in after_counts.head(20).items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write(f"\n**Unique values before**: {len(before_counts)}\n")
                f.write(f"**Unique values after**: {len(after_counts)}\n")
                f.write(f"**Reduction**: {len(before_counts) - len(after_counts)} values standardized\n\n")
            
            # How Reported analysis
            if 'How Reported' in df_before.columns and 'How Reported' in df_after.columns:
                f.write("## How Reported Normalization\n\n")
                
                before_counts = df_before['How Reported'].value_counts()
                after_counts = df_after['How Reported'].value_counts()
                
                f.write("### Before Normalization\n\n")
                for val, count in before_counts.items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write("\n### After Normalization\n\n")
                for val, count in after_counts.items():
                    f.write(f"- `{val}`: {count:,}\n")
                
                f.write(f"\n**Unique values before**: {len(before_counts)}\n")
                f.write(f"**Unique values after**: {len(after_counts)}\n")
                f.write(f"**Reduction**: {len(before_counts) - len(after_counts)} values standardized\n\n")
        
        logger.info(f"Normalization report: {report_path}")
        return report_path
    
    def _backfill_pdzone_from_rms(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Backfill missing PDZone and Grid values from RMS.
        
        IMPORTANT: This preserves existing values - only backfills where missing.
        RMS backfill should ideally happen in master_pipeline BEFORE ESRI generation,
        but this provides a fallback when running ESRI generator directly.
        
        Args:
            df: Input DataFrame with ReportNumberNew column
            
        Returns:
            DataFrame with PDZone and Grid backfilled where missing
        """
        if not self.enable_rms_backfill:
            return df
        
        # Check if PDZone needs backfilling
        if 'PDZone' not in df.columns:
            df['PDZone'] = np.nan
        
        # Check if Grid needs backfilling
        if 'Grid' not in df.columns:
            df['Grid'] = np.nan
        
        # Count missing values (only where currently missing - preserve existing values)
        missing_pdzone = df['PDZone'].isna() | (df['PDZone'].astype(str).str.strip() == '')
        missing_grid = df['Grid'].isna() | (df['Grid'].astype(str).str.strip() == '')
        
        missing_pdzone_count = missing_pdzone.sum()
        missing_grid_count = missing_grid.sum()
        
        if missing_pdzone_count == 0 and missing_grid_count == 0:
            logger.info("No missing PDZone or Grid values to backfill")
            return df
        
        logger.info(f"Backfilling {missing_pdzone_count:,} missing PDZone and {missing_grid_count:,} missing Grid values from RMS...")
        
        try:
            # Load RMS data
            rms_df = self._load_rms_data()
            if rms_df.empty:
                logger.warning("No RMS data available for backfill")
                return df
            
            # Normalize join keys
            if 'ReportNumberNew' not in df.columns:
                logger.warning("ReportNumberNew column not found, cannot backfill from RMS")
                return df
            
            df['_join_key'] = df['ReportNumberNew'].astype(str).str.strip().str.upper()
            rms_df['_join_key'] = rms_df['Case Number'].astype(str).str.strip().str.upper()
            
            # Get Zone and Grid from RMS
            rms_fields = ['_join_key']
            if 'Zone' in rms_df.columns:
                rms_fields.append('Zone')
            if 'Grid' in rms_df.columns:
                rms_fields.append('Grid')
            
            rms_data = rms_df[rms_fields].drop_duplicates(subset='_join_key', keep='first')
            
            # Merge RMS data to CAD
            df_merged = df.merge(
                rms_data,
                on='_join_key',
                how='left',
                suffixes=('', '_rms')
            )
            
            # Backfill PDZone where missing (preserve existing values)
            if 'Zone' in rms_df.columns:
                backfill_pdzone_mask = missing_pdzone & df_merged['Zone'].notna()
                backfilled_pdzone_count = backfill_pdzone_mask.sum()
                
                if backfilled_pdzone_count > 0:
                    df.loc[backfill_pdzone_mask, 'PDZone'] = df_merged.loc[backfill_pdzone_mask, 'Zone']
                    self.stats['pdzone_backfilled'] = backfilled_pdzone_count
                    self.stats['rms_backfill_applied'] = True
                    logger.info(f"Backfilled {backfilled_pdzone_count:,} PDZone values from RMS Zone")
            
            # Backfill Grid where missing (preserve existing values)
            if 'Grid' in rms_df.columns:
                backfill_grid_mask = missing_grid & df_merged['Grid_rms'].notna()
                backfilled_grid_count = backfill_grid_mask.sum()
                
                if backfilled_grid_count > 0:
                    df.loc[backfill_grid_mask, 'Grid'] = df_merged.loc[backfill_grid_mask, 'Grid_rms']
                    self.stats['grid_backfilled'] = backfilled_grid_count
                    self.stats['rms_backfill_applied'] = True
                    logger.info(f"Backfilled {backfilled_grid_count:,} Grid values from RMS Grid")
            
            # Clean up temporary column
            df = df.drop('_join_key', axis=1, errors='ignore')
            
        except Exception as e:
            logger.warning(f"RMS backfill failed: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        return df
    
    def _load_rms_data(self) -> pd.DataFrame:
        """Load RMS data from directory."""
        if self.rms_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
            self.rms_dir = base_dir / 'data' / 'rms'
        
        rms_dir = Path(self.rms_dir)
        if not rms_dir.exists():
            logger.warning(f"RMS directory not found: {rms_dir}")
            return pd.DataFrame()
        
        # Find RMS files
        rms_files = list(rms_dir.glob('*.xlsx')) + list(rms_dir.glob('*.csv'))
        if not rms_files:
            logger.warning(f"No RMS files found in {rms_dir}")
            return pd.DataFrame()
        
        # Load RMS files (or combine if multiple)
        try:
            rms_dfs = []
            for rms_file in rms_files[:5]:  # Limit to first 5 files
                if rms_file.suffix == '.xlsx':
                    df = pd.read_excel(rms_file, engine='openpyxl')
                else:
                    # Try multiple encodings for CSV files
                    encodings = ['utf-8-sig', 'utf-8', 'latin1', 'cp1252', 'iso-8859-1']
                    df = None
                    for encoding in encodings:
                        try:
                            import io
                            with open(rms_file, 'r', encoding=encoding, errors='replace') as f:
                                df = pd.read_csv(io.StringIO(f.read()), low_memory=False)
                            break
                        except (UnicodeDecodeError, UnicodeError, Exception):
                            continue
                    if df is None:
                        logger.warning(f"Could not read {rms_file.name} with any encoding, skipping")
                        continue
                
                # Check for required columns (Case Number is required, Zone and Grid are optional)
                if 'Case Number' in df.columns:
                    cols_to_keep = ['Case Number']
                    if 'Zone' in df.columns:
                        cols_to_keep.append('Zone')
                    if 'Grid' in df.columns:
                        cols_to_keep.append('Grid')
                    rms_dfs.append(df[cols_to_keep])
            
            if rms_dfs:
                rms_df = pd.concat(rms_dfs, ignore_index=True)
                rms_df = rms_df.drop_duplicates(subset='Case Number', keep='first')
                logger.info(f"Loaded {len(rms_df):,} RMS records for backfill")
                return rms_df
            else:
                logger.warning("No RMS files with required column (Case Number)")
                return pd.DataFrame()
        except Exception as e:
            logger.warning(f"Error loading RMS data: {e}")
            return pd.DataFrame()
    
    def generate_outputs(
        self,
        df: pd.DataFrame,
        output_dir: Path,
        base_filename: str = "CAD_ESRI",
        format: str = 'excel'
    ) -> Dict[str, Path]:
        """
        Generate draft and polished ESRI outputs.
        
        Args:
            df: Input DataFrame
            output_dir: Output directory
            base_filename: Base filename for outputs
            format: Output format ('csv' or 'excel')
            
        Returns:
            Dict with paths to generated files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        outputs = {}
        
        # Backfill PDZone from RMS if needed
        df = self._backfill_pdzone_from_rms(df)
        
        # Store original for comparison
        df_original = df.copy()
        
        # Generate draft output
        draft_df = self._prepare_draft_output(df)
        draft_filename = f"{base_filename}_DRAFT_{self.timestamp}"
        
        if format == 'csv':
            draft_path = output_dir / f"{draft_filename}.csv"
            draft_df.to_csv(draft_path, index=False, encoding='utf-8-sig')
        else:
            draft_path = output_dir / f"{draft_filename}.xlsx"
            # Clean illegal Excel characters before writing
            draft_df_clean = draft_df.copy()
            for col in draft_df_clean.select_dtypes(include=['object']).columns:
                draft_df_clean[col] = draft_df_clean[col].astype(str).apply(
                    lambda x: ''.join(char for char in x if ord(char) >= 32 or char in '\t\n\r') if pd.notna(x) else x
                )
            draft_df_clean.to_excel(draft_path, index=False, engine='openpyxl')
        
        outputs['draft'] = draft_path
        logger.info(f"Draft output: {draft_path} ({len(draft_df):,} rows)")
        
        # Generate polished output
        polished_df = self._prepare_polished_output(df)
        polished_filename = f"{base_filename}_POLISHED_{self.timestamp}"
        
        if format == 'csv':
            polished_path = output_dir / f"{polished_filename}.csv"
            polished_df.to_csv(polished_path, index=False, encoding='utf-8-sig')
        else:
            polished_path = output_dir / f"{polished_filename}.xlsx"
            # Clean illegal Excel characters before writing
            polished_df_clean = polished_df.copy()
            for col in polished_df_clean.select_dtypes(include=['object']).columns:
                polished_df_clean[col] = polished_df_clean[col].astype(str).apply(
                    lambda x: ''.join(char for char in x if ord(char) >= 32 or char in '\t\n\r') if pd.notna(x) else x
                )
            polished_df_clean.to_excel(polished_path, index=False, engine='openpyxl')
        
        outputs['polished'] = polished_path
        logger.info(f"Polished output: {polished_path} ({len(polished_df):,} rows)")
        
        # Generate normalization report
        report_path = self._generate_normalization_report(
            df_original,
            polished_df,
            output_dir
        )
        outputs['normalization_report'] = report_path
        
        # Generate stats summary
        stats_path = output_dir / f"generation_stats_{self.timestamp}.json"
        import json
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_to_native(obj):
            """Recursively convert numpy types to native Python types."""
            if isinstance(obj, dict):
                return {key: convert_to_native(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(item) for item in obj]
            elif isinstance(obj, (np.integer, np.int64, np.int32)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            else:
                return obj
        
        stats_json = convert_to_native(self.stats)
        with open(stats_path, 'w') as f:
            json.dump(stats_json, f, indent=2)
        outputs['stats'] = stats_path
        
        return outputs


def main():
    """Main generation workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate complete ESRI outputs with all normalizations"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input dataset (CSV or Excel)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/03_final"),
        help="Output directory"
    )
    parser.add_argument(
        "--incident-mapping",
        type=Path,
        help="Path to CallType_Categories_clean.csv"
    )
    parser.add_argument(
        "--base-filename",
        default="CAD_ESRI",
        help="Base filename for outputs"
    )
    parser.add_argument(
        "--format",
        choices=['csv', 'excel'],
        default='excel',
        help="Output format"
    )
    parser.add_argument(
        "--zonecalc-source",
        choices=['PDZone', 'Grid'],
        default='PDZone',
        help="Source for ZoneCalc column"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers"
    )
    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel processing"
    )
    parser.add_argument(
        "--rms-dir",
        type=Path,
        help="Path to RMS data directory (for PDZone/Grid backfill)"
    )
    parser.add_argument(
        "--no-rms-backfill",
        action="store_true",
        help="Disable RMS backfill for missing PDZone/Grid"
    )
    
    args = parser.parse_args()
    
    # Load input
    logger.info(f"Loading input from {args.input}...")
    if args.input.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(args.input, engine='openpyxl')
    else:
        df = pd.read_csv(args.input, encoding='utf-8', encoding_errors='ignore')
    
    logger.info(f"Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    # Rename consolidated CSV columns to ESRI expected names
    column_renames = {
        'TimeOfCall': 'Time of Call',
        'TimeDispatched': 'Time Dispatched',
        'TimeOut': 'Time Out',
        'TimeIn': 'Time In',
        'TimeSpent': 'Time Spent',
        'TimeResponse': 'Time Response',
        'HowReported': 'How Reported'
    }
    df.rename(columns=column_renames, inplace=True)
    logger.info(f"Renamed columns for ESRI compatibility")
    
    # Generate outputs
    generator = CompleteESRIOutputGenerator(
        incident_mapping_path=args.incident_mapping,
        zonecalc_source=args.zonecalc_source,
        n_workers=args.workers,
        enable_parallel=not args.no_parallel,
        enable_rms_backfill=not args.no_rms_backfill,
        rms_dir=args.rms_dir
    )
    
    outputs = generator.generate_outputs(
        df,
        args.output_dir,
        args.base_filename,
        args.format
    )
    
    # Summary
    logger.info(f"\n{'='*80}")
    logger.info("Generation Complete")
    logger.info(f"{'='*80}")
    for output_type, path in outputs.items():
        logger.info(f"{output_type}: {path}")


if __name__ == "__main__":
    main()
