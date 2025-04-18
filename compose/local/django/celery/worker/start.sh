#!/bin/bash

set -o errexit
set -o nounset

watchfiles \
  --filter python \
  'celery -A core worker --loglevel=info -Q default,high_priority'