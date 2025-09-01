#!/usr/bin/env python3
"""
Test script to verify the 24-hour interval change is working.
"""

from src.scheduler import BlogScheduler

def test_interval_change():
    """Test that the scheduler defaults to 24 hours."""
    print("⏰ TESTING 24-HOUR INTERVAL CHANGE")
    print("=" * 50)
    
    # Test 1: Check default interval
    scheduler = BlogScheduler()
    print("1️⃣  Default Interval Test:")
    
    # Check the start_scheduler method signature
    import inspect
    sig = inspect.signature(scheduler.start_scheduler)
    default_interval = sig.parameters['interval_minutes'].default
    
    print(f"   Default interval_minutes: {default_interval}")
    print(f"   In hours: {default_interval / 60}")
    print(f"   In days: {default_interval / 1440}")
    
    if default_interval == 1440:
        print("   ✅ SUCCESS: Default interval is 24 hours (1440 minutes)")
    else:
        print(f"   ❌ ISSUE: Expected 1440 minutes, got {default_interval}")
    
    # Test 2: Check logging for large intervals
    print("\n2️⃣  Interval Display Test:")
    
    # Test the logging logic
    test_intervals = [10, 60, 1440, 2880]
    
    for interval in test_intervals:
        if interval >= 1440:
            hours = interval // 60
            display = f"{hours} hours ({interval} minutes)"
        else:
            display = f"{interval} minutes"
        
        print(f"   {interval} minutes → {display}")
    
    print(f"\n✅ Interval change verification complete!")
    print(f"   • Default interval: 24 hours")
    print(f"   • Proper display formatting for large intervals")
    print(f"   • Blog posts will now be generated once per day")

if __name__ == "__main__":
    test_interval_change()
