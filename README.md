# Inline Code Scanner & Refactoring Utility

A comprehensive toolchain for auditing, assessing, and refactoring inline JavaScript and CSS to comply with strict Content Security Policy (CSP) requirements.

---

## 1. Project Overview
**Goal**: Enable strict CSP (`default-src 'self'`) in .NET/Web applications by automating the detection and remediation of inline code.

**Key Capabilities**:
1.  **Scan**: Identify all inline scripts, styles, event handlers, and `javascript:` URIs.
2.  **AJAX Detection**: Automatically detect and analyze all AJAX calls (jQuery, Fetch, Axios, XMLHttpRequest) with endpoint extraction and server dependency analysis.
3.  **Assess**: Grade the difficulty of refactoring each file based on complexity.
4.  **Refactor**: Automatically move inline code to external files and update the source code in a safe, copy-first manner.

---

## 2. Quick Start & Installation

**Prerequisites**: Python 3.8+

```bash
pip install -r requirements.txt
```

### Directory Structure
```text
inline_scanner/
├── src/                # Core Logic (Scanner, Parser, Reporter)
├── refactoring_utility/# Refactoring Engine (Check, Refactor)
├── main.py             # Entry Point
└── output/             # ALL tool outputs go here
```

---

## 3. Workflow & Usage

### Command Examples

**Windows (PowerShell)**:
```powershell
# Scan current directory
python main.py --root . --output output

# Scan specific application
python main.py --root "C:\inetpub\wwwroot\MyApp" --output "C:\Reports\output"

# Refactor (after scanning)
python refactoring_utility\refactor.py --root "C:\MyApp" --extracted "output\extracted_code" --output "output\Refactored_App"
```

**Windows (CMD)**:
```cmd
REM Scan current directory
python main.py --root . --output output

REM Scan specific application
python main.py --root "C:\inetpub\wwwroot\MyApp" --output "C:\Reports\output"

REM Refactor (after scanning)
python refactoring_utility\refactor.py --root "C:\MyApp" --extracted "output\extracted_code" --output "output\Refactored_App"
```

**Linux/Mac (Bash)**:
```bash
# Scan current directory
python main.py --root . --output output

# Scan specific application
python main.py --root /var/www/myapp --output ~/reports/output

# Refactor (after scanning)
python refactoring_utility/refactor.py --root /var/www/myapp --extracted output/extracted_code --output output/Refactored_App
```

### Step 1: Scan & Assess

Run the main scanner to audit your codebase.

```powershell
python main.py --root "C:\Path\To\YourApp" --output "output"
```

**Outputs (in `output/`)**:
*   `InlineCode_Scan_<Date>.xlsx`: Detailed audit report with **5 tabs**:
    *   **Summary**: Statistics and metadata
    *   **Inline JavaScript**: All JS findings
    *   **Inline CSS**: All CSS findings
    *   **AJAX Code**: 🆕 Dedicated AJAX analysis with pattern detection, endpoint URLs, and server dependency flags
    *   **External Resources**: External scripts and stylesheets
*   `Refactoring_Assessment.xlsx`: **The Tracker**. Prioritizes work:
    *   🟢 **Ready**: Safe to refactor automatically.
    *   🟡 **Needs Rewrite**: Event handlers (`onclick`) that need manual event listener attachment.
    *   🔴 **Blocked**: Server-side code (`@Model`, `<%= %>`) that requires logic changes.
*   `extracted_code/`: The actual `.js` and `.css` files extracted from your source.

### AJAX Detection Features 🆕

The scanner automatically detects and analyzes all AJAX patterns in your codebase:

**Supported AJAX Patterns** (8 types):
- ✅ **XMLHttpRequest**: `new XMLHttpRequest()`
- ✅ **jQuery**: `$.ajax()`, `$.get()`, `$.post()`, `$.getJSON()`, `$.load()`
- ✅ **Fetch API**: `fetch()`, `window.fetch()`
- ✅ **Axios**: `axios.get()`, `axios.post()`, `axios.put()`, `axios.delete()`, etc.

**AJAX Tab Columns**:
1. **AJAX Type**: Pattern detected (e.g., `jquery_ajax`, `fetch_api`)
2. **Endpoint/URL**: Extracted API endpoint
3. **Has Server Dependencies**: 🔴 Red (Yes) / 🟢 Green (No)
4. **Is Inline**: 🟡 Yellow (Yes) / No color (No)

**Color Coding Guide**:
- 🔴 **Red (Server Dependencies)**: Contains `@Model`, `@ViewBag`, `<%=`, etc. - Requires refactoring before extraction
- 🟢 **Green (Clean)**: Pure JavaScript - Safe to extract immediately
- 🟡 **Yellow (Inline)**: In view/template files - Needs extraction to external `.js`

