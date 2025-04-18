#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
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
  python <<END
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
  echo >&2 'Waiting for PostgreSQL to become available...'
  sleep 1
done
echo >&2 'PostgreSQL is available'

exec "$@"
