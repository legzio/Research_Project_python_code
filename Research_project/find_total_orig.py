import os
import json
import idna

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folders = {
    "kluczowe": 40,
    "pomocnicze": 20,
    "tlds": 20,
    "sld_tld": 20
}
# Path to the output file
output_file = "result.json"

# Load keywords from files in dict folders
keywords = {}
for folder, weight in dict_folders.items():
    keywords[folder] = set()
    for filename in os.listdir(f"dict/{folder}"):
        with open(f"dict/{folder}/{filename}", "r") as f:
            for line in f:
                keywords[folder].add(line.strip())

# Search for records with domains containing any keyword
results = {}
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            if record["timestamp"] not in results:
                results[record["timestamp"]] = {"record": record, "weight": 0}
            for folder, weight in dict_folders.items():
                if any(keyword in record["domain"] for keyword in keywords[folder]):
                    results[record["timestamp"]]["weight"] += weight
            try:
                encoded_domain = idna.encode(record["domain"])
                if record["domain"] != encoded_domain.decode():
                    results[record["timestamp"]]["weight"] += 20
            except idna.IDNAError:  
                print (f'{record["domain"]} is not a valid IDN domain') 

            dot_count = record["domain"].count('.')
            if dot_count > 2:
                results[record["timestamp"]]["weight"] += dot_count * 3

            dash_count = record["domain"].count('-')
            if dash_count > 1:
                results[record["timestamp"]]["weight"] += dash_count * 3

            domain_length = len(record["domain"])
            if domain_length > 40:
                results[record["timestamp"]]["weight"] += 10
    
        

# Write results to output file
num_records = 0
with open(output_file, "w") as f:
    for record_id, result in results.items():
        if result["weight"] >= 80:
            f.write(json.dumps(result["record"]) + "\n")
            num_records += 1
            print("Weight:", result["weight"])
# Print the number of records
print("Number of records:", num_records)
