
// Real AJAX (Count: 4)
$.ajax('/api/valid');
fetch('/api/valid');
axios.post('/api/valid');
var req = new XMLHttpRequest();

// Fake Calls (Count: 0)
var myMap = new Map();
myMap.get('key');
myList.post(data);
loader.load();

// Inline CSS/JS for testing (Count: 2 CSS, 1 JS)
var html = '<div style="color:red"></div>';
// Note: The python script parses file content, so even inside JS strings it might catch it depending on regex.
// The user asked for "Inline_CSS_Count" which usually target HTML files, but our scanner checks *all* valid extensions.
// <style>
// body { color: blue; }
// </style>
