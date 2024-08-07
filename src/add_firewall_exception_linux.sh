#!/bin/bash
# Define the path to the application or service to add to the firewall
PROGRAM_PATH="/path/to/your/application"

# Add a new rule to allow connections
sudo ufw allow from any to any port 12345 proto tcp
