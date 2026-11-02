import json

# Read existing file
with open("C:/xampp/htdocs/new help/Your AI Doctor/data/symptom_disease_map.json", "r") as f:
    data = json.load(f)

# Write back with proper formatting
with open("C:/xampp/htdocs/new help/Your AI Doctor/data/symptom_disease_map.json", "w") as f:
    json.dump(data, f, indent=2)

print("Done! File updated successfully.")
print(f"Symptom mappings: {len(data['symptom_disease_mapping'])}")