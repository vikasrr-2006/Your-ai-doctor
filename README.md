# Your AI Doctor

A simple medical symptom checker that predicts possible diseases based on your symptoms.

## SDLC Process
This project uses a **Spiral Model**. See: [`spiral_model.md`](./spiral_model.md) | [View Diagram](./diagrams/spiral_model.html)


## Quick Setup

1. **Install Python** (version 3.8 or higher required)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Create models**: `python create_models.py`
4. **Start app**: `python app.py`
5. **Open browser**: Go to `http://localhost:5000`

## Application Flow

```
User Opens App
      ↓
Select Symptoms from List (25 options)
      ↓
Click "Predict Disease" Button
      ↓
[Decision Tree Model] → Processes Symptoms
                      ↓
[Random Forest Model] → Validates Prediction
      ↓
Display Results:
  • Predicted Disease + Confidence %
  • Alternative Predictions
  • Treatment Options
  • Prevention Tips
  • Ayurvedic Remedies
  • When to See Doctor Alert
```

## Available Symptoms (25)

Fever, Cough, Headache, Fatigue, Sore Throat, Runny Nose, Chest Pain, Shortness of Breath, Nausea, Vomiting, Diarrhea, Abdominal Pain, Back Pain, Joint Pain, Muscle Pain, Dizziness, Rash, Itching, Swelling, Blurred Vision, Hearing Loss, Insomnia, Anxiety, Depression, Wheezing

## Project Files and Their Functions

### Main Application
- **app.py** - Main Flask application that handles all web routes, API endpoints, and coordinates the prediction workflow

### Model Files
- **create_models.py** - Script that trains and creates the Decision Tree and Random Forest ML models
- **models/decision_tree.pkl** - Trained Decision Tree model for disease prediction
- **models/random_forest.pkl** - Trained Random Forest model for validating predictions

### Services
- **services/symptom_mapper.py** - Core prediction engine that maps symptoms to diseases and handles combination logic
- **services/__init__.py** - Package initialization file for services module

### Data Files
- **data/symptom_disease_map.json** - Main mapping data for 1675 symptom combinations across 25 symptoms
- **data/disease_solutions.json** - Comprehensive disease information (89 diseases) including treatments, prevention, and Ayurvedic remedies
- **data/doctors_database.json** - Comprehensive directory of 290 doctors across 58 hospitals in Bengaluru, Mysuru, Mandya, Tumakuru, and Chamarajanagar districts, covering 29 taluks/towns with precise GPS coordinates
- **data/comprehensive_doctors_dataset.json** - Full expanded doctor dataset (290 doctors) with taluk, district, coordinates, and Google Maps links
- **data/comprehensive_doctors_dataset.csv** - CSV export of the comprehensive doctor dataset
- **data/diagnostic_testing_matrix.json** - Diagnostic test recommendations with ICD codes
- **data/symptom_disease_dataset.csv** - CSV version of symptom-disease mapping data
- **data/clean_diseases.py** - Script for cleaning and processing disease data
- **data/build_json.py** - Script to build JSON data files
- **data/generate_combos_v3.py** - Script to generate symptom combinations
- **data/generate_expanded_doctors_v2.py** - Script that generated the comprehensive 290-doctor dataset with full taluk/hospital coverage

### Frontend Files
- **templates/index.html** - Home page with symptom selection interface
- **templates/consult.html** - Doctor finder page with location search
- **templates/about.html** - About page with project information
- **static/css/style.css** - Main stylesheet for the application
- **static/js/script.js** - JavaScript for home page predictions
- **static/js/consult.js** - JavaScript for doctor finder functionality
- **static/js/main.js** - Shared utility JavaScript functions

### XAMPP Integration (Windows)
- **index.php** - PHP entry point that redirects to Flask app
- **proxy.php** - PHP proxy to handle requests between XAMPP and Flask
- **access.html** - Access guide for XAMPP users
- **start_flask.bat** - Windows batch file to start Flask server
- **.htaccess** - Apache configuration for URL routing

### Configuration
- **requirements.txt** - Python package dependencies
- **README.md** - This documentation file

## Two-Symptom Combinations

Popular combinations and their predictions:

| Symptom 1 | Symptom 2 | Predicted Disease |
|-----------|-----------|-------------------|
| Fever | Cough | Common Cold |
| Fever | Headache | Viral Fever |
| Fever | Fatigue | Flu |
| Cough | Runny Nose | Common Cold |
| Headache | Nausea | Migraine |
| Chest Pain | Shortness of Breath | Breathing Issue |
| Fever | Rash | Viral Infection |

## What You See

When you select symptoms and click "Predict Disease":
- Predicted disease with confidence percentage
- Alternative disease suggestions
- Treatment recommendations
- Prevention tips
- Ayurvedic remedies
- When to consult a doctor
- Recommended specialist type

## Doctor Finder

Find doctors across 5 districts by specialty and taluk with precise location-based recommendations:
- **Districts covered**: Bengaluru, Mysuru, Mandya, Tumakuru, Chamarajanagar
- **Taluks/towns**: 29 major taluks and surrounding towns across all districts
- **Hospitals**: 58 unique facilities (urban + rural)
- **Doctors**: 290 specialists across 12 specialties
- **Specialties**: General Physician, Cardiologist, Pulmonologist, Orthopedist, Gastroenterologist, Neurologist, Dermatologist, ENT Specialist, Psychiatrist, Allergist, Infectious Disease Specialist, Hematologist
- **Features**: High-accuracy GPS location detection, distance-based sorting, Google Maps navigation with turn-by-turn directions

## Tech Used

- Backend: Flask (Python)
- ML: Decision Tree & Random Forest
- Data: JSON files
- Frontend: HTML, CSS, JavaScript

## Important

This app is for learning only. See a real doctor for medical advice.

## Model Accuracy

The machine learning models are trained with 300 samples per disease pattern:
- **Decision Tree**: ~95-100% training accuracy on test patterns
- **Random Forest**: ~95-100% training accuracy on test patterns

Training uses weighted samples:
- 60% perfect symptom matches
- 25% missing one primary symptom  
- 15% with one additional noise symptom

Note: These are training accuracies on synthetic data. Real-world accuracy would vary with actual patient data.