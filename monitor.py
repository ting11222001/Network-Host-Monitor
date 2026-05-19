"""
monitor.py
Network Host Monitor - Phase 1

Pings a list of hosts, measures latency, and logs results to a CSV file.
"""

import csv
from datetime import datetime

HOSTS = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1",      # Cloudflare DNS
    "github.com",
]

OUTPUT_FILE = "results.csv"
LATENCY_THRESHOLD_MS = 100  # Flag as "slow" if above this value. Will try to lower down this threshold to test edge cases

def write_result(writer, host, latency, status, timestamp):
    """
    Writes one row to the CSV file.
    """
    latency_display = f"{latency}" if latency is not None else "N/A"
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
            latency = None
            status = "unknown"
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