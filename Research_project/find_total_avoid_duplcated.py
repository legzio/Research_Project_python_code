import os
import json
import idna

# Path to the data folder containing JSON files
data_folder = "data"
# Path to the dict folder containing keywords text file
dict_folders_domain = {
    "kluczowe": 50,
    "pomocnicze": 25
}
dict_folders_tld = {    
    "tlds": 20
}
dict_folders_sld_tld = {
    "sld_tld": 20
}
dict_folders_allowed = "dict\\dozwolone"
dict_folders_issuers = "dict\\wystawcy"


# Path to the output file
output_file1 = "result_low.json"
output_file2 = "result_medium.json"
output_file3 = "result_high.json"

# Load keywords from files in dict folders
keywords_domain = {}
for folder, weight in dict_folders_domain.items():
    keywords_domain[folder] = set()
    for filename in os.listdir(f"dict/{folder}"):
        with open(f"dict/{folder}/{filename}", "r") as f:
            for line in f:
                keywords_domain[folder].add(line.strip())

keywords_tld = {}
for folder, weight in dict_folders_tld.items():
    keywords_tld[folder] = set()
    for filename in os.listdir(f"dict/{folder}"):
        with open(f"dict/{folder}/{filename}", "r") as f:
            for line in f:
                keywords_tld[folder].add(line.strip())

keywords_sld_tld = {}
for folder, weight in dict_folders_sld_tld.items():
    keywords_sld_tld[folder] = set()
    for filename in os.listdir(f"dict/{folder}"):
        with open(f"dict/{folder}/{filename}", "r") as f:
            for line in f:
                keywords_sld_tld[folder].add(line.strip())

keywords_allowwed = set()
for filename in os.listdir(dict_folders_allowed):
    with open(os.path.join(dict_folders_allowed, filename), "r") as f:
        for line in f:
            keywords_allowwed.add(line.strip())

keywords_issuers = set()
for filename in os.listdir(dict_folders_issuers):
    with open(os.path.join(dict_folders_issuers, filename), "r") as f:
        for line in f:
            keywords_issuers.add(line.strip())


# Search for records with domains containing any keyword
results = {}
temp = 0
rec_tot = 0
for filename in os.listdir(data_folder):
    with open(os.path.join(data_folder, filename), "r") as f:
        for line in f:
            record = json.loads(line)
            if not any(keyword in record["regdomain"] or keyword in record["domain"] for keyword in keywords_allowwed):
                if record["issuer"] and any(keyword in record["issuer"] for keyword in keywords_issuers):
                    rec_tot += 1
                    if record["timestamp"] not in results:
                        results[record["timestamp"]] = {"record": record, "weight": 0}
                    for folder, weight in dict_folders_domain.items():
                        if any(keyword in record["domain"] for keyword in keywords_domain[folder]):
                            results[record["timestamp"]]["weight"] += weight
                            # print("Weight keywords:", results[record["timestamp"]]["weight"])
                    for folder, weight in dict_folders_tld.items():
                        if any(keyword == record["TLD"] for keyword in keywords_tld[folder]):
                            results[record["timestamp"]]["weight"] += weight
                            # print("Weight TLD:", results[record["timestamp"]]["weight"])
                    for folder, weight in dict_folders_sld_tld.items():
                        if any(keyword == record["SLD_TLD"] for keyword in keywords_sld_tld[folder]):
                            results[record["timestamp"]]["weight"] += weight
                            # print("Weight SLD_TLD:", results[record["timestamp"]]["weight"])
                    try:
                        encoded_domain = idna.encode(record["domain"])
                        if record["domain"] != encoded_domain.decode() or "xn--" in record["domain"]:
                            results[record["timestamp"]]["weight"] += 20
                            # print("Weight IDN:", results[record["timestamp"]]["weight"])
                    except idna.IDNAError:  
                        #print (f'{record["domain"]} is not a valid IDN domain') 
                        temp += 1

                    dot_count = record["domain"].count('.')
                    if dot_count > 2:
                        if results[record["timestamp"]]["weight"] > 0:
                            results[record["timestamp"]]["weight"] += dot_count * 3
                        # print("Weight dots:", results[record["timestamp"]]["weight"])

                    dash_count = record["domain"].count('-')
                    if dash_count > 1:
                        if not "xn--" in record["domain"]:
                            results[record["timestamp"]]["weight"] += dash_count * 3
                            # print("Weight dashes:", results[record["timestamp"]]["weight"])

                    domain_length = len(record["domain"])
                    if domain_length > 40:
                        results[record["timestamp"]]["weight"] += 10
                        # print("Weight lenght:", results[record["timestamp"]]["weight"])
    
        
print("Number of records - analyzed:", rec_tot)
# Write results to output file

num_records = 0
written_domains = set()  # Set to keep track of written domains
with open(output_file1, "w") as f:
    for record_id, result in results.items():
        if result["weight"] >= 50 and result["weight"] < 70:
            domain = result["record"]["domain"]
            if domain not in written_domains:  # Check if domain has not been written already
                f.write(json.dumps(result["record"]) + "\n")
                num_records += 1
                written_domains.add(domain)  # Add domain to set of written domains
                #print("Weight:", result["weight"])
# Print the number of records
print("Number of records - low probability:", num_records)

num_records = 0
written_domains = set()  # Set to keep track of written domains
with open(output_file2, "w") as f:
    for record_id, result in results.items():
        if result["weight"] >= 70 and result["weight"] < 80:
            domain = result["record"]["domain"]
            if domain not in written_domains:  # Check if domain has not been written already
                f.write(json.dumps(result["record"]) + "\n")
                num_records += 1
                written_domains.add(domain)  # Add domain to set of written domains
                #print("Weight:", result["weight"])
# Print the number of records
print("Number of records - medium probability:", num_records)

num_records = 0
written_domains = set()  # Set to keep track of written domains
with open(output_file3, "w") as f:
    for record_id, result in results.items():
        if result["weight"] >= 80:
            domain = result["record"]["domain"]
            if domain not in written_domains:  # Check if domain has not been written already
                f.write(json.dumps(result["record"]) + "\n")
                num_records += 1
                written_domains.add(domain)  # Add domain to set of written domains
                #print("Weight:", result["weight"])
# Print the number of records
print("Number of records - high probability:", num_records)
