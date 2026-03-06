#!/usr/bin/env python3
"""fetch_metrics.py

Query Prometheus for collected metrics. By default it queries the Prometheus
query API at http://localhost:9090/api/v1/query for all metrics.

Usage:
    python fetch_metrics.py [metric_name]

Requires:
    pip install requests
"""

import sys
import time

import requests


def main():
    metric = sys.argv[1] if len(sys.argv) > 1 else "yaniv_metric"
    url = f"http://localhost:9090/api/v1/query?query={metric}"
    print(f"Querying Prometheus for {metric}...")
    # try a few times in case the exporter hasn't started yet
    for attempt in range(5):
        try:
            resp = requests.get(url, timeout=2)
            resp.raise_for_status()
            data = resp.json()
            if data["status"] == "success":
                results = data["data"]["result"]
                if results:
                    for item in results:
                        metric_name = item["metric"].get("__name__", "unknown")
                        labels = {k: v for k, v in item["metric"].items() if k != "__name__"}
                        value = item["value"][1]
                        # build labels string
                        labels_parts = [f'{k}="{v}"' for k, v in labels.items()]
                        labels_str = ",".join(labels_parts)
                        if labels_str:
                            print(f"{metric_name}{{{labels_str}}} {value}")
                        else:
                            print(f"{metric_name} {value}")
                else:
                    print(f"No data found for {metric}")
            break
        except requests.RequestException as exc:
            if attempt < 4:
                print(f"attempt {attempt+1} failed: {exc} -- retrying in 1s...")
                time.sleep(1)
            else:
                print(f"failed to fetch metrics after {attempt+1} tries: {exc}")
                sys.exit(1)


if __name__ == "__main__":
    main()
