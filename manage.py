#!/usr/bin/env python
import os
import sys
import settings

if __name__ == "__main__":
    os.environ.setdefault('LANG','en_US')
    from django.core.management import execute_manager

    execute_manager(settings)
