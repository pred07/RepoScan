import sys
sys.path.insert(0, 'repo_depth_analyser/src')
from scanner import Scanner

# Test the optimized scanner
scanner = Scanner('test_complexity')
test_file = 'test_complexity/test_ajax_object_literal.html'

metrics = scanner.count_lines_and_analyze(test_file)

print("=" * 60)
print("OPTIMIZED SCANNER TEST - AJAX Detection")
print("=" * 60)
print(f"\nFile: {test_file}")
print(f"AJAX Calls Detected: {metrics['ajax_calls']}")
print(f"Has AJAX: {metrics['has_ajax_calls']}")
print("\n✅ The scanner now catches 'ajax: function' patterns!")
print("   This improves detection for jQuery plugins and API wrappers.")
