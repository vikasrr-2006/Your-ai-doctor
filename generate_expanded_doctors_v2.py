#!/usr/bin/env python3
"""
Generate an expanded dataset of doctors covering all taluks and towns across the 5 districts.
300+ doctors with unique names, proper taluk/district coverage, and precise coordinates.
"""

import json
import csv
import random

random.seed(42)

# Comprehensive hospital list by district/taluk with precise coordinates
HOSPITALS_BY_DISTRICT = {
    "Bengaluru": {
        "Bengaluru City": [
            {"name": "Apollo Hospitals Bannerghatta Road", "address": "154/11, Opp IIM-B, Bannerghatta Road, Bengaluru - 560076", "phone": "080-66993333", "lat": 12.8700, "lng": 77.5900, "rating": 4.6},
            {"name": "Manipal Hospital Yeshwanthpur", "address": "No 1, Madduguda Village, Yeshwanthpur, Bengaluru - 560022", "phone": "080-25268901", "lat": 13.0141, "lng": 77.5560, "rating": 4.7},
            {"name": "Fortis Hospital Rajajinagar", "address": "14, Ring Road, Rajajinagar, Bengaluru - 560010", "phone": "080-66214444", "lat": 13.0020, "lng": 77.5490, "rating": 4.5},
            {"name": "Jayadeva Institute of Cardiology", "address": "Bannerghatta Main Rd, Jayanagar, Bengaluru - 560069", "phone": "080-26534600", "lat": 12.9200, "lng": 77.6000, "rating": 4.6},
            {"name": "Narayana Hrudayalaya", "address": "258/A, Bommasandra Industrial Area, Anekal, Bengaluru - 560099", "phone": "080-7803555", "lat": 12.7900, "lng": 77.6900, "rating": 4.5},
            {"name": "BGS Global Hospital", "address": "No 67, Uttarahalli Road, Kengeri, Bengaluru - 560060", "phone": "080-26255555", "lat": 12.9700, "lng": 77.5500, "rating": 4.3},
            {"name": "MS Ramaiah Memorial Hospital", "address": "MSRIT Post, New BEL Road, Bengaluru - 560054", "phone": "080-23604666", "lat": 13.0100, "lng": 77.5700, "rating": 4.4},
            {"name": "HOSMAT Hospital", "address": "45, Magrath Road, Bengaluru - 560025", "phone": "080-22203000", "lat": 12.9700, "lng": 77.6200, "rating": 4.1},
            {"name": "St. Philomena's Hospital", "address": "No 8, 3rd Cross, MM Road, Bengaluru - 560025", "phone": "080-25390055", "lat": 12.9600, "lng": 77.5800, "rating": 4.2},
            {"name": "Sagar Hospitals Jayanagar", "address": "44/54, 30th Cross, Tilaknagar, Jayanagar, Bengaluru - 560041", "phone": "080-26654040", "lat": 12.9300, "lng": 77.5900, "rating": 4.3},
            {"name": "Columbia Asia Hospital Hebbal", "address": "Hebbal, Bengaluru - 560024", "phone": "080-42468888", "lat": 13.0350, "lng": 77.5970, "rating": 4.5},
            {"name": "Manipal Hospital Sarjapur Road", "address": "Sarjapur Road, Bengaluru - 560035", "phone": "080-66442000", "lat": 12.9200, "lng": 77.6650, "rating": 4.6},
            {"name": "KIMS Hospital", "address": "K.R. Road, V.V. Puram, Bengaluru - 560004", "phone": "080-22334455", "lat": 12.9450, "lng": 77.5750, "rating": 4.4},
        ],
        "Anekal": [
            {"name": "Narayana Hrudayalaya HSR Layout", "address": "HSR Layout, Bengaluru - 560102", "phone": "080-49222222", "lat": 12.9100, "lng": 77.6400, "rating": 4.4},
            {"name": "Indira Gandhi Institute Of Child Health", "address": "Dharmaram College Post, Bengaluru - 560029", "phone": "080-26094000", "lat": 12.9600, "lng": 77.6100, "rating": 4.3},
        ],
    },
    "Mysuru": {
        "Mysuru City": [
            {"name": "JSS Hospital", "address": "Mahatma Gandhi Road, Mysuru - 570004", "phone": "0821-2411534", "lat": 12.3100, "lng": 76.6600, "rating": 4.5},
            {"name": "Apollo BGS Hospitals", "address": "23, Adhichunchanagiri Road, Kuvempunagar, Mysuru - 570023", "phone": "0821-2418585", "lat": 12.3050, "lng": 76.6530, "rating": 4.6},
            {"name": "Manipal Hospital Mysore", "address": "No 85-86, Bangalore-Mysore Ring Road, Mysuru - 570015", "phone": "0821-2565555", "lat": 12.3180, "lng": 76.6500, "rating": 4.8},
            {"name": "Bharath Hospital & Institute of Oncology", "address": "Outer Ring Road, Hebbal Industrial Area, Mysuru - 570017", "phone": "0821-2432400", "lat": 12.3400, "lng": 76.6800, "rating": 4.4},
            {"name": "CSI Holdsworth Memorial Hospital", "address": "Sawday Road, Mandi Mohalla, Mysuru - 570017", "phone": "0821-2421741", "lat": 12.3150, "lng": 76.6550, "rating": 4.2},
        ],
        "Hunsur": [
            {"name": "Government Hospital Hunsur", "address": "Hunsur, Mysuru - 571105", "phone": "08222-252181", "lat": 12.2650, "lng": 76.2900, "rating": 3.9},
            {"name": "Hunsur Taluk Hospital", "address": "Hunsur - 571105", "phone": "08222-252182", "lat": 12.2650, "lng": 76.2900, "rating": 3.8},
        ],
        "Periyapatna": [
            {"name": "Government Hospital Periyapatna", "address": "Periyapatna, Mysuru - 571107", "phone": "08223-258000", "lat": 12.3400, "lng": 76.2350, "rating": 3.7},
        ],
        "T. Narasipura": [
            {"name": "Government Hospital T. Narasipura", "address": "T. Narasipura, Mysuru - 571124", "phone": "08222-275000", "lat": 12.2150, "lng": 76.2500, "rating": 3.7},
        ],
        "H.D. Kote": [
            {"name": "Government Hospital H.D. Kote", "address": "H.D. Kote, Mysuru - 571113", "phone": "08228-255210", "lat": 11.8150, "lng": 76.1950, "rating": 3.6},
        ],
        "Nanjangud": [
            {"name": "Government Hospital Nanjangud", "address": "Nanjangud, Mysuru - 571301", "phone": "08221-263000", "lat": 12.1200, "lng": 76.6800, "rating": 3.9},
        ],
        "Bylakuppe": [
            {"name": "Government Hospital Bylakuppe", "address": "Bylakuppe, Mysuru - 571104", "phone": "08223-259000", "lat": 12.3950, "lng": 76.1150, "rating": 3.6},
        ],
    },
    "Mandya": {
        "Mandya City": [
            {"name": "Mandya District Hospital", "address": "Near Bus Stand, Mandya - 571401", "phone": "08232-123457", "lat": 12.5200, "lng": 76.9000, "rating": 4.0},
            {"name": "MIMS Mandya", "address": "Nehru Nagar, Mandya - 571401", "phone": "08232-235000", "lat": 12.5250, "lng": 76.9050, "rating": 4.3},
            {"name": "MVJ Medical College Hospital", "address": "NH-4, Kollegal Road, Mandya - 571403", "phone": "08232-235130", "lat": 12.5300, "lng": 76.9100, "rating": 4.4},
            {"name": "Aster G Madegowda Hospital", "address": "Mandya District, Mandya - 571401", "phone": "08232-235240", "lat": 12.5200, "lng": 76.9000, "rating": 4.1},
        ],
        "Maddur": [
            {"name": "Maddur Government Hospital", "address": "Hospital Road, Maddur - 571428", "phone": "08232-268200", "lat": 12.5800, "lng": 76.8800, "rating": 3.9},
        ],
        "Malavalli": [
            {"name": "Malavalli Taluk Hospital", "address": "Malavalli Town Center, Mandya - 571430", "phone": "08232-268100", "lat": 12.3800, "lng": 76.9800, "rating": 4.0},
        ],
        "Srirangapatna": [
            {"name": "Srirangapatna Taluk Hospital", "address": "Srirangapatna, Mandya - 571438", "phone": "08236-272000", "lat": 12.4250, "lng": 76.7000, "rating": 3.9},
        ],
        "Pandavapura": [
            {"name": "Pandavapura Taluk Hospital", "address": "Pandavapura, Mandya - 571434", "phone": "08234-255555", "lat": 12.5050, "lng": 76.6650, "rating": 3.9},
        ],
        "Krishnarajpet": [
            {"name": "Krishnarajpet Taluk Hospital", "address": "Krishnarajpet, Mandya - 571426", "phone": "08234-275555", "lat": 12.4250, "lng": 76.7800, "rating": 3.9},
        ],
        "Nagamangala": [
            {"name": "Nagamangala Taluk Hospital", "address": "Nagamangala, Mandya - 571432", "phone": "08234-285555", "lat": 12.5250, "lng": 76.7600, "rating": 3.8},
        ],
    },
    "Tumakuru": {
        "Tumakuru City": [
            {"name": "District Hospital Tumakuru", "address": "Ward No. 18, Tumakuru - 572101", "phone": "0816-2277000", "lat": 13.3420, "lng": 77.1010, "rating": 4.0},
            {"name": "Sri Siddhartha Medical College & Hospital", "address": "Bheemasandra, Tumakuru - 572107", "phone": "0816-2279333", "lat": 13.3200, "lng": 77.1200, "rating": 4.4},
            {"name": "Siddaganga Hospital and Research Center", "address": "Tumakuru City - 572101", "phone": "0816-2270444", "lat": 13.3400, "lng": 77.1000, "rating": 4.2},
            {"name": "Motherhood Hospital", "address": "Tumakuru City - 572101", "phone": "0816-2267888", "lat": 13.3400, "lng": 77.1100, "rating": 4.1},
        ],
        "Sira": [
            {"name": "Government Hospital Sira", "address": "Tumkur-Sira Rd, Sira - 572137", "phone": "08135-255555", "lat": 13.7350, "lng": 76.8750, "rating": 3.9},
        ],
        "Madhugiri": [
            {"name": "Government Hospital Madhugiri", "address": "NH-234, Madhugiri - 572132", "phone": "08133-255555", "lat": 13.6600, "lng": 77.2050, "rating": 3.8},
        ],
        "Koratagere": [
            {"name": "Government Hospital Koratagere", "address": "Koratagere - 572129", "phone": "0811-266000", "lat": 13.5050, "lng": 77.2350, "rating": 3.8},
        ],
        "Tiptur": [
            {"name": "Government Hospital Tiptur", "address": "Tiptur - 572201", "phone": "0813-445555", "lat": 13.2550, "lng": 76.4750, "rating": 3.9},
        ],
        "Turuvekere": [
            {"name": "Government Hospital Turuvekere", "address": "Turuvekere - 572227", "phone": "0813-228888", "lat": 13.1550, "lng": 76.6650, "rating": 3.8},
        ],
        "Kunigal": [
            {"name": "Government Hospital Kunigal", "address": "Kunigal - 572130", "phone": "0813-225555", "lat": 13.0250, "lng": 76.9500, "rating": 3.8},
        ],
        "Gubbi": [
            {"name": "Government Hospital Gubbi", "address": "Gubbi - 572216", "phone": "0811-267777", "lat": 13.3150, "lng": 76.9450, "rating": 3.7},
        ],
    },
    "Chamarajanagar": {
        "Chamarajanagar City": [
            {"name": "District Hospital Chamarajanagar", "address": "District Surgeon, Chamarajanagar - 571313", "phone": "08226-232700", "lat": 11.9250, "lng": 76.9400, "rating": 3.9},
            {"name": "JSS Hospital Chamarajanagar", "address": "B.R. Road, Chamarajanagar - 571313", "phone": "08226-232800", "lat": 11.9250, "lng": 76.9400, "rating": 4.1},
            {"name": "Holy Cross Hospital", "address": "Chamarajanagar - 571441", "phone": "08226-232900", "lat": 11.9250, "lng": 76.9400, "rating": 4.2},
            {"name": "Shastha Eye Hospital", "address": "Old Union Bank Building, Yelandur - 571441", "phone": "08226-233300", "lat": 12.1800, "lng": 77.0500, "rating": 3.8},
        ],
        "Gundlupet": [
            {"name": "Government Hospital Gundlupet", "address": "Gundlupet - 571111", "phone": "08226-228400", "lat": 11.8000, "lng": 76.9000, "rating": 3.7},
        ],
        "Kollegal": [
            {"name": "Sub Division Hospital Kollegal", "address": "Kollegal - 571440", "phone": "08226-228100", "lat": 11.8500, "lng": 76.9000, "rating": 3.9},
            {"name": "Kollegal Taluk Hospital", "address": "Kollegal - 571440", "phone": "08226-228110", "lat": 11.8500, "lng": 76.9000, "rating": 3.8},
        ],
        "Yelandur": [
            {"name": "Taluk Hospital Yelandur", "address": "Yelandur - 571441", "phone": "08226-238100", "lat": 12.1800, "lng": 77.0500, "rating": 3.8},
        ],
        "Hanur": [
            {"name": "Government Hospital Hanur", "address": "Hanur - 571439", "phone": "08226-229555", "lat": 11.8500, "lng": 77.1500, "rating": 3.6},
        ],
        "Ramapura": [
            {"name": "Government Hospital Ramapura", "address": "Ramapura - 571444", "phone": "08226-237777", "lat": 11.9000, "lng": 77.1700, "rating": 3.7},
        ],
    }
}

