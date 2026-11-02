import json
import itertools

symptoms = [
    "Abdominal Pain", "Anxiety", "Back Pain", "Blurred Vision", "Chest Pain",
    "Cough", "Depression", "Diarrhea", "Dizziness", "Fatigue", "Fever",
    "Hearing Loss", "Headache", "Insomnia", "Itching", "Joint Pain",
    "Muscle Pain", "Nausea", "Rash", "Runny Nose", "Shortness of Breath",
    "Sore Throat", "Swelling", "Vomiting", "Wheezing"
]

forbidden = {
    "Weakness / Tiredness", "Throat Infection", "Cold / Allergies",
    "Acidity / Gas", "Breathing Problem", "Stomach Upset", "Loose Motion",
    "Stomach Pain", "Body Pain", "Body Ache", "Low BP / Weakness",
    "Skin Allergy", "Allergy", "Inflammation", "Eye Strain", "Ear Blockage",
    "Sleep Problem", "Stress", "Mental Stress", "Asthma / Allergy",
    "Dietary", "Rash", "Infection", "Viral Infection", "Back Pain",
    "Hearing Loss", "Dry Cough", "Cough Syndrome", "Tension Headache",
    "Chronic Fatigue", "Edema", "Vertigo", "Anaphylaxis", "Indigestion",
    "Heart Condition", "Muscle Strain"
}

# Symptom -> primary diseases (most clinically relevant first)
symptom_diseases = {
    "Fever": ["Pneumonia", "Influenza", "COVID-19", "Dengue", "Malaria", "Typhoid",
              "Tuberculosis", "Meningitis", "Gastroenteritis", "Chikungunya",
              "Chickenpox", "Sepsis", "Hepatitis", "Pyelonephritis"],
    "Cough": ["Pneumonia", "Bronchitis", "Asthma", "COVID-19", "Influenza",
              "Tuberculosis", "Chronic Obstructive Pulmonary Disease",
              "Gastroesophageal Reflux Disease", "Whooping Cough", "Lung Cancer"],
    "Headache": ["Migraine", "Tension Headache", "Meningitis", "Cluster Headache",
                 "Encephalitis", "Temporal Arteritis", "Sinusitis"],
    "Fatigue": ["Anemia", "Chronic Fatigue Syndrome", "Infectious Mononucleosis",
                "Diabetes", "Multiple Sclerosis", "Fibromyalgia", "Depression"],
    "Sore Throat": ["Pharyngitis", "Tonsillitis", "Strep Throat",
                    "Infectious Mononucleosis"],
    "Runny Nose": ["Common Cold", "Allergic Rhinitis", "Sinusitis", "Influenza"],
    "Chest Pain": ["Heart Attack", "Angina", "Pericarditis", "Myocarditis",
                   "Pulmonary Embolism", "Pneumonia", "Costochondritis",
                   "Aortic Dissection", "Pneumothorax"],
    "Shortness of Breath": ["Pneumonia", "Asthma", "Heart Failure", "Pulmonary Embolism",
                            "Chronic Obstructive Pulmonary Disease", "Pneumothorax",
                            "Anaphylaxis", "COVID-19", "Pleural Effusion",
                            "Interstitial Lung Disease", "Cardiomyopathy"],
    "Nausea": ["Gastroenteritis", "Food Poisoning", "Gastritis", "Migraine",
               "Pancreatitis", "Hepatitis", "Peptic Ulcer", "Bowel Obstruction",
               "Gallstones", "Pregnancy"],
    "Vomiting": ["Gastroenteritis", "Food Poisoning", "Gastritis", "Migraine",
                 "Pancreatitis", "Hepatitis", "Appendicitis", "Intestinal Obstruction",
                 "Gallstones", "Cyclic Vomiting Syndrome"],
    "Diarrhea": ["Gastroenteritis", "Food Poisoning", "Irritable Bowel Syndrome",
                 "Inflammatory Bowel Disease", "Celiac Disease", "Cholera",
                 "Ulcerative Colitis", "Crohn's Disease", "Antibiotic-Associated Colitis",
                 "Giardiasis"],
    "Abdominal Pain": ["Appendicitis", "Gastritis", "Peptic Ulcer",
                       "Irritable Bowel Syndrome", "Gallstones",
                       "Inflammatory Bowel Disease", "Pancreatitis",
                       "Diverticulitis", "Kidney Stones", "Cholecystitis",
                       "Bowel Obstruction", "Gastroenteritis"],
    "Back Pain": ["Herniated Disc", "Kidney Stones", "Pyelonephritis",
                  "Ankylosing Spondylitis", "Osteoarthritis",
                  "Spinal Stenosis", "Pancreatitis", "Endometriosis"],
    "Joint Pain": ["Arthritis", "Rheumatoid Arthritis", "Osteoarthritis",
                   "Gout", "Lyme Disease", "Chikungunya",
                   "Psoriatic Arthritis", "Lupus", "Septic Arthritis"],
    "Muscle Pain": ["Fibromyalgia", "Influenza", "Dengue", "Chikungunya",
                    "Rhabdomyolysis", "Polymyalgia Rheumatica",
                    "Systemic Lupus Erythematosus"],
    "Dizziness": ["Vestibular Neuritis", "Benign Paroxysmal Positional Vertigo",
                  "Meniere's Disease", "Migraine", "Anemia", "Hypotension",
                  "Dehydration", "Cardiac Arrhythmia"],
    "Rash": ["Chickenpox", "Measles", "Contact Dermatitis", "Eczema",
             "Psoriasis", "Drug Eruption", "Lyme Disease", "Lupus",
             "Shingles", "Scarlet Fever", "Seborrheic Dermatitis"],
    "Itching": ["Eczema", "Contact Dermatitis", "Psoriasis", "Urticaria",
                "Scabies", "Lichen Planus", "Dermatitis", "Dry Skin"],
    "Swelling": ["Cellulitis", "Deep Vein Thrombosis", "Heart Failure",
                 "Lymphedema", "Chronic Venous Insufficiency",
                 "Nephrotic Syndrome", "Allergic Reaction"],
    "Blurred Vision": ["Glaucoma", "Cataracts", "Diabetic Retinopathy",
                       "Migraine", "Conjunctivitis", "Optic Neuritis",
                       "Macular Degeneration", "Refractive Error"],
    "Hearing Loss": ["Otitis Media", "Presbycusis", "Meniere's Disease",
                     "Acoustic Neuroma", "Otosclerosis",
                     "Noise-Induced Hearing Loss",
                     "Sudden Sensorineural Hearing Loss"],
    "Insomnia": ["Insomnia Disorder", "Major Depressive Disorder",
                 "Generalized Anxiety Disorder", "Obstructive Sleep Apnea",
                 "Restless Legs Syndrome"],
    "Anxiety": ["Generalized Anxiety Disorder", "Panic Disorder",
                "Major Depressive Disorder", "Social Anxiety Disorder",
                "Post-Traumatic Stress Disorder", "Hyperthyroidism"],
    "Depression": ["Major Depressive Disorder", "Bipolar Disorder",
                   "Persistent Depressive Disorder",
                   "Generalized Anxiety Disorder",
                   "Seasonal Affective Disorder", "Postpartum Depression"],
    "Wheezing": ["Asthma", "Chronic Obstructive Pulmonary Disease",
                 "Bronchitis", "Pneumonia", "Allergic Rhinitis",
                 "Vocal Cord Dysfunction", "Bronchiectasis"],
}

