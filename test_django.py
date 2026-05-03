#!/usr/bin/env python
import os
import sys

print(f"Python: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

try:
    import django
    print(f"Django version: {django.get_version()}")
    print("✓ Django imported successfully")
except ImportError as e:
    print(f"✗ Django import failed: {e}")

try:
    from django.conf import settings
    print("✓ Django settings imported")
except ImportError as e:
    print(f"✗ Django settings import failed: {e}")

print("\nPython path:")
for path in sys.path:
    if 'site-packages' in path:
        print(f"  {path}")
