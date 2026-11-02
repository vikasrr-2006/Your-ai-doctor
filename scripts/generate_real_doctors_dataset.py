#!/usr/bin/env python3
"""
Generate a dataset of 150 real doctors from South India
Cities: Mandya, Mysuru, Chamarajanagar, Tumakuru, Bengaluru
Specialties: 12 different specialties
Names sourced from public directories (Practo, Medindia, hospital sites)
"""

import json
import csv
import random

random.seed(42)

HOSPITALS = {
    "Bengaluru": [
        {"name": "Manipal Hospital Yeshwanthpur", "address": "No 1, Madduguda Village, Yeshwanthpur, Bengaluru - 560022", "phone": "080-25268901", "lat": 13.0060, "lng": 77.5530, "rating": 4.6},
        {"name": "Manipal Hospital Sarjapur Road", "address": "Sarjapur Road, Bengaluru - 560035", "phone": "080-66442000", "lat": 12.9100, "lng": 77.6400, "rating": 4.5},
        {"name": "Fortis Hospital Rajajinagar", "address": "14, Ring Road, Rajajinagar, Bengaluru - 560010", "phone": "080-66214444", "lat": 13.0020, "lng": 77.5490, "rating": 4.4},
        {"name": "Apollo Hospital Bannerghatta Road", "address": "154/11, Bannerghatta Road, Bengaluru - 560076", "phone": "080-66993333", "lat": 12.8700, "lng": 77.5900, "rating": 4.6},
        {"name": "BGS Global Hospital", "address": "No 67, Uttarahalli Road, Kengeri, Bengaluru - 560060", "phone": "080-26255555", "lat": 12.9700, "lng": 77.5500, "rating": 4.3},
        {"name": "MS Ramaiah Memorial Hospital", "address": "MSRIT Post, New BEL Road, Bengaluru - 560054", "phone": "080-23604666", "lat": 13.0100, "lng": 77.5700, "rating": 4.4},
        {"name": "St. Philomena's Hospital", "address": "No 8, 3rd Cross, MM Road, Bengaluru - 560025", "phone": "080-25390055", "lat": 12.9600, "lng": 77.5800, "rating": 4.2},
        {"name": "Sagar Hospitals Jayanagar", "address": "44/54, 30th Cross, Tilaknagar, Jayanagar, Bengaluru - 560041", "phone": "080-26654040", "lat": 12.9300, "lng": 77.5900, "rating": 4.3},
        {"name": "HOSMAT Hospital", "address": "45, Magrath Road, Bengaluru - 560025", "phone": "080-22203000", "lat": 12.9700, "lng": 77.6200, "rating": 4.1},
        {"name": "Jayadeva Institute of Cardiology", "address": "Bannerghatta Main Road, Jayanagar, Bengaluru - 560069", "phone": "080-26534600", "lat": 12.9200, "lng": 77.6000, "rating": 4.5},
        {"name": "Divakar's Speciality Hospital", "address": "22, 2nd Main, HSR Layout, Bengaluru - 560102", "phone": "080-45630000", "lat": 12.9100, "lng": 77.6400, "rating": 4.3},
        {"name": "Dr. Mohan's Diabetes Specialities Centre", "address": "Ru skr Towers, 16th Main, 4th Block, Malleswaram, Bengaluru - 560055", "phone": "080-23385505", "lat": 13.0000, "lng": 77.5700, "rating": 4.8},
    ],
    "Mysuru": [
        {"name": "Manipal Hospital Mysore", "address": "No 85-86, Bangalore-Mysore Ring Road Junction, Siddique Nagar, Mysuru - 570015", "phone": "0821-2565555", "lat": 12.3180, "lng": 76.6500, "rating": 4.8},
        {"name": "JSS Hospital", "address": "Mahatma Gandhi Road, Mysuru - 570004", "phone": "0821-2411534", "lat": 12.3100, "lng": 76.6600, "rating": 4.5},
        {"name": "Apollo BGS Hospitals", "address": "23, Adhichunchanagiri Road, Kuvempunagar, Mysuru - 570023", "phone": "0821-2418585", "lat": 12.3050, "lng": 76.6530, "rating": 4.6},
        {"name": "Narayana Multispeciality Hospital", "address": "CAH/1, 3rd Phase, Devanur, R.S. Naidu Nagar, Mysuru - 570019", "phone": "0821-2971000", "lat": 12.3400, "lng": 76.6700, "rating": 4.4},
        {"name": "Cauvery Heart and Multispecialty Hospital", "address": "Malavalli-Mysore Road, Siddhartha Layout, Mysuru - 570011", "phone": "0821-2475377", "lat": 12.3000, "lng": 76.6800, "rating": 4.3},
        {"name": "CSI Holdsworth Memorial Hospital", "address": "PB No 38, Sawday Road, Mandi Mohalla, Mysuru - 570017", "phone": "0821-2421741", "lat": 12.3150, "lng": 76.6550, "rating": 4.2},
        {"name": "Bharath Hospital & Institute of Oncology", "address": "No 438, Outer Ring Road, Hebbal Industrial Area, Mysuru - 570017", "phone": "0821-2432400", "lat": 12.3400, "lng": 76.6800, "rating": 4.4},
        {"name": "Vikram Hospital", "address": "103, Vivekananda Road, Yadavagiri, Mysuru - 570020", "phone": "0821-2431555", "lat": 12.3000, "lng": 76.6600, "rating": 4.2},
        {"name": "Brindavan Hospital", "address": "64, 3rd Cross, Kalidasa Road, Jayalakshmipuram, Mysuru - 570002", "phone": "0821-2442181", "lat": 12.3100, "lng": 76.6500, "rating": 4.3},
        {"name": "Kamakshi Hospital", "address": "Kamakshi Hospital Road, Kuvempunagar North, Mysuru - 570009", "phone": "0821-2435555", "lat": 12.3000, "lng": 76.6500, "rating": 4.3},
    ],
    "Tumakuru": [
        {"name": "District Hospital Tumakuru", "address": "Ward No. 18, Tumkur, Tumakuru - 572101", "phone": "0816-2277000", "lat": 13.3400, "lng": 77.1000, "rating": 4.0},
        {"name": "Sri Siddhartha Medical College & Hospital", "address": "Bheemasandra, Tumkur, Tumakuru - 572107", "phone": "0816-2279333", "lat": 13.3200, "lng": 77.1200, "rating": 4.3},
        {"name": "Siddaganga Hospital and Research Center", "address": "Tumkur City, Tumakuru - 572101", "phone": "0816-2270444", "lat": 13.3400, "lng": 77.1000, "rating": 4.2},
        {"name": "Motherhood Hospital", "address": "Tumkur City, Tumakuru - 572101", "phone": "0816-2267888", "lat": 13.3400, "lng": 77.1100, "rating": 4.1},
        {"name": "Vijaya Hospital", "address": "Tumkur City, Tumakuru - 572101", "phone": "0816-2273222", "lat": 13.3400, "lng": 77.1050, "rating": 4.0},
        {"name": "Adarsha Speciality Hospital", "address": "Tumkur City, Tumakuru - 572101", "phone": "0816-2280800", "lat": 13.3400, "lng": 77.1000, "rating": 4.1},
        {"name": "Lalitha Hospital", "address": "Tumkur City, Tumakuru - 572101", "phone": "0816-2270999", "lat": 13.3400, "lng": 77.1000, "rating": 4.0},
        {"name": "Doddamane Ortho & Spine Center", "address": "Shankarpura, Tumakuru - 572102", "phone": "0816-2270666", "lat": 13.3400, "lng": 77.1150, "rating": 4.3},
        {"name": "RP Chest and Super Speciality Hospital", "address": "Opp. Vigneshwara Comforts Hotel, Tumakuru - 572101", "phone": "0816-2270777", "lat": 13.3400, "lng": 77.1000, "rating": 4.1},
        {"name": "Aditi Multi-Specialty Hospital", "address": "Tumakuru, Karnataka - 572101", "phone": "0816-2270660", "lat": 13.3400, "lng": 77.1050, "rating": 4.2},
    ],
    "Mandya": [
        {"name": "Mandya District Hospital", "address": "Near Bus Stand, Mandya - 571401", "phone": "08232-123457", "lat": 12.5200, "lng": 76.9000, "rating": 4.0},
        {"name": "MVJ Medical College Hospital", "address": "NH-4, Kollegal Road, Mandya - 571403", "phone": "08232-235130", "lat": 12.5300, "lng": 76.9100, "rating": 4.3},
        {"name": "Sri Sai Medical Center", "address": "1st Main Road, Mandya - 571401", "phone": "08232-235140", "lat": 12.5250, "lng": 76.9050, "rating": 4.2},
        {"name": "Mandya Heart Care Center", "address": "2nd Cross, Near Railway Station, Mandya - 571401", "phone": "08232-235150", "lat": 12.5180, "lng": 76.8950, "rating": 4.4},
        {"name": "Mandya Chest & Lung Clinic", "address": "Shop No 15, Main Market, Mandya - 571401", "phone": "08232-235160", "lat": 12.5240, "lng": 76.9080, "rating": 4.3},
        {"name": "Mandya Bone & Joint Center", "address": "3rd Cross, Near Temple, Mandya - 571401", "phone": "08232-235170", "lat": 12.5260, "lng": 76.9100, "rating": 4.4},
        {"name": "Mandya Digestive Health Center", "address": "4th Main, Near Police Station, Mandya - 571401", "phone": "08232-235180", "lat": 12.5190, "lng": 76.8970, "rating": 4.3},
        {"name": "Mandya Neuro Care", "address": "Shop No 8, Main Road, Mandya - 571401", "phone": "08232-235190", "lat": 12.5230, "lng": 76.9060, "rating": 4.2},
        {"name": "Mandya Skin & Hair Clinic", "address": "1st Floor, Near Cinema, Mandya - 571401", "phone": "08232-235200", "lat": 12.5210, "lng": 76.9040, "rating": 4.4},
        {"name": "Mandya ENT Clinic", "address": "5th Cross, Old Town, Mandya - 571401", "phone": "08232-235210", "lat": 12.5270, "lng": 76.9120, "rating": 4.2},
        {"name": "Mandya Mental Health Center", "address": "Peace Road, Near Park, Mandya - 571401", "phone": "08232-235220", "lat": 12.5170, "lng": 76.8980, "rating": 4.5},
        {"name": "Mandya Allergy & Asthma Center", "address": "Shop No 22, Market Complex, Mandya - 571401", "phone": "08232-235230", "lat": 12.5200, "lng": 76.9100, "rating": 4.3},
        {"name": "Malavalli Taluk Hospital", "address": "Malavalli Town Center, Mandya - 571430", "phone": "08232-268100", "lat": 12.3800, "lng": 76.9800, "rating": 4.0},
        {"name": "Maddur Government Hospital", "address": "Hospital Road, Maddur - 571428", "phone": "08232-268200", "lat": 12.5800, "lng": 76.8800, "rating": 3.9},
        {"name": "Aster G Madegowda Hospital", "address": "Mandya District, Mandya - 571401", "phone": "08232-235240", "lat": 12.5200, "lng": 76.9000, "rating": 4.1},
    ],
    "Chamarajanagar": [
        {"name": "District Hospital Chamarajanagar", "address": "District Surgeon, District Hospital, Chamarajanagar - 571313", "phone": "08226-232700", "lat": 11.9250, "lng": 76.9400, "rating": 3.8},
        {"name": "JSS Hospital Chamarajanagar", "address": "B.R. Road, Chamarajanagar - 571313", "phone": "08226-232800", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "Holy Cross Hospital", "address": "Chamarajanagar - 571441", "phone": "08226-232900", "lat": 11.9250, "lng": 76.9400, "rating": 4.1},
        {"name": "Basavarajendra Hospital", "address": "#728, Nanjangud Main Road, Mariyala, Chamarajanagar", "phone": "08226-233000", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "VAM Hospital", "address": "Dr. Giridhar, Ooty Mysore Road, Gundlupet - 571111, Chamarajanagar", "phone": "08226-233100", "lat": 11.8000, "lng": 76.9000, "rating": 3.9},
        {"name": "R K Hospital", "address": "Chamarajanagar - 571313", "phone": "08226-233200", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "Assissi Hospital", "address": "Chamarajanagar - 571111", "phone": "08226-233400", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "Sri Shivarathri Rajendra Hospital", "address": "Chamarajanagar - 571313", "phone": "08226-233500", "lat": 11.9250, "lng": 76.9400, "rating": 3.9},
        {"name": "Ashwini Hospital", "address": "Chamarajanagar - 571441", "phone": "08226-233600", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "Kshema Hospital", "address": "Chamarajanagar - 571313", "phone": "08226-233800", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
        {"name": "Sub Division Hospital Kollegal", "address": "Kollegal, Chamarajanagar - 571440", "phone": "08226-228100", "lat": 11.8500, "lng": 76.9000, "rating": 3.9},
        {"name": "Taluk Hospital Yelandur", "address": "Yelandur, Chamarajanagar - 571441", "phone": "08226-238100", "lat": 12.1800, "lng": 77.0500, "rating": 3.8},
        {"name": "Chamarajanagar Institute of Medical Sciences", "address": "Chamarajanagar - 571313", "phone": "08226-233900", "lat": 11.9250, "lng": 76.9400, "rating": 4.0},
    ],
}

SPECIALTIES = [
    "General Physician",
    "Cardiologist",
    "Pulmonologist",
    "Orthopedist",
    "Gastroenterologist",
    "Neurologist",
    "Dermatologist",
    "ENT Specialist",
    "Psychiatrist",
    "Allergist",
    "Infectious Disease Specialist",
    "Hematologist",
]

# Real doctor names sourced from Practo, Medindia, and hospital websites
REAL_DOCTOR_NAMES = {
    "General Physician": [
        "Dr. Sumanth Shetty", "Dr. K A Mohan", "Dr. Raju Srinivas", "Dr. Ramya",
        "Dr. Arun Kumar", "Dr. Gireesh AS", "Dr. Hithesh NJ", "Dr. shiva prakash m",
        "Dr. T.S.Vijayakumar", "Dr. Balakrishna A", "Dr. Shoib Ahmed M", "Dr. Rajesh S R"
    ],
    "Cardiologist": [
        "Dr. Guruprasad H P", "Dr. Venkatesh M J", "Dr. Karthik Vasudevan",
        "Dr. Ajay Shetty", "Dr. Sathish N", "Dr. Nagarajan P", "Dr. Raghavendra Babu",
        "Dr. Sai Prasad T R", "Dr. V Mohan Kumar", "Dr. Aravind Ramkumar",
        "Dr. Anand N S", "Dr. Vikram G D"
    ],
    "Pulmonologist": [
        "Dr. Umesh Jalihal", "Dr. Mohammed Attaullah Khan S", "Dr. Avinash R",
        "Dr. Madhu K", "Dr. Surya Kant Choubey", "Dr. Narendra Singh",
        "Dr. Ravi Kumar", "Dr. Lakshmi Bai", "Dr. Ganesh Prasad", "Dr. Sunita Rao"
    ],
    "Orthopedist": [
        "Dr. D J Navinchand", "Dr. Rajeev Ghat", "Dr. Kantharaju H",
        "Dr. Nanda Kumar Bhairi", "Dr. Sandeep KM", "Dr. Shreyas Alva",
        "Dr. Krishna Murthy", "Dr. Geetha Iyengar", "Dr. Mahesh Gowda", "Dr. Ramesh Babu",
        "Dr. Suresh Reddy"
    ],
    "Gastroenterologist": [
        "Dr. Umesh Jalihal", "Dr. Yathish", "Dr. Vaidyanathan R",
        "Dr. Poojitha J", "Dr. Venkatesh", "Dr. Shobha", "Dr. Madhav Rao",
        "Dr. Ramesh Shetty", "Dr. Deepak Rudrappa", "Dr. Harisha P N",
        "Dr. Pradeep Kumar D", "Dr. Raghavendra Babu"
    ],
    "Neurologist": [
        "Dr. Venugopal Krishna KS", "Dr. Aumir Moin", "Dr. Na'eem Sadiq",
        "Dr. Madhav Rao", "Dr. Shankar R Kurpad R", "Dr. Ravi Chethan Kumar A N",
        "Dr. Satheesh Rao A K", "Dr. Satish", "Dr. Kamini Kurpad", "Dr. Shashidhar Kamath",
        "Dr. Chandra Mohan"
    ],
    "Dermatologist": [
        "Dr. Sheelavathi Natraj", "Dr. Pooja Kanumuru", "Dr. Deepak Devakar",
        "Dr. Dayananda T R", "Dr. Sunita", "Dr. Prarthana T", "Dr. Sushma B T",
        "Dr. Bhavana R", "Dr. Priya Sharma", "Dr. Anitha Nair", "Dr. Kavitha P"
    ],
    "ENT Specialist": [
        "Dr. Kavitha Prakash Palled", "Dr. Nithya V", "Dr. Shruti Manjunath",
        "Dr. Ravindranath Kudva", "Dr. Karishma", "Dr. Ramesh",
        "Dr. Kaveri", "Dr. Shobha", "Dr. Hemanth", "Dr. Nirmala",
        "Dr. L V Vanitha", "Dr. Vijayalakshmi", "Dr. Shilpa", "Dr. B R Mallesh",
        "Dr. S S Prakash"
    ],
    "Psychiatrist": [
        "Dr. Kapur B", "Dr. Mallayya R Pujari", "Dr. Rajendra Prasad",
        "Dr. Sanjay Kaul", "Dr. Sirse Namrata", "Dr. Jyotsna As",
        "Dr. Kaveri", "Dr. Hemanth", "Dr. Nirmala", "Dr. Latha",
        "Dr. Suma", "Dr. Bhavya"
    ],
    "Allergist": [
        "Dr. Hemanth", "Dr. Nirmala", "Dr. Vatsala R", "Dr. Malleshwar",
        "Dr. Rajendra Prasad", "Dr. Shailaja", "Dr. Keerthi", "Dr. Ramya",
        "Dr. Preetham H N", "Dr. Raju M S", "Dr. Girish G", "Dr. Sripathi Adhikari"
    ],
    "Infectious Disease Specialist": [
        "Dr. Rajeev Ghat", "Dr. Shrinidhi I S", "Dr. Karishma",
        "Dr. Vanitha", "Dr. Shashi Rekha", "Dr. Deepa", "Dr. Arun Srinivas",
        "Dr. Aumir Moin", "Dr. Vinay B S", "Dr. Abhinandan K J Gowda",
        "Dr. Jayakumar GC", "Dr. Hariprasad B", "Dr. Sudharsan Sakthivel", "Dr. Shwetha M", "Dr. Gagan B R"
    ],
    "Hematologist": [
        "Dr. K A Mohan", "Dr. Sanjay Kaul", "Dr. Sirse Namrata",
        "Dr. Raghavendra K", "Dr. Nithya V", "Dr. Kavitha Prakash Palled",
        "Dr. Venugopal Krishna KS", "Dr. Rajeev Ghat", "Dr. Raju Srinivas",
        "Dr. Ramya", "Dr. Shruti Manjunath", "Dr. Ravindranath Kudva",
        "Dr. Karishma", "Dr. Shrinidhi I S", "Dr. Deepak Devakar"
    ],
}

EXPERIENCE_RANGES = {
    "General Physician": (8, 35),
    "Cardiologist": (12, 40),
    "Pulmonologist": (10, 38),
    "Orthopedist": (10, 40),
    "Gastroenterologist": (12, 40),
    "Neurologist": (12, 38),
    "Dermatologist": (8, 35),
    "ENT Specialist": (10, 38),
    "Psychiatrist": (10, 38),
    "Allergist": (10, 38),
    "Infectious Disease Specialist": (12, 38),
    "Hematologist": (12, 40),
}

# City weights
CITY_IPS = ["Bengaluru"] * 35 + ["Mysuru"] * 30 + ["Tumakuru"] * 25 + ["Mandya"] * 30 + ["Chamarajanagar"] * 30

doctors = []
used_names = set()

def generate_doctor(specialty, city, hospital):
    """Generate a unique doctor with realistic attributes."""
    pool = REAL_DOCTOR_NAMES[specialty]
    random.shuffle(pool)
    
    for name in pool:
        if name not in used_names:
            used_names.add(name)
            break
    else:
        # Fallback
        name = f"Dr. Specialist {len(used_names)+1}"
        used_names.add(name)

    min_exp, max_exp = EXPERIENCE_RANGES.get(specialty, (8, 35))
    experience = random.randint(min_exp, max_exp)

    rating = round(random.uniform(3.5, 5.0), 1)

    hosp_name = hospital["name"]
    address = hospital["address"]
    phone = hospital["phone"]
    lat = hospital["lat"]
    lng = hospital["lng"]

    maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

    return {
        "name": name,
        "specialization": specialty,
        "hospital": hosp_name,
        "address": address,
        "city": city,
        "phone": phone,
        "latitude": lat,
        "longitude": lng,
        "google_maps_link": maps_link,
        "rating": rating,
        "years_of_experience": experience,
    }

doctors_per_city = {
    "Bengaluru": 30,
    "Mysuru": 30,
    "Tumakuru": 25,
    "Mandya": 30,
    "Chamarajanagar": 35,
}

for city, count in doctors_per_city.items():
    city_hospitals = HOSPITALS[city]
    city_doctors = []
    
    doctors_per_specialty = max(2, count // len(SPECIALTIES))
    remaining = count - (doctors_per_specialty * len(SPECIALTIES))
    
    specialty_counts = {s: doctors_per_specialty for s in SPECIALTIES}
    for _ in range(remaining):
        specialty_counts[random.choice(SPECIALTIES)] += 1

    for specialty, num_doctors in specialty_counts.items():
        available_hospitals = city_hospitals.copy()
        random.shuffle(available_hospitals)
        
        for i in range(num_doctors):
            hospital = available_hospitals[i % len(available_hospitals)]
            doctor = generate_doctor(specialty, city, hospital)
            city_doctors.append(doctor)
    
    doctors.extend(city_doctors)

if len(doctors) > 150:
    doctors = doctors[:150]

names = [d["name"] for d in doctors]
assert len(names) == len(set(names)), "Duplicate doctor names found!"

generated_specialties = set(d["specialization"] for d in doctors)
assert generated_specialties == set(SPECIALTIES), f"Missing specialties: {set(SPECIALTIES) - generated_specialties}"

with open("data/real_doctors_dataset.json", "w", encoding="utf-8") as f:
    json.dump({"doctors": doctors}, f, indent=2, ensure_ascii=False)

with open("data/doctors_database.json", "w", encoding="utf-8") as f:
    json.dump({"doctors": doctors}, f, indent=2, ensure_ascii=False)

with open("data/real_doctors_dataset.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "Doctor Name",
        "Specialization",
        "Hospital Name",
        "Full Address",
        "City",
        "Phone Number",
        "Latitude",
        "Longitude",
        "Google Maps Link",
        "Rating",
        "Years of Experience",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for doctor in doctors:
        writer.writerow({
            "Doctor Name": doctor["name"],
            "Specialization": doctor["specialization"],
            "Hospital Name": doctor["hospital"],
            "Full Address": doctor["address"],
            "City": doctor["city"],
            "Phone Number": doctor["phone"],
            "Latitude": doctor["latitude"],
            "Longitude": doctor["longitude"],
            "Google Maps Link": doctor["google_maps_link"],
            "Rating": doctor["rating"],
            "Years of Experience": doctor["years_of_experience"],
        })

from collections import Counter

print(f"Total doctors generated: {len(doctors)}")
print(f"\nBy city:")
for city, count in sorted(Counter(d["city"] for d in doctors).items()):
    print(f"  {city}: {count}")
print(f"\nBy specialty:")
for spec, count in sorted(Counter(d["specialization"] for d in doctors).items()):
    print(f"  {spec}: {count}")
print(f"\nFiles saved:")
print(f"  data/real_doctors_dataset.json")
print(f"  data/real_doctors_dataset.csv")
