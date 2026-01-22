
import sys
import os
import pandas as pd
import shutil

# Setup paths
sys.path.append(os.path.abspath("repo_depth_analyser/src"))
from scanner import Scanner
from reporter import Reporter

# Config
TEST_DIR = os.path.abspath("test_complexity")
OUTPUT_DIR = os.path.abspath("output_final_verify")

# Clean previous output
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

def verify_end_to_end():
    print("1. Running Scanner...")
    scanner = Scanner(TEST_DIR)
    inventory, dir_stats = scanner.scan()
    
    print(f"   Found {len(inventory)} files.")

    print("2. Generating Report...")
    reporter = Reporter(OUTPUT_DIR)
    report_path = reporter.generate_report(inventory, dir_stats)
    
    print(f"   Report generated: {report_path}")

    print("3. Verifying Excel Content...")
    df = pd.read_excel(report_path, sheet_name='Complexity_Metrics')
    
    # Filter for our specific test file
    row = df[df['Filename'] == 'test_final_verify.js'].iloc[0]
    
    count = row['AJAX_Calls_Count']
    has_ajax = row['Has_Ajax_Calls']
    
    print(f"\n--- VERIFICATION RESULTS ---")
    print(f"File: test_final_verify.js")
    print(f"AJAX Calls Expected: 4 | Found: {count}")
    print(f"Has_Ajax_Calls Expected: Yes | Found: {has_ajax}")
    
    if count == 4 and has_ajax == "Yes":
        print("SUCCESS: Logic matches requirements.")
    else:
        print("FAILURE: deviations detected.")

if __name__ == "__main__":
    verify_end_to_end()
