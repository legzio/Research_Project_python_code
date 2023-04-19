import json
import certstream
import datetime
import sys
import time
import os


def write_to_file(records, file_path):
    folder_path = "data"
    os.makedirs(folder_path, exist_ok=True)  # create the folder if it doesn't exist
    file_path = os.path.join(folder_path, file_path)  # append the folder path to the file path

    with open(file_path, "w") as file:
        for record in records:
            # Extract the relevant information from the certificate
            domain = record['data']['leaf_cert']['all_domains'][0]
            issuer = record['data']['leaf_cert']['issuer']['O']
            timestamp = record['data']['cert_index']

            # Extract Top Level Domain (TLD) from domain name
            domain_parts = domain.split('.')
            tld = domain_parts[-1]

            # Extract Second Level Domain (SLD) from domain name
            sld = domain_parts[-2]

            # Create regdomain string
            if sld in ["com", "gov", "edu", "org", "net", "mil"]:
                regdomain = domain_parts[-3] + '.' + sld + '.' + tld
            else:
                regdomain = sld + '.' + tld

            # Create sld+tld string
            sld_tld = sld + '.' + tld

            # Write the information to a file in JSON format
            json_data = {"timestamp": timestamp, "domain": domain, "regdomain": regdomain, "SLD_TLD": sld_tld, "SLD": sld, "TLD": tld, "issuer": issuer}
            file.write(json.dumps(json_data) + "\n")


def listen_for_certstream(num_files):
    count = 0
    records = []
    url = "wss://certstream.calidog.io/"
    #url = "ws://192.168.51.63:4000/"
    
    def message_callback(message, context):
        nonlocal count
        if message['message_type'] == "certificate_update":
            records.append(message)
            if len(records) == 10000:
                now = datetime.datetime.now()
                timestamp_now = now.strftime('%Y-%m-%d_%H-%M-%S')
                file_path = f"certstream_{timestamp_now}.json"
                write_to_file(records, file_path)
                # time.sleep(10)
                count += 1
                print(count, ", ")
                records.clear()
                if count == num_files:
                    sys.exit()

    # Call listen_for_events with the context object
    certstream.listen_for_events(message_callback, url)

listen_for_certstream(1000)


