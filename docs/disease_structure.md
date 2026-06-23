# Disease Structure Documentation

**Version**: 3.1.0  
**Last Updated**: 2026-05-02  
**Total Symptoms**: 25  
**Source**: data/symptom_disease_map.json

## Overview

This document details the symptoms, diseases, and their combinations present in the AI Doctor system. The system uses a symptom-based approach with severity analysis and multi-symptom disease mapping.

---

## Symptom Database (25 Symptoms)

### Critical Symptoms (Emergency Flag: True)

| Symptom | Category | Severity | Common Triggers | Emergency |
|---------|----------|----------|----------------|----------|
| **Chest Pain** | Respiratory | Critical | Cardiac issues, muscle strain, lung problems | 🔴 True |
| **Shortness of Breath** | Respiratory | Critical | Asthma, cardiac issues, anxiety, lung conditions | 🔴 True |
| **Wheezing** | Respiratory | Critical | Asthma, bronchitis, allergic reaction, COPD | 🔴 True |

### Moderate Severity Symptoms (13 symptoms)

| Symptom | Category | Triggers |
|---------|----------|----------|
| Fever | General | Infection, inflammation, heat exposure |
| Headache | General | Tension, dehydration, migraine, stress |
| Vomiting | Gastrointestinal | Food poisoning, infection, motion sickness, migraine |
| Diarrhea | Gastrointestinal | Infection, food intolerance, medication |
| Abdominal Pain | Gastrointestinal | Indigestion, gas, infection, appendicitis |
| Back Pain | Musculoskeletal | Poor posture, muscle strain, injury, disc issues |
| Joint Pain | Musculoskeletal | Arthritis, injury, overuse, inflammation |
| Dizziness | General | Dehydration, low blood sugar, vertigo, medication |
| Swelling | Skin | Inflammation, injury, allergic reaction, fluid retention |
| Blurred Vision | Neurological | Eye strain, migraine, diabetes, glaucoma |
| Hearing Loss | Neurological | Ear infection, wax buildup, aging, noise exposure |
| Depression | Mental Health | Stress, loss, chemical imbalance, chronic illness |

### Mild Severity Symptoms (10 symptoms)

| Symptom | Category | Triggers |
|---------|----------|----------|
| Cough | Respiratory | Respiratory infection, allergies, irritants |
| Fatigue | General | Lack of sleep, stress, anaemia, overwork |
| Sore Throat | Respiratory | Viral infection, bacterial infection, allergies |
| Runny Nose | Respiratory | Allergies, cold, flu, sinusitis |
| Nausea | Gastrointestinal | Food poisoning, motion sickness, medication, pregnancy |
| Muscle Pain | Musculoskeletal | Exercise, tension, injury, fibromyalgia |
| Rash | Skin | Allergies, infection, irritants, autoimmune |
| Itching | Skin | Allergies, dry skin, insect bites, skin conditions |
| Insomnia | Mental Health | Stress, anxiety, poor sleep habits, depression |
| Anxiety | Mental Health | Stress, trauma, medication, medical conditions |

---

## Multi-Symptom Disease Mapping

### Disease Database (services/symptom_mapper.py)

The system maps 25+ diseases to symptom combinations:

#### Respiratory Diseases
- **Flu**: Fever(85%), Cough(70%), Fatigue(80%), Headache(75%), Muscle Pain(85%)
- **Common Cold**: Runny Nose(90%), Cough(65%), Sore Throat(80%)
- **Pneumonia**: Cough(85%), Fever(80%), Chest Pain(55%), Shortness of Breath(75%)
- **Bronchitis**: Cough(90%), Wheezing(65%), Chest Pain(45%)
- **Asthma**: Wheezing(90%), Shortness of Breath(90%), Cough(70%)
- **Sinusitis**: Runny Nose(70%), Headache(75%), Cough(55%)

#### Infectious Diseases
- **Malaria**: Fever(90%), Fatigue(80%), Headache(80%), Muscle Pain(75%)
- **Dengue**: Fever(85%), Fatigue(80%), Headache(70%), Muscle Pain(80%), Rash(60%)
- **Typhoid**: Fever(75%), Gastroenteritis symptoms

#### Gastrointestinal Diseases
- **Gastroenteritis**: Nausea(80%), Vomiting(75%), Diarrhea(85%), Abdominal Pain(75%)
- **Food Poisoning**: Nausea(85%), Vomiting(85%), Diarrhea(80%), Abdominal Pain(70%)

#### Neurological Diseases
- **Migraine**: Headache(90%), Nausea(60%), Dizziness(50%), Blurred Vision(45%)

#### Other Diseases
- **Anemia**: Fatigue(85%), Dizziness(55%), Shortness of Breath(55%)
- **Diabetes**: Blurred Vision(70%), Fatigue(60%)
- **Hypertension**: Headache(50%), Chest Pain(40%), Shortness of Breath(40%)
- **Thyroid Disorder**: Fatigue(70%), Insomnia(50%), Anxiety(45%), Depression(40%)
- **Allergies**: Runny Nose(85%), Itching(85%), Rash(70%), Swelling(55%)
- **Arthritis**: Joint Pain(75%), Back Pain(55%), Swelling(60%)
- **Ear Infection**: Ear Pain(90%), Hearing Loss(70%)

---

