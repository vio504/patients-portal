#!/bin/bash

request_payload_path="payloads/update_patient.json"

payload=$(cat "$request_payload_path")
patient_id="30ed4a02-40e0-40a5-a939-e7f38a81acab"

curl -X PUT -H "Content-Type: application/json" -d "$payload" "127.0.0.1:5000/patient/$patient_id"