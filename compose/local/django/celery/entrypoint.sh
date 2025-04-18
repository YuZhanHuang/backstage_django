#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

MAX_RETRIES=30
RETRY_DELAY=5
COUNT=0

while ! (echo "quit" | telnet web 8000 2>/dev/null | grep -q "Connected"); do
  echo "Waiting for web to be ready... ($COUNT/$MAX_RETRIES)"
  sleep $RETRY_DELAY
  COUNT=$((COUNT+1))
  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "Web service did not become ready in time. Exiting."
    exit 1
  fi
done

echo "Web is ready. Proceeding with Celery startup."

exec "$@"
