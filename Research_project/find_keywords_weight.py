import os
import json

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folder = "dict\\kluczowe"
# Path to the output file
output_file = "results_kluczowe.json"

# Load keywords from file in dict folder
keywords = set()
for filename in os.listdir(dict_folder):
    with open(os.path.join(dict_folder, filename), "r") as f:
        for line in f:
            keywords.add(line.strip())

# Search for records with domains containing any keyword
results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            weight = 0 # weight for this script
            if any(keyword in record["domain"] for keyword in keywords):
                weight = weight + 50
                record["weight"] = weight
                results.append(record)

# Write results to output file
num_records = 0
with open(output_file, "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
        num_records += 1

# Print the number of records
print("Number of records:", num_records)        
