#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


exec celery -A core beat -l INFO