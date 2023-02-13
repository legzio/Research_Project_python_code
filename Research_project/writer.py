import json
import certstream

def handle_message(message, context):
    # Check if the message contains a certificate
    if message['message_type'] == "certificate_update":
        # Extract the relevant information from the certificate
        domain = message['data']['leaf_cert']['all_domains'][0]
        serial_number = message['data']['leaf_cert']['serial_number']
        timestamp = message['data']['cert_index']

       # Write the information to a file in JSON format
        with open("certificate_transparency_logs.json", "a") as file:
            log_entry = {"timestamp": timestamp, "domain": domain, "serial_number": serial_number}
            file.write(json.dumps(log_entry) + "\n")

# Start the certstream client
certstream.listen_for_events(handle_message, url='wss://certstream.calidog.io/')

