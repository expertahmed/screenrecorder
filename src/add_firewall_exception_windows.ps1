# Define the path to the application or service to add to the firewall
$programPath = "C:\path\to\your\application.exe"
$ruleName = "My Application Firewall Rule"

# Add a new inbound rule to allow connections
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Program $programPath -Action Allow -Profile Any
