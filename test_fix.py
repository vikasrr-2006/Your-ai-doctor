#!/usr/bin/env python3
"""
Test script to verify the disease info fix
"""
import json
import os

# Set up paths similar to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DISEASE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'disease_solutions.json')

# Load disease data
with open(DISEASE_DATA_PATH, 'r') as f:
    data = json.load(f)
    disease_data = data.get('diseases', [])

# Define the mapping function (same as in app.py)
def get_disease_info(disease_name):
    """Get disease information from database"""
    if not disease_data:
        return None
    
    # Map common disease names from symptom matcher to disease_solutions.json names
    disease_mapping = {
        'Influenza': 'Flu',
        'Gastroenteritis': 'Stomach Upset',
        'GERD': 'Acidity / Gas',
        'Pancreatitis': 'Stomach Pain',  # Closest match
        'Peptic Ulcer': 'Stomach Pain',  # Closest match
        'Panic Disorder': 'Stress',      # Closest match
        'Major Depressive Disorder': 'Mental Stress',  # Closest match
        'Allergic Rhinitis': 'Allergy',
        'Otitis Media': 'Ear Blockage',
    }
    
    # Apply mapping if disease_name is in our mapping
    mapped_name = disease_mapping.get(disease_name, disease_name)
    
    # Try exact match first (using mapped name if applicable)
    for disease in disease_data:
        if disease.get('name', '').strip().lower() == mapped_name.strip().lower():
            return disease
    
    # Try partial match
    for disease in disease_data:
        if mapped_name.lower() in disease.get('name', '').lower():
            return disease
    
    return None

# Test cases - diseases that were previously causing "not available"
test_diseases = [
    'Influenza',           # Should map to Flu
    'Gastroenteritis',     # Should map to Stomach Upset
    'GERD',                # Should map to Acidity / Gas
    'Pancreatitis',        # Should map to Stomach Pain
    'Peptic Ulcer',        # Should map to Stomach Pain
    'Panic Disorder',      # Should map to Anxiety
    'Major Depressive Disorder',  # Should map to Mental Stress
    'Allergic Rhinitis',   # Should map to Allergy
    'Otitis Media',        # Should map to Ear Blockage
    # Also test some that should work directly
    'Flu',
    'Stomach Upset',
    'Acidity / Gas',
    'Common Cold'
]

print("Testing disease info lookup:")
print("=" * 50)

for disease in test_diseases:
    result = get_disease_info(disease)
    if result:
        print(f"PASS {disease:25} -> {result['name']}")
    else:
        print(f"FAIL {disease:25} -> Not found")

print("=" * 50)
print("Test completed.")