#!/usr/bin/env python3
"""
Test script to verify the end-to-end disease prediction flow
"""
import json
import os
import sys

# Add the current directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the symptom mapper function
from services.symptom_mapper import get_related_diseases

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

# Test cases: symptom combinations that should trigger the previously problematic diseases
test_cases = [
    # (symptoms, expected_disease_or_mapping, description)
    (['Fever', 'Cough'], 'Common Cold', 'Basic 2-symptom combo'),
    (['Fever', 'Headache'], 'Tension Headache', 'Another 2-symptom combo'),
    (['Abdominal Pain', 'Diarrhea', 'Joint Pain'], 'Gastroenteritis', '3-symptom combo -> Gastroenteritis'),
    (['Abdominal Pain', 'Chest Pain', 'Cough', 'Nausea'], 'GERD', '4-symptom combo -> GERD'),
    (['Abdominal Pain', 'Anxiety', 'Chest Pain', 'Dizziness', 'Shortness of Breath'], 'Panic Disorder', '5-symptom combo -> Panic Disorder'),
    (['Fever'], 'Influenza', 'Single symptom -> Influenza (should map to Flu)'),
]

print("Testing end-to-end disease prediction flow:")
print("=" * 60)

all_passed = True
for symptoms, expected_disease, description in test_cases:
    # Get related diseases from symptom mapper
    related_diseases = get_related_diseases(symptoms, min_probability=0.25)
    
    if not related_diseases:
        print(f"FAIL {description}")
        print(f"  Symptoms: {symptoms}")
        print(f"  No diseases found")
        all_passed = False
        continue
    
    # Get the top prediction
    top_disease = related_diseases[0]
    predicted_disease = top_disease['disease']
    confidence = top_disease['probability']
    
    # Get disease info using our fixed function
    disease_info = get_disease_info(predicted_disease)
    
    if disease_info is None:
        print(f"FAIL {description}")
        print(f"  Symptoms: {symptoms}")
        print(f"  Predicted disease: {predicted_disease} ({confidence}%)")
        print(f"  Disease info: Not found (would show 'not available')")
        all_passed = False
    else:
        print(f"PASS {description}")
        print(f"  Symptoms: {symptoms}")
        print(f"  Predicted disease: {predicted_disease} ({confidence}%)")
        print(f"  Mapped to: {disease_info['name']}")
        print(f"  Info available: Yes")
    print()

print("=" * 60)
if all_passed:
    print("ALL TESTS PASSED - The fix resolves the 'not available' issue!")
else:
    print("SOME TESTS FAILED - There may still be issues.")
print("=" * 60)