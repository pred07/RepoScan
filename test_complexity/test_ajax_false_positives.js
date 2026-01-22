
// Real AJAX
$.ajax('/api/data');
fetch('/api/data');
axios.get('/api/data');
var xhr = new XMLHttpRequest();

// False Positives (Likely)
var map = new Map();
map.get('key');
var data = new FormData();
data.get('field');
var params = new URLSearchParams(window.location.search);
params.get('id');
myArray.load(); // generic load method
