
import sys
import os
sys.path.append(os.path.abspath("repo_depth_analyser/src"))
from scanner import Scanner

def check_metrics():
    target_file = os.path.abspath("test_complexity/test_cross_check.js")
    scanner = Scanner("test_complexity")
    metrics = scanner.count_lines_and_analyze(target_file)
    
    print("\n--- Python Scanner Results ---")
    print(f"File: {target_file}")
    print(f"Inline_CSS: {metrics['inline_css']}")
    print(f"Internal_Style: {metrics['internal_style_blocks']}")
    print(f"Inline_JS: {metrics['inline_js']}")
    print(f"Internal_Script: {metrics['internal_script_blocks']}")
    print(f"Ajax_Calls: {metrics['ajax_calls']}")

if __name__ == "__main__":
    check_metrics()
