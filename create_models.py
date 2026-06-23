import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import json

# Predefined symptoms list (exactly 25 essential symptoms)
SYMPTOMS = [
    'Fever', 'Cough', 'Headache', 'Fatigue', 'Sore Throat',
    'Runny Nose', 'Chest Pain', 'Shortness of Breath', 'Nausea',
    'Vomiting', 'Diarrhea', 'Abdominal Pain', 'Back Pain',
    'Joint Pain', 'Muscle Pain', 'Dizziness', 'Rash', 'Itching',
    'Swelling', 'Blurred Vision', 'Hearing Loss', 'Insomnia', 'Anxiety', 'Depression', 'Wheezing'
]

# Disease to symptoms mapping - Optimized for exactly 25 essential symptoms
DISEASE_SYMPTOMS = {
    # Respiratory - distinct patterns
    'Common Cold': ['Runny Nose', 'Sore Throat', 'Cough'],  
    'Flu': ['Fever', 'Muscle Pain', 'Headache', 'Cough', 'Fatigue'],  
    'Pneumonia': ['Fever', 'Cough', 'Shortness of Breath', 'Chest Pain', 'Fatigue'],  
    'Bronchitis': ['Cough', 'Wheezing', 'Sore Throat', 'Fatigue'],  
    'Asthma': ['Shortness of Breath', 'Wheezing', 'Chest Pain', 'Cough'],  

    # Neurological
    'Migraine': ['Headache', 'Nausea', 'Blurred Vision', 'Dizziness'],  

    # GI - distinct
    'Gastroenteritis': ['Nausea', 'Vomiting', 'Diarrhea', 'Abdominal Pain'],  
    'Food Poisoning': ['Nausea', 'Vomiting', 'Diarrhea', 'Fever', 'Abdominal Pain'],  

    # ENT
    'Sinusitis': ['Headache', 'Runny Nose', 'Cough'],  
    'Tonsillitis': ['Sore Throat', 'Swelling', 'Fever'],  
    'Ear Infection': ['Hearing Loss', 'Dizziness', 'Fever'],  

    # Chronic
    'Diabetes': ['Fatigue', 'Blurred Vision', 'Dizziness'],  
    'Hypertension': ['Headache', 'Dizziness', 'Chest Pain'],  
    'Arthritis': ['Joint Pain', 'Swelling', 'Back Pain'],  
    'Thyroid Disorder': ['Fatigue', 'Anxiety', 'Insomnia', 'Depression'],  
    'Anemia': ['Fatigue', 'Dizziness', 'Shortness of Breath'],  

    # Allergies & Skin
    'Allergies': ['Runny Nose', 'Itching', 'Rash'],
    'Eczema': ['Rash', 'Itching'],
    'Skin Infection': ['Rash', 'Itching', 'Swelling', 'Fever'],

    # Infectious
    'Malaria': ['Fever', 'Headache', 'Muscle Pain', 'Fatigue', 'Nausea', 'Vomiting'],
    'Dengue': ['Fever', 'Rash', 'Joint Pain', 'Muscle Pain', 'Fatigue'],
    'Typhoid': ['Fever', 'Headache', 'Fatigue', 'Abdominal Pain', 'Nausea'],
    'Chickenpox': ['Fever', 'Rash', 'Itching', 'Fatigue'],
    'Measles': ['Fever', 'Rash', 'Cough', 'Fatigue'],

    # Emergency
    'Heart Attack': ['Chest Pain', 'Shortness of Breath', 'Nausea', 'Fatigue', 'Dizziness'],
    'Appendicitis': ['Abdominal Pain', 'Nausea', 'Vomiting', 'Fever'],

    # Urological
    'Kidney Stone': ['Back Pain', 'Abdominal Pain', 'Nausea', 'Vomiting'],
    'Kidney Problem': ['Back Pain', 'Swelling', 'Fatigue'],

    # Musculoskeletal
    'Muscle Strain': ['Muscle Pain', 'Back Pain', 'Joint Pain'],

    # Metabolic
    'Low Blood Sugar': ['Dizziness', 'Fatigue', 'Anxiety', 'Blurred Vision'],

    # ENT
    'Swimmer\'s Ear': ['Hearing Loss', 'Dizziness'],
    'Otitis Media': ['Hearing Loss', 'Fever'],
    'Earwax Buildup': ['Hearing Loss'],

    # Eye
    'Eye Infection': ['Blurred Vision', 'Headache'],

    # Mental Health
    'Anxiety Disorder': ['Anxiety', 'Insomnia'],

    # Additional diseases matching symptom_disease_map.json
    'Acidity': ['Chest Pain', 'Nausea', 'Abdominal Pain'],
    'Acidity / Gas': ['Chest Pain', 'Nausea', 'Abdominal Pain'],
    'Allergic Rhinitis': ['Runny Nose', 'Itching', 'Sore Throat'],
    'Allergy': ['Runny Nose', 'Itching', 'Rash'],
    'Anaphylaxis': ['Rash', 'Itching', 'Swelling', 'Shortness of Breath'],
    'Angina': ['Chest Pain', 'Shortness of Breath', 'Fatigue'],
    'Aortic Dissection': ['Chest Pain', 'Back Pain', 'Shortness of Breath'],
    'Asthma / Allergy': ['Wheezing', 'Cough', 'Runny Nose'],
    'Back Pain': ['Back Pain', 'Muscle Pain', 'Joint Pain'],
    'Body Ache': ['Muscle Pain', 'Fatigue', 'Joint Pain'],
    'Body Pain': ['Muscle Pain', 'Joint Pain', 'Back Pain'],
    'Breathing Problem': ['Shortness of Breath', 'Cough', 'Chest Pain'],
    'Chronic Fatigue': ['Fatigue', 'Muscle Pain', 'Joint Pain', 'Dizziness'],
    'Cold / Allergies': ['Runny Nose', 'Sore Throat', 'Cough'],
    'Contact Dermatitis': ['Rash', 'Itching', 'Swelling'],
    'Cough Syndrome': ['Cough', 'Sore Throat', 'Runny Nose'],
    'COVID-19': ['Fever', 'Cough', 'Fatigue', 'Shortness of Breath'],
    'Chikungunya': ['Fever', 'Joint Pain', 'Muscle Pain', 'Rash'],
    'Chronic Fatigue Syndrome': ['Fatigue', 'Muscle Pain', 'Joint Pain', 'Dizziness'],
    'Dry Cough': ['Cough', 'Sore Throat', 'Runny Nose'],
    'Ear Blockage': ['Hearing Loss', 'Dizziness', 'Earwax Buildup'],
    'Edema': ['Swelling', 'Shortness of Breath', 'Fatigue'],
    'Endocarditis': ['Fever', 'Chest Pain', 'Fatigue', 'Shortness of Breath'],
    'Eye Strain': ['Blurred Vision', 'Headache', 'Dizziness'],
    'Fibromyalgia': ['Fatigue', 'Muscle Pain', 'Joint Pain', 'Dizziness'],
    'GERD': ['Chest Pain', 'Nausea', 'Abdominal Pain'],
    'Gout': ['Joint Pain', 'Swelling', 'Back Pain'],
    'Heart Condition': ['Chest Pain', 'Shortness of Breath', 'Fatigue'],
    'Heart Failure': ['Chest Pain', 'Shortness of Breath', 'Fatigue', 'Swelling'],
    'Herniated Disc': ['Back Pain', 'Muscle Pain', 'Joint Pain', 'Dizziness'],
    'Indigestion': ['Abdominal Pain', 'Nausea', 'Chest Pain', 'Fatigue'],
    'Infection': ['Fever', 'Swelling', 'Fatigue'],
    'Inflammation': ['Swelling', 'Joint Pain', 'Back Pain'],
    'Influenza': ['Fever', 'Muscle Pain', 'Headache', 'Cough', 'Fatigue'],
    'Loose Motion': ['Diarrhea', 'Abdominal Pain', 'Nausea'],
    'Low BP / Weakness': ['Dizziness', 'Fatigue', 'Shortness of Breath'],
    'Lupus': ['Fatigue', 'Joint Pain', 'Rash', 'Swelling'],
    'Lyme Disease': ['Fever', 'Rash', 'Joint Pain', 'Muscle Pain'],
    'Major Depressive Disorder': ['Depression', 'Anxiety', 'Insomnia', 'Fatigue'],
    'Meniere\'s Disease': ['Dizziness', 'Hearing Loss', 'Nausea', 'Blurred Vision'],
    'Meningitis': ['Fever', 'Headache', 'Nausea', 'Rash'],
    'Mental Stress': ['Anxiety', 'Insomnia', 'Depression', 'Headache'],
    'Musculoskeletal Issue': ['Muscle Pain', 'Back Pain', 'Joint Pain'],
    'Osteoarthritis': ['Joint Pain', 'Swelling', 'Back Pain'],
    'Pancreatitis': ['Abdominal Pain', 'Nausea', 'Vomiting'],
    'Peptic Ulcer': ['Abdominal Pain', 'Nausea', 'Chest Pain'],
    'Psoriasis': ['Rash', 'Itching', 'Joint Pain'],
    'Psoriatic Arthritis': ['Joint Pain', 'Swelling', 'Rash'],
    'Pulmonary Embolism': ['Shortness of Breath', 'Chest Pain', 'Cough'],
    'Pyelonephritis': ['Fever', 'Back Pain', 'Nausea'],
    'Rash': ['Rash', 'Itching', 'Fever'],
    'Rheumatoid Arthritis': ['Joint Pain', 'Swelling', 'Back Pain', 'Fatigue'],
    'Scarlet Fever': ['Fever', 'Rash', 'Sore Throat'],
    'Skin Allergy': ['Rash', 'Itching', 'Swelling'],
    'Sleep Disorder': ['Insomnia', 'Anxiety', 'Fatigue'],
    'Sleep Problem': ['Insomnia', 'Anxiety', 'Fatigue'],
    'Stomach Pain': ['Abdominal Pain', 'Nausea', 'Vomiting'],
    'Stomach Upset': ['Nausea', 'Vomiting', 'Abdominal Pain'],
    'Stress': ['Anxiety', 'Insomnia', 'Headache'],
    'Tension Headache': ['Headache', 'Anxiety', 'Insomnia'],
    'Throat Infection': ['Sore Throat', 'Fever', 'Cough'],
    'Vertigo': ['Dizziness', 'Nausea', 'Blurred Vision'],
    'Viral Fever': ['Fever', 'Headache', 'Muscle Pain'],
    'Viral Infection': ['Fever', 'Fatigue', 'Cough'],
    'Weakness / Tiredness': ['Fatigue', 'Dizziness', 'Muscle Pain'],
}

# Additional symptoms for variation (only from the 25 list)
ADDITIONAL_SYMPTOMS = {
    'Common Cold': [],
    'Flu': [],
    'Pneumonia': [],
    'Bronchitis': ['Shortness of Breath'],
    'Asthma': ['Cough'],
    'Migraine': [],
    'Gastroenteritis': [],
    'Food Poisoning': [],
    'Sinusitis': [],
    'Tonsillitis': [],
    'Ear Infection': [],
    'Diabetes': [],
    'Hypertension': [],
    'Arthritis': [],
    'Thyroid Disorder': [],
    'Anemia': [],
    'Allergies': [],
    'Eczema': [],
    'Skin Infection': [],
    'Malaria': ['Nausea', 'Vomiting'],
    'Dengue': ['Nausea'],
    'Typhoid': ['Diarrhea'],
    'Heart Attack': [],
    'Appendicitis': [],
    'Kidney Stone': [],
    'Kidney Problem': [],
    'Muscle Strain': [],
    'Low Blood Sugar': [],
    'Swimmer\'s Ear': [],
    'Otitis Media': [],
    'Earwax Buildup': [],
    'Eye Infection': [],
    'Anxiety Disorder': [],
    'Acidity': ['Cough'],
    'Acidity / Gas': ['Cough'],
    'Allergic Rhinitis': ['Cough'],
    'Allergy': [],
    'Anaphylaxis': ['Nausea', 'Vomiting'],
    'Angina': ['Back Pain'],
    'Aortic Dissection': ['Shoulder Pain'],
    'Asthma / Allergy': ['Sore Throat'],
    'Back Pain': [],
    'Body Ache': [],
    'Body Pain': [],
    'Breathing Problem': ['Wheezing'],
    'Chronic Fatigue': ['Insomnia'],
    'Cold / Allergies': ['Fever'],
    'Contact Dermatitis': ['Fever'],
    'Cough Syndrome': ['Wheezing'],
    'COVID-19': ['Fever', 'Cough'],
    'Chikungunya': ['Rash'],
    'Chronic Fatigue Syndrome': ['Insomnia'],
    'Dry Cough': ['Cough'],
    'Ear Blockage': ['Earwax Buildup'],
    'Edema': ['Swelling'],
    'Endocarditis': ['Fever'],
    'Eye Strain': ['Dizziness'],
    'Fibromyalgia': ['Headache', 'Dizziness'],
    'GERD': ['Chest Pain'],
    'Gout': ['Fever'],
    'Heart Condition': [],
    'Heart Failure': ['Swelling'],
    'Herniated Disc': ['Dizziness'],
    'Indigestion': ['Nausea'],
    'Infection': ['Pain'],
    'Inflammation': ['Fever'],
    'Influenza': ['Fever', 'Cough'],
    'Loose Motion': ['Vomiting'],
    'Low BP / Weakness': [],
    'Lupus': ['Fever', 'Rash'],
    'Lyme Disease': ['Fever', 'Rash'],
    'Major Depressive Disorder': ['Fatigue'],
    'Meniere\'s Disease': ['Rash'],
    'Meningitis': ['Fever'],
    'Mental Stress': ['Fatigue'],
    'Musculoskeletal Issue': ['Fatigue'],
    'Osteoarthritis': ['Joint Pain'],
    'Pancreatitis': ['Fever'],
    'Peptic Ulcer': ['Fever'],
    'Psoriasis': ['Joint Pain'],
    'Psoriatic Arthritis': ['Rash'],
    'Pulmonary Embolism': ['Cough'],
    'Pyelonephritis': ['Fever'],
    'Rash': ['Fever'],
    'Rheumatoid Arthritis': ['Fever'],
    'Scarlet Fever': ['Rash'],
    'Skin Allergy': ['Fever'],
    'Sleep Disorder': [],
    'Sleep Problem': [],
    'Stomach Pain': ['Diarrhea'],
    'Stomach Upset': ['Diarrhea'],
    'Stress': ['Fatigue'],
    'Tension Headache': ['Fatigue'],
    'Throat Infection': ['Swelling'],
    'Vertigo': ['Nausea'],
    'Viral Fever': ['Cough'],
    'Viral Infection': ['Cough'],
    'Weakness / Tiredness': [],
}

