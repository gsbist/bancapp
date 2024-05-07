#!/bin/bash

source venv/bin/activate
celery -A home.tasks worker --loglevel=INFO