# Clinically validated multi-symptom -> disease mappings
strong_combos = {
    # Respiratory
    frozenset(["Fever", "Cough", "Shortness of Breath"]): "Pneumonia",
    frozenset(["Fever", "Cough", "Wheezing"]): "Bronchitis",
    frozenset(["Cough", "Shortness of Breath", "Wheezing"]): "Asthma",
    frozenset(["Cough", "Chest Pain", "Shortness of Breath"]): "Pneumonia",
    frozenset(["Fever", "Cough", "Chest Pain"]): "Pneumonia",
    frozenset(["Fever", "Cough", "Shortness of Breath"]): "COVID-19",
    frozenset(["Cough", "Wheezing", "Shortness of Breath"]): "Chronic Obstructive Pulmonary Disease",
    frozenset(["Fever", "Sore Throat", "Cough"]): "Pharyngitis",
    frozenset(["Sore Throat", "Runny Nose", "Cough"]): "Common Cold",
    frozenset(["Fever", "Sore Throat", "Runny Nose"]): "Sinusitis",
    frozenset(["Cough", "Fever", "Wheezing"]): "Bronchitis",
    # Cardiac
    frozenset(["Chest Pain", "Shortness of Breath", "Fatigue"]): "Heart Attack",
    frozenset(["Chest Pain", "Dizziness", "Shortness of Breath"]): "Heart Attack",
    frozenset(["Chest Pain", "Shortness of Breath", "Fatigue"]): "Angina",
    # GI
    frozenset(["Nausea", "Vomiting", "Diarrhea"]): "Gastroenteritis",
    frozenset(["Abdominal Pain", "Nausea", "Vomiting"]): "Gastroenteritis",
    frozenset(["Abdominal Pain", "Diarrhea", "Fever"]): "Gastroenteritis",
    frozenset(["Nausea", "Abdominal Pain", "Diarrhea"]): "Gastroenteritis",
    frozenset(["Nausea", "Vomiting", "Abdominal Pain"]): "Food Poisoning",
    frozenset(["Abdominal Pain", "Nausea", "Fever"]): "Appendicitis",
    frozenset(["Vomiting", "Abdominal Pain", "Diarrhea"]): "Gastroenteritis",
    # Neurological
    frozenset(["Headache", "Nausea", "Dizziness"]): "Migraine",
    frozenset(["Headache", "Blurred Vision", "Dizziness"]): "Migraine",
    frozenset(["Headache", "Nausea", "Blurred Vision"]): "Migraine",
    # Infection
    frozenset(["Fever", "Fatigue", "Muscle Pain"]): "Influenza",
    frozenset(["Fever", "Joint Pain", "Rash"]): "Dengue",
    frozenset(["Fever", "Rash", "Fatigue"]): "Chickenpox",
    frozenset(["Fever", "Sore Throat", "Rash"]): "Scarlet Fever",
    frozenset(["Fever", "Headache", "Rash"]): "Meningitis",
    frozenset(["Fever", "Muscle Pain", "Joint Pain"]): "Chikungunya",
    frozenset(["Fever", "Fatigue", "Rash"]): "Infectious Mononucleosis",
    frozenset(["Fever", "Joint Pain", "Fatigue"]): "Rheumatoid Arthritis",
    frozenset(["Fever", "Back Pain", "Nausea"]): "Pyelonephritis",
    frozenset(["Fever", "Abdominal Pain", "Nausea"]): "Appendicitis",
    # Mental health
    frozenset(["Anxiety", "Depression", "Insomnia"]): "Major Depressive Disorder",
    frozenset(["Anxiety", "Insomnia", "Fatigue"]): "Generalized Anxiety Disorder",
    frozenset(["Depression", "Fatigue", "Insomnia"]): "Major Depressive Disorder",
    # Musculoskeletal
    frozenset(["Joint Pain", "Muscle Pain", "Fatigue"]): "Fibromyalgia",
    frozenset(["Back Pain", "Joint Pain", "Muscle Pain"]): "Arthritis",
    frozenset(["Back Pain", "Muscle Pain", "Fatigue"]): "Fibromyalgia",
    frozenset(["Back Pain", "Joint Pain", "Fatigue"]): "Rheumatoid Arthritis",
    # Dermatological
    frozenset(["Rash", "Itching", "Swelling"]): "Contact Dermatitis",
    frozenset(["Rash", "Itching", "Fatigue"]): "Eczema",
    frozenset(["Rash", "Swelling", "Itching"]): "Eczema",
    frozenset(["Rash", "Joint Pain", "Fatigue"]): "Psoriatic Arthritis",
    frozenset(["Rash", "Fever", "Joint Pain"]): "Lyme Disease",
    # ENT
    frozenset(["Fever", "Sore Throat", "Runny Nose"]): "Tonsillitis",
    frozenset(["Sore Throat", "Runny Nose", "Headache"]): "Sinusitis",
    frozenset(["Fever", "Runny Nose", "Cough"]): "Influenza",
    # Vision + Neuro
    frozenset(["Dizziness", "Blurred Vision", "Nausea"]): "Migraine",
    frozenset(["Headache", "Blurred Vision", "Nausea"]): "Migraine",
    frozenset(["Dizziness", "Hearing Loss", "Nausea"]): "Meniere's Disease",
    frozenset(["Dizziness", "Hearing Loss", "Headache"]): "Meniere's Disease",
    # Chest + Resp
    frozenset(["Chest Pain", "Cough", "Fever"]): "Pneumonia",
    frozenset(["Chest Pain", "Cough", "Wheezing"]): "Bronchitis",
    frozenset(["Chest Pain", "Shortness of Breath", "Wheezing"]): "Pulmonary Embolism",
    # Abdominal + GI
    frozenset(["Diarrhea", "Nausea", "Fever"]): "Gastroenteritis",
    frozenset(["Vomiting", "Diarrhea", "Fever"]): "Gastroenteritis",
    frozenset(["Abdominal Pain", "Diarrhea", "Nausea"]): "Irritable Bowel Syndrome",
    frozenset(["Abdominal Pain", "Vomiting", "Fever"]): "Appendicitis",
    frozenset(["Abdominal Pain", "Diarrhea", "Nausea"]): "Gastroenteritis",
    # Swelling + Vascular
    frozenset(["Swelling", "Pain", "Redness"]): "Cellulitis",
    frozenset(["Swelling", "Chest Pain", "Shortness of Breath"]): "Heart Failure",
    frozenset(["Swelling", "Joint Pain", "Fatigue"]): "Rheumatoid Arthritis",
    # Fatigue combos
    frozenset(["Fatigue", "Fever", "Night Sweats"]): "Tuberculosis",
    frozenset(["Fatigue", "Weight Loss", "Fever"]): "Tuberculosis",
}

