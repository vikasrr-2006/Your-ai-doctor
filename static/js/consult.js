// ================================================
// Your AI Doctor - Consult Page Scripts
// ================================================

let userLocation = null;
let currentSpecialization = '';
let currentDistrict = 'Mandya';

let specializationSelect;
let districtSelect;
let detectLocationBtn;
let locationStatus;
let doctorsList;
let loadingDoctors;
let noDoctors;

document.addEventListener('DOMContentLoaded', function() {
    specializationSelect = document.getElementById('specialization');
    districtSelect = document.getElementById('district');
    detectLocationBtn = document.getElementById('detectLocation');
    locationStatus = document.getElementById('locationStatus');
    doctorsList = document.getElementById('doctorsList');
    loadingDoctors = document.getElementById('loadingDoctors');
    noDoctors = document.getElementById('noDoctors');

    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    if (specializationSelect) {
        specializationSelect.addEventListener('change', function() {
            currentSpecialization = this.value;
            loadDoctors();
        });
    }

    if (districtSelect) {
        districtSelect.addEventListener('change', function() {
            currentDistrict = this.value;
            loadDoctors();
        });
    }

    if (detectLocationBtn) {
        detectLocationBtn.addEventListener('click', detectUserLocation);
    }

    loadDoctors();
});

function detectUserLocation() {
    if (!navigator.geolocation) {
        locationStatus.textContent = 'Geolocation not supported';
        locationStatus.className = 'location-status error';
        return;
    }

    locationStatus.textContent = 'Detecting location...';
    locationStatus.className = 'location-status';
    detectLocationBtn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        function(position) {
            userLocation = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy
            };
            
            const acc = Math.round(position.coords.accuracy);
            locationStatus.textContent = `Location detected (±${acc}m)`;
            locationStatus.className = 'location-status success';
            detectLocationBtn.disabled = false;
            
            loadDoctors();
        },
        function(error) {
            let errorMessage = 'Unable to detect location';
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = 'Location permission denied';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = 'Location unavailable';
                    break;
                case error.TIMEOUT:
                    errorMessage = 'Location request timeout';
                    break;
            }
            locationStatus.textContent = errorMessage;
            locationStatus.className = 'location-status error';
            detectLocationBtn.disabled = false;
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
}

async function loadDoctors() {
    showLoading();

    try {
        let url = 'api/doctors';
        const params = new URLSearchParams();

        if (currentSpecialization) {
            params.append('specialization', currentSpecialization);
        }

        if (currentDistrict) {
            params.append('district', currentDistrict);
        }

        if (userLocation) {
            params.append('latitude', userLocation.latitude);
            params.append('longitude', userLocation.longitude);
        }

        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch doctors');
        }

        const doctors = await response.json();
        displayDoctors(doctors);

    } catch (error) {
        console.error('Error loading doctors:', error);
        showError();
    }
}

function displayDoctors(doctors) {
    hideAll();

    if (doctors.length === 0) {
        noDoctors.classList.remove('hidden');
        return;
    }

    doctorsList.innerHTML = '';

    doctors.forEach((doctor, index) => {
        const card = createDoctorCard(doctor, index);
        doctorsList.appendChild(card);
    });

    doctorsList.classList.remove('hidden');
}

function createDoctorCard(doctor, index) {
    const card = document.createElement('div');
    card.className = 'doctor-card';
    
    const initials = doctor.name
        .replace('Dr.', '')
        .trim()
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase();

    const mapQuery = encodeURIComponent(`${doctor.hospital} ${doctor.address}`);
    const viewMapLink = `https://www.google.com/maps/search/?api=1&query=${mapQuery}`;
    const directionsLink = userLocation 
        ? `https://www.google.com/maps/dir/?api=1&origin=${userLocation.latitude},${userLocation.longitude}&destination=${doctor.latitude},${doctor.longitude}`
        : viewMapLink;

    card.innerHTML = `
        <div class="doctor-header">
            <div class="doctor-avatar">${initials}</div>
            <div class="doctor-info">
                <h3>${doctor.name}</h3>
                <span class="specialization">${doctor.specialization}</span>
            </div>
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
        ${doctor.distance ? `<div class="distance-tag">
            <i class="fas fa-location-arrow"></i>
            ${doctor.distance} km away
        </div>` : ''}
        <div class="doctor-actions">
            <a href="${directionsLink}" target="_blank" rel="noopener noreferrer" class="btn-directions">
                <i class="fas fa-location-arrow"></i>
                Get Directions
            </a>
            <a href="${viewMapLink}" target="_blank" rel="noopener noreferrer" class="btn-map">
                <i class="fas fa-map"></i>
                View on Map
            </a>
        </div>
    `;

    return card;
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

function showLoading() {
    hideAll();
    loadingDoctors.classList.remove('hidden');
}

function showError() {
    hideAll();
    noDoctors.querySelector('h3').textContent = 'Error Loading Doctors';
    noDoctors.querySelector('p').textContent = 'Please try again later';
    noDoctors.classList.remove('hidden');
}

function hideAll() {
    loadingDoctors.classList.add('hidden');
    doctorsList.classList.add('hidden');
    noDoctors.classList.add('hidden');
    
    noDoctors.querySelector('h3').textContent = 'No Doctors Found';
    noDoctors.querySelector('p').textContent = 'Try selecting a different specialization or city';
}

window.addEventListener('popstate', function() {
    const urlParams = new URLSearchParams(window.location.search);
    currentSpecialization = urlParams.get('specialization') || '';
    currentDistrict = urlParams.get('district') || 'Mandya';
    if (specializationSelect && currentSpecialization) {
        specializationSelect.value = currentSpecialization;
    }
    if (districtSelect && currentDistrict) {
        districtSelect.value = currentDistrict;
    }
    loadDoctors();
});

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        loadDoctors();
    }
});
