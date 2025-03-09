import os
from datetime import datetime

# File paths for scan results
scan_file_1 = "nmap_scan_2025-03-08_14-42-32.txt"
scan_file_2 = "nmap_scan_2025-03-08_15-39-38.txt"
log_file = "nmap_scan_changes.log"

# Function to parse Nmap scan files
def parse_scan_results(file_path):
    hosts = {}
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return hosts

    with open(file_path, "r") as file:
        lines = file.readlines()
        current_host = None

        for line in lines:
            line = line.strip()
            if line.startswith("✅ Host:"):
                current_host = line.split()[2]  # Extract IP address
                hosts[current_host] = []
            elif current_host and "↳ Port Found:" in line:
                port_info = line.split(": ")[1]
                port, service = port_info.split(" (")
                service = service.strip(")")
                hosts[current_host].append((int(port), service))

    return hosts

# Load scan data
scan_data_1 = parse_scan_results(scan_file_1)
scan_data_2 = parse_scan_results(scan_file_2)

# Compare results
differences = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

differences.append(f"\n🔍 Nmap Scan Comparison - {timestamp}\n{'='*50}")

# Check for new hosts
new_hosts = set(scan_data_2.keys()) - set(scan_data_1.keys())
for host in new_hosts:
    differences.append(f"🆕 New Host Detected: {host}")

# Check for removed hosts
removed_hosts = set(scan_data_1.keys()) - set(scan_data_2.keys())
for host in removed_hosts:
    differences.append(f"❌ Host Removed: {host}")

# Check for port changes in existing hosts
for host in scan_data_1.keys() & scan_data_2.keys():
    old_ports = set(scan_data_1[host])
    new_ports = set(scan_data_2[host])

    added_ports = new_ports - old_ports
    removed_ports = old_ports - new_ports

    if added_ports:
        differences.append(f"🔺 {host} - New Open Ports: {', '.join(f'{p[0]} ({p[1]})' for p in added_ports)}")
    if removed_ports:
        differences.append(f"🔻 {host} - Closed Ports: {', '.join(f'{p[0]} ({p[1]})' for p in removed_ports)}")

# Write differences to log file
with open(log_file, "a") as log:
    for diff in differences:
        log.write(diff + "\n")

# Print summary
if differences:
    print("\n".join(differences))
    print(f"\n✅ Changes logged in {log_file}")
else:
    print("✅ No changes detected.")