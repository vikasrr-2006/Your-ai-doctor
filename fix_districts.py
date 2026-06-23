#!/usr/bin/env python3
"""
Fix district field in the generated comprehensive dataset.
"""

import json

with open('data/comprehensive_doctors_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract district from area name or hospital name
for doctor in data['doctors']:
    area = doctor.get('city', '')
    hospital = doctor.get('hospital', '')
    
    # Determine district from area/taluk name
    if area in ['Mandya City', 'Maddur', 'Malavalli', 'Srirangapatna', 'Pandavapura', 'Krishnarajpet', 'Nagamangala', 'Kollegal Road']:
        doctor['district'] = 'Mandya'
    elif area in ['Siddique Nagar', 'MG Road', 'Kuvempunagar', 'R.S. Naidu Nagar', 'Siddhartha Layout', 'Mandi Mohalla', 'V.V. Mohalla', 'Hebbal Industrial Area', 'Yadavagiri', 'Jayalakshmipuram', 'Vidyaranyapura', 'Bannimantap', 'Bylakuppe', 'Nanjangud', 'Gundlupet']:
        doctor['district'] = 'Mysuru'
    elif area in ['Tumkur City', 'Sira', 'Madhugiri', 'Koratagere', 'Tiptur', 'Turuvekere', 'Kunigal', 'Shankarpura', 'Bheemasandra']:
        doctor['district'] = 'Tumakuru'
    elif area in ['Chamarajanagar', 'Kollegal', 'Yelandur', 'Hanur', 'Ramapura', 'Gundlupet']:
        doctor['district'] = 'Chamarajanagar'
    elif area in ['Hebbal', 'Rajajinagar', 'Jayanagar', 'HSR Layout', 'JP Nagar', 'Malleswaram', 'Bommasandra', 'Whitefield', 'VV Puram', 'Ashok Nagar', 'Shivaji Nagar', 'Cantonment', 'Richmond Town', 'Sampangi Rama Nagar', 'Frazer Town', 'Peenya', 'Kengeri', 'Bannerghatta', 'Yeshwanthpur', 'Sarjapur', 'New BEL Road']:
        doctor['district'] = 'Bengaluru'
    else:
        doctor['district'] = area

with open('data/comprehensive_doctors_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated districts in comprehensive_doctors_dataset.json")

# Print distribution
from collections import Counter
districts = Counter(d['district'] for d in data['doctors'])
for district, count in sorted(districts.items()):
    print(f"  {district}: {count}")