**Example Output**:
```
AJAX Type: jquery_ajax
Endpoint: /api/users
Server Deps: No (Green) ← Safe to extract
Is Inline: Yes (Yellow) ← Needs extraction
```

### Step 2: Auto-Refactor

Generate a **refactored copy** of your application.

```powershell
python refactoring_utility/refactor.py --root "C:\Path\To\YourApp" --extracted "output/extracted_code" --output "output/Refactored_App"
```

**What happens:**
1.  Copies `C:\Path\To\YourApp` -> `output/Refactored_App`.
2.  **Script/Style Blocks**: Replaced with `<script src="...">` / `<link href="...">`.
3.  **Event Handlers**: Marked with comments (`<!-- TODO: Refactor onclick... -->`) for manual fix.

---

## 4. Output Structure
All outputs are strictly contained within the dashboard.

```
output/
├── extracted_code/
│   ├── inline_javascript/
│   │   └── page.html_scriptblock_line10-20.js
│   └── inline_css/
│       └── page.html_styleblock_line5-8.css
├── Refactoring_Assessment.xlsx  <-- Your Work Tracker
├── InlineCode_Scan_....xlsx     <-- Detailed Audit
└── Refactored_App/              <-- Your Modified Project Copy
```

---

## 5. Technical Design Specification

### 5.1 Architecture
The system uses a pipeline approach: Scan -> Parse -> Report -> Bundle -> Assess -> Refactor.

```mermaid
graph TD
    User[User] -->|Run Scan| Main(main.py)
    Main -->|Walk Directory| Scanner[src/scanner.py]
    Scanner -->|File Content| Parser[src/parser.py]
    Parser -->|Findings| Reporter[src/reporter.py]
    Reporter -->|Excel Report| ScanReport(InlineCode_Scan.xlsx)
    Reporter -->|Extracted Files| Bundler(extracted_code/*.js/css)
    
    Bundler -->|Input| Checker[refactoring_utility/check.py]
    Checker -->|Analysis| Tracker(Refactoring_Assessment.xlsx)
    
    User -->|Run Refactor| RefactorUtil[refactoring_utility/refactor.py]
    ScanReport & Tracker -.-> RefactorUtil
    RefactorUtil -->|Copy & Mod| NewCode(Output/Refactored_App)
```

### 5.2 Refactoring Logic Flow
The refactoring utility ensures safety by **never modifying** the original source.

```mermaid
sequenceDiagram
    participant User
    participant RefactorTool
    participant FileSystem
    
    User->>RefactorTool: Execute (Root, ExtractedDir, OutputDir)
    RefactorTool->>FileSystem: Create Full Copy of Root -> OutputDir
    
    loop For Each Extracted File
        RefactorTool->>RefactorTool: Parse Metadata (OriginalFile, LineStart, LineEnd)
        RefactorTool->>FileSystem: Open Copied Source File
        alt Type == ScriptBlock
            RefactorTool->>RefactorTool: Replace Lines X-Y with <script src="...">
        else Type == StyleBlock
            RefactorTool->>RefactorTool: Replace Lines X-Y with <link href="...">
        else Type == EventHandler
            RefactorTool->>RefactorTool: Insert TODO Comment
        end
        RefactorTool->>FileSystem: Save Modified File
    end
```

### 5.3 Core Modules

#### Parser Logic (`src/parser.py`)
Uses regex for robustness against mixed server-side tags:
*   **Script**: `<script[^>]*>(.*?)</script>`
*   **Events**: `\s(on\w+)=["']`
*   **Pseudo-Protocols**: `href=["']javascript:`

#### Assessment Logic (`refactoring_utility/check.py`)
Analyzes extracted content to determine safety:
*   **Blocked (Red)**: Contains ASP.NET/Razor tags (`<%`, `@Model`).
*   **Needs Rewrite (Yellow)**: Contains `document.write` or is an event handler.
*   **Ready (Green)**: Pure JS/CSS, safe for extraction.

#### Safety Mechanisms (`refactoring_utility/refactor.py`)
*   **Immutable Source**: Input directory is treated as read-only.

---

## 6. Repository Depth Analyser

**Goal**: Provide a high-level "Inventory & Shape" analysis of the codebase to understand its scale and complexity before diving into code.

### Usage
```powershell
python repo_depth_analyser/main.py <TargetDirectory> --output <OutputDirectory>
```

### Features
*   **Noise Reduction**: Automatically excludes system directories (`.git`, `.vscode`, `node_modules`, `__pycache__`) and temporary lock files (`~$*`) to give an accurate source code count.
*   **Structural Analysis**: Calculates directory depth and extension distribution per folder.
*   **Reporting**: Generates a 3-tab Excel Tracker:
    1.  **Summary_Dashboard**: High-level metrics (Total Files, Lines of Code, Extension Breakdown).
    2.  **Directory_Analysis**: Per-folder statistics with depth and file types.
    3.  **File_Details**: Complete inventory of every file scanned.

