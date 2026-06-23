from flask import Flask, render_template, request, jsonify
import os
import pickle
import json
import numpy as np
import math

# Import symptom mapper service
from services.symptom_mapper import get_related_diseases, get_symptom_info, SYMPTOM_DISEASE_MAP

# Get the base directory (where app.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# Configure for XAMPP proxy
app.config['APPLICATION_ROOT'] = '/new help/Your AI Doctor'

# Load ML models at startup
MODEL_PATHS = {
    'decision_tree': os.path.join(BASE_DIR, 'models', 'decision_tree.pkl'),
    'random_forest': os.path.join(BASE_DIR, 'models', 'random_forest.pkl')
}

# Load disease information
DISEASE_DATA_PATH = os.path.join(BASE_DIR, 'data', 'disease_solutions.json')

# Load diagnostic testing matrix
DIAGNOSTIC_MATRIX_PATH = os.path.join(BASE_DIR, 'data', 'diagnostic_testing_matrix.json')

# Load doctor database
DOCTOR_DATA_PATH = os.path.join(BASE_DIR, 'data', 'doctors_database.json')

# Predefined symptoms list (25 symptoms - full list for ML model compatibility)
SYMPTOMS = [
    'Fever', 'Cough', 'Headache', 'Fatigue', 'Sore Throat',
    'Runny Nose', 'Chest Pain', 'Shortness of Breath', 'Nausea',
    'Vomiting', 'Diarrhea', 'Abdominal Pain', 'Back Pain',
    'Joint Pain', 'Muscle Pain', 'Dizziness', 'Rash', 'Itching',
    'Swelling', 'Blurred Vision', 'Hearing Loss', 'Insomnia', 'Anxiety', 'Depression', 'Wheezing'
]

# Main symptoms (first 15 - shown by default)
MAIN_SYMPTOMS = [
    'Fever', 'Cough', 'Headache', 'Fatigue', 'Sore Throat',
    'Runny Nose', 'Nausea', 'Vomiting', 'Diarrhea', 'Muscle Pain',
    'Abdominal Pain', 'Dizziness', 'Joint Pain', 'Shortness of Breath', 'Chest Pain'
]

# Extra symptoms (remaining 10 - shown with "More" button)
EXTRA_SYMPTOMS = [
    'Back Pain', 'Rash', 'Itching', 'Swelling', 'Blurred Vision',
    'Hearing Loss', 'Insomnia', 'Anxiety', 'Depression', 'Wheezing'
]

# Global variables for models and data
models = {}
disease_data = []
doctors = []
diagnostic_matrix = {}
model_symptoms = []  # Store symptoms from the model

def load_resources():
    """Load ML models and data files at startup"""
    global models, disease_data, doctors, diagnostic_matrix, model_symptoms
    
    # Load ML models
    for model_name, path in MODEL_PATHS.items():
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    models[model_name] = pickle.load(f)
                print(f"Loaded model: {model_name}")
            except Exception as e:
                print(f"Warning: Failed to load model '{model_name}': {e}")
        else:
            print(f"Warning: Model file not found: {path}")
    
    # Set symptoms list explicitly for feature vector generation
    model_symptoms = SYMPTOMS
    
    # Load disease information
    if os.path.exists(DISEASE_DATA_PATH):
        try:
            with open(DISEASE_DATA_PATH, 'r') as f:
                data = json.load(f)
                disease_data = data.get('diseases', [])
                print(f"Loaded {len(disease_data)} disease entries")
        except Exception as e:
            print(f"Warning: Failed to load disease data: {e}")
    else:
        print(f"Warning: Disease data file not found: {DISEASE_DATA_PATH}")
    
    # Load diagnostic testing matrix
    if os.path.exists(DIAGNOSTIC_MATRIX_PATH):
        try:
            with open(DIAGNOSTIC_MATRIX_PATH, 'r') as f:
                diagnostic_matrix = json.load(f)
                print("Loaded diagnostic testing matrix")
        except Exception as e:
            print(f"Warning: Failed to load diagnostic matrix: {e}")
    else:
        print(f"Warning: Diagnostic matrix not found: {DIAGNOSTIC_MATRIX_PATH}")
    
    # Load doctor database
    if os.path.exists(DOCTOR_DATA_PATH):
        try:
            with open(DOCTOR_DATA_PATH, 'r') as f:
                data = json.load(f)
                doctors = data.get('doctors', [])
                print(f"Loaded {len(doctors)} doctors")
        except Exception as e:
            print(f"Warning: Failed to load doctors database: {e}")
            doctors = []
    else:
        print(f"Warning: Doctors database not found: {DOCTOR_DATA_PATH}")
        doctors = []

