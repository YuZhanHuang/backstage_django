#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

MAX_RETRIES=30
RETRY_DELAY=5
COUNT=0

COUNT=0
MAX_RETRIES=30  # 最大重試次數
RETRY_DELAY=5   # 每次重試間隔 (秒)

while ! curl -s -o /dev/null -w "%{http_code}" http://nginx/api/v1/health/ | grep -q "200"; do
  echo "Waiting for Nginx to route requests correctly... ($COUNT/$MAX_RETRIES)"
  sleep $RETRY_DELAY
  COUNT=$((COUNT+1))
  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "Nginx did not route requests successfully in time. Exiting."
    exit 1
  fi
done

echo "Web is successfully routing requests!"

exec "$@"
