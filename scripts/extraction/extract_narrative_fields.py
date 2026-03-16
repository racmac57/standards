#!/usr/bin/env python3
"""
RMS Narrative Field Extractor v1.0
Extracts structured data from RMS Narrative field using pattern matching and NLP.

Based on extraction hints from rms_export_field_definitions.md

Usage:
    python extract_narrative_fields.py input_file.csv [output_file.csv]

Extracts:
    - Suspect descriptions (physical characteristics, clothing)
    - Vehicle information (type, color, make, model, plate)
    - Property details (items, values, serial numbers)
    - Modus Operandi (M.O.) - method of entry, tools used
    - Temporal indicators (date/time patterns)
"""

import re
import csv
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import pandas as pd
from datetime import datetime


@dataclass
class SuspectDescription:
    """Extracted suspect description."""
    gender: Optional[str] = None
    race: Optional[str] = None
    age_range: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    clothing_upper: Optional[str] = None
    clothing_lower: Optional[str] = None
    distinguishing_features: Optional[str] = None
    raw_text: Optional[str] = None


@dataclass
class VehicleDescription:
    """Extracted vehicle description."""
    vehicle_type: Optional[str] = None
    color: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    plate: Optional[str] = None
    state: Optional[str] = None
    raw_text: Optional[str] = None


@dataclass
class PropertyInfo:
    """Extracted property information."""
    item_description: Optional[str] = None
    quantity: Optional[int] = None
    value: Optional[float] = None
    serial_number: Optional[str] = None
    brand: Optional[str] = None
    raw_text: Optional[str] = None


@dataclass
class ModusOperandi:
    """Extracted M.O. information."""
    entry_point: Optional[str] = None
    entry_method: Optional[str] = None
    tools_used: Optional[str] = None
    time_of_day: Optional[str] = None
    duration: Optional[str] = None
    raw_text: Optional[str] = None


