#!/bin/bash
# check_services.sh - verify if Grafana and Prometheus are running

SERVICES=("grafana-server" "prometheus")

for svc in "${SERVICES[@]}"; do
    if systemctl >/dev/null 2>&1; then
        # try systemctl first
        status=$(systemctl is-active "$svc" 2>/dev/null)
        if [ "$status" = "active" ]; then
            echo "$svc is running (systemctl)"
            continue
        fi
    fi
    # fallback to ps/pgrep
    if pgrep -f "$svc" >/dev/null 2>&1; then
        echo "$svc process found"
    else
        echo "$svc not running"
    fi
done
