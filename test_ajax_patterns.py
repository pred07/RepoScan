import re

# Read test file
with open('test_complexity/test_ajax_object_literal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Current pattern (from scanner.py)
current_pattern = re.compile(
    r'(\bfetch\s*\(|'
    r'new\s+XMLHttpRequest\s*\(|'
    r'(?:\$|jQuery|axios|superagent|http)\s*\.\s*(?:ajax|get|post|getJSON|getScript|load|request)\s*\(|'
    r'\.open\s*\(\s*["\'](?:GET|POST|PUT|DELETE|PATCH)["\']|'
    r'\bonreadystatechange\s*=|'
    r'\.send\s*\(|'
    r'\baxios(?:\.\w+)?\s*\(|'
    r'new\s+WebSocket\s*\(|'
    r'new\s+EventSource\s*\()',
    re.IGNORECASE
)

# Friend's suggested patterns
friend_patterns = re.compile(
    r'(\bajax\s*:\s*function|'
    r'\bget\s*:\s*function|'
    r'\bpost\s*:\s*function|'
    r'\bXMLHttpRequest\b)',
    re.IGNORECASE
)

current_matches = current_pattern.findall(content)
friend_matches = friend_patterns.findall(content)

print("=" * 60)
print("AJAX PATTERN DETECTION TEST")
print("=" * 60)
print(f"\nCurrent Pattern Matches: {len(current_matches)}")
for i, m in enumerate(current_matches, 1):
    print(f"  {i}. {m}")

print(f"\nFriend's Pattern Matches: {len(friend_matches)}")
for i, m in enumerate(friend_matches, 1):
    print(f"  {i}. {m}")

# Combined pattern (union of both)
combined_pattern = re.compile(
    r'(\bfetch\s*\(|'
    r'new\s+XMLHttpRequest\s*\(|'
    r'(?:\$|jQuery|axios|superagent|http)\s*\.\s*(?:ajax|get|post|getJSON|getScript|load|request)\s*\(|'
    r'\.open\s*\(\s*["\'](?:GET|POST|PUT|DELETE|PATCH)["\']|'
    r'\bonreadystatechange\s*=|'
    r'\.send\s*\(|'
    r'\baxios(?:\.\w+)?\s*\(|'
    r'new\s+WebSocket\s*\(|'
    r'new\s+EventSource\s*\(|'
    # Friend's additions
    r'\bajax\s*:\s*function|'
    r'\bget\s*:\s*function|'
    r'\bpost\s*:\s*function)',
    re.IGNORECASE
)

combined_matches = combined_pattern.findall(content)
print(f"\nCombined Pattern Matches: {len(combined_matches)}")
for i, m in enumerate(combined_matches, 1):
    print(f"  {i}. {m}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
if len(combined_matches) > len(current_matches):
    print(f"✅ Friend's patterns catch {len(combined_matches) - len(current_matches)} additional AJAX cases!")
    print("   These are valid object literal AJAX method definitions.")
    print("   RECOMMENDATION: Add friend's patterns to improve detection.")
else:
    print("✅ Current patterns are comprehensive!")