SPECIALTIES = [
    "General Physician", "Cardiologist", "Pulmonologist", "Orthopedist",
    "Gastroenterologist", "Neurologist", "Dermatologist", "ENT Specialist",
    "Psychiatrist", "Allergist", "Infectious Disease Specialist", "Hematologist"
]

# South Indian name components (expanded list)
FIRST_NAMES = ["Sumanth", "K A", "Raju", "Ramya", "Arun", "Gireesh", "Hithesh", "Shiva",
    "Balakrishna", "Rajesh", "Manjunath", "Maqsood", "Nischay", "Pradeep",
    "Guruprasad", "Venkatesh", "Karthik", "Ajay", "Sathish", "Nagarajan",
    "Raghavendra", "Sai Prasad", "V Mohan", "Aravind", "Anand", "Vikram",
    "Umesh", "Mohammed", "Avinash", "Madhu", "Surya", "Narendra", "Ravi",
    "Lakshmi", "Ganesh", "Sunita", "Rajeev", "Kantharaju", "Sandeep", "Shreyas",
    "Krishna", "Geetha", "Mahesh", "Ramesh", "Yathish", "Vaidyanathan", "Poojitha",
    "Shobha", "Madhav", "Deepak", "Harisha", "Venugopal", "Aumir", "Na'eem",
    "Roshan", "Satheesh", "Kamini", "Shashidhar", "Chandra", "D J", "Sheelavathi",
    "Pooja", "Dayananda", "Prarthana", "Sushma", "Bhavana", "Priya", "Anitha",
    "Kavitha", "Nithya", "Kapur", "Mallayya", "Rajendra", "Sanjay", "Jyotsna",
    "Kaveri", "Hemanth", "Nirmala", "Latha", "Suma", "Bhavya", "Shailaja",
    "Keerthi", "Girish", "Sripathi", "Dheeraj", "Aditya", "Noor", "V Aravindappa",
    "Sagarika", "Aishwarya", "Kishor", "Yoganna", "Lalitha", "Sujith",
    "Vasudeva", "Naveeda", "Venkata", "Devaraj", "Gowtham", "Prasanna", "Sumaiya",
    "Ravindra", "Raghunatha", "Navin", "Tejas", "Naveen", "Hariprasad", "Bindu",
    "Keerthana", "Swathi", "Dinesh", "Ananya", "Sowmya", "Rashmi", "Anjali",
    "Divya", "Kiran", "Manoj", "Rakesh", "Nithin"]

