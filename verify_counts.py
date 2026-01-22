
import os
import re
import pandas as pd
import glob

# Paths
REPO_PATH = r"c:\Users\groot\Music\susu\WebGoat.NET"
OUTPUT_DIR = r"c:\Users\groot\Music\susu\output"

# Regex Patterns (Simplified for verification)
patterns = {
    'inline_css': re.compile(r'style\s*=\s*["\'][^"\']*["\']', re.IGNORECASE),
    'internal_style_blocks': re.compile(r'<style\b[^>]*>[\s\S]*?</style>', re.IGNORECASE),
    'inline_js': re.compile(r'(\bon\w+\s*=\s*["\'][^"\']*["\']|href=["\']\s*javascript:)', re.IGNORECASE),
    'internal_script_blocks': re.compile(r'<script\b(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>', re.IGNORECASE),
    'ajax_calls': re.compile(r'(\bfetch\s*\(|new\s+XMLHttpRequest\s*\(|\$\.ajax\s*\(|\$\.get\s*\(|\$\.post\s*\()', re.IGNORECASE)
}

# Supported Extensions
extensions = {'.html', '.htm', '.aspx', '.ascx', '.cshtml', '.master', '.php', '.jsp', '.js', '.ts', '.vue', '.jsx', '.tsx'}

def count_patterns(repo_path):
    print(f"Scanning {repo_path}...")
    totals = {key: 0 for key in patterns}
    file_count = 0
    
    for root, _, files in os.walk(repo_path):
        if any(ex in root for ex in ['node_modules', '.git', 'bin', 'obj']):
            continue
            
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for key, pattern in patterns.items():
                            totals[key] += len(pattern.findall(content))
                    file_count += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    print(f"Scanned {file_count} files manually.")
    return totals

def get_latest_report(output_dir):
    files = glob.glob(os.path.join(output_dir, "Application_Depth_Tracker_*.xlsx"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def compare_results(manual_counts, report_path):
    print(f"\nReading report: {report_path}")
    df = pd.read_excel(report_path, sheet_name='Complexity_Metrics')
    
    report_totals = {
        'inline_css': df['Inline_CSS_Count'].sum(),
        'internal_style_blocks': df['Internal_Style_Blocks_Count'].sum(),
        'inline_js': df['Inline_JS_Count'].sum(),
        'internal_script_blocks': df['Internal_Script_Blocks_Count'].sum(),
        'ajax_calls': df['AJAX_Calls_Count'].sum()
    }
    
    print("\n--- COMPARISON RESULTS ---")
    print(f"{'Metric':<25} | {'Manual':<10} | {'Report':<10} | {'Diff':<10}")
    print("-" * 65)
    
    for key in manual_counts:
        m = manual_counts[key]
        r = report_totals.get(key, 0)
        diff = m - r
        print(f"{key:<25} | {m:<10} | {r:<10} | {diff:<10}")

if __name__ == "__main__":
    manual_counts = count_patterns(REPO_PATH)
    latest_report = get_latest_report(OUTPUT_DIR)
    
    if latest_report:
        compare_results(manual_counts, latest_report)
    else:
        print("No report found to compare.")
