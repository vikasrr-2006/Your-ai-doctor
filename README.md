# 🩺 Your AI Doctor
### AI-Powered Healthcare Assistant | Machine Learning | Python

<p align="center">
  **An intelligent symptom-based disease prediction system designed to provide preliminary healthcare information.**
</p>

---

## 📌 About the Project

**Your AI Doctor** is a web-based healthcare assistance application developed using Python and Machine Learning. It allows users to select their symptoms and receive predictions about possible health conditions.

The system analyzes the selected symptoms using machine-learning models and provides preliminary health information, recommendations, precautions and guidance on when to seek medical attention.

This project demonstrates how Artificial Intelligence and Machine Learning can support accessible healthcare information.

## ✨ Key Features

- 🩺 **Symptom Checker:** Select symptoms from an available list of 25 symptoms.
- 🤖 **Disease Prediction:** Predicts possible diseases using Machine Learning.
- 📊 **Prediction Confidence:** Displays prediction confidence and alternative predictions.
- 💊 **Health Recommendations:** Provides basic treatment information and precautions.
- 🌿 **Ayurvedic Information:** Displays relevant traditional remedy information.
- 🏥 **Doctor Information:** Provides doctor-related information.
- 📍 **Location-Based Assistance:** Helps users explore healthcare services.
- ⚠️ **Medical Alerts:** Provides guidance on when professional medical attention is required.
- 💻 **User-Friendly Interface:** Simple and accessible web interface.

## 🧠 Machine Learning Models

The project uses Machine Learning techniques for symptom-based disease prediction.

| Model | Purpose |
|---|---|
| Decision Tree | Primary disease prediction |
| Random Forest | Additional prediction validation |

### Prediction Workflow

1. User selects symptoms.
2. System processes the selected symptoms.
3. Decision Tree predicts a possible disease.
4. Random Forest provides additional model-based validation.
5. The application displays prediction results and health recommendations.

## 🩻 Available Symptoms

The application includes 25 symptoms:

- Fever
- Cough
- Headache
- Fatigue
- Sore Throat
- Runny Nose
- Chest Pain
- Shortness of Breath
- Nausea
- Vomiting
- Diarrhea
- Abdominal Pain
- Back Pain
- Joint Pain
- Muscle Pain
- Dizziness
- Rash
- Itching
- Swelling
- Blurred Vision
- Hearing Loss
- Insomnia
- Anxiety
- Depression
- Wheezing

## 🛠️ Technologies Used

**Frontend**
- HTML5
- CSS3
- JavaScript

**Backend**
- Python
- Flask

**Machine Learning**
- Scikit-learn
- Pandas
- NumPy
- Decision Tree
- Random Forest

**Development Tools**
- Visual Studio Code
- Git
- GitHub

## 📂 Project Structure

```text
Your-ai-doctor/
│
├── Your-ai-doctor/
├── data/
├── models/
├── screenshots/
├── scripts/
├── static/
│   └── js/
├── templates/
│
└── README.md
```

*The structure above reflects the main folders currently visible in the GitHub repository. The nested folder and individual file contents may contain additional application components.*

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vikasrr-2006/Your-ai-doctor.git
```

### 2. Navigate to the Project Directory

```bash
cd Your-ai-doctor
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Generate Machine Learning Models

```bash
python create_models.py
```

### 7. Start the Application

```bash
python app.py
```

### 8. Open in Your Browser

```text
http://127.0.0.1:5000
```

*Note: Run these commands from the directory containing the respective files. If the application files are inside the nested project folder, navigate into that folder first.*

## 📸 Application Screenshots

Screenshots of the application are available in the [`screenshots`](screenshots/) directory.

Add the following views to this section using their actual filenames:

- Home Page
- Symptom Selection Page
- Disease Prediction Results
- Doctor Information Page
- About Page

## 🎯 Project Objectives

- Develop an AI-powered healthcare assistance application.
- Demonstrate Machine Learning applications in healthcare.
- Provide preliminary symptom-based health information.
- Improve accessibility to basic healthcare information.
- Build a user-friendly web-based application.

## 🔮 Future Enhancements

- Integration of advanced Machine Learning and Deep Learning models.
- Improved multilingual support.
- More comprehensive and medically validated datasets.
- Enhanced doctor and hospital discovery.
- Improved location-based healthcare recommendations.
- Better mobile responsiveness.

## 👨‍💻 Developer

**Vikas R R**

Final-Year BCA Project

GitHub: [@vikasrr-2006](https://github.com/vikasrr-2006)

**Project Repository:**  
[Your AI Doctor](https://github.com/vikasrr-2006/Your-ai-doctor)

## ⚠️ Medical Disclaimer

Your AI Doctor is an academic project developed for educational and research purposes.

The predictions and recommendations provided by this application are not a substitute for professional medical diagnosis, consultation or treatment.

Always consult a qualified healthcare professional for medical advice. Do not delay emergency medical care based on an application prediction.

## 📄 License

Refer to the repository's LICENSE file for licensing information.
