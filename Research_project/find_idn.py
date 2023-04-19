import os
import json
import idna

# Path to the data folder containing JSON files
data_folder = "data"

# Path to the output file
output_file = "results_idn.json"


# Search for records with domains containing any keyword
results = []
temp = 0
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            domain_name = record["domain"]
            try:
                encoded_domain = idna.encode(domain_name)
                if domain_name != encoded_domain.decode() or "xn--" in domain_name:
                    results.append(record)
            except idna.IDNAError:  
                #print (f'{domain_name} is not a valid IDN domain')  
                temp+=1   

# Write results to output file
num_records = 0
with open(output_file, "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")
        num_records += 1

# Print the number of records
print("Number of records:", num_records)        
