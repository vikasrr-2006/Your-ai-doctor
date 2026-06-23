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

Fever, Cough, Headache, Fatigue, Sore Throat, Runny Nose, Chest Pain, Shortness of Breath, Nausea, Vomiting, Diarrhea, Abdominal Pain, Back Pain, Joint Pain, Muscle Pain, Dizziness, Rash, Itching, Swelling, Blurred Vision, Hearing Loss, Insomnia, Anxiety, Depression, Wheezing.

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
