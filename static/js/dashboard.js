// ================================================
// Your AI Doctor - PHC Dashboard Scripts
// ================================================

let currentPatient = null;
let patientQueue = [];
try {
    const stored = localStorage.getItem('patientQueue');
    patientQueue = stored ? JSON.parse(stored) : [];
} catch (e) {
    console.warn('localStorage not available:', e);
    patientQueue = [];
}

document.addEventListener('DOMContentLoaded', function() {
    loadQueue();
    setupEventListeners();
});

function setupEventListeners() {
    const moreBtn = document.getElementById('dashboardMoreBtn');
    const extraSymptoms = document.getElementById('dashboardExtraSymptoms');
    if (moreBtn && extraSymptoms) {
        moreBtn.addEventListener('click', function() {
            extraSymptoms.classList.toggle('hidden');
            const isHidden = extraSymptoms.classList.contains('hidden');
            this.innerHTML = isHidden 
                ? '<i class="fas fa-plus"></i> More Symptoms' 
                : '<i class="fas fa-minus"></i> Less Symptoms';
        });
    }

    const patientForm = document.getElementById('patientForm');
    if (patientForm) {
        patientForm.addEventListener('submit', handleTriage);
    }

    const clearBtn = document.getElementById('clearPatientBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearForm);
    }

    const findReferralBtn = document.getElementById('findReferralBtn');
    if (findReferralBtn) {
        findReferralBtn.addEventListener('click', findReferrals);
    }
}

function switchMode(mode) {
    const patientBtn = document.getElementById('patientModeBtn');
    const workerBtn = document.getElementById('workerModeBtn');
    
    if (mode === 'patient') {
        patientBtn.classList.add('active');
        workerBtn.classList.remove('active');
        window.location.href = '../';
    } else {
        workerBtn.classList.add('active');
        patientBtn.classList.remove('active');
        window.location.href = './dashboard';
    }
}

async function handleTriage(e) {
    e.preventDefault();
    
    const patientName = document.getElementById('patientName').value.trim();
    const patientAge = document.getElementById('patientAge').value;
    const patientGender = document.getElementById('patientGender').value;
    
    const symptoms = Array.from(document.querySelectorAll('#dashboardMainSymptoms input:checked, #dashboardExtraSymptoms input:checked'))
        .map(cb => cb.value);

    if (!patientName || !patientAge || !patientGender) {
        alert('Please fill in patient details');
        return;
    }

    if (symptoms.length === 0) {
        alert('Please select at least one symptom');
        return;
    }

    currentPatient = {
        name: patientName,
        age: patientAge,
        gender: patientGender,
        symptoms: symptoms,
        timestamp: new Date().toISOString()
    };

    document.getElementById('triageLoading').classList.remove('hidden');
    document.getElementById('triageResults').classList.add('hidden');
    document.getElementById('triageError').classList.add('hidden');
    document.getElementById('diagnosticResults').classList.add('hidden');

    try {
        const predictResponse = await fetch('predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: symptoms })
        });
        
        const predictData = await predictResponse.json();
        
        if (!predictResponse.ok) {
            throw new Error(predictData.error || 'Prediction failed');
        }

        displayTriageResults(predictData, patientName);

        const diagnosticResponse = await fetch('api/diagnosis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                symptoms: symptoms,
                demographic: {
                    age_group: getAgeGroup(patientAge),
                    gender: patientGender === 'male' ? 'male' : 'female',
                    has_comorbidity: false
                }
            })
        });

        const diagnosticData = await diagnosticResponse.json();
        
        if (diagnosticResponse.ok && diagnosticData.diagnostic_results) {
            displayDiagnosticResults(diagnosticData);
        }

        if (predictData.disease_info && predictData.disease_info.specialist) {
            document.getElementById('referralSpec').value = predictData.disease_info.specialist;
            findReferrals();
        }

    } catch (error) {
        document.getElementById('triageLoading').classList.add('hidden');
        document.getElementById('triageError').classList.remove('hidden');
        document.getElementById('triageErrorMessage').textContent = error.message;
    }
}

