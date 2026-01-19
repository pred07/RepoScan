# Inline Code Scanner Utility

## Overview
A powerful Python based utility designed to recursively scan local .NET/Web application folders. It detects and catalogs all instances of **Inline JavaScript**, **Inline CSS**, and **External Resource References** to assist with Content Security Policy (CSP) implementation and security hardening.

## Features
*   **Comprehensive Detection**: Finds script blocks, event handlers (onclick, onmouseover, etc.), `javascript:` URIs, and style attributes.
*   **Detailed Reporting**: Generates a multi-tab Excel tracker with code snippets, line numbers, and "Full Code" extraction.
*   **Smart Parsing**: Uses DOM parsing (BeautifulSoup) for accuracy and Regex for legacy patterns.
*   **AJAX Detection**: Flags scripts containing AJAX keywords (`fetch`, `xhr`, `$.ajax`).
*   **Clean Output**: Automatically manages output directories and log files.

## Prerequisites
*   **Python 3.8+** installed on your system.
*   **pip** (Python Package Manager).

## Installation

1.  **Download/Clone** this folder to your local machine.
2.  Open a terminal (Command Prompt, PowerShell, or Bash) in the folder.
3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Windows
Run the scanner by pointing it to your target application's root source folder.

```powershell
# Basic usage (defaults to current folder if no root specified)
python main.py --root "C:\Path\To\Your\WebApp"

# Specify a custom output folder
python main.py --root "C:\Path\To\Your\WebApp" --output "C:\Reports"
```

### Linux / macOS
```bash
# Basic usage
python3 main.py --root /home/user/projects/my-web-app

# Specify output
python3 main.py --root /home/user/projects/my-web-app --output ./reports
```

## Configuration
Customize `config.ini` to control the scan:

*   **`include_extensions`**: Add files to scan (e.g., `.php`, `.jsp` if needed).
*   **`exclude_folders`**: Folders to skip (default: `bin`, `obj`, `node_modules`, `.git`).
*   **`exclude_files`**: Patterns to ignore (e.g., `*.min.js`, `jquery*.js`).

## Output
The tool creates two folders:

1.  **`output/`**: Contains the Excel Scan Report (`InlineCode_Scan_YYYYMMDD_HHMMSS.xlsx`).
    *   *Note: Old reports in this folder are automatically deleted before a new scan.*
2.  **`logs/`**: Contains execution logs (`scanner_error_YYYYMMDD.log`) useful for debugging parsing errors.

## Excel Report Structure
*   **Summary**: Dashboard with total counts.
*   **Inline JavaScript**: Details of every JS instance found (Line #, Code Snippet, Full Code, AJAX Detected).
*   **Inline CSS**: Details of every CSS instance found.
*   **External Resources**: List of all external scripts and stylesheets linked.
