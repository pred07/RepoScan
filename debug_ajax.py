import os
import re

REPO_PATH = r"c:\Users\groot\Music\susu\WebGoat.NET"

# The Scanner's Broad AJAX Regex
ajax_regex = re.compile(
    r'(\bfetch\s*\(|'
    r'new\s+XMLHttpRequest\s*\(|'
    r'[A-Za-z_$]\w*\s*\.\s*(?:ajax|get|post|getJSON|getScript|load|request)\s*\(|'
    r'\.open\s*\(\s*["\'](?:GET|POST|PUT|DELETE|PATCH)["\']|'
    r'\bonreadystatechange\s*=|'
    r'\.send\s*\(|'
    r'\baxios(?:\.\w+)?\s*\(|'
    r'new\s+WebSocket\s*\(|'
    r'new\s+EventSource\s*\()',
    re.IGNORECASE
)

extensions = {'.html', '.htm', '.aspx', '.ascx', '.cshtml', '.master', '.php', '.jsp', '.js', '.ts', '.vue', '.jsx', '.tsx'}

def audit_ajax_matches(repo_path):
    print(f"Auditing AJAX matches in {repo_path}...")
    match_count = 0
    
    for root, _, files in os.walk(repo_path):
        if any(ex in root for ex in ['node_modules', '.git', 'bin', 'obj']):
            continue
            
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            matches = ajax_regex.findall(line)
                            for match in matches:
                                match_count += 1
                                print(f"[Match {match_count}] File: {file} | Line {i+1}: {match.strip()} -> Full Line: {line.strip()[:100]}")
                                if match_count >= 50:
                                    print("Stopping after 50 matches.")
                                    return
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    audit_ajax_matches(REPO_PATH)
