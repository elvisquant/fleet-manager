#!/bin/bash
set -euo pipefail

MAX_RETRIES=10
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    if curl -f https://api.elvisquant.com/health >/dev/null 2>&1; then
        echo "✅ Application is healthy"
        exit 0
    fi
    echo "⚠️ Attempt $i/$MAX_RETRIES: Application not ready, retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
done

echo "❌ Application health check failed after $MAX_RETRIES attempts"
exit 1