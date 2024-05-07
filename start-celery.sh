#!/bin/bash

source venv/bin/activate
celery -A home.views worker --loglevel=INFO