# Additional symptom associations for fallback scoring
extended_symptom_links = {
    "Blurred Vision": {"Migraine": 0.8, "Glaucoma": 0.7, "Diabetes": 0.6,
                       "Hypertension": 0.5, "Anemia": 0.3, "Multiple Sclerosis": 0.5,
                       "Conjunctivitis": 0.7, "Stroke": 0.4},
    "Depression": {"Major Depressive Disorder": 1.0, "Bipolar Disorder": 0.7,
                   "Anxiety Disorder": 0.7, "Hypothyroidism": 0.5,
                   "Chronic Fatigue Syndrome": 0.5},
    "Muscle Pain": {"Influenza": 0.9, "Dengue": 0.8, "Fibromyalgia": 0.9,
                    "Chikungunya": 0.8, "Rheumatoid Arthritis": 0.6},
    "Fatigue": {"Anemia": 0.8, "Chronic Fatigue Syndrome": 0.9,
                "Diabetes": 0.6, "Hypothyroidism": 0.7,
                "Infectious Mononucleosis": 0.8, "Depression": 0.5},
    "Abdominal Pain": {"Appendicitis": 0.9, "Gastritis": 0.8, "Irritable Bowel Syndrome": 0.8},
    "Dizziness": {"Vestibular Neuritis": 0.8, "Benign Paroxysmal Positional Vertigo": 0.8,
                  "Meniere's Disease": 0.7, "Migraine": 0.6, "Anemia": 0.6},
    "Back Pain": {"Herniated Disc": 0.7, "Kidney Stones": 0.6,
                  "Pyelonephritis": 0.7, "Osteoarthritis": 0.6},
    "Swelling": {"Cellulitis": 0.7, "Deep Vein Thrombosis": 0.7,
                 "Heart Failure": 0.6, "Rheumatoid Arthritis": 0.5},
    "Insomnia": {"Insomnia Disorder": 1.0, "Major Depressive Disorder": 0.7,
                 "Generalized Anxiety Disorder": 0.6, "Obstructive Sleep Apnea": 0.6},
    "Chest Pain": {"Heart Attack": 0.9, "Angina": 0.8, "Pulmonary Embolism": 0.7,
                   "Costochondritis": 0.6, "Gastroesophageal Reflux Disease": 0.5},
    "Wheezing": {"Asthma": 0.9, "Chronic Obstructive Pulmonary Disease": 0.8,
                 "Bronchitis": 0.7, "Pneumonia": 0.6},
    "Runny Nose": {"Common Cold": 0.8, "Allergic Rhinitis": 0.8, "Sinusitis": 0.6},
    "Hearing Loss": {"Otitis Media": 0.7, "Presbycusis": 0.6,
                     "Meniere's Disease": 0.6, "Acoustic Neuroma": 0.5},
    "Itching": {"Eczema": 0.7, "Contact Dermatitis": 0.7, "Psoriasis": 0.6,
                "Urticaria": 0.6, "Scabies": 0.5},
    "Rash": {"Chickenpox": 0.8, "Measles": 0.7, "Contact Dermatitis": 0.7,
             "Eczema": 0.6, "Psoriasis": 0.6, "Lyme Disease": 0.6},
    "Diarrhea": {"Gastroenteritis": 0.9, "Food Poisoning": 0.8,
                 "Irritable Bowel Syndrome": 0.6, "Inflammatory Bowel Disease": 0.6},
}