## Symptom Combination Analysis

### Single Symptom Examples
- **Fever alone**: Malaria (90%), Flu (85%), Pneumonia (80%)
- **Cough alone**: Bronchitis (90%), Pneumonia (85%), Flu (70%)

### Two-Symptom Combinations
- **Fever + Cough**: Flu (85%), Pneumonia (77.5%), COVID-style presentation
- **Fever + Fatigue**: Malaria (85%), Flu (82.5%), Dengue (82.5%)
- **Headache + Nausea**: Migraine (70%), Flu (65%)
- **Cough + Wheezing**: Asthma (82.5%), Bronchitis (77.5%)

### Three-Symptom Combinations
- **Fever + Cough + Fatigue**: Flu (80%), Pneumonia (66.7%), Malaria (75%)
- **Nausea + Vomiting + Diarrhea**: Food Poisoning (81.7%), Gastroenteritis (80%)
- **Headache + Dizziness + Nausea**: Migraine (60%), Anemia (53.3%)

### Multi-System Presentations
- **Fever + Rash + Joint Pain**: Dengue (75%), Autoimmune conditions
- **Chest Pain + Shortness of Breath + Dizziness**: Cardiac emergency, PE
- **Fatigue + Insomnia + Depression**: Thyroid disorder (55%), Mood disorder

---

## Disease Categories by System

### Respiratory System (6 diseases)
- Flu, Common Cold, Pneumonia, Bronchitis, Asthma, Sinusitis

### Infectious Diseases (3 diseases)
- Malaria, Dengue, Typhoid

### Gastrointestinal System (2 diseases)
- Gastroenteritis, Food Poisoning

### Neurological System (1 disease)
- Migraine

### Cardiovascular/Metabolic (3 diseases)
- Anemia, Diabetes, Hypertension

### Endocrine System (1 disease)
- Thyroid Disorder

### Musculoskeletal System (1 disease)
- Arthritis

### Allergic/Immune (1 disease)
- Allergies

### Ear/Nose/Throat (1 disease)
- Ear Infection

---

## Data Sources

### 1. symptom_disease_map.json
- 25 symptoms with metadata
- Categories, severity levels, emergency flags
- Common triggers for each symptom

### 2. symptom_mapper.py
- SYMPTOM_DISEASE_MAP: Direct symptom-to-disease probability mapping
- get_related_diseases(): Multi-symptom combination analysis
- CRITICAL_SYMPTOMS: Emergency condition flags

### 3. disease_solutions.json
- Disease-specific treatment recommendations
- Prevention strategies
- Ayurvedic remedies
- Consultation guidelines

---

## Analysis Methodology

### Probability Calculation
For N symptoms with individual disease probabilities P₁, P₂, ..., PN:
- **Normalized Score** = (Σ Pi) / N
- Higher scores = stronger symptom-disease match

### Criticality Assessment
- Chest Pain, Shortness of Breath → Cardiac/Pulmonary emergencies
- High Fever + Confusion → Meningitis, Sepsis risk
- Severe Abdominal Pain → Appendicitis, perforation risk

### Specificity Principle
- 1 symptom: Broad differential (5-10 possible diseases)
- 2 symptoms: Moderate specificity (3-5 possible diseases)
- 3+ symptoms: High specificity (1-3 likely diseases)

---

## Clinical Correlation

### High-Priority Presentations
| Symptoms | Likely Disease | Action |
|----------|---------------|--------|
| Chest Pain + SOB | Cardiac/Pulmonary | Immediate ER |
| Fever + Rash + Bleeding | Dengue/Malaria | Urgent care |
| Severe Headache + Neck Stiffness | Meningitis | Emergency |
| Abdominal Pain + Fever | Appendicitis | Surgical eval |

### Chronic Presentations
| Symptoms | Likely Disease | Management |
|----------|---------------|------------|
| Fatigue + Insomnia + Depression | Thyroid/Mood | Lab tests, referral |
| Joint Pain + Swelling + Fatigue | Arthritis | Rheumatology |
| Cough + Wheezing (chronic) | Asthma | Pulmonary function tests |

---

## System Implementation

### Integration Points
1. **app.py**: Loads symptom data, calls get_related_diseases()
2. **symptom_mapper.py**: Core disease mapping logic
3. **ML Models**: Decision Tree, Random Forest for pattern recognition
4. **Frontend**: Symptom selection interface, results display

### Data Flow
```
User selects symptoms → app.py validates → symptom_mapper.get_related_diseases()
    ↓
Probability calculation → Disease ranking → Criticality check
    ↓
Results formatted → Frontend display + Doctor recommendations
```

### API Endpoints Using Disease Data
- `POST /predict`: Disease prediction from symptoms
- `POST /api/diagnosis`: Detailed diagnostic information
- `GET /api/doctors`: Specialist matching based on predicted diseases

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.1.0 | 2026-05-02 | Multi-symptom disease mapping, 25 diseases added |
| 3.0.0 | 2026-05-01 | Symptom database reorganization |
| 2.5.0 | 2026-04-28 | Critical symptom flagging system |

---

## Notes

- Disease probabilities are based on symptom co-occurrence patterns
- Not a diagnostic tool - always consult healthcare professionals
- Emergency symptoms should trigger immediate medical attention
- System designed for educational and preliminary screening purposes
