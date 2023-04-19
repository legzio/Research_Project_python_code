import os
import json
from collections import defaultdict

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folder1 = "dict\\tlds"
dict_folder2 = "dict\\sld_tld"
# Path to the output file
output_file = "results_free_tlds_ilosc.json"

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

# Create a dictionary to store the keyword occurrences
keyword_occurrences = defaultdict(int)

# Search for records with domains containing any keyword
results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            if any(keyword == record["TLD"] for keyword in keywords1) or any(keyword == record["SLD_TLD"] for keyword in keywords2):
                results.append(record)
                if any(keyword == record["TLD"] for keyword in keywords1):
                    keyword_occurrences[record["TLD"]] += 1
                if any(keyword == record["SLD_TLD"] for keyword in keywords2):
                    keyword_occurrences[record["SLD_TLD"]] += 1

# Write keyword counts to output file
with open(output_file, "w") as f:
    json.dump(dict(keyword_occurrences), f)

# Print the keyword counts
for keyword, count in keyword_occurrences.items():
    print("Keyword:", keyword, "Count:", count)

