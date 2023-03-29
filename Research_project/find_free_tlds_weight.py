import os
import json

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folder1 = "dict\\tlds"
dict_folder2 = "dict\\sld_tld"
# Path to the output file
output_file = "results_free_tlds.json"

# Load keywords from file TLD in dict folder
keywords1 = set()
for filename in os.listdir(dict_folder1):
    with open(os.path.join(dict_folder1, filename), "r") as f:
        for line in f:
            keywords1.add(line.strip())

# Load keywords from file SLD_TLD in dict folder
keywords2 = set()
for filename in os.listdir(dict_folder2):
    with open(os.path.join(dict_folder2, filename), "r") as f:
        for line in f:
            keywords2.add(line.strip())

# Search for records with domains containing any keyword
results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            weight = 0 # weight for this script
            if any(keyword == record["TLD"] for keyword in keywords1) or any(keyword == record["SLD_TLD"] for keyword in keywords2):
                weight = weight + 20
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
