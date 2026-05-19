"""
monitor.py
Network Host Monitor - Phase 1

Pings a list of hosts, measures latency, and logs results to a CSV file.
"""

import csv

HOSTS = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1",      # Cloudflare DNS
    "github.com",
]

OUTPUT_FILE = "results.csv"
LATENCY_THRESHOLD_MS = 100  # Flag as "slow" if above this value. Will try to lower down this threshold to test edge cases

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

if __name__ == "__main__":
    main()