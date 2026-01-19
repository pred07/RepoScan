# Inline Code Scanner - Tool Definition & Technical Documentation

## 1. Tool Definition
The **Inline Code Scanner** is a specialized security auditing utility designed recursively scan web application source code (specifically .NET and modern web apps) to identify and catalog instances of "inline" code. It detects inline JavaScript, inline CSS, and external resource references that would violate strict **Content Security Policy (CSP)** rules.

## 2. Purpose
The primary purpose of this tool is to assist security engineers and developers in hardening web applications by preparing them for Content Security Policy (CSP) implementation.

*   **CSP Preparation**: finding all inline scripts `onclick="..."` and style attributes `style="..."` that need to be refactored or whitelisted (via nonce/hash).
*   **Attack Surface Reduction**: Identifying legacy inline event handlers that are often vectors for XSS (Cross-Site Scripting).
*   **Inventory Management**: Creating a comprehensive inventory of all external scripts and stylesheets loaded by the application.

## 3. Installation

### Prerequisites
*   **Python 3.8** or higher.
*   **pip** (Python Package Manager).

### Steps
1.  Clone or download the repository to your local machine.
2.  Navigate to the tool's directory in your terminal.
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Run Command

Execute the tool via the `main.py` entry point. You can run it from any terminal (Command Prompt, PowerShell, Bash).

### Basic Usage
Scans the current directory (default) and outputs to `./output`.
```bash
python main.py
```

### Advanced Usage
Specify a target root folder and a custom output directory.
```bash
python main.py --root "C:\Path\To\Target\App" --output "C:\MyReports"
```

| Argument | Description |
| :--- | :--- |
| `--root` | The absolute or relative path to the application source code you want to scan. |
| `--output` | The directory where the Excel report and logs will be saved. |
| `--config` | (Optional) Path to a custom `config.ini` file. Defaults to `config.ini` in the current folder. |

## 5. Configuration (`config.ini`)
The tool is highly configurable via the `config.ini` file. This allows you to fine-tune the scan scope.

### [Paths]
*   `root_folder`: Default directory to scan if `--root` is not provided.
*   `output_folder`: Default output directory.

### [Filters]
*   `include_extensions`: Comma-separated list of file extensions to scan (e.g., `.aspx, .html, .js`).
*   `exclude_folders`: Directories to completely ignore (e.g., `node_modules, bin, obj, .git`).
*   `exclude_files`: Glob patterns for filenames to ignore (e.g., `*.min.js, jquery*.js` to skip minified libraries).

### [Limits]
*   `max_file_size_mb`: Skips files larger than this size (default: 10MB) to prevent memory issues.
*   `snippet_max_length`: Truncates code snippets in the Excel report to this character length.

## 6. Working Logic
The tool operates in a linear **3-Phase Process**:

### Phase 1: Discovery (Scanning)
1.  The `Scanner` module traverses the `root_folder`.
2.  It filters files based on `include_extensions`.
3.  It excludes directories and files matching the exclusion rules in `config.ini`.
4.  It yields a list of valid file paths to be processed.

### Phase 2: Analysis (Parsing)
1.  The `Parser` module reads each file.
2.  **DOM Parsing**: It uses `BeautifulSoup` to parse HTML/ASPX content.
    *   Finds `<script>` tags (inline and external).
    *   Finds `<style>` tags.
    *   Finds all tags with inline event handlers (e.g., `onclick`, `onload`, `onmouseover`).
    *   Finds all tags with `style="..."` attributes.
    *   Finds `javascript:` URIs in `href` or `src` attributes.
    *   Finds `<link rel="stylesheet">` tags.
3.  **AJAX Detection**: It scans caught scripts for keywords like `fetch`, `XMLHttpRequest`, `$.ajax` to flag potential dynamic data loading.
4.  **Regex Fallback**: Uses Regex to catch edge cases like `javascript:` links that might be missed by the DOM parser in fragments.
5.  It captures line numbers, code snippets, and specific failure types.

### Phase 3: Reporting
1.  The `Reporter` module collects all findings.
2.  It generates an Excel file (`.xlsx`) using `openpyxl`.
3.  The report is organized into tabs:
    *   **Summary**: A high-level dashboard with counts.
    *   **Inline JavaScript**: Detailed list of script blocks and event handlers.
    *   **Inline CSS**: Detailed list of style blocks and attributes.
    *   **External Resources**: List of linked JS and CSS files.
4.  If the output file is open/locked, it gracefully handles the finding.

## 7. Functions of Main Files

### `main.py`
**Role**: Entry Point & Orchestrator.
*   `main()`: Coordinates the flow. Sets up logging, parses args, initiates the scan, runs the loop for parsing, and triggers report generation.
*   `cleanup_old_reports()`: A utility function that deletes previous `.xlsx` reports from the output folder before a new run to avoid clutter.

### `src/scanner.py`
**Role**: File System Traversal.
*   `Scanner.scan()`: Generator that walks the directory tree.
*   `Scanner._should_include()`: Validates files against the extension whitelist and exclusion blacklists (folders/files/size).

### `src/parser.py`
**Role**: Core Analysis Engine.
*   `Parser.parse()`: Main entry for analyzing a single file's content.
*   `Parser._scan_dom()`: Uses `BeautifulSoup` to navigate the DOM tree and extract nodes of interest (scripts, styles, attributes).
*   `Parser._scan_regex()`: Secondary scan for patterns hard to catch with DOM parsers (like simple text searches for `javascript:`).
*   `Parser._get_line_number()`: Attempts to resolve the exact line number of a finding using BS4's `sourceline` or falling back to a text search.
*   `Parser._detect_ajax()`: Simple keyword matching to flag AJAX usage.

### `src/reporter.py`
**Role**: Output Generator.
*   `Reporter.generate_report()`: Creates the Excel workbook structure.
*   `Reporter._create_summary_sheet()`: Builds the dashboard tab with logic-driven formatting (colors, counts).
*   `Reporter._create_js_sheet()`: Formats the JS findings table.
*   `Reporter._create_css_sheet()`: Formats the CSS findings table.

### `src/config.py`
**Role**: Configuration Management.
*   `ScannerConfig`: Data class that holds runtime settings.
*   `ScannerConfig.load()`: Reads and parses the `config.ini` file.
*   `parse_arguments()`: Handles command-line arguments and overrides `config.ini` settings if flags are provided.

### `src/logger.py`
**Role**: Logging Infrastructure.
*   `setup_logger()`: Configures Python's `logging` module to write errors to a file in the `logs/` directory and print info to the console.
