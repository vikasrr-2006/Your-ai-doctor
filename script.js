// ================================================
// Your AI Doctor - Home Page Scripts
// ================================================

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const predictBtn = document.getElementById('predictBtn');
    const clearBtn = document.getElementById('clearBtn');
    const symptomCheckboxes = document.querySelectorAll('input[name="symptoms"]');
    
    // Result states
    const initialState = document.getElementById('initialState');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const successState = document.getElementById('successState');
    
    // Result elements
    const predictedDisease = document.getElementById('predictedDisease');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');
    const alternativesList = document.getElementById('alternativesList');
    const treatmentInfo = document.getElementById('treatmentInfo');
    const preventionInfo = document.getElementById('preventionInfo');
    const consultInfo = document.getElementById('consultInfo');
    const specialistInfo = document.getElementById('specialistInfo');
    const ayurvedaInfo = document.getElementById('ayurvedaInfo');
    const errorMessage = document.getElementById('errorMessage');

    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Predict button click handler
    if (predictBtn) {
        predictBtn.addEventListener('click', predictDisease);
    }

    // Clear button click handler
    if (clearBtn) {
        clearBtn.addEventListener('click', clearSelection);
    }

    // More symptoms button handler
    const moreSymptomsBtn = document.getElementById('moreSymptomsBtn');
    const extraSymptoms = document.getElementById('extraSymptoms');
    if (moreSymptomsBtn && extraSymptoms) {
        moreSymptomsBtn.addEventListener('click', function() {
            extraSymptoms.classList.toggle('hidden');
            if (extraSymptoms.classList.contains('hidden')) {
                moreSymptomsBtn.innerHTML = '<i class="fas fa-plus"></i> More Symptoms';
            } else {
                moreSymptomsBtn.innerHTML = '<i class="fas fa-minus"></i> Less Symptoms';
            }
        });
    }

    // Function to predict disease
    async function predictDisease() {
        // Get selected symptoms
        const selectedSymptoms = Array.from(symptomCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        // Validate selection
        if (selectedSymptoms.length === 0) {
            showError('No symptoms are selected. Please select at least one symptom.');
            return;
        }

        // Show loading state
        showLoading();

        try {
            const response = await fetch('predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symptoms: selectedSymptoms
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Prediction failed');
            }

            const data = await response.json();
            showSuccess(data);

        } catch (error) {
            console.error('Prediction error:', error);
            showError(error.message || 'An error occurred during prediction');
        }
    }

    // Function to clear selection
    function clearSelection() {
        symptomCheckboxes.forEach(cb => {
            cb.checked = false;
        });
        showInitial();
    }

    // Function to show initial state
    function showInitial() {
        hideAllStates();
        initialState.classList.remove('hidden');
    }

    // Function to show loading state
    function showLoading() {
        hideAllStates();
        loadingState.classList.remove('hidden');
    }

    // Function to show error state
    function showError(message) {
        hideAllStates();
        errorMessage.textContent = message;
        errorState.classList.remove('hidden');
    }

    // Function to show success state
    function showSuccess(data) {
        hideAllStates();
        
        // Update main prediction
        predictedDisease.textContent = data.predicted_disease;
        
        // Update confidence
        const confidence = data.confidence;
        confidenceValue.textContent = `${confidence}%`;
        confidenceFill.style.width = `${confidence}%`;
        
        // Update alternatives
        alternativesList.innerHTML = '';
        if (data.alternatives && data.alternatives.length > 0) {
            data.alternatives.forEach(alt => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${alt.disease}</span>
                    <span class="alt-confidence">${alt.confidence}%</span>
                `;
                alternativesList.appendChild(li);
            });
        }
        
        // Update disease info
        if (data.disease_info) {
            treatmentInfo.textContent = data.disease_info.primary_treatment || 'Not available';
            preventionInfo.textContent = data.disease_info.prevention_tips || 'Not available';
            consultInfo.textContent = data.disease_info.when_to_consult || 'Not available';
            specialistInfo.textContent = data.disease_info.recommended_specialist || 'General Physician';
            ayurvedaInfo.textContent = data.disease_info.ayurvedic_remedies || 'Not available';
        } else {
            treatmentInfo.textContent = 'Information not available';
            preventionInfo.textContent = 'Information not available';
            consultInfo.textContent = 'Consult a doctor if symptoms persist';
            specialistInfo.textContent = 'General Physician';
            ayurvedaInfo.textContent = 'Not available';
        }
        
        // Store predicted disease in sessionStorage for consult page
        sessionStorage.setItem('predictedDisease', data.predicted_disease);
        
        successState.classList.remove('hidden');
        
        // Scroll to results
        successState.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Function to hide all states
    function hideAllStates() {
        initialState.classList.add('hidden');
        loadingState.classList.add('hidden');
        errorState.classList.add('hidden');
        successState.classList.add('hidden');
    }

    // Add keyboard support
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.type !== 'textarea') {
            if (predictBtn && document.activeElement === predictBtn) {
                predictDisease();
            }
        }
    });
});
