import os
import json
from collections import defaultdict

# Path to the data folder containing test database with JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folder = "dict\\kluczowe"
# Path to the output file
output_file = "results_kluczowe_ilosc_blik.json"

# Load keywords from file in dict folder
keywords = set()
for filename in os.listdir(dict_folder):
    with open(os.path.join(dict_folder, filename), "r") as f:
        for line in f:
            keywords.add(line.strip())

# Create a defaultdict to store keyword counts
keyword_counts = defaultdict(int)

# Search for records with domains containing any keyword
results = []
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            for keyword in keywords:
                if keyword in record["domain"]:
                    keyword_counts[keyword] += 1

# Write keyword counts to output file
with open(output_file, "w") as f:
    json.dump(dict(keyword_counts), f)

# Print the keyword counts
for keyword, count in keyword_counts.items():
    print("Keyword:", keyword, "Count:", count)
