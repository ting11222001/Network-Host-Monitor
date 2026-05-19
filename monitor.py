"""
monitor.py
Network Host Monitor - Phase 1

Pings a list of hosts, measures latency, and logs results to a CSV file.
"""
import subprocess
import csv
from datetime import datetime
import platform

HOSTS = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1",      # Cloudflare DNS
    "github.com",
]

OUTPUT_FILE = "results.csv"
LATENCY_THRESHOLD_MS = 100  # Flag as "slow" if above this value. Will try to lower down this threshold to test edge cases

def ping_host(host):
    """
    Pings a single host once.
    Returns latency in ms as a float, or None if the host is unreachable.
    Currently implemented for Windows. For other OSes, it will print a message and return None.
    """
    system = platform.system()

    # Windows: ping -n 1 -w 2000 <host>
    if system == "Windows":
        command = ["ping", "-n", "1", "-w", "2000", host]
    else:
        command = None

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,     # With PIPE: output is silent in the terminal but accessible via result.stdout.
            text=True
        )
        output = result.stdout

        # Parse latency from ping output
        if system == "Windows":
            # Windows output example: "Average = 14ms"
            for line in output.splitlines():
                if "Average" in line:
                    parts = line.split("=")
                    latency_str = parts[-1].strip().replace("ms", "")
                    return float(latency_str)
        else:
            # Linux/macOS output
            print("Unsupported OS for pinging. Please run this script on Windows.")

        return None
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None

def get_status(latency):
    """
    Returns a status string based on latency.
    """
    if latency is None:
        return "DOWN"
    if latency > LATENCY_THRESHOLD_MS:
        return "SLOW"
    return "UP"

def write_result(writer, host, latency, status, timestamp):
    """
    Writes one row to the CSV file.
    """
    latency_display = f"{latency:.2f}" if latency is not None else "N/A"
    writer.writerow([timestamp, host, latency_display, status])

def run_check():
    """
    Polls all hosts once and appends results to the CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Checking {len(HOSTS)} hosts...")
    
    # Open CSV in append mode so results build up over time
    with open(OUTPUT_FILE, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)

        for host in HOSTS:
            latency = ping_host(host)
            status = get_status(latency)
            write_result(writer, host, latency, status, timestamp)

def main():
    # Write CSV header if file does not exist yet
    # "x" means: create the file, but fail if it already exists.
    try:
        with open(OUTPUT_FILE, "x", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["timestamp", "host", "latency_ms", "status"])
    except FileExistsError:
        pass  # File already exists, skip header

    print("Network Host Monitor started.")
    print(f"Results will be saved to: {OUTPUT_FILE}")
    print(f"Latency threshold: {LATENCY_THRESHOLD_MS} ms")

    run_check()
    print("\nDone. Open results.csv to see the output.")

if __name__ == "__main__":
    main()