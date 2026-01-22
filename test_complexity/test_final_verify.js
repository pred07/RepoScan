
// Real AJAX (Count: 4)
$.ajax('/api/valid');
fetch('/api/valid');
axios.post('/api/valid');
var req = new XMLHttpRequest();

// Fake Calls (Count: 0)
// These previously triggered false positives
var myMap = new Map();
myMap.get('key');
myList.post(data);
loader.load();
