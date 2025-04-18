#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# 檢查並創建 logs 目錄
LOG_DIR="/app/logs"
if [ ! -d "$LOG_DIR" ]; then
  mkdir -p "$LOG_DIR"
  chmod 777 "$LOG_DIR"
  echo "Created logs directory at $LOG_DIR"
else
  echo "Logs directory already exists at $LOG_DIR"
fi


postgres_ready() {
python << END
import sys

import psycopg

try:
    psycopg.connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'


rabbitmq_ready() {
    echo "Waiting for rabbitmq..."

    while ! nc -z rabbitmq 5672; do
      sleep 1
    done

    echo "rabbitmq started"
}

rabbitmq_ready

exec "$@"