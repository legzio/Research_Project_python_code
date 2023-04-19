import json
import datetime
import os


def write_to_file(records, file_path):
    folder_path = "data"
    os.makedirs(folder_path, exist_ok=True)  # create the folder if it doesn't exist
    file_path = os.path.join(folder_path, file_path)  # append the folder path to the file path

    with open(file_path, "w") as file:
        for record in records:
            # Extract the relevant information from the certificate
            if len(record['data']['leaf_cert']['all_domains']) > 0:
                domain = record['data']['leaf_cert']['all_domains'][0]
                #domain = record['data']['leaf_cert']['all_domains'][0]
                issuer = record['data']['leaf_cert']['issuer']['O']
                timestamp = record['data']['cert_index']

                # Extract Top Level Domain (TLD) from domain name
                domain_parts = domain.split('.')
                tld = domain_parts[-1]

                # Extract Second Level Domain (SLD) from domain name
                sld = domain_parts[-2] if len(domain_parts) > 1 else ""

                # Create regdomain string
                if len(domain_parts) > 2 and sld in ["com", "gov", "edu", "org", "net", "mil"]:
                    regdomain = domain_parts[-3] + '.' + sld + '.' + tld
                else:
                    regdomain = sld + '.' + tld

                # Create sld+tld string
                sld_tld = sld + '.' + tld

                # Write the information to a file in JSON format
                json_data = {"timestamp": timestamp, "domain": domain, "regdomain": regdomain, "SLD_TLD": sld_tld, "SLD": sld, "TLD": tld, "issuer": issuer}
                file.write(json.dumps(json_data) + "\n")
            else:
                domain = ""



def listen_for_json_files(source_folder,num_files):
    records = []
    count = 0

    for file_path in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_path)
        with open(file_path, "r") as file:
            file_data = json.load(file)

        print(f"Loaded {len(file_data)} records from {file_path}.")  # add this line

        for record in file_data:
            records.append(record)

            if len(records) == 10000:
                now = datetime.datetime.now()
                timestamp_now = now.strftime('%Y-%m-%d_%H-%M-%S-%f')
                file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{timestamp_now}.json"
                write_to_file(records, file_name)
                count += 1
                print(f"Processed {len(records)} records from {file_path}.")
                records.clear()
                if count == num_files:
                    return

    if len(records) > 0:
        now = datetime.datetime.now()
        timestamp_now = now.strftime('%Y-%m-%d_%H-%M-%S-%f')
        file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{timestamp_now}.json"
        write_to_file(records, file_name)
        print(f"Processed {len(records)} records from {file_path}.")


listen_for_json_files("source",5000)


