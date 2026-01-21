# RepoScan Tool Functionality & Logic Deep-Dive

This document provides a comprehensive breakdown of the internal logic, optimization patterns, and detection strategies used by the RepoScan toolset.

---

## 1. Detection Engine: The "Hybrid Sense" Approach

RepoScan uses a **Hybrid Sensing** model to ensure 100% accuracy across diverse file types (.aspx, .js, .html, .cshtml).

### 1.1 DOM Parsing (Structural Analysis)
For HTML-based files, the tool uses **BeautifulSoup 4** with a specific focus on:
- **Script/Style Blocks**: Identifying tags without `src` attributes as candidates for extraction.
- **Event Handlers**: Attribute-level scanning for over 40 event types (e.g., `onclick`, `onmouseover`).
- **Pseudo-Protocols**: Detecting `javascript:` URIs in `href` and `src` attributes.

### 1.2 Regex Scanning (Exhaustive Detection)
While DOM parsing finds the "where," Regex finds the "what." Unlike basic scanners that mark a file as "having AJAX," RepoScan performs **Literal Occurrence Counting**:
- It scans the *entire content* of a script block or standalone JS file.
- It sums every instance of a pattern (e.g., finding 12 `$.ajax` calls in a single minified file).
- This ensures the "Summary Dashboard" reflects the true volume of network and dynamic calls.

---

## 2. Advanced Detection Patterns

### 2.1 AJAX & Network Discovery
The scanner identifies legacy, modern, and manual network implementations:
- **Legacy**: `XMLHttpRequest`, `$.ajax`.
- **Modern**: `fetch()`, `axios`, `window.fetch`.
- **Real-Time**: `WebSocket`, `EventSource`.
- **Manual States**: `onreadystatechange`, `.send()`.

### 2.2 Dynamic Code Generation (Security Sinks)
The tool flags code that dynamically generates HTML or executes strings, as these are high-risk for CSP bypass:
- **DOM Sinks**: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`.
- **Execution Sinks**: `eval()`, `new Function()`, `setTimeout(string)`, `setInterval(string)`.
- **Dynamic Loading**: `document.createElement('script')`, setting `.src` or `.href` dynamically.

---

## 3. Optimization & Accuracy Patterns

### 3.1 Standalone JS Scanning
The tool does not stop at HTML. It performs a **Deep Scan** on `.js` files:
- Analyzes library files (e.g., `jquery.min.js`) to find internal network implementations.
- Extracts endpoint URLs from external scripts.
- Classifies them as `LOCAL` source type to distinguish from `INLINE` code.

### 3.2 Metadata-Driven Tracking
Every extracted snippet is saved with a unique **Metadata Filename**:
`{FilePath}_{Type}_L{StartLine}-L{EndLine}.js`
- This allows for stateless refactoring; the tool knows exactly where a block came from just by looking at the filename.

---

## 4. Refactorability Assessment (The Grading Matrix)

The `check.py` module applies a heuristic engine to categorize risk:

| Grade | Color | Criteria | Refactoring Strategy |
| :--- | :--- | :--- | :--- |
| **GREEN** | **High** | Pure JS/CSS with no dependencies. | **Auto**: Safe to extract immediately. |
| **YELLOW**| **Med**  | Event Handlers or Dynamic Sinks. | **Manual Rewrite**: Convert to `addEventListener`. |
| **RED**   | **Low**  | Server Syntax (`<%= %>`, `@Model`). | **Architectural**: Decouple server data first. |

---

## 5. Directory Depth Logic (Inventory Engine)

In the `repo_depth_analyser`, we use **Structural Heuristics** to map the application "shape":
- **Depth Calculation**: Measuring folder nesting to identify architectural "sprawl."
- **Noise Filtering**: Excluding `.git`, `node_modules`, and `bin` to provide a "Clean Code Base" metric.
- **Split Metrics**: Separating `<style>` blocks from `<link>` tags to plan CSP `style-src` accurately.

---

## 6. Comprehensive Pattern Library

For technical transparency, here are the exact regex patterns used for detection:

### 6.1 Network & AJAX Patterns
| Pattern Name | Logic / Regex | Matches |
| :--- | :--- | :--- |
| **XMLHttpRequest** | `new\s+XMLHttpRequest\s*\(` | Manual XHR instantiation. |
| **jQuery AJAX** | `[A-Za-z_$]\w*\s*\.\s*(?:ajax\|get\|post\|getJSON\|getScript\|load\|request)\s*\(` | All jQuery network methods. |
| **Fetch API** | `\bfetch\s*\(|window\.fetch\s*\(` | Native browser Fetch API. |
| **Axios** | `\baxios(?:\.\w+)?\s*\(` | Axios library calls. |
| **XHR State** | `\bonreadystatechange\s*=\|.send\(` | Manual XHR cycle management. |
| **WebSocket** | `new\s+WebSocket\s*\(` | Real-time communication. |
| **EventSource** | `new\s+EventSource\s*\(` | Server-Sent Events (SSE). |

### 6.2 Dynamic Code Sinks (Security Risk)
| Sink Type | Regex | Description |
| :--- | :--- | :--- |
| **DOM Insertion** | `\.(innerHTML\|outerHTML\|insertAdjacentHTML\|write\|writeln)\s*=` | Raw HTML injection. |
| **Execution** | `\b(eval\|new\s+Function\|setTimeout\|setInterval)\s*\(` | String-to-code execution. |
| **Dynamic Load** | `\.(src\|href)\s*=\s*\|document\.createElement\s*\(\s*["\'](script\|style\|link)["\']\s*\)` | Runtime asset injection. |

### 6.3 Dynamic Styling Sinks
| Feature | Regex | Target |
| :--- | :--- | :--- |
| **CSS Injection** | `\.rel\s*=\s*["\']stylesheet["\']\|setProperty\s*\(\|insertRule\s*\(` | Manual style rule manipulation. |
| **Property Control**| `\.style\.\w+\s*=\|\.style\[\s*["\'][^"\']+["\']\s*\]\s*=` | Direct DOM style property modification. |
| **Asset Creation** | `document\.createElement\s*\(\s*["\'](style\|link)["\']\s*\)` | Runtime creation of styling elements. |

### 6.4 Server-Side Dependencies (Refactoring Blocks)
| Dependency | Regex | Support Area |
| :--- | :--- | :--- |
| **Razor / ASP.NET** | `@Model\.`, `@ViewBag\.`, `@ViewData\.`, `@Url\.Action` | .NET MVC / Razor Pages. |
| **Classic ASP/WebForms**| `<%=`, `<%:`, `<%\s`, `\bResponse\.Write\b` | Legacy .NET / ASP. |
| **General Templates** | `\{\{.*?\}\}` | Angular, Handlebars, etc. |

### 6.4 Core Tag Discovery
| Feature | Regex | Target |
| :--- | :--- | :--- |
| **Inline CSS** | `style\s*=\s*["\'][^"\']*["\']` | HTML `style` attributes. |
| **Style Block** | `<style\b[^>]*>[\s\S]*?</style>` | Internal CSS blocks. |
| **Script Block** | `<script\b(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>` | Internal JS without `src`. |
| **Event Handlers** | `(\bon\w+\s*=\s*["\'][^"\']*["\']\|href=["\']\s*javascript:)` | `onclick`, `onload`, and JS URIs. |

