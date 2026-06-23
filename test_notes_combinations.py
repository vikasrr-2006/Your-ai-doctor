#!/usr/bin/env python3
"""
Script to test specific symptom combinations from the user's notes file
and see what disease names they return, and whether those are handled correctly.
"""
import sys
import os
import json

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

# Test cases - combinations that were previously problematic
test_cases = [
    # 2-symptom combinations (for comparison)
    (['Fever', 'Cough'], 'Common Cold', 'Fever + Cough (2 symptoms)'),
    
    # 3-symptom combinations that use our mapping
    (['Abdominal Pain', 'Diarrhea', 'Joint Pain'], 'Gastroenteritis', 'Abdominal Pain + Diarrhea + Joint Pain (3 symptoms)'),
    
    # 4-symptom combination that uses our mapping
    (['Abdominal Pain', 'Chest Pain', 'Cough', 'Nausea'], 'GERD', 'Abdominal Pain + Chest Pain + Cough + Nausea (4 symptoms)'),
    
    # 5-symptom combination that uses our mapping
    (['Abdominal Pain', 'Anxiety', 'Chest Pain', 'Dizziness', 'Shortness of Breath'], 'Panic Disorder', '5 symptoms to Panic Disorder'),
    
    # Single symptom (to test direct mapping)
    (['Insomnia'], 'Sleep Problem', 'Single symptom: Insomnia'),
]

print("Testing symptom combinations:")
print("=" * 60)

all_good = True
for symptoms, expected_prediction, description in test_cases:
    # Get related diseases from symptom mapper
    related_diseases = get_related_diseases(symptoms, min_probability=0.25)
    
    if not related_diseases:
        print(f"FAIL {description}")
        print(f"   Symptoms: {symptoms}")
        print(f"   No diseases found")
        all_good = False
        continue
    
    # Get the top prediction
    top_disease = related_diseases[0]
    predicted_disease = top_disease['disease']
    confidence = top_disease['probability']
    
    # Get disease info using our fixed function
    disease_info = get_disease_info(predicted_disease)
    
    # Check if prediction matches expected and if info is available
    prediction_matches = (expected_prediction.lower() == predicted_disease.lower())
    
    if disease_info is None:
        print(f"FAIL {description}")
        print(f"   Symptoms: {symptoms}")
        print(f"   Predicted disease: {predicted_disease} ({confidence}%)")
        print(f"   Disease info: NOT AVAILABLE (would show 'not available')")
        all_good = False
    else:
        status = "PASS" if prediction_matches else "INFO"
        print(f"{status} {description}")
        print(f"   Symptoms: {symptoms}")
        print(f"   Predicted disease: {predicted_disease} ({confidence}%)")
        print(f"   Expected from combinations: {expected_prediction} {'OK' if prediction_matches else 'DIFF'}")
        print(f"   Mapped to disease info: {disease_info['name']}")
    print()

print("=" * 60)
if all_good:
    print("ALL TESTS PASSED - No 'not available' issues detected for these combinations!")
else:
    print("SOME TESTS FAILED - These combinations would show 'not available' information.")
print("=" * 60)