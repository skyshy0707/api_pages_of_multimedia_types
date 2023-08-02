#!/bin/bash
cd /code/src
celery -A settings worker --loglevel=debug --concurrency 1 -E --purge