import json

# Original diseases list
original_diseases = [
    "Acidity", "Acidity / Gas", "Allergic Rhinitis", "Allergy", "Anaphylaxis", "Anemia",
    "Angina", "Aortic Dissection", "Arthritis", "Asthma", "Asthma / Allergy", "Back Pain",
    "Body Ache", "Body Pain", "Breathing Problem", "Bronchitis", "COVID-19", "Chickenpox",
    "Chikungunya", "Chronic Fatigue", "Chronic Fatigue Syndrome", "Cold / Allergies",
    "Common Cold", "Contact Dermatitis", "Cough Syndrome", "Dengue", "Diabetes", "Dietary",
    "Dry Cough", "Ear Blockage", "Edema", "Endocarditis", "Eye Strain", "Fibromyalgia",
    "Food Poisoning", "GERD", "Gastroenteritis", "Gout", "Hearing Loss", "Heart Attack",
    "Heart Condition", "Heart Failure", "Herniated Disc", "Indigestion", "Infection",
    "Inflammation", "Influenza", "Loose Motion", "Low BP / Weakness", "Lupus", "Lyme Disease",
    "Major Depressive Disorder", "Measles", "Meniere's Disease", "Meningitis", "Mental Stress",
    "Migraine", "Muscle Strain", "Osteoarthritis", "Otitis Media", "Pancreatitis", "Panic Disorder",
    "Peptic Ulcer", "Pneumonia", "Psoriasis", "Psoriatic Arthritis", "Pulmonary Embolism",
    "Pyelonephritis", "Rash", "Rheumatoid Arthritis", "Scarlet Fever", "Skin Allergy",
    "Sleep Disorder", "Sleep Problem", "Stomach Pain", "Stomach Upset", "Stress",
    "Tension Headache", "Throat Infection", "Tonsillitis", "Typhoid", "Vertigo",
    "Viral Fever", "Viral Infection", "Weakness / Tiredness"
]

# Classification and cleaning mappings
symptoms_to_replace = {
    "Acidity": "Gastroesophageal Reflux Disease (GERD)",
    "Acidity / Gas": "Gastroesophageal Reflux Disease (GERD)",
    "Ear Blockage": "Otitis Media",
    "Breathing Problem": "Chronic Obstructive Pulmonary Disease (COPD)",
    "Body Pain": "Fibromyalgia",
    "Body Ache": "Viral Infection",
    "Dry Cough": "Upper Respiratory Infection",
    "Cough Syndrome": "Bronchitis",
    "Weakness / Tiredness": "Chronic Fatigue Syndrome",
    "Rash": "Contact Dermatitis",
    "Skin Allergy": "Allergic Contact Dermatitis",
    "Cold / Allergies": "Allergic Rhinitis",
    "Loose Motion": "Gastroenteritis",
    "Stomach Pain": "Gastritis",
    "Stomach Upset": "Gastroenteritis",
    "Indigestion": "Gastroesophageal Reflux Disease (GERD)",
    "Eye Strain": "Computer Vision Syndrome",
    "Sleep Problem": "Insomnia",
    "Mental Stress": "Anxiety Disorder",
    "Allergy": "Allergic Rhinitis"
}

generic_to_replace = {
    "Infection": "Bacterial Infection",
    "Inflammation": "Inflammatory Disease",
    "Heart Condition": "Coronary Artery Disease",
    "Dietary": "Nutritional Deficiency",
    "Back Pain": "Herniated Disc",
    "Muscle Strain": "Muscle Injury"
}

duplicates = {
    "Chronic Fatigue": "Myalgic Encephalomyelitis (Chronic Fatigue Syndrome)",
    "Chronic Fatigue Syndrome": "Myalgic Encephalomyelitis (Chronic Fatigue Syndrome)",
    "Arthritis": "Rheumatoid Arthritis",
    "Osteoarthritis": "Rheumatoid Arthritis",
    "Rheumatoid Arthritis": "Rheumatoid Arthritis",
    "Asthma / Allergy": "Asthma",
    "Vertigo": "Benign Paroxysmal Positional Vertigo",
    "Viral Fever": "Viral Infection",
    "Viral Infection": "Viral Infection",
    "Tension Headache": "Tension-Type Headache",
    "Throat Infection": "Tonsillitis",
    "Allergic Rhinitis": "Allergic Rhinitis",
    "Sleep Disorder": "Insomnia",
    "Stress": "Anxiety Disorder"
}

non_medical = ["Dietary", "Mental Stress", "Stress"]

# Build cleaned disease list
cleaned_diseases = {}
removed = []
replaced = []

for d in original_diseases:
    if d in non_medical:
        removed.append(d)
        continue
    if d in symptoms_to_replace:
        new_d = symptoms_to_replace[d]
        cleaned_diseases[new_d] = cleaned_diseases.get(new_d, 0) + 1
        replaced.append({"from": d, "to": new_d})
        continue
    if d in generic_to_replace:
        new_d = generic_to_replace[d]
        cleaned_diseases[new_d] = cleaned_diseases.get(new_d, 0) + 1
        replaced.append({"from": d, "to": new_d})
        continue
    if d in duplicates:
        new_d = duplicates[d]
        cleaned_diseases[new_d] = cleaned_diseases.get(new_d, 0) + 1
        if d != new_d:
            replaced.append({"from": d, "to": new_d})
        continue
    cleaned_diseases[d] = cleaned_diseases.get(d, 0) + 1

final_diseases = sorted(set(cleaned_diseases.keys()))

print("=== Classification Summary ===")
print(f"Original count: {len(original_diseases)}")
print(f"Removed labels: {removed}")
print(f"Replaced count: {len(replaced)}")
print(f"Final cleaned count: {len(final_diseases)}")
print()
print("Final disease list:")
for d in final_diseases:
    print(f"  - {d}")