function displayTriageResults(data, patientName) {
    document.getElementById('triageLoading').classList.add('hidden');
    document.getElementById('triageResults').classList.remove('hidden');
    
    document.getElementById('resultPatientName').textContent = patientName;
    document.getElementById('predictedDisease').textContent = data.predicted_disease;
    
    const confidence = Math.round(data.confidence);
    document.getElementById('confidenceValue').textContent = confidence + '%';
    document.getElementById('confidenceFill').style.width = confidence + '%';
    
    const fill = document.getElementById('confidenceFill');
    if (confidence >= 70) {
        fill.style.background = 'var(--secondary-color)';
    } else if (confidence >= 40) {
        fill.style.background = 'var(--accent-color)';
    } else {
        fill.style.background = 'var(--danger-color)';
    }

    const alternativesList = document.getElementById('alternativesList');
    alternativesList.innerHTML = '';
    
    if (data.alternatives && data.alternatives.length > 0) {
        data.alternatives.forEach(alt => {
            const li = document.createElement('li');
            li.innerHTML = `<span>${alt.disease}</span> <span class="alt-confidence">${Math.round(alt.confidence)}%</span>`;
            alternativesList.appendChild(li);
        });
    } else {
        alternativesList.innerHTML = '<li>No alternative diagnoses available</li>';
    }

    const criticalWarning = document.getElementById('criticalWarning');
    const triageBadge = document.getElementById('triageBadge');
    
    if (data.is_critical) {
        criticalWarning.classList.remove('hidden');
        document.getElementById('criticalMessage').textContent = data.warning || 'Critical symptoms detected. Immediate medical attention required.';
        triageBadge.className = 'triage-badge urgent';
        triageBadge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Urgent';
        
        addToQueue(currentPatient, true);
    } else {
        criticalWarning.classList.add('hidden');
        triageBadge.className = 'triage-badge non-urgent';
        triageBadge.innerHTML = '<i class="fas fa-clock"></i> Non-Urgent';
        
        addToQueue(currentPatient, false);
    }

    const diseaseInfoSection = document.getElementById('diseaseInfoSection');
    if (diseaseInfoSection) {
        diseaseInfoSection.classList.add('hidden');
    }

    if (data.disease_info) {
        const treatmentInfo = document.getElementById('treatmentInfo');
        const preventionInfo = document.getElementById('preventionInfo');
        const consultInfo = document.getElementById('consultInfo');
        const specialistInfo = document.getElementById('specialistInfo');
        
        if (treatmentInfo) treatmentInfo.textContent = data.disease_info.primary_treatment || 'Not available';
        if (preventionInfo) preventionInfo.textContent = data.disease_info.prevention_tips || 'Not available';
        if (consultInfo) consultInfo.textContent = data.disease_info.when_to_consult || 'Not available';
        if (specialistInfo) specialistInfo.textContent = data.disease_info.recommended_specialist || 'General Physician';
        
        if (diseaseInfoSection) {
            diseaseInfoSection.classList.remove('hidden');
        }
    }
}

function displayDiagnosticResults(data) {
    document.getElementById('diagnosticLoading').classList.add('hidden');
    const container = document.getElementById('diagnosticResults');
    const content = document.getElementById('diagnosticContent');
    
    if (!data.diagnostic_results || data.diagnostic_results.length === 0) {
        content.innerHTML = '<p style="text-align: center; color: var(--gray-500); padding: 20px;">No specific diagnostic guidance available for these symptoms.</p>';
        container.classList.remove('hidden');
        return;
    }

    content.innerHTML = data.diagnostic_results.map(symptom => {
        const conditions = symptom.conditions.slice(0, 3).map(condition => {
            const topTests = condition.tests.slice(0, 2).map(test => test.test_name).join(', ');
            return `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--gray-200);">
                    <div>
                        <strong style="color: var(--dark-color);">${condition.condition_name}</strong>
                        <div style="font-size: 0.8rem; color: var(--gray-500); margin-top: 2px;">${topTests || 'No specific tests'}</div>
                    </div>
                    <span style="font-weight: 600; color: var(--primary-color);">${condition.probability}%</span>
                </div>
            `;
        }).join('');

        return `
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <strong style="color: var(--dark-color);"><i class="fas fa-stethoscope"></i> ${symptom.symptom_name}</strong>
                    ${symptom.emergency_flag ? '<span style="background: #fef2f2; color: var(--danger-color); padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">EMERGENCY</span>' : ''}
                </div>
                ${conditions}
            </div>
        `;
    }).join('');

    container.classList.remove('hidden');
}

async function findReferrals() {
    const specialization = document.getElementById('referralSpec').value;
    const district = document.getElementById('referralDistrict').value;
    
    document.getElementById('referralLoading').classList.remove('hidden');
    document.getElementById('referralResults').innerHTML = '';
    document.getElementById('noReferrals').classList.add('hidden');

    try {
        const params = new URLSearchParams();
        if (specialization) params.append('specialization', specialization);
        if (district) params.append('district', district);
        const query = params.toString();
        const url = 'api/doctors' + (query ? '?' + query : '');
        const response = await fetch(url);
        const doctors = await response.json();
        
        document.getElementById('referralLoading').classList.add('hidden');
        
        if (doctors.length === 0) {
            document.getElementById('noReferrals').classList.remove('hidden');
            return;
        }

        const container = document.getElementById('referralResults');
        container.innerHTML = doctors.map(doctor => {
            const initials = doctor.name
                .replace('Dr.', '')
                .trim()
                .split(' ')
                .map(n => n[0])
                .join('')
                .toUpperCase();

            const mapQuery = encodeURIComponent(`${doctor.hospital} ${doctor.address}`);
            const viewMapLink = `https://www.google.com/maps/search/?api=1&query=${mapQuery}`;

            return `
                <div class="doctor-card">
                    <div class="doctor-header">
                        <div class="doctor-avatar">${initials}</div>
                        <div class="doctor-info">
                            <h4>${doctor.name}</h4>
                            <span class="specialization">${doctor.specialization}</span>
                        </div>
                        ${doctor.distance ? `<span class="doctor-distance"><i class="fas fa-map-marker-alt"></i> ${doctor.distance} km</span>` : ''}
                    </div>
                    <div class="doctor-details">
                        <div class="doctor-detail">
                            <i class="fas fa-hospital"></i>
                            <span>${doctor.hospital}</span>
                        </div>
                        <div class="doctor-detail">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>${doctor.taluk ? doctor.taluk + ', ' : ''}${doctor.district}</span>
                        </div>
                        <div class="doctor-detail">
                            <i class="fas fa-phone"></i>
                            <span>${doctor.phone}</span>
                        </div>
                    </div>
                    <div class="rating">
                        ${generateStars(doctor.rating)}
                        <span>${doctor.rating}</span>
                    </div>
                    <div class="doctor-actions">
                        <a href="${viewMapLink}" target="_blank" rel="noopener noreferrer" class="btn-directions">
                            <i class="fas fa-location-arrow"></i>
                            Get Directions
                        </a>
                        <a href="${viewMapLink}" target="_blank" rel="noopener noreferrer" class="btn-map">
                            <i class="fas fa-map"></i>
                            View on Map
                        </a>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        document.getElementById('referralLoading').classList.add('hidden');
        console.error('Referral search error:', error);
    }
}

function generateStars(rating) {
    let stars = '';
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }

    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }

    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }

    return stars;
}

function addToQueue(patient, isUrgent) {
    const existingIndex = patientQueue.findIndex(p => p.name === patient.name && p.timestamp === patient.timestamp);
    if (existingIndex === -1) {
        patientQueue.unshift({ ...patient, isUrgent, id: Date.now() });
        localStorage.setItem('patientQueue', JSON.stringify(patientQueue));
        loadQueue();
    }
}

function removeFromQueue(id) {
    patientQueue = patientQueue.filter(p => p.id !== id);
    localStorage.setItem('patientQueue', JSON.stringify(patientQueue));
    loadQueue();
}

function loadQueue() {
    const container = document.getElementById('patientQueue');
    const countBadge = document.getElementById('queueCount');
    
    countBadge.textContent = `${patientQueue.length} patient${patientQueue.length !== 1 ? 's' : ''}`;
    
    if (patientQueue.length === 0) {
        container.innerHTML = `
            <div class="empty-queue">
                <i class="fas fa-inbox"></i>
                <p>No patients in queue. Add patients from the intake form above.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = patientQueue.map(patient => `
        <div class="queue-item ${patient.isUrgent ? 'urgent' : ''}">
            <div class="queue-item-info">
                <div class="queue-item-name">${patient.name} ${patient.isUrgent ? '<i class="fas fa-exclamation-triangle" style="color: var(--danger-color);"></i>' : ''}</div>
                <div class="queue-item-meta">
                    ${patient.age} yrs | ${patient.gender} | ${patient.symptoms.length} symptoms | ${new Date(patient.timestamp).toLocaleTimeString()}
                </div>
            </div>
            <div class="queue-item-actions">
                <button class="btn-view" onclick="viewPatient(${patient.id})">View</button>
                <button class="btn-remove" onclick="removeFromQueue(${patient.id})">Remove</button>
            </div>
        </div>
    `).join('');
}

function viewPatient(id) {
    const patient = patientQueue.find(p => p.id === id);
    if (!patient) return;

    document.getElementById('patientName').value = patient.name;
    document.getElementById('patientAge').value = patient.age;
    document.getElementById('patientGender').value = patient.gender;
    
    document.querySelectorAll('#dashboardMainSymptoms input, #dashboardExtraSymptoms input').forEach(cb => {
        cb.checked = patient.symptoms.includes(cb.value);
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function clearForm() {
    document.getElementById('patientForm').reset();
    document.getElementById('triageResults').classList.add('hidden');
    document.getElementById('triageLoading').classList.add('hidden');
    document.getElementById('triageError').classList.add('hidden');
    document.getElementById('diagnosticResults').classList.add('hidden');
    document.getElementById('referralResults').innerHTML = '';
    document.getElementById('noReferrals').classList.add('hidden');
    currentPatient = null;
}

function getAgeGroup(age) {
    const ageNum = parseInt(age);
    if (ageNum < 18) return 'child';
    if (ageNum < 60) return 'adult';
    return 'elderly';
}
