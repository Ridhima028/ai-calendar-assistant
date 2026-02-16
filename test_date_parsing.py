#!/usr/bin/env python3
"""
Test script to verify date parsing works correctly
"""
from datetime import datetime, timedelta
from gemini_parser import parse_event
import json

print("=" * 60)
print("Testing Date Parsing for Event Creation")
print("=" * 60)
print(f"Current date: {datetime.now().date()}")
print(f"Tomorrow: {(datetime.now() + timedelta(days=1)).date()}")
print()

test_cases = [
    "create a meeting tomorrow 9pm",
    "tomorrow at 2pm meeting with john",
    "schedule a call today at 3pm"
]

for test_input in test_cases:
    print(f"\n📝 Input: '{test_input}'")
    print("-" * 60)
    
    result = parse_event(test_input)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        if 'raw' in result:
            print(f"Raw: {result['raw']}")
    else:
        print(f"✅ Parsed successfully:")
        print(f"   Title: {result.get('title')}")
        print(f"   Start: {result.get('start')}")
        print(f"   End: {result.get('end')}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
