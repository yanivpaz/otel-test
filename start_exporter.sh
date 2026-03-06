#!/bin/bash
# start_exporter.sh - Start the OpenTelemetry metrics exporter in background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORTER="$SCRIPT_DIR/exporter_random_metric.py"

if [ ! -f "$EXPORTER" ]; then
    echo "✗ Error: $EXPORTER not found"
    exit 1
fi

# Check if already running
if pgrep -f "exporter_random_metric.py" > /dev/null; then
    echo "✓ Exporter is already running"
    exit 0
fi

# Start exporter in background
python3 "$EXPORTER" > /tmp/exporter.log 2>&1 &
PID=$!

sleep 1

# Verify it started
if kill -0 $PID 2>/dev/null; then
    echo "✓ Exporter started successfully (PID: $PID)"
    echo "  Metrics endpoint: http://localhost:8000/metrics"
else
    echo "✗ Failed to start exporter. Check /tmp/exporter.log"
    exit 1
fi
