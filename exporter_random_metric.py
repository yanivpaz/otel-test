#!/usr/bin/env python3
"""exporter_random_metric.py

Simple script that uses OpenTelemetry to record a random gauge metric and
expose it to Prometheus.

The script runs indefinitely, continuously pushing random values every 2
seconds. A Prometheus exporter is started on localhost:8000 so that a
Prometheus server can scrape it.

Usage:
    python exporter_random_metric.py

Requirements:
    pip install opentelemetry-api opentelemetry-sdk \
                opentelemetry-exporter-prometheus prometheus_client
"""

import random
import time

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import Observation
from prometheus_client import start_http_server


def main() -> None:
    # start HTTP server on port 8000 for metrics endpoint
    start_http_server(8000)
    
    print("Prometheus metrics endpoint listening on http://localhost:8000/metrics")
    
    # configure the meter provider with a Prometheus reader
    reader = PrometheusMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)

    meter = metrics.get_meter(__name__)

    # keep a variable for the latest value so we can print it
    current_value = {"v": 0.0}

    def observe_random(callback_options):
        # yield the current metric value as an Observation
        yield Observation(current_value["v"], {})

    gauge = meter.create_observable_gauge(
        "yaniv_metric",
        callbacks=[observe_random],
        description="Random value between 0 and 1 (yaniv_metric)",
    )

    # run indefinitely, update value every 2s and print it
    try:
        print("Exporter running indefinitely. Press Ctrl+C to stop.")
        while True:
            # generate and record new random number
            current_value["v"] = random.random()
            print(f"updated yaniv_metric -> {current_value['v']}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExporter stopped.")


if __name__ == "__main__":
    main()