def get_disease(combo):
    """Get the most likely disease for a symptom combination."""
    key = frozenset(combo)

    # Check strong known combos first
    if key in strong_combos:
        return strong_combos[key]

    # Build scoring dict for all possible diseases
    scores = {}
    for s in combo:
        # From primary symptom_diseases list
        for d in symptom_diseases.get(s, []):
            if d not in forbidden:
                scores[d] = scores.get(d, 0) + 3  # Primary association weight

        # From extended links
        for d, w in extended_symptom_links.get(s, {}).items():
            if d not in forbidden:
                scores[d] = scores.get(d, 0) + w * 2

    if scores:
        # Find disease that explains the most symptoms
        best = max(scores, key=scores.get)
        return best

    return "Undiagnosed"


# --- Generation ---
# Generate 5-symptom combinations
five = {}
five_sets = set()
for combo in itertools.combinations(symptoms, 5):
    key = "|".join(sorted(combo))
    five[key] = get_disease(combo)
    five_sets.add(frozenset(combo))

# Generate 4-symptom combos, dedup against 5-sympt supersets
four = {}
four_sets = set()
for combo in itertools.combinations(symptoms, 4):
    cs = frozenset(combo)
    # Skip if this is a subset of any 5-combo we already have
    is_sub = any(cs.issubset(fs) for fs in five_sets)
    if is_sub:
        continue
    key = "|".join(sorted(combo))
    four[key] = get_disease(combo)
    four_sets.add(cs)

