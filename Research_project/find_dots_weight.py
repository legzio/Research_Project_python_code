import os
import json

# Path to the data folder containing JSON files
data_folder = "data"

# Path to the output file
output_file = "results_dots.json"


# Search for records with domains containing any keyword
results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            weight = 3 # weight for this script
            dot_count = record["domain"].count('.')
            if dot_count > 2:
                record["weight"] = weight * dot_count
                results.append(record)

# Write results to output file
num_records = 0
with open(output_file, "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
        num_records += 1

# Print the number of records
print("Number of records:", num_records)        
