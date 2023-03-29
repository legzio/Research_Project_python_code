import json
import certstream
import time
import sys
import datetime


def handle_message(message, context):
    # Check if the message contains a certificate
    if message['message_type'] == "certificate_update":
        # Extract the relevant information from the certificate
        domain = message['data']['leaf_cert']['all_domains'][0]
        issuer = message['data']['leaf_cert']['issuer']['O']
        timestamp = message['data']['cert_index']

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
        with open(filename_stream, "a") as file:
            log_entry = {"timestamp": timestamp, "domain": domain, "regdomain": regdomain, "SLD_TLD": sld_tld, "SLD": sld, "TLD": tld, "issuer": issuer}
            file.write(json.dumps(log_entry) + ",")

        # Increment the counter
        counter += 1
        if counter > 10:
            print("Finished collecting records.")
            with open(filename_stream, "a") as file:
                file.write(chr(ord("]")))
            sys.exit()
        

# Start the certstream client, with retry logic if an error occurs


    counter = 0
    # Get the current date and time
    now = datetime.datetime.now()
    timestamp_now = now.strftime('%Y-%m-%d_%H-%M-%S')
    filename_stream = f"my_file_{timestamp_now}.txt"
    with open(filename_stream, "w") as file:
        file.write(chr(ord("[")))

    certstream.listen_for_events(handle_message, url='wss://certstream.calidog.io/')

#print("Finished collecting records.")
#with open("certificate_transparency_logs.json", "a") as file:
#    file.write(chr(ord("]")))

