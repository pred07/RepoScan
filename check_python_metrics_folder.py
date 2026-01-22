
import sys
import os
sys.path.append(os.path.abspath("repo_depth_analyser/src"))
from scanner import Scanner

def check_metrics_folder():
    target_dir = os.path.abspath("test_complexity")
    scanner = Scanner(target_dir)
    # scanner.scan() returns (inventory, stats)
    inventory, _ = scanner.scan()
    
    totals = {
        'Inline_CSS': 0, 'Internal_Style': 0,
        'Inline_JS': 0, 'Internal_Script': 0,
        'Ajax_Calls': 0
    }
    
    file_count = 0
    for item in inventory:
        # Filter same as PS: no .git/bin/obj (already handled by scanner)
        if item['Extension'] in ['.html', '.cshtml', '.js', '.aspx', '.php']:
            file_count += 1
            totals['Inline_CSS'] += item['Inline_CSS_Count']
            totals['Internal_Style'] += item['Internal_Style_Blocks_Count']
            totals['Inline_JS'] += item['Inline_JS_Count']
            totals['Internal_Script'] += item['Internal_Script_Blocks_Count']
            totals['Ajax_Calls'] += item['AJAX_Calls_Count']
            
    print("\n--- Python Scanner Results (Folder) ---")
    print(f"Total Files Scanned: {file_count}")
    for k, v in sorted(totals.items()):
        print(f"{k}: {v}")

if __name__ == "__main__":
    check_metrics_folder()
