#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

exec celery -A core worker -l INFO