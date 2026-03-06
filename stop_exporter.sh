#!/bin/bash
# stop_exporter.sh - Stop the OpenTelemetry metrics exporter

if pkill -f "exporter_random_metric.py"; then
    echo "✓ Exporter stopped successfully"
else
    echo "✗ Exporter is not running"
    exit 1
fi