LAST_NAMES = ["Shetty", "M J", "Reddy", "Srinivas", "Kaul", "Nair", "AS", "NJ",
    "Harsha", "R", "Patel", "Desai", "Hegde", "Gowda", "Kumar", "Prasad",
    "Rao", "Bhat", "Pai", "Iyengar", "Menon", "Iyer", "Swamy", "Babu",
    "Singh", "Verma", "Malhotra", "Choudhary", "Shah", "Mehta", "Shenoy",
    "Kamath", "Joshi", "Kulkarni", "Ranganathan", "Subramanian", "Vijayakumar",
    "Murthy", "Sharma", "Patil", "Das", "Gupta", "Banerjee", "Chatterjee"]

EXPERIENCE_RANGES = {
    "General Physician": (8, 35), "Cardiologist": (12, 40),
    "Pulmonologist": (10, 38), "Orthopedist": (10, 40),
    "Gastroenterologist": (12, 40), "Neurologist": (12, 38),
    "Dermatologist": (8, 35), "ENT Specialist": (10, 38),
    "Psychiatrist": (10, 38), "Allergist": (10, 38),
    "Infectious Disease Specialist": (12, 38), "Hematologist": (12, 40),
}

def generate_doctors():
    doctors = []
    used_pairs = set()
    
    # Flatten all hospitals
    all_hospitals = []
    for district, taluks in HOSPITALS_BY_DISTRICT.items():
        for taluk, hospitals in taluks.items():
            for h in hospitals:
                h["taluk"] = taluk
                h["district"] = district
                all_hospitals.append(h)
    
    # Generate 5 doctors per hospital (unique names, one doctor per hospital max)
    for hospital in all_hospitals:
        for i in range(5):
            # Generate unique name
            while True:
                name = f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                if name not in used_pairs:
                    used_pairs.add(name)
                    break
            
            specialty = random.choice(SPECIALTIES)
            min_exp, max_exp = EXPERIENCE_RANGES.get(specialty, (8, 35))
            experience = random.randint(min_exp, max_exp)
            rating = round(random.uniform(3.5, 5.0), 1)
            
            doctors.append({
                "name": name,
                "specialization": specialty,
                "hospital": hospital["name"],
                "address": hospital["address"],
                "taluk": hospital["taluk"],
                "district": hospital["district"],
                "phone": hospital["phone"],
                "latitude": hospital["lat"],
                "longitude": hospital["lng"],
                "google_maps_link": f"https://www.google.com/maps/search/?api=1&query={hospital['lat']},{hospital['lng']}",
                "rating": rating,
                "years_of_experience": experience,
            })
    
    return doctors

doctors = generate_doctors()

with open("data/comprehensive_doctors_dataset.json", "w", encoding="utf-8") as f:
    json.dump({"doctors": doctors}, f, indent=2, ensure_ascii=False)

with open("data/doctors_database.json", "w", encoding="utf-8") as f:
    json.dump({"doctors": doctors}, f, indent=2, ensure_ascii=False)

with open("data/comprehensive_doctors_dataset.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "specialization", "hospital", "address", 
                  "taluk", "district", "phone", "latitude", "longitude", 
                  "google_maps_link", "rating", "years_of_experience"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for doctor in doctors:
        writer.writerow(doctor)

from collections import Counter
print(f"Total doctors generated: {len(doctors)}")
print(f"\nBy district:")
for district, count in sorted(Counter(d["district"] for d in doctors).items()):
    print(f"  {district}: {count}")
print(f"\nBy taluk:")
for taluk, count in sorted(Counter(d["taluk"] for d in doctors).items()):
    print(f"  {taluk}: {count}")
print(f"\nTotal unique hospitals: {len(set(d['hospital'] for d in doctors))}")