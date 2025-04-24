#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys

LOG_FILE = "site.log"
logging.basicConfig(
    level=logging.INFO,  # Adjust to DEBUG for more verbosity
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hse_task.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
