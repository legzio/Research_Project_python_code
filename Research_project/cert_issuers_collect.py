import os
import json

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the output file
output_file = "cert_issuers.txt"

# Set to store unique issuers
issuers = set()

for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            data = json.loads(line)
            # Add the issuer to the set
            issuers.add(data["issuer"])
            
        

# Write results to output file
num_records = 0
with open(output_file, "w") as file:
    for issuer in issuers:
        file.write(issuer + "\n")
        num_records += 1

# Print the number of records
print("Number of records:", num_records)     

