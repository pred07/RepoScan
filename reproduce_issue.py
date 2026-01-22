
import sys
import os

# Add the src directory to the path so we can import the scanner
sys.path.append(os.path.abspath("repo_depth_analyser/src"))

from scanner import Scanner

def test_scanner():
    target_file = os.path.abspath("test_complexity/test_ajax_false_positives.js")
    
    scanner = Scanner("test_complexity")
    metrics = scanner.count_lines_and_analyze(target_file)
    
    print(f"File: {target_file}")
    print(f"AJAX Calls Count: {metrics['ajax_calls']}")
    
    # We expect 4 real calls ($.ajax, fetch, axios.get, new XMLHttpRequest)
    # If the count is > 4, we have false positives.
    if metrics['ajax_calls'] > 4:
        print("FAIL: False positives detected!")
    else:
        print("PASS: Accurate count.")

if __name__ == "__main__":
    test_scanner()
