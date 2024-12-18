#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import django
import sys
from django.core.management import execute_from_command_line


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineacademy.settings")
    django.setup()
    execute_from_command_line()
