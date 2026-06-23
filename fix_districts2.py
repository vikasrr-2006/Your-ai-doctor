#!/usr/bin/env python3
"""
Final fix for remaining area names as districts.
"""

import json

with open('data/comprehensive_doctors_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

AREA_TO_DISTRICT = {
    "CFTRI Layout": "Mysuru",
    "H.D. Kote": "Mysuru",  # Taluk in Mysuru district
    "Krishnarajanagara": "Mandya",  # K.R. Pet taluk, Mandya district
    "Mariyala": "Chamarajanagar",
    "S.S.Puram": "Tumakuru",
    "Saraswathipuram": "Mysuru",
    "Urdigere": "Tumakuru",
    "Bylakuppe": "Mysuru",
    "Gundlupet": "Chamarajanagar",
    "Hunsur": "Mysuru",
    "Periyapatna": "Mysuru",
    "T. Narasipura": "Mysuru",
    "Nanjangud": "Mysuru",
}

for doctor in data['doctors']:
    area = doctor.get('city', '')
    if area in AREA_TO_DISTRICT:
        doctor['district'] = AREA_TO_DISTRICT[area]

with open('data/comprehensive_doctors_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed remaining districts")
from collections import Counter
districts = Counter(d['district'] for d in data['doctors'])
for district, count in sorted(districts.items()):
    print(f"  {district}: {count}")