DISEASES = list(DISEASE_SYMPTOMS.keys())

print(f"Training models with {len(SYMPTOMS)} symptoms and {len(DISEASES)} diseases...")
print("\nDisease-Symptom mappings:")
for disease, symptoms in DISEASE_SYMPTOMS.items():
    print(f"  {disease}: {symptoms}")

# Generate training data with PROPER symptom-disease correlations
# Using weighted approach: clean samples get higher weight
np.random.seed(42)
X = []
y = []

# Generate samples for each disease
for disease_idx, disease in enumerate(DISEASES):
    primary_symptoms = DISEASE_SYMPTOMS[disease]

    # Generate 300 samples per disease with different quality levels
    # Level 1: Perfect match (60%) - all primary symptoms exactly
    for _ in range(180):
        symptom_vector = np.zeros(len(SYMPTOMS))
        for symptom in primary_symptoms:
            if symptom in SYMPTOMS:
                idx = SYMPTOMS.index(symptom)
                symptom_vector[idx] = 1
        X.append(symptom_vector)
        y.append(disease)

    # Level 2: Missing one symptom (25%) - 1 symptom missing
    for _ in range(75):
        symptom_vector = np.zeros(len(SYMPTOMS))
        missing_idx = np.random.randint(0, len(primary_symptoms))
        for i, symptom in enumerate(primary_symptoms):
            if symptom in SYMPTOMS and i != missing_idx:
                idx = SYMPTOMS.index(symptom)
                symptom_vector[idx] = 1
        X.append(symptom_vector)
        y.append(disease)

    # Level 3: Adding one noise symptom (15%) - 1 extra symptom
    for _ in range(45):
        symptom_vector = np.zeros(len(SYMPTOMS))
        for symptom in primary_symptoms:
            if symptom in SYMPTOMS:
                idx = SYMPTOMS.index(symptom)
                symptom_vector[idx] = 1
        # Add one random other symptom that's not in primary
        other_symptoms = [s for s in SYMPTOMS if s not in primary_symptoms]
        if other_symptoms:
            random_symptom = np.random.choice(other_symptoms)
            idx = SYMPTOMS.index(random_symptom)
            symptom_vector[idx] = 1
        X.append(symptom_vector)
        y.append(disease)