def predict_disease(symptoms_selected):
    """Predict disease using ML models"""
    if not symptoms_selected:
        return None, 0, []
    
    # Use model symptoms if available, otherwise use default SYMPTOMS
    symptoms_list = model_symptoms if model_symptoms else SYMPTOMS
    
    # Create feature vector (one-hot encoding)
    feature_vector = [1 if symptom in symptoms_selected else 0 for symptom in symptoms_list]
    
    predictions = []
    
    # Get predictions from both models
    for model_name, model in models.items():
        if model:
            prediction = model.predict([feature_vector])[0]
            confidence = model.predict_proba([feature_vector]).max() * 100
            predictions.append((prediction, confidence, model_name))
    
    # Sort by confidence and get top predictions
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    if predictions:
        top_prediction = predictions[0]
        alternatives = predictions[1:4]  # Top 3 alternatives
        return top_prediction[0], top_prediction[1], alternatives
    
    return None, 0, []

def get_disease_info(disease_name):
    """Get disease information from database"""
    if not disease_data:
        return None
    
    # Map common disease names from symptom matcher to disease_solutions.json names
    disease_mapping = {
        # Already existing mappings
        'Influenza': 'Flu',
        'Gastroenteritis': 'Stomach Upset',
        'GERD': 'Acidity / Gas',
        'Pancreatitis': 'Stomach Pain',  # Closest match
        'Peptic Ulcer': 'Stomach Pain',  # Closest match
        'Panic Disorder': 'Stress',      # Closest match
        'Major Depressive Disorder': 'Mental Stress',  # Closest match
        'Allergic Rhinitis': 'Allergy',
        'Otitis Media': 'Ear Blockage',
        
        # Additional mappings for missing diseases
        'Bronchitis': 'Common Cold',  # Respiratory infection
        'Chickenpox': 'Viral Fever',  # Viral infection
        'Dengue': 'Dengue Fever',  # Same disease, different naming
        'Aortic Dissection': 'Heart Attack',  # Cardiovascular emergency
        'Heart Failure': 'Heart Attack',  # Cardiovascular condition
        'Angina': 'Heart Attack',  # Cardiovascular condition
        'Thyroid Disorder': 'Stress',  # Endocrine with stress-like symptoms
        'Diabetes': 'Weakness / Tiredness',  # Can cause fatigue
        'COPD': 'Breathing Problem',  # Respiratory condition
        'Asthma': 'Asthma / Allergy',  # Same base condition
        'Arthritis': 'Body Pain',  # Joint/muscle pain
        'Osteoarthritis': 'Body Pain',  # Joint/muscle pain
        'Rheumatoid Arthritis': 'Inflammation',  # Chronic inflammation
        'Psoriatic Arthritis': 'Inflammation',  # Chronic inflammation
        'Gout': 'Joint Pain',  # Acute joint inflammation (similar to arthritis)
        'Allergies': 'Allergy',  # Same condition
        'Depression': 'Mental Stress',  # Mental health
        'Ear Infection': 'Ear Blockage',  # Hearing/ear issues
        'Dry Skin': 'Skin Allergy',  # Skin condition
        'Dermatitis': 'Skin Allergy',  # Skin inflammation
        'Fibromyalgia': 'Body Pain',  # Chronic pain
        'Chronic Fatigue Syndrome': 'Weakness / Tiredness',  # Fatigue
        'Chronic Illness': 'Weakness / Tiredness',  # General chronic condition
        'Meniere\'s Disease': 'Dizziness',  # Vestibular disorder (maps via symptom)
        'Herniated Disc': 'Back Pain',  # Spine issue (similar to Muscle Strain)
        'Musculoskeletal Issue': 'Body Pain',  # General muscle/bone issue
        'Injury': 'Muscle Strain',  # Trauma/injury
        'Noise Exposure': 'Ear Blockage',  # Hearing damage
        'Pleuritic Pain': 'Pneumonia',  # Chest pain with breathing
        'Pulmonary Embolism': 'Breathing Problem',  # Lung vascular issue
        'Pyelonephritis': 'Stomach Upset',  # Kidney infection (can map)
        'Scarlet Fever': 'Throat Infection',  # Strep infection
        'Typhoid': 'Viral Fever',  # Systemic infection
        'Lupus': 'Inflammation',  # Autoimmune inflammation
        'Lyme Disease': 'Flu',  # Tick-borne illness (flu-like)
        'Measles': 'Viral Fever',  # Viral rash illness
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

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def filter_doctors(specialization, user_location=None, district='Mandya'):
    """Filter and sort doctors by specialization, district/taluk and distance"""
    filtered = []
    district_lower = district.lower() if district else ''
    
    for doctor in doctors:
        doctor_district = doctor.get('district', '').lower()
        doctor_taluk = doctor.get('taluk', '').lower()
        
        if district_lower == 'all':
            pass
        elif doctor_district == district_lower:
            pass
        else:
            continue
        
        if specialization and specialization.lower() != doctor['specialization'].lower():
            continue
        
        if user_location:
            doctor_location = (doctor['latitude'], doctor['longitude'])
            distance = calculate_distance(user_location[0], user_location[1], 
                                         doctor_location[0], doctor_location[1])
            doctor['distance'] = distance
        
        filtered.append(doctor)
    
    if user_location and filtered:
        filtered.sort(key=lambda x: x.get('distance', 0))
    
    return filtered

@app.route('/')
def home():
    """Home page with symptom selection and prediction"""
    return render_template('index.html', symptoms=SYMPTOMS, main_symptoms=MAIN_SYMPTOMS, extra_symptoms=EXTRA_SYMPTOMS)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for disease prediction"""
    try:
        data = request.json or {}
        symptoms_selected = data.get('symptoms', [])
        
        if not symptoms_selected:
            return jsonify({'error': 'No symptoms are selected. Please select at least one symptom.'}), 400
        
        # Use symptom-based mapping instead of ML model for better accuracy
        related_diseases = get_related_diseases(symptoms_selected, min_probability=0.25)
        
        if not related_diseases:
            return jsonify({'error': 'No related diseases found for these symptoms'}), 404
        
        # Get top prediction
        top_disease = related_diseases[0]
        disease_name = top_disease['disease']
        confidence = top_disease['probability']
        
        # Get alternatives (diseases 2-4)
        alternatives = [
            {'disease': d['disease'], 'confidence': d['probability'], 'matched_symptoms': d.get('matched_symptoms', [])}
            for d in related_diseases[1:4]
        ]
        
        disease_info = get_disease_info(disease_name)
        
        result = {
            'predicted_disease': disease_name,
            'confidence': confidence,
            'alternatives': alternatives,
            'disease_info': disease_info,
            'all_predictions': related_diseases,
            'is_critical': top_disease.get('is_critical', False),
            'warning': 'Please consult a doctor immediately for accurate diagnosis' if top_disease.get('is_critical') else None
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/api/diagnosis', methods=['POST'])
def api_diagnosis():
    """API endpoint for diagnostic information based on symptoms"""
    try:
        data = request.json or {}
        symptoms_selected = data.get('symptoms', [])
        demographic_info = data.get('demographic', {})
        
        if not symptoms_selected:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        if not diagnostic_matrix or 'symptoms' not in diagnostic_matrix:
            return jsonify({'error': 'Diagnostic matrix not available'}), 500
        
        results = []
        threshold = diagnostic_matrix.get('metadata', {}).get('probability_threshold', 0.15)
        
        for symptom_name in symptoms_selected:
            symptom_data = None
            for symptom in diagnostic_matrix['symptoms']:
                if symptom['symptom_name'].lower() == symptom_name.lower():
                    symptom_data = symptom
                    break
            
            if not symptom_data:
                continue
            
            symptom_result = {
                'symptom_name': symptom_data['symptom_name'],
                'icd11_code': symptom_data['icd11_code'],
                'emergency_flag': symptom_data['emergency_flag'],
                'emergency_protocols': symptom_data.get('emergency_conditions', []),
                'conditions': []
            }
            
            age_group = demographic_info.get('age_group', 'adult')
            gender = demographic_info.get('gender', 'adult')
            has_comorbidity = demographic_info.get('has_comorbidity', False)
            
            for condition in symptom_data.get('associated_conditions', []):
                adjusted_prob = condition.get('adjusted_probability', {})
                
                if age_group in adjusted_prob:
                    prob = adjusted_prob[age_group]
                elif gender in adjusted_prob:
                    prob = adjusted_prob[gender]
                elif has_comorbidity and 'with_comorbidity' in adjusted_prob:
                    prob = adjusted_prob['with_comorbidity']
                else:
                    prob = condition.get('base_probability', 0)
                
                if prob >= threshold:
                    condition_result = {
                        'rank': condition['rank'],
                        'condition_name': condition['condition_name'],
                        'icd10_code': condition['icd10_code'],
                        'probability': round(prob * 100, 2),
                        'confidence_interval': condition.get('confidence_interval', []),
                        'tests': []
                    }
                    
                    for test in condition.get('tests', []):
                        test_info = {
                            'test_name': test['test_name'],
                            'specificity': test['specificity'],
                            'sensitivity': test['sensitivity'],
                            'priority': test['priority'],
                            'prerequisites': test.get('prerequisites', []),
                            'turnaround_hours': test.get('turnaround_hours', 0),
                            'cost_category': test.get('cost_category', 'basic')
                        }
                        condition_result['tests'].append(test_info)
                    
                    symptom_result['conditions'].append(condition_result)
            
            if symptom_result['conditions']:
                results.append(symptom_result)
        
        return jsonify({
            'diagnostic_results': results,
            'metadata': {
                'version': diagnostic_matrix.get('metadata', {}).get('version', '1.0.0'),
                'probability_threshold': threshold,
                'methodology': diagnostic_matrix.get('methodology', {}).get('framework', 'Bayesian')
            }
        })
    except Exception as e:
        return jsonify({'error': f'Diagnostic error: {str(e)}'}), 500

@app.route('/consult')
def consult():
    """Doctor consultation page"""
    specializations = sorted(set([d['specialization'] for d in doctors])) if doctors else []
    return render_template('consult.html', specializations=specializations)

@app.route('/api/doctors', methods=['GET'])
def api_doctors():
    """API endpoint to get doctors"""
    specialization = request.args.get('specialization', '')
    district = request.args.get('district', 'Mandya')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    user_location = None
    if latitude and longitude:
        try:
            user_location = (float(latitude), float(longitude))
        except ValueError:
            return jsonify({'error': 'Invalid coordinates'}), 400
    
    doctors_list = filter_doctors(specialization, user_location, district)
    
    response = []
    for doctor in doctors_list:
        doctor_data = {
            'name': doctor['name'],
            'specialization': doctor['specialization'],
            'hospital': doctor['hospital'],
            'address': doctor['address'],
            'taluk': doctor.get('taluk', ''),
            'district': doctor.get('district', doctor.get('city', '')),
            'phone': doctor['phone'],
            'rating': doctor['rating'],
            'latitude': doctor['latitude'],
            'longitude': doctor['longitude'],
            'google_maps_link': doctor.get('google_maps_link', f"https://www.google.com/maps/search/?api=1&query={doctor['latitude']},{doctor['longitude']}")
        }
        
        if 'distance' in doctor:
            doctor_data['distance'] = round(doctor['distance'], 2)
        
        response.append(doctor_data)
    
    return jsonify(response)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# Load resources before first request
load_resources()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
