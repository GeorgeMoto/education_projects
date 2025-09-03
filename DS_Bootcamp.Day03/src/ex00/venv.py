#!/usr/bin/env python3
import os

virtual_env = os.environ.get('VIRTUAL_ENV')
if virtual_env:
    print(f"Your current virtual env is {virtual_env}")
else:
    print("No virtual environment is active")