X = np.array(X)
y = np.array(y)

print(f"\nTotal training samples: {len(X)}")
print(f"Feature shape: {X.shape}")

# Train Decision Tree model
print("\nTraining Decision Tree model...")
dt_model = DecisionTreeClassifier(random_state=42, max_depth=15, min_samples_split=5)
dt_model.fit(X, y)

# Train Random Forest model
print("Training Random Forest model...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15, min_samples_split=5)
rf_model.fit(X, y)

# Save models
print("\nSaving models...")
with open('models/decision_tree.pkl', 'wb') as f:
    pickle.dump(dt_model, f)

with open('models/random_forest.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

print("Models created and saved successfully!")

# Verify model accuracy on training data
dt_train_acc = dt_model.score(X, y)
rf_train_acc = rf_model.score(X, y)
print(f"\nDecision Tree training accuracy: {dt_train_acc*100:.2f}%")
print(f"Random Forest training accuracy: {rf_train_acc*100:.2f}%")

# Test predictions with exactly 25 symptoms
print("\n--- Testing Model Predictions ---")
test_cases = [
    {'symptoms': ['Runny Nose', 'Sore Throat', 'Cough'], 'expected': ['Common Cold']},
    {'symptoms': ['Fever', 'Muscle Pain', 'Headache', 'Cough', 'Fatigue'], 'expected': ['Flu']},
    {'symptoms': ['Fever', 'Cough', 'Shortness of Breath', 'Chest Pain', 'Fatigue'], 'expected': ['Pneumonia']},
    {'symptoms': ['Cough', 'Wheezing', 'Sore Throat', 'Fatigue'], 'expected': ['Bronchitis']},
    {'symptoms': ['Shortness of Breath', 'Wheezing', 'Chest Pain'], 'expected': ['Asthma']},
    {'symptoms': ['Headache', 'Nausea', 'Blurred Vision', 'Dizziness'], 'expected': ['Migraine']},
    {'symptoms': ['Nausea', 'Vomiting', 'Diarrhea', 'Abdominal Pain'], 'expected': ['Gastroenteritis']},
    {'symptoms': ['Nausea', 'Vomiting', 'Diarrhea', 'Fever', 'Abdominal Pain'], 'expected': ['Food Poisoning']},
    {'symptoms': ['Headache', 'Runny Nose', 'Cough'], 'expected': ['Sinusitis']},
    {'symptoms': ['Sore Throat', 'Swelling', 'Fever'], 'expected': ['Tonsillitis']},
    {'symptoms': ['Hearing Loss', 'Dizziness', 'Fever'], 'expected': ['Ear Infection']},
    {'symptoms': ['Fatigue', 'Blurred Vision'], 'expected': ['Diabetes']},
    {'symptoms': ['Headache', 'Dizziness', 'Chest Pain'], 'expected': ['Hypertension']},
    {'symptoms': ['Joint Pain', 'Swelling', 'Back Pain'], 'expected': ['Arthritis']},
    {'symptoms': ['Fatigue', 'Anxiety', 'Insomnia', 'Depression'], 'expected': ['Thyroid Disorder']},
    {'symptoms': ['Fatigue', 'Dizziness', 'Shortness of Breath'], 'expected': ['Anemia']},
    {'symptoms': ['Runny Nose', 'Itching', 'Rash'], 'expected': ['Allergies']},
    {'symptoms': ['Fever', 'Headache', 'Muscle Pain', 'Fatigue'], 'expected': ['Malaria']},
    {'symptoms': ['Fever', 'Rash', 'Joint Pain', 'Muscle Pain', 'Fatigue'], 'expected': ['Dengue']},
]

for test in test_cases:
    # Create feature vector
    feature_vector = [1 if s in test['symptoms'] else 0 for s in SYMPTOMS]

    # Get predictions from both models
    dt_pred = dt_model.predict([feature_vector])[0]
    rf_pred = rf_model.predict([feature_vector])[0]

    dt_proba = dt_model.predict_proba([feature_vector]).max() * 100
    rf_proba = rf_model.predict_proba([feature_vector]).max() * 100

    print(f"\nInput: {test['symptoms']}")
    print(f"  Decision Tree: {dt_pred} ({dt_proba:.1f}%)")
    print(f"  Random Forest:  {rf_pred} ({rf_proba:.1f}%)")
    print(f"  Expected: {test['expected']}")

# Save disease information
disease_solutions = [
    {
        "name": "Common Cold",
        "treatment": "Rest, fluids, OTC cold medications, pain relievers, decongestants",
        "prevention": "Wash hands frequently, avoid close contact with sick people, don't touch your face",
        "when_to_consult": "Symptoms last more than 10 days, high fever over 101°F, or difficulty breathing",
        "specialization": "General Physician"
    },
    {
        "name": "Flu",
        "treatment": "Antiviral medications (if early), rest, fluids, pain relievers, fever reducers",
        "prevention": "Annual flu vaccine, wash hands frequently, avoid crowded places during flu season",
        "when_to_consult": "High fever (above 102°F), chest pain, shortness of breath, or symptoms worsen after improving",
        "specialization": "General Physician"
    },
    {
        "name": "Migraine",
        "treatment": "Pain relievers (ibuprofen, acetaminophen), triptans, anti-nausea meds, rest in dark room",
        "prevention": "Identify and avoid triggers, regular sleep schedule, manage stress, stay hydrated",
        "when_to_consult": "First migraine with severe symptoms, change in migraine pattern, or neurological symptoms",
        "specialization": "Neurologist"
    },
    {
        "name": "Gastroenteritis",
        "treatment": "Hydration with ORS, bland diet (BRAT), rest, anti-diarrheals if prescribed",
        "prevention": "Wash hands thoroughly, safe food handling, drink clean water, avoid contaminated foods",
        "when_to_consult": "Blood in stool, dehydration signs, high fever above 101°F, or symptoms last more than 3 days",
        "specialization": "Gastroenterologist"
    },
    {
        "name": "Pneumonia",
        "treatment": "Antibiotics (if bacterial), rest, fluids, oxygen therapy, fever reducers, breathing treatments",
        "prevention": "Pneumonia vaccine, good hygiene, quit smoking, manage chronic conditions",
        "when_to_consult": "High fever, chest pain, difficulty breathing, confusion, or cough with blood",
        "specialization": "Pulmonologist"
    },
    {
        "name": "Bronchitis",
        "treatment": "Bronchodilators, cough suppressants, fluids, rest, humidifier, pain relievers",
        "prevention": "Avoid smoking, wash hands, get flu vaccine, avoid air pollutants",
        "when_to_consult": "High fever, blood in mucus, shortness of breath, or symptoms last more than 3 weeks",
        "specialization": "Pulmonologist"
    },
    {
        "name": "Asthma",
        "treatment": "Quick-relief inhaler (albuterol), long-term control meds (inhalers), avoid triggers",
        "prevention": "Identify and avoid allergens, take controller medications regularly, regular check-ups",
        "when_to_consult": "Asthma attack not controlled by rescue inhaler, frequent symptoms, or nighttime symptoms",
        "specialization": "Pulmonologist"
    },
    {
        "name": "Diabetes",
        "treatment": "Diabetes medications or insulin, diet control, regular exercise, blood sugar monitoring",
        "prevention": "Healthy diet, regular exercise, maintain healthy weight, regular screening",
        "when_to_consult": "Any symptoms of high or low blood sugar, regular check-ups every 3-6 months",
        "specialization": "Endocrinologist"
    },
    {
        "name": "Hypertension",
        "treatment": "Lifestyle changes (diet, exercise), blood pressure medications, stress management",
        "prevention": "Low sodium diet, regular exercise, limit alcohol, maintain healthy weight, manage stress",
        "when_to_consult": "Blood pressure above 180/120, chest pain, vision problems, headache, or difficulty breathing",
        "specialization": "Cardiologist"
    },
    {
        "name": "Arthritis",
        "treatment": "Pain relievers, anti-inflammatory drugs, disease-modifying drugs, physical therapy, exercise",
        "prevention": "Maintain healthy weight, exercise regularly, protect joints, avoid injury",
        "when_to_consult": "Joint swelling, redness, warmth, severe pain, or reduced range of motion",
        "specialization": "Rheumatologist"
    },
    {
        "name": "Allergies",
        "treatment": "Antihistamines, nasal sprays, decongestants, eye drops, allergen avoidance",
        "prevention": "Identify and avoid allergens, keep home clean, use air purifiers, wash hands frequently",
        "when_to_consult": "Severe allergic reaction, breathing difficulties, or symptoms not controlled by OTC meds",
        "specialization": "Allergist"
    },
    {
        "name": "Sinusitis",
        "treatment": "Decongestants, nasal sprays, saline irrigation, antibiotics if bacterial, pain relievers",
        "prevention": "Treat allergies promptly, avoid pollutants, use humidifier, don't smoke",
        "when_to_consult": "Symptoms last more than 10 days, severe symptoms, or vision changes",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Tonsillitis",
        "treatment": "Antibiotics if bacterial (strep), pain relievers, rest, fluids, warm salt water gargle",
        "prevention": "Wash hands, avoid sharing utensils, maintain good hygiene",
        "when_to_consult": "Difficulty breathing, severe pain, high fever, or trouble swallowing",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Ear Infection",
        "treatment": "Pain relievers, ear drops, antibiotics if bacterial, warm compress",
        "prevention": "Keep ears dry, avoid cotton swabs, treat allergies promptly, don't smoke",
        "when_to_consult": "Severe pain, ear discharge, hearing loss, fever, or symptoms not improving",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Food Poisoning",
        "treatment": "Hydration with ORS, rest, bland diet, anti-diarrheals, IV fluids if severe",
        "prevention": "Cook food thoroughly, wash hands, store food properly, avoid risky foods",
        "when_to_consult": "Blood in stool, high fever, severe dehydration, or symptoms last more than 3 days",
        "specialization": "Gastroenterologist"
    },
    {
        "name": "Malaria",
        "treatment": "Antimalarial medication (prescribed based on type and location), rest, fluids",
        "prevention": "Mosquito nets, insect repellents, prophylaxis when traveling, eliminate breeding sites",
        "when_to_consult": "Fever, chills, or other symptoms after traveling to endemic areas",
        "specialization": "Infectious Disease Specialist"
    },
    {
        "name": "Dengue",
        "treatment": "Rest, fluids, paracetamol for fever (NOT NSAIDs), acetaminophen, monitor platelets",
        "prevention": "Mosquito control, repellents, eliminate standing water, wear protective clothing",
        "when_to_consult": "Severe abdominal pain, bleeding, sudden drop in platelet count, or warning signs",
        "specialization": "Infectious Disease Specialist"
    },
    {
        "name": "Thyroid Disorder",
        "treatment": "Thyroid hormone medication (levothyroxine), regular monitoring, lifestyle changes",
        "prevention": "Healthy diet with iodine, regular check-ups, manage stress, avoid radiation exposure",
        "when_to_consult": "Symptoms of thyroid imbalance, lumps in neck, or abnormal thyroid tests",
        "specialization": "Endocrinologist"
    },
    {
        "name": "Anemia",
        "treatment": "Iron supplements, vitamin B12 or folate, dietary changes, blood transfusions if severe",
        "prevention": "Iron-rich diet, regular check-ups, manage chronic conditions, prenatal care",
        "when_to_consult": "Severe fatigue, shortness of breath, dizziness, pale skin, or rapid heart rate",
        "specialization": "Hematologist"
    },
    {
        "name": "Eczema",
        "treatment": "Moisturizers, steroid creams, antihistamines",
        "prevention": "Avoid triggers, keep skin moisturized, use gentle soaps",
        "when_to_consult": "Severe itching, skin infection, or symptoms not improving",
        "specialization": "Dermatologist"
    },
    {
        "name": "Skin Infection",
        "treatment": "Antibiotics (oral or topical), keep area clean",
        "prevention": "Good hygiene, avoid scratching, keep wounds clean",
        "when_to_consult": "Spreading redness, fever, or pus drainage",
        "specialization": "Dermatologist"
    },
    {
        "name": "Typhoid",
        "treatment": "Antibiotics (azithromycin, ciprofloxacin), fluids, rest, fever reducers",
        "prevention": "Drink clean water, proper food hygiene, typhoid vaccination when traveling to endemic areas",
        "when_to_consult": "High sustained fever, abdominal pain, headache, or rose-colored rash, especially after travel to endemic regions",
        "specialization": "Infectious Disease Specialist"
    },
    {
        "name": "Chickenpox",
        "treatment": "Calamine lotion, fever reducers, rest",
        "prevention": "Vaccination, avoid contact with infected persons",
        "when_to_consult": "High fever, difficulty breathing, or severe rash",
        "specialization": "General Physician"
    },
    {
        "name": "Measles",
        "treatment": "Fever reducers, rest, vitamin A supplements",
        "prevention": "MMR vaccination, avoid contact with infected persons",
        "when_to_consult": "High fever, difficulty breathing, or severe complications",
        "specialization": "General Physician"
    },
    {
        "name": "Heart Attack",
        "treatment": "Emergency medical care, aspirin, clot-busting drugs, angioplasty, bypass surgery",
        "prevention": "Regular exercise, healthy diet, no smoking, manage cholesterol and blood pressure, manage stress",
        "when_to_consult": "Immediately call emergency services for chest pain with shortness of breath, sweating, nausea, or pain radiating to arm/jaw",
        "specialization": "Cardiologist"
    },
    {
        "name": "Appendicitis",
        "treatment": "Surgical removal (appendectomy), antibiotics before and after surgery, pain management",
        "prevention": "No known prevention, but high-fiber diet may reduce risk",
        "when_to_consult": "Immediately for severe right lower abdominal pain, nausea, vomiting, fever, or pain that starts around the navel and shifts to the right",
        "specialization": "General Surgeon"
    },
    {
        "name": "Kidney Stone",
        "treatment": "Pain relievers, increased water intake, alpha blockers, lithotripsy for large stones",
        "prevention": "Drink 2-3 liters of water daily, reduce sodium, limit oxalate-rich foods, moderate animal protein",
        "when_to_consult": "Severe flank pain, blood in urine, fever with chills, or inability to urinate",
        "specialization": "Urologist"
    },
    {
        "name": "Kidney Problem",
        "treatment": "Medications based on underlying cause, dietary changes, dialysis for severe cases",
        "prevention": "Stay hydrated, control blood pressure and diabetes, avoid excessive painkillers, healthy diet",
        "when_to_consult": "Swelling in legs/ankles, changes in urination, fatigue, or persistent back pain",
        "specialization": "Nephrologist"
    },
    {
        "name": "Muscle Strain",
        "treatment": "Rest, ice, compression, elevation (RICE), pain relievers, physical therapy if severe",
        "prevention": "Warm up before exercise, proper stretching, avoid overexertion, maintain good posture",
        "when_to_consult": "Severe pain, inability to move the affected area, swelling that doesn't improve, or numbness",
        "specialization": "Orthopedic Specialist"
    },
    {
        "name": "Low Blood Sugar",
        "treatment": "Consume fast-acting glucose (juice, candy), glucagon injection for severe cases",
        "prevention": "Regular meals, carry glucose tablets, monitor blood sugar if diabetic, avoid skipping meals",
        "when_to_consult": "Recurrent episodes, confusion, loss of consciousness, or blood sugar below 70 mg/dL with symptoms",
        "specialization": "Endocrinologist"
    },
    {
        "name": "Swimmer's Ear",
        "treatment": "Antibiotic ear drops, keeping ear dry, pain relievers",
        "prevention": "Dry ears after swimming, avoid inserting objects in ears, use ear plugs while swimming",
        "when_to_consult": "Ear pain, itching, discharge, or reduced hearing",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Earwax Buildup",
        "treatment": "Ear drops, irrigation, manual removal by doctor",
        "prevention": "Avoid using cotton swabs, regular ear cleaning",
        "when_to_consult": "Hearing loss, ear pain, dizziness, or feeling of fullness in ear",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Otitis Media",
        "treatment": "Antibiotics, pain relievers, ear drops",
        "prevention": "Avoid smoke, treat allergies promptly, breastfeed infants",
        "when_to_consult": "Ear pain, fever, hearing loss, or discharge from ear",
        "specialization": "ENT Specialist"
    },
    {
        "name": "Eye Infection",
        "treatment": "Antibiotic or antiviral eye drops, warm compress, good hygiene",
        "prevention": "Wash hands frequently, avoid touching eyes, don't share towels, replace eye makeup regularly",
        "when_to_consult": "Eye redness, discharge, pain, sensitivity to light, or vision changes",
        "specialization": "Ophthalmologist"
    },
    {
        "name": "Panic Disorder",
        "treatment": "Therapy, medications, breathing exercises",
        "prevention": "Stress management, regular exercise, avoid caffeine",
        "when_to_consult": "Frequent panic attacks affecting daily life",
        "specialization": "Psychiatrist"
    },
    {
        "name": "Anxiety Disorder",
        "treatment": "Therapy, medications, lifestyle changes",
        "prevention": "Stress management, regular exercise, avoid triggers",
        "when_to_consult": "Persistent anxiety affecting daily life",
        "specialization": "Psychiatrist"
    },
    {
        "name": "Depression",
        "treatment": "Therapy, medications, lifestyle changes",
        "prevention": "Regular exercise, social connections, stress management",
        "when_to_consult": "Persistent sadness, loss of interest, or thoughts of self-harm",
        "specialization": "Psychiatrist"
    }
]

with open('data/disease_solutions.json', 'w') as f:
    json.dump(disease_solutions, f, indent=4)

print("\nDisease information saved!")

# Save doctor database (same as before)
doctors_database = [
    {
        "name": "Dr. Sarah Johnson",
        "specialization": "General Physician",
        "hospital": "City Medical Center",
        "address": "123 Health Street, Downtown",
        "phone": "+1-555-0101",
        "rating": 4.8,
        "latitude": 40.7128,
        "longitude": -74.006,
        "district": "Mandya"
    },
    {
        "name": "Dr. Michael Chen",
        "specialization": "General Physician",
        "hospital": "Wellness Clinic",
        "address": "456 Care Avenue, Uptown",
        "phone": "+1-555-0102",
        "rating": 4.6,
        "latitude": 40.758,
        "longitude": -73.9855,
        "district": "Mandya"
    },
    {
        "name": "Dr. Emily Williams",
        "specialization": "Cardiologist",
        "hospital": "Heart Care Hospital",
        "address": "789 Heart Lane, Medical District",
        "phone": "+1-555-0201",
        "rating": 4.9,
        "latitude": 40.7489,
        "longitude": -73.968,
        "district": "Mandya"
    },
    {
        "name": "Dr. James Brown",
        "specialization": "Cardiologist",
        "hospital": "Cardiovascular Center",
        "address": "321 Pulse Road, East Side",
        "phone": "+1-555-0202",
        "rating": 4.7,
        "latitude": 40.7614,
        "longitude": -73.9776,
        "district": "Mandya"
    },
    {
        "name": "Dr. Lisa Anderson",
        "specialization": "Neurologist",
        "hospital": "Brain & Spine Institute",
        "address": "555 Neuro Way, West End",
        "phone": "+1-555-0301",
        "rating": 4.8,
        "latitude": 40.7549,
        "longitude": -73.984,
        "district": "Mandya"
    },
    {
        "name": "Dr. Robert Martinez",
        "specialization": "Neurologist",
        "hospital": "Neurology Associates",
        "address": "888 Mind Street, Central",
        "phone": "+1-555-0302",
        "rating": 4.5,
        "latitude": 40.742,
        "longitude": -73.99,
        "district": "Mandya"
    },
    {
        "name": "Dr. Jennifer Taylor",
        "specialization": "Pulmonologist",
        "hospital": "Respiratory Care Center",
        "address": "222 Breath Blvd, Lung District",
        "phone": "+1-555-0401",
        "rating": 4.7,
        "latitude": 40.73,
        "longitude": -74.0,
        "district": "Mandya"
    },
    {
        "name": "Dr. David Wilson",
        "specialization": "Pulmonologist",
        "hospital": "Lung Health Clinic",
        "address": "444 Air Avenue, North Side",
        "phone": "+1-555-0402",
        "rating": 4.6,
        "latitude": 40.75,
        "longitude": -73.97,
        "district": "Mandya"
    },
    {
        "name": "Dr. Amanda Lee",
        "specialization": "Gastroenterologist",
        "hospital": "Digestive Health Center",
        "address": "666 Stomach Street, GI District",
        "phone": "+1-555-0501",
        "rating": 4.9,
        "latitude": 40.74,
        "longitude": -73.985,
        "district": "Mandya"
    },
    {
        "name": "Dr. Christopher Davis",
        "specialization": "Gastroenterologist",
        "hospital": "GI Specialists",
        "address": "777 Digest Way, South End",
        "phone": "+1-555-0502",
        "rating": 4.4,
        "latitude": 40.72,
        "longitude": -73.995,
        "district": "Mandya"
    },
    {
        "name": "Dr. Michelle Garcia",
        "specialization": "Endocrinologist",
        "hospital": "Hormone Health Center",
        "address": "999 Gland Road, Endocrine Park",
        "phone": "+1-555-0601",
        "rating": 4.8,
        "latitude": 40.76,
        "longitude": -73.965,
        "district": "Mandya"
    },
    {
        "name": "Dr. Daniel Thompson",
        "specialization": "Endocrinologist",
        "hospital": "Metabolic Disorders Clinic",
        "address": "111 Hormone Lane, Wellness Area",
        "phone": "+1-555-0602",
        "rating": 4.6,
        "latitude": 40.735,
        "longitude": -73.975,
        "district": "Mandya"
    },
    {
        "name": "Dr. Rachel White",
        "specialization": "Rheumatologist",
        "hospital": "Joint & Bone Center",
        "address": "333 Arthritis Street, Ortho District",
        "phone": "+1-555-0701",
        "rating": 4.7,
        "latitude": 40.745,
        "longitude": -73.98,
        "district": "Mandya"
    },
    {
        "name": "Dr. Kevin Harris",
        "specialization": "Rheumatologist",
        "hospital": "Arthritis Treatment Center",
        "address": "444 Rheum Road, Mobility Hub",
        "phone": "+1-555-0702",
        "rating": 4.5,
        "latitude": 40.725,
        "longitude": -73.965,
        "district": "Mandya"
    },
    {
        "name": "Dr. Susan Clark",
        "specialization": "Allergist",
        "hospital": "Allergy & Immunology Center",
        "address": "555 Sneeze Way, Allergy Park",
        "phone": "+1-555-0801",
        "rating": 4.8,
        "latitude": 40.755,
        "longitude": -73.97,
        "district": "Mandya"
    },
    {
        "name": "Dr. Mark Lewis",
        "specialization": "Allergist",
        "hospital": "Immunology Associates",
        "address": "666 Itch Street, Reaction Center",
        "phone": "+1-555-0802",
        "rating": 4.6,
        "latitude": 40.738,
        "longitude": -73.992,
        "district": "Mandya"
    },
    {
        "name": "Dr. Patricia Robinson",
        "specialization": "ENT Specialist",
        "hospital": "Ear Nose Throat Center",
        "address": "777 ENT Avenue, Sinus Plaza",
        "phone": "+1-555-0901",
        "rating": 4.9,
        "latitude": 40.752,
        "longitude": -73.978,
        "district": "Mandya"
    },
    {
        "name": "Dr. Steven Hall",
        "specialization": "ENT Specialist",
        "hospital": "Head & Neck Surgeons",
        "address": "888 Throat Lane, Voice Center",
        "phone": "+1-555-0902",
        "rating": 4.4,
        "latitude": 40.728,
        "longitude": -73.988,
        "district": "Mandya"
    },
    {
        "name": "Dr. Nancy Young",
        "specialization": "Infectious Disease Specialist",
        "hospital": "Infectious Disease Center",
        "address": "999 Infection Road, Virus Park",
        "phone": "+1-555-1001",
        "rating": 4.7,
        "latitude": 40.758,
        "longitude": -73.972,
        "district": "Mandya"
    },
    {
        "name": "Dr. Brian King",
        "specialization": "Infectious Disease Specialist",
        "hospital": "Tropical Disease Clinic",
        "address": "111 Germ Street, Pathogen District",
        "phone": "+1-555-1002",
        "rating": 4.5,
        "latitude": 40.732,
        "longitude": -73.982,
        "district": "Mandya"
    },
    {
        "name": "Dr. Karen Wright",
        "specialization": "Hematologist",
        "hospital": "Blood Disorder Center",
        "address": "222 Blood Lane, Hematology Hub",
        "phone": "+1-555-1101",
        "rating": 4.8,
        "latitude": 40.746,
        "longitude": -73.976,
        "district": "Mandya"
    },
    {
        "name": "Dr. Thomas Scott",
        "specialization": "Hematologist",
        "hospital": "Oncology & Hematology Institute",
        "address": "333 Cell Street, Cancer Center",
        "phone": "+1-555-1102",
        "rating": 4.6,
        "latitude": 40.722,
        "longitude": -73.994,
        "district": "Mandya"
    }
]

with open('data/doctors_database.json', 'w') as f:
    json.dump(doctors_database, f, indent=4)

print("Doctor database saved!")
print("\n" + "="*50)
print("All files created successfully!")
print("="*50)
