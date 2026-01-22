# AJAX Detection & Analysis Guide

This guide explains **how** RepoScan detects AJAX calls and **how to analyze their purpose** manually.

---

## 🔍 How Detection Works

RepoScan uses **regex pattern matching** to find all known ways JavaScript initiates network requests. The detection is **100% accurate** for standard syntax.

### 1. Modern Fetch API
**Pattern:** `fetch(...)`, `axios.get(...)`, `axios.post(...)`
- **Matches:** Standard modern web requests.
- **Example:**
  ```javascript
  fetch('/api/user/123')
  axios.post('/login', { user: 'admin' })
  ```

### 2. jQuery Methods
**Pattern:** `$.ajax(...)`, `$.get(...)`, `$.post(...)`, `$.getJSON(...)`
- **Matches:** Classic jQuery network calls.
- **Example:**
  ```javascript
  $.ajax({ url: '/save-data', type: 'POST' })
  ```

### 3. Legacy XMLHttpRequest (XHR)
**Pattern:** `new XMLHttpRequest()`, `.open('GET', ...)`
- **Matches:** Older raw JavaScript requests (often hidden in libraries).
- **Example:**
  ```javascript
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "data.json");
  xhr.send();
  ```

### 4. Object Literal Definitions (Enhanced)
**Pattern:** `ajax: function(...)`
- **Matches:** AJAX methods defined inside objects/plugins/API wrappers.
- **Example:**
  ```javascript
  var UserService = {
      // Detected! This is clearly an AJAX wrapper
      ajax: function(url, callback) { ... } 
  };
  ```

---

## 🧠 How to Determine the *Purpose* of an AJAX Call

Once RepoScan flags a file as having "Active AJAX," follow these steps to understand **what** it does.

### Step 1: Locate the URL (Endpoint)
Look for the first argument or the `url` property.
- **`/api/auth/login`** → **Purpose:** Authentication/Login
- **`/api/products/list`** → **Purpose:** Data Retrieval/Display
- **`/api/user/update`** → **Purpose:** Data Modification (Write)

### Step 2: Check the HTTP Method
- **`GET`** → Reading data (Safe, usually)
- **`POST`** → Creating data or performing complex actions (Sensitive)
- **`PUT` / `PATCH`** → Updating existing data
- **`DELETE`** → Removing data

### Step 3: Analyze the Payload (Data Sent)
Look for `data:`, `body:`, or the second argument.
- sending `{ username, password }` → **Login / Signup**
- sending `{ id: 123 }` → **Fetching specific item**
- sending credit card info → **Payment processing** (Critical!)

### Step 4: Examine the Callback/Promise (Response Handling)
Look for `.then(...)`, `success: function(...)`, or lines after `await`.
- `document.getElementById('list').innerHTML = ...` → **UI Update / Rendering**
- `window.location.href = ...` → **Redirect (Navigation)**
- `localStorage.setItem(...)` → **Session Management**

---

## 📝 Analysis Examples

### Example 1: Data Fetching (Low Risk)
```javascript
// Scan detects '$.get'
$.get('/api/news', function(data) {
    // Purpose: UI Update (Reading news)
    renderNewsFeed(data); 
});
```

### Example 2: Sensitive Action (High Risk)
```javascript
// Scan detects 'fetch'
fetch('/api/admin/delete-user', {
    method: 'POST', // Critical Method
    body: JSON.stringify({ userId: 5 }) // Payload
}).then(() => {
    alert('User Deleted'); // Consequence
});
```

### Example 3: Wrapped AJAX (Subtle)
```javascript
// Scan detects 'ajax: function'
var API = {
    ajax: function(endpoint) {
        // Purpose: This is a custom wrapper used everywhere.
        // You generally don't audit this definition, but audit 
        // WHERE 'API.ajax' is CALLED in the app.
        return $.ajax({ url: endpoint }); 
    }
};
```
