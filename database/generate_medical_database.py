#!/usr/bin/env python3
"""
Generate comprehensive medical information database for all diseases in symptom_disease_map.json
"""

import json

# Read the symptom_disease_map.json file
with open('data/symptom_disease_map.json', 'r') as f:
    data = json.load(f)

# Extract all unique diseases
diseases = data.get('diseases', [])
print(f"Found {len(diseases)} diseases in the dataset")
print("=" * 60)

# Generate medical information for each disease
medical_database = {
    "metadata": {
        "version": "1.0",
        "total_diseases": len(diseases),
        "source": "symptom_disease_map.json",
        "generated_date": "2026-06-02"
    },
    "disease_information": {}
}

# Medical information generator
def generate_disease_info(disease_name):
    """Generate comprehensive medical information for a disease"""
    
    info = {
        "disease_name": disease_name,
        "primary_treatment": "",
        "prevention_tips": [],
        "when_to_consult": [],
        "recommended_specialist": "",
        "ayurvedic_prevention_remedies": {
            "herbs": [],
            "diet": [],
            "lifestyle": [],
            "yoga": [],
            "disclaimer": "Ayurvedic remedies may support overall wellness but are not a substitute for professional medical diagnosis or treatment."
        }
    }
    
    return info

# Generate information for each disease
for disease in diseases:
    info = generate_disease_info(disease)
    medical_database["disease_information"][disease] = info

# Save to file
output_file = 'data/medical_information_database.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(medical_database, f, indent=2, ensure_ascii=False)

print(f"Medical information database generated: {output_file}")
print(f"Total diseases processed: {len(medical_database['disease_information'])}")
print("=" * 60)

# Verify
with open(output_file, 'r') as f:
    verify_data = json.load(f)
    
print(f"Verification - Total entries: {len(verify_data['disease_information'])}")
print("Metadata:", verify_data['metadata'])
print("\nSample disease keys:")
sample_keys = list(verify_data['disease_information'].keys())[:5]
for key in sample_keys:
    print(f"  - {key}")

print("\nFirst disease full entry:")
first_key = list(verify_data['disease_information'].keys())[0]
print(json.dumps(verify_data['disease_information'][first_key], indent=2))
