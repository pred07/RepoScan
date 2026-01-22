# AJAX Capabilities & Use Cases: "What Can It Do?"

AJAX is not just for "getting data." It is a generic transport tunnel that can be used to load **anything** the server sends.

Functionally, AJAX is capable of **5 Distinct Operations** in a web application.

---

## 1. Data Exchange (The Standard)
**Capability:** Sending/Receiving raw data (JSON/XML) to update the application model without UI refresh.
*   **Reading:** Get a list of products, read user profile, load comments.
*   **Writing:** Submit a form, upvote a post, save settings.

```javascript
// Example: Reading Data
fetch('/api/user/profile').then(data => updateProfileModel(data));
```

## 2. Dynamic UI Generation (Server-Side Rendering)
**Capability:** Fetching pre-built HTML fragments to inject directly into the page.
*   **Context:** Instead of building HTML in JavaScript, the server sends a complete `<div>...</div>` string.
*   **Risk:** High XSS risk if unchecked.

```javascript
// Example: Loading a Dialog Box content
$.get('/views/login-modal.html', function(html) {
    $('#modal-container').html(html); // Injects HTML tags!
});
```

## 3. Dynamic Script Loading (Code Injection)
**Capability:** Fetching and executing new JavaScript code on the fly.
*   **Use Case:** Lazy-loading heavy libraries (charts, maps) only when the user goes to that page.
*   **Mechanism:** Fetching a `.js` file and running `eval()` or appending a `<script>` tag.

```javascript
// Example: Lazy-loading a library
$.getScript('/assets/map-plugin.js', function() {
    initMap(); // This function didn't exist before the AJAX call!
});
```

## 4. Dynamic Style Injection (CSS Transformation)
**Capability:** Fetching CSS rules or stylesheets to change the look of the page dynamically.
*   **Use Case:** Theming (Dark Mode), loading page-specific styles.

```javascript
// Example: Loading a theme
fetch('/themes/dark-mode.css')
    .then(res => res.text())
    .then(css => {
        $('<style>').text(css).appendTo('head'); // Injects raw CSS rules
    });
```

## 5. Silent Telemetry (Tracking)
**Capability:** Sending data "fire-and-forget" without waiting for a response.
*   **Use Case:** Analytics, error logging, user activity tracking.
*   **Note:** Often uses `navigator.sendBeacon` because it survives page navigation.

```javascript
// Example: Logging a button click
navigator.sendBeacon('/api/log', JSON.stringify({ event: 'click' }));
```

---

## Summary Matrix: Capabilities vs. Detection

| Capability | What is Transferred? | Key Detection Clues (In Response) |
| :--- | :--- | :--- |
| **Data Exchange** | JSON / XML Objects | `.json()`, `loop`, `object.property` |
| **UI Generation** | HTML Strings | `.html()`, `.innerHTML`, `<div>` tags |
| **JS Loading** | Executable Code | `.getScript()`, `eval()`, `<script>` tags |
| **CSS Loading** | Style Rules | `<style>`, `<link>`, `.text()` handled as CSS |
| **Telemetry** | One-way Data | `sendBeacon`, no callback used, `void` return |

---

## Why This Matters for Analysis

When scanning code, identifying the *Capability* determines the **Risk Profile**:

*   **Data Exchange** → Business Logic Audit (Safe mostly)
*   **UI Generation** → **XSS Audit** (Sanitization check needed)
*   **JS Loading** → **Security Audit** (Where is that code coming from? Is it trusted?)
*   **CSS Loading** → UI/UX Audit (Breaking changes?)
*   **Telemetry** → Privacy Audit (GDPR/Compliance)