class NarrativeExtractor:
    """Extract structured data from RMS narrative text."""

    def __init__(self):
        # Suspect-related patterns
        self.gender_patterns = r'\b(male|female|man|woman|boy|girl)\b'
        self.race_patterns = r'\b(white|black|hispanic|asian|native american|middle eastern|latino|latina)\b'
        self.age_patterns = r'\b(\d{1,2})[\s-]?(?:to|-)[\s-]?(\d{1,2})[\s-]?(?:years?[\s-]?old|y/?o)|\b(\d{1,2})[\s-]?(?:years?[\s-]?old|y/?o)\b'
        self.height_patterns = r'\b(\d)\'[\s-]?(\d{1,2})"?|(\d{3})[\s-]?cm\b'
        self.weight_patterns = r'\b(\d{2,3})[\s-]?(?:lbs?|pounds?)\b'

        # Clothing patterns
        self.clothing_colors = r'\b(red|blue|green|black|white|gray|grey|brown|yellow|orange|purple|pink|tan|navy)\b'
        self.clothing_items = r'\b(hoodie|jacket|coat|shirt|t-shirt|jeans|pants|shorts|dress|skirt|hat|cap|shoes|boots|sneakers|sweatshirt)\b'

        # Vehicle patterns
        self.vehicle_types = r'\b(car|sedan|suv|truck|van|motorcycle|bike|vehicle|coupe|convertible|minivan|pickup)\b'
        self.vehicle_colors = r'\b(red|blue|green|black|white|gray|grey|silver|brown|yellow|gold|tan|beige|maroon)\b'
        self.vehicle_makes = r'\b(ford|toyota|honda|chevrolet|chevy|nissan|dodge|jeep|bmw|mercedes|audi|volkswagen|vw|hyundai|kia|mazda|subaru|lexus)\b'
        self.plate_patterns = r'\b([A-Z]{2,3}[\s-]?\d{3,4}|[A-Z]{3}[\s-]?[A-Z0-9]{3,4})\b'

        # Property patterns
        self.currency_patterns = r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)[\s-]?dollars?'
        self.serial_patterns = r'\b(?:serial|s/n|sn)[\s#:]*([A-Z0-9]{6,})\b'

        # M.O. patterns
        self.entry_points = r'\b(window|door|rear|front|side|back|basement|garage|balcony|roof)\b'
        self.entry_methods = r'\b(forced|pried|broke|broken|kicked|smashed|picked|unlocked|cut|jimmied)\b'
        self.tools = r'\b(crowbar|screwdriver|hammer|pry bar|tool|knife|wire|glass cutter)\b'

        # Temporal patterns
        self.time_patterns = r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?[\s]?(?:(am|pm|hours?))?\b'
        self.date_patterns = r'\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b'

    def extract_all(self, narrative: str, case_number: str = None) -> Dict:
        """Extract all available information from narrative."""
        if pd.isna(narrative) or not narrative.strip():
            return {}

        narrative_lower = narrative.lower()

        return {
            'case_number': case_number,
            'suspects': self.extract_suspects(narrative, narrative_lower),
            'vehicles': self.extract_vehicles(narrative, narrative_lower),
            'property': self.extract_property(narrative, narrative_lower),
            'modus_operandi': self.extract_mo(narrative, narrative_lower),
            'temporal_info': self.extract_temporal(narrative, narrative_lower)
        }

    def extract_suspects(self, narrative: str, narrative_lower: str) -> List[SuspectDescription]:
        """Extract suspect descriptions from narrative."""
        suspects = []

        # Find suspect-related sentences
        suspect_sentences = self._find_suspect_sentences(narrative)

        for sentence in suspect_sentences:
            suspect = SuspectDescription()
            sentence_lower = sentence.lower()

            # Gender
            gender_match = re.search(self.gender_patterns, sentence_lower)
            if gender_match:
                suspect.gender = gender_match.group(1).capitalize()

            # Race/ethnicity
            race_match = re.search(self.race_patterns, sentence_lower)
            if race_match:
                suspect.race = race_match.group(1).capitalize()

            # Age
            age_match = re.search(self.age_patterns, sentence_lower)
            if age_match:
                if age_match.group(1) and age_match.group(2):
                    suspect.age_range = f"{age_match.group(1)}-{age_match.group(2)}"
                elif age_match.group(3):
                    suspect.age_range = age_match.group(3)

            # Height
            height_match = re.search(self.height_patterns, sentence_lower)
            if height_match:
                if height_match.group(1) and height_match.group(2):
                    suspect.height = f"{height_match.group(1)}'{height_match.group(2)}\""
                elif height_match.group(3):
                    suspect.height = f"{height_match.group(3)} cm"

            # Weight
            weight_match = re.search(self.weight_patterns, sentence_lower)
            if weight_match:
                suspect.weight = f"{weight_match.group(1)} lbs"

            # Clothing
            clothing_info = self._extract_clothing(sentence_lower)
            suspect.clothing_upper = clothing_info.get('upper')
            suspect.clothing_lower = clothing_info.get('lower')

            suspect.raw_text = sentence

            # Only add if we extracted at least one attribute
            if any([suspect.gender, suspect.race, suspect.age_range, suspect.height,
                   suspect.weight, suspect.clothing_upper, suspect.clothing_lower]):
                suspects.append(suspect)

        return suspects

    def extract_vehicles(self, narrative: str, narrative_lower: str) -> List[VehicleDescription]:
        """Extract vehicle descriptions from narrative."""
        vehicles = []

        # Find vehicle-related sentences
        vehicle_sentences = self._find_vehicle_sentences(narrative)

        for sentence in vehicle_sentences:
            vehicle = VehicleDescription()
            sentence_lower = sentence.lower()

            # Vehicle type
            type_match = re.search(self.vehicle_types, sentence_lower)
            if type_match:
                vehicle.vehicle_type = type_match.group(1).upper()

            # Color
            color_match = re.search(self.vehicle_colors, sentence_lower)
            if color_match:
                vehicle.color = color_match.group(1).capitalize()

            # Make
            make_match = re.search(self.vehicle_makes, sentence_lower)
            if make_match:
                make = make_match.group(1).capitalize()
                if make.lower() == 'chevy':
                    make = 'Chevrolet'
                elif make.lower() == 'vw':
                    make = 'Volkswagen'
                vehicle.make = make

            # License plate
            plate_match = re.search(self.plate_patterns, sentence.upper())
            if plate_match:
                vehicle.plate = plate_match.group(1)

            # State (often follows plate)
            if vehicle.plate:
                state_match = re.search(r'\b([A-Z]{2})\s+(?:plate|registration)', sentence.upper())
                if state_match:
                    vehicle.state = state_match.group(1)

            vehicle.raw_text = sentence

            # Only add if we extracted at least one attribute
            if any([vehicle.vehicle_type, vehicle.color, vehicle.make, vehicle.plate]):
                vehicles.append(vehicle)

        return vehicles

    def extract_property(self, narrative: str, narrative_lower: str) -> List[PropertyInfo]:
        """Extract property information from narrative."""
        property_items = []

        # Find property-related sentences
        property_sentences = self._find_property_sentences(narrative)

        for sentence in property_sentences:
            prop = PropertyInfo()

            # Extract value
            value_match = re.search(self.currency_patterns, sentence, re.IGNORECASE)
            if value_match:
                value_str = value_match.group(1) or value_match.group(2)
                try:
                    prop.value = float(value_str.replace(',', ''))
                except:
                    pass

            # Extract serial number
            serial_match = re.search(self.serial_patterns, sentence, re.IGNORECASE)
            if serial_match:
                prop.serial_number = serial_match.group(1)

            # Extract item description (context around "stolen" or "taken")
            item_match = re.search(r'(?:stolen|taken|missing|recovered)[\s:]+([^,.;]{5,50})',
                                  sentence, re.IGNORECASE)
            if item_match:
                prop.item_description = item_match.group(1).strip()

            prop.raw_text = sentence

            if any([prop.item_description, prop.value, prop.serial_number]):
                property_items.append(prop)

        return property_items

    def extract_mo(self, narrative: str, narrative_lower: str) -> ModusOperandi:
        """Extract modus operandi information from narrative."""
        mo = ModusOperandi()

        # Entry point
        entry_point_match = re.search(self.entry_points, narrative_lower)
        if entry_point_match:
            # Get context around entry point
            context = self._get_context(narrative_lower, entry_point_match.start(), 30)
            mo.entry_point = entry_point_match.group(1).capitalize()
            mo.raw_text = context

        # Entry method
        method_match = re.search(self.entry_methods, narrative_lower)
        if method_match:
            mo.entry_method = method_match.group(1).capitalize()

        # Tools used
        tools_match = re.search(self.tools, narrative_lower)
        if tools_match:
            mo.tools_used = tools_match.group(1).capitalize()

        return mo if any([mo.entry_point, mo.entry_method, mo.tools_used]) else None

    def extract_temporal(self, narrative: str, narrative_lower: str) -> Dict:
        """Extract temporal information from narrative."""
        temporal = {
            'times_mentioned': [],
            'dates_mentioned': []
        }

        # Extract times
        for match in re.finditer(self.time_patterns, narrative_lower):
            hour = match.group(1)
            minute = match.group(2)
            period = match.group(4) if match.group(4) else ''
            temporal['times_mentioned'].append(f"{hour}:{minute} {period}".strip())

        # Extract dates
        for match in re.finditer(self.date_patterns, narrative):
            temporal['dates_mentioned'].append(match.group(0))

        return temporal if (temporal['times_mentioned'] or temporal['dates_mentioned']) else None

    def _find_suspect_sentences(self, narrative: str) -> List[str]:
        """Find sentences containing suspect descriptions."""
        suspect_keywords = ['suspect', 'subject', 'male', 'female', 'person', 'individual', 'wearing']
        return self._find_sentences_with_keywords(narrative, suspect_keywords)

    def _find_vehicle_sentences(self, narrative: str) -> List[str]:
        """Find sentences containing vehicle descriptions."""
        vehicle_keywords = ['vehicle', 'car', 'sedan', 'suv', 'truck', 'plate', 'registration', 'driven']
        return self._find_sentences_with_keywords(narrative, vehicle_keywords)

    def _find_property_sentences(self, narrative: str) -> List[str]:
        """Find sentences containing property information."""
        property_keywords = ['stolen', 'taken', 'missing', 'recovered', 'value', 'serial', 'item']
        return self._find_sentences_with_keywords(narrative, property_keywords)

    def _find_sentences_with_keywords(self, narrative: str, keywords: List[str]) -> List[str]:
        """Find sentences containing any of the given keywords."""
        sentences = re.split(r'[.!?]+', narrative)
        matching = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in keywords):
                matching.append(sentence)
        return matching

    def _extract_clothing(self, sentence: str) -> Dict:
        """Extract clothing descriptions."""
        clothing = {'upper': None, 'lower': None}

        # Find clothing items with colors
        color_matches = list(re.finditer(self.clothing_colors, sentence))
        item_matches = list(re.finditer(self.clothing_items, sentence))

        for item_match in item_matches:
            item = item_match.group(1)
            color = None

            # Look for color near this item (within 20 characters)
            for color_match in color_matches:
                if abs(color_match.start() - item_match.start()) < 20:
                    color = color_match.group(1)
                    break

            description = f"{color} {item}" if color else item

            # Categorize as upper or lower body
            upper_items = ['hoodie', 'jacket', 'coat', 'shirt', 't-shirt', 'sweatshirt']
            lower_items = ['jeans', 'pants', 'shorts', 'skirt']

            if item in upper_items and not clothing['upper']:
                clothing['upper'] = description
            elif item in lower_items and not clothing['lower']:
                clothing['lower'] = description

        return clothing

    def _get_context(self, text: str, pos: int, window: int = 50) -> str:
        """Get context around a position in text."""
        start = max(0, pos - window)
        end = min(len(text), pos + window)
        return text[start:end].strip()


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python extract_narrative_fields.py input_file.csv [output_file.csv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'narrative_extraction_output.csv'

    # Load data
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    if 'Narrative' not in df.columns:
        print("Error: CSV must contain 'Narrative' column")
        sys.exit(1)

    # Extract from each narrative
    extractor = NarrativeExtractor()
    results = []

    print(f"Extracting narrative fields from {len(df)} records...")

    for idx, row in df.iterrows():
        case_num = row.get('Case Number', f'Row {idx + 1}')
        narrative = row.get('Narrative', '')

        extracted = extractor.extract_all(narrative, case_num)

        # Flatten extracted data for CSV output
        for i, suspect in enumerate(extracted.get('suspects', [])):
            results.append({
                'case_number': case_num,
                'extraction_type': 'suspect',
                'index': i + 1,
                **{k: v for k, v in asdict(suspect).items() if k != 'raw_text'}
            })

        for i, vehicle in enumerate(extracted.get('vehicles', [])):
            results.append({
                'case_number': case_num,
                'extraction_type': 'vehicle',
                'index': i + 1,
                **{k: v for k, v in asdict(vehicle).items() if k != 'raw_text'}
            })

        for i, prop in enumerate(extracted.get('property', [])):
            results.append({
                'case_number': case_num,
                'extraction_type': 'property',
                'index': i + 1,
                **{k: v for k, v in asdict(prop).items() if k != 'raw_text'}
            })

        if extracted.get('modus_operandi'):
            mo = extracted['modus_operandi']
            results.append({
                'case_number': case_num,
                'extraction_type': 'modus_operandi',
                'index': 1,
                **{k: v for k, v in asdict(mo).items() if k != 'raw_text'}
            })

    # Save results
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        print(f"\n✓ Extracted {len(results)} items from narratives")
        print(f"✓ Output saved to: {output_file}")

        # Print summary
        extraction_counts = results_df['extraction_type'].value_counts()
        print("\nExtraction Summary:")
        for extraction_type, count in extraction_counts.items():
            print(f"  {extraction_type}: {count}")
    else:
        print("\n⚠ No narrative fields could be extracted")

    return 0


if __name__ == '__main__':
    sys.exit(main())
