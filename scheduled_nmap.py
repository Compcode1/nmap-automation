import nmap
import time
from datetime import datetime

print("✅ Script has started running...")  # Debugging print statement

# Create an Nmap scanner object
nm = nmap.PortScanner()

# Define target and scan parameters
target = "192.168.1.0/24"  # Replace with your subnet if different
scan_arguments = "-sV -T4"  # Standard scan options

print(f"🔍 Target network: {target}")
print(f"🔹 Scan arguments: {scan_arguments}")

# Run Nmap scan every 15 minutes for an hour
for i in range(4):  # 4 scans (one per 15 minutes)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"nmap_scan_{timestamp}.txt"
    
    print(f"\n🔍 Running scan {i+1}/4 at {timestamp}...")

    # Run the scan
    nm.scan(hosts=target, arguments=scan_arguments)

    print("✅ Scan completed. Saving results...")

    # Save results to a file
    with open(filename, "w") as file:
        file.write(f"Nmap Scan Results - {timestamp}\n")
        file.write("=" * 40 + "\n")
        
        for host in nm.all_hosts():
            file.write(f"\n✅ Host: {host}\n")
            if nm[host].all_protocols():
                for proto in nm[host].all_protocols():
                    open_ports = nm[host][proto].keys()
                    for port in sorted(open_ports):
                        service = nm[host][proto][port]['name']
                        file.write(f"  - Port {port}: {service}\n")
            else:
                file.write("❌ No open ports found.\n")

    print(f"📄 Scan {i+1} saved to {filename}")

    if i < 3:  # Sleep for 15 minutes between scans, except after the last one
        print("⏳ Waiting 15 minutes before next scan...")
        time.sleep(900)  # Sleep for 15 minutes

print("\n✅ All scans completed.")