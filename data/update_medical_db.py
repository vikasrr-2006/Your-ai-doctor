import json

with open('medical_information_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

disease_info = {
    "Acidity": {
        "primary_treatment": "Antacids or proton pump inhibitors to neutralize stomach acid. Avoid trigger foods.",
        "prevention_tips": ["Avoid trigger foods", "Eat smaller meals", "Don't lie down after eating"],
        "when_to_consult": ["Persistent symptoms >2 weeks", "Difficulty swallowing", "Unexplained weight loss"],
        "recommended_specialist": "Gastroenterologist",
        "ayurvedic_herbs": ["Amla", "Yashtimadhu", "Shankhapushpi"],
        "ayurvedic_diet": ["Avoid spicy foods", "Eat cooling foods like cucumber"],
        "ayurvedic_lifestyle": ["Regular meal times", "Stress management"],
        "ayurvedic_yoga": ["Vajrasana", "Sheetali pranayama"]
    },
    "Anaphylaxis": {
        "primary_treatment": "Epinephrine injection immediately",
        "prevention_tips": ["Carry epinephrine auto-injector", "Avoid known allergens"],
        "when_to_consult": ["Severe allergic reaction", "Trouble breathing", "Swelling of throat"],
        "recommended_specialist": "Allergist",
        "ayurvedic_herbs": ["Consult Ayurvedic practitioner"],
        "ayurvedic_diet": ["Avoid allergens", "Simple clean diet"],
        "ayurvedic_lifestyle": ["Medical alert tags", "Emergency plan"],
        "ayurvedic_yoga": ["Stress management"]
    },
    "Diabetes": {
        "primary_treatment": "Metformin or insulin with blood sugar monitoring",
        "prevention_tips": ["Healthy weight", "Regular exercise", "Balanced diet"],
        "when_to_consult": ["Frequent urination", "Excessive thirst", "Unexplained weight loss"],
        "recommended_specialist": "Endocrinologist",
        "ayurvedic_herbs": ["Gudmar", "Bitter gourd", "Fenugreek"],
        "ayurvedic_diet": ["Low GI foods", "Avoid refined sugars"],
        "ayurvedic_lifestyle": ["Regular exercise", "Monitor sugar levels"],
        "ayurvedic_yoga": ["Dhanurasana", "Pranayama"]
    },
    "Migraine": {
        "primary_treatment": "Pain relievers, anti-nausea medications, prevention",
        "prevention_tips": ["Regular sleep", "Avoid triggers", "Stay hydrated"],
        "when_to_consult": ["Severe headache", "Vision changes", "Numbness"],
        "recommended_specialist": "Neurologist",
        "ayurvedic_herbs": ["Brahmi", "Jatamansi"],
        "ayurvedic_diet": ["Avoid aged cheese", "Limit caffeine"],
        "ayurvedic_lifestyle": ["Stress management", "Regular routine"],
        "ayurvedic_yoga": ["Shavasana", "Pranayama"]
    },
    "Asthma": {
        "primary_treatment": "Inhaled corticosteroids and bronchodilators",
        "prevention_tips": ["Avoid triggers", "Use air purifiers", "Regular exercise"],
        "when_to_consult": ["Frequent attacks", "Wheezing", "Night symptoms"],
        "recommended_specialist": "Pulmonologist",
        "ayurvedic_herbs": ["Tulsi", "Vasa", "Licorice"],
        "ayurvedic_diet": ["Warm foods", "Honey and ginger"],
        "ayurvedic_lifestyle": ["Clean air", "Avoid smoke"],
        "ayurvedic_yoga": ["Bhramari pranayama", "Matsyasana"]
    }
}

for disease, info in disease_info.items():
    if disease in db['disease_information']:
        db['disease_information'][disease]['primary_treatment'] = info['primary_treatment']
        db['disease_information'][disease]['prevention_tips'] = info['prevention_tips']
        db['disease_information'][disease]['when_to_consult'] = info['when_to_consult']
        db['disease_information'][disease]['recommended_specialist'] = info['recommended_specialist']
        db['disease_information'][disease]['ayurvedic_prevention_remedies']['herbs'] = info['ayurvedic_herbs']
        db['disease_information'][disease]['ayurvedic_prevention_remedies']['diet'] = info['ayurvedic_diet']
        db['disease_information'][disease]['ayurvedic_prevention_remedies']['lifestyle'] = info['ayurvedic_lifestyle']
        db['disease_information'][disease]['ayurvedic_prevention_remedies']['yoga'] = info['ayurvedic_yoga']

with open('medical_information_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print('Updated 5 diseases with medical information')
