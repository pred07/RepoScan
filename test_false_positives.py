import re

# Test for false positives
test_code = """
// TRUE POSITIVES (should match)
var api = {
    ajax: function() { return $.ajax(); },
    get: function() { return fetch(); },
    post: function(data) { return $.post('/api', data); }
};

var xhr = new XMLHttpRequest();

// FALSE POSITIVES (should NOT match - but friend's pattern would)
var utils = {
    getData: function() { return [1,2,3]; },  // NOT ajax
    getUser: function() { return {name: 'John'}; },  // NOT ajax
    postMessage: function() { console.log('hi'); }  // NOT ajax
};

function getItems() { }  // NOT ajax
function postComment() { }  // NOT ajax
"""

# Friend's original pattern (might have false positives)
friend_pattern = re.compile(
    r'(\bajax\s*:\s*function|'
    r'\bget\s*:\s*function|'
    r'\bpost\s*:\s*function)',
    re.IGNORECASE
)

matches = friend_pattern.findall(test_code)
print(f"Friend's pattern matches: {len(matches)}")
for m in matches:
    print(f"  - {m}")

print("\n⚠️ ISSUE: 'get: function' and 'post: function' are TOO BROAD")
print("   They match ANY object method named 'get' or 'post'")
print("   Not all 'get/post' methods are AJAX-related!")
print("\n💡 SOLUTION: Keep 'ajax: function' but be cautious with get/post")
