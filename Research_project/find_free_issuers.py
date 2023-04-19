import os
import json

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folder = "dict\\wystawcy"
# Path to the output file
output_file = "results_wystawcy.json"

# Load keywords from file in dict folder
keywords = set()
for filename in os.listdir(dict_folder):
    with open(os.path.join(dict_folder, filename), "r") as f:
        for line in f:
            keywords.add(line.strip())

# Count the number of occurrences of each keyword
counts = {keyword: 0 for keyword in keywords}
total_records = 0
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            total_records += 1
            record = json.loads(line)
            for keyword in keywords:
                if record["issuer"] and keyword in record["issuer"]:
                    counts[keyword] += 1
                    
# Add total records processed to the counts dictionary
counts["TOTAL"] = total_records

# Output the results
with open(output_file, "w") as f:
    json.dump(counts, f)

