# Demo for otel  

This repository contains a minimal demonstration of using OpenTelemetry
in Python to generate metrics for Prometheus scraping, along with a
small utility script for checking Grafana/Prometheus services.

## OpenTelemetry Prometheus Demo

The script `exporter_random_metric.py` generates a random gauge metric
(`yaniv_metric`) every 2 seconds, prints each value to the console, and
exposes it via a Prometheus-compatible HTTP endpoint.

### Dependencies

Install the needed Python packages before running the demo:

```bash
pip install opentelemetry-api opentelemetry-sdk \
            opentelemetry-exporter-prometheus prometheus_client
```

### Usage

1. Run the metric exporter:

   ```bash
   python exporter_random_metric.py
   ```

   The script announces the metrics endpoint at `http://localhost:8000/metrics`
   and runs indefinitely, continuously generating random values.

2. Prometheus is configured (in `/opt/prometheus/prometheus.yml`) to scrape
   this endpoint every 2 seconds, automatically collecting the metrics.

### Querying Metrics

**Quick query** (latest value):
```bash
python3 fetch_metrics.py yaniv_metric
```

**Historical values** (last hour with 2s interval):
```bash
curl -s "http://localhost:9090/api/v1/query_range?query=yaniv_metric&start=$(date -d '1 hour ago' +%s)&end=$(date +%s)&step=2s" | python3 -m json.tool
```

**View in Prometheus UI**:
Go to http://localhost:9090, type `yaniv_metric` in the expression field,
and select the "Graph" tab to visualize values over time.

### Helper Scripts

- `check_services.sh` — simple shell script that verifies Grafana and
  Prometheus are running either via `systemctl` or by looking for their
  processes.
- `fetch_metrics.py` — Python utility to pull whatever text is exposed
  at a Prometheus metrics endpoint. It defaults to
  `http://localhost:9090/metrics` (Prometheus server port) but you may
  specify a different URL on the command line. Requires the `requests`
  package.