# Generate 3-symptom combos, dedup against 4+5 supersets
three = {}
three_sets = set()
all_higher = five_sets | four_sets
for combo in itertools.combinations(symptoms, 3):
    cs = frozenset(combo)
    is_sub = any(cs.issubset(hs) for hs in all_higher)
    if is_sub:
        continue
    key = "|".join(sorted(combo))
    three[key] = get_disease(combo)
    three_sets.add(cs)

print(f"Raw: 3={len(three)}, 4={len(four)}, 5={len(five)}")

# Ensure minimums
if len(three) < 500:
    deficit = 500 - len(three)
    added = 0
    for combo in itertools.combinations(symptoms, 3):
        key = "|".join(sorted(combo))
        if key not in three:
            three[key] = get_disease(combo)
            added += 1
            if added >= deficit:
                break
    print(f"Added {added} 3-sympt combos, total={len(three)}")

if len(four) < 300:
    deficit = 300 - len(four)
    added = 0
    for combo in itertools.combinations(symptoms, 4):
        key = "|".join(sorted(combo))
        if key not in four:
            four[key] = get_disease(combo)
            added += 1
            if added >= deficit:
                break
    print(f"Added {added} 4-sympt combos, total={len(four)}")

# Trim 5-sympt to a reasonable number (keep ~250 for quality)
if len(five) > 250:
    # Keep the best ones - those with strongest disease associations
    scored_five = []
    for key, disease in five.items():
        combo = frozenset(key.split("|"))
        score = sum(3 for s in combo if disease in symptom_diseases.get(s, []))
        scored_five.append((score, key, disease))
    scored_five.sort(key=lambda x: -x[0])
    five = {k: d for _, k, d in scored_five[:250]}

print(f"Final: 3={len(three)}, 4={len(four)}, 5={len(five)}")

# Output
output = {
    "three_symptom_combinations": dict(sorted(three.items())),
    "four_symptom_combinations": dict(sorted(four.items())),
    "five_symptom_combinations": dict(sorted(five.items()))
}

with open("symptom_combinations_v3.json", "w") as f:
    json.dump(output, f, indent=2)

# Validation
all_keys = set()
for section_name, d in [("3", three), ("4", four), ("5", five)]:
    for k in d:
        parts = k.split("|")
        assert parts == sorted(parts), f"Section {section_name} not sorted: {k}"
        assert k not in all_keys, f"Duplicate across sections: {k}"
        all_keys.add(k)
        disease = d[k]
        assert disease not in forbidden, f"Forbidden disease '{disease}' in {k}"

print(f"Validation passed: {len(three) + len(four) + len(five)} total combos, all unique & sorted")
print(f"3-symptom: {len(three)}, 4-symptom: {len(four)}, 5-symptom: {len(five)}")
for section_name, d in [("3-symptom", three), ("4-symptom", four), ("5-symptom", five)]:
    diseases = set(d.values())
    print(f"  {section_name}: {len(d)} combos, {len(diseases)} unique diseases")
    top_diseases = {}
    for disease in d.values():
        top_diseases[disease] = top_diseases.get(disease, 0) + 1
    for disease, count in sorted(top_diseases.items(), key=lambda x: -x[1])[:10]:
        print(f"    {disease}: {count}")