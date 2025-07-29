#!/usr/bin/env python3
"""Simple test for video_to_text functionality"""

import os
from video_to_text import video_to_text_converter

# Test with a fake video path
test_path = "test_nonexistent.mp4"
print("Testing video_to_text_converter...")

try:
    result = video_to_text_converter(test_path, language='th-TH')
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()