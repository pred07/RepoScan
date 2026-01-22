# Repository Depth Analyzer

A standalone utility to analyze codebase structure and complexity metrics.

## Features

- **File Inventory**: Scans all files in a directory and collects metadata
- **Complexity Analysis**: Detects inline/internal CSS, JS, AJAX calls, and dynamic resource generation
- **Directory Statistics**: Provides breakdown by directory depth and file extensions
- **Multithreaded Scanning**: Fast processing using concurrent file analysis
- **Excel Reports**: Professional, styled Excel output with multiple tabs

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py <path_to_target_directory> [--output <output_directory>]
```

### Examples

```bash
# Scan current directory
python main.py .

# Scan specific project
python main.py C:\Projects\MyApp

# Specify custom output location
python main.py C:\Projects\MyApp --output C:\Reports
```

## Output

The tool generates an Excel file: `Application_Depth_Tracker_YYYYMMDD_HHMMSS.xlsx`

### Report Tabs

1. **Summary_Dashboard**: 
   - **Basic Metrics**: Total files, code lines, and size
   - **Complexity Metrics Summary**: Totals for all detected patterns (CSS, JS, AJAX, Dynamic code)
   - **Global Extension Breakdown**: File count by extension
2. **Directory_Analysis**: Statistics grouped by directory with depth information
3. **File_Details**: Basic file metadata (path, name, extension, lines, size)
4. **Complexity_Metrics**: Detailed per-file complexity analysis with full paths

### Summary Dashboard Highlights

The **Summary_Dashboard** tab provides an at-a-glance overview with totals for:

**CSS Patterns:**
- Inline CSS (style="...") 
- Internal Style Blocks (<style>)
- External Stylesheets (<link>)

**JavaScript Patterns:**
- Inline JS (event handlers)
- Internal Script Blocks (<script>)
- External Script Tags (src="...")

**AJAX & Network Calls:**
- Total AJAX Calls Detected
- Files with AJAX

**Dynamic Code Generation:**
- Dynamic JS (eval, innerHTML, etc.)
- Dynamic CSS (style manipulation)

### Complexity Metrics

The **Complexity_Metrics** tab provides granular code complexity insights with **100% detection accuracy** matching the main RepoScan utility:

- **Inline_CSS_Count**: `style="..."` attributes
- **Internal_CSS_Count**: `<style>...</style>` blocks
- **Inline_JS_Count**: 40+ event handlers (`onclick`, `onload`, `onsubmit`, `onkeydown`, etc.) and `javascript:` URLs
- **Internal_JS_Count**: `<script>...</script>` blocks
- **AJAX_Calls_Count**: Comprehensive detection of:
  - jQuery: `$.ajax()`, `$.get()`, `$.post()`, `$.getJSON()`, `$.getScript()`, `$.load()`
  - Native: `XMLHttpRequest`, `fetch()`, `ActiveXObject` (IE legacy)
  - Modern: `axios()`, `axios.get/post/put/delete/patch()`
  - Object Literals: `ajax: function()` (jQuery plugins, API wrappers)
  - Headers: `setRequestHeader('X-Requested-With')`
- **Dynamic_JS_Gen_Count**: Dynamic script creation (`createElement('script')`, `eval()`, `new Function()`)
- **Dynamic_CSS_Gen_Count**: Dynamic style creation (`createElement('style')`, `createElement('link')`)

## Requirements

- Python 3.7+
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## Performance

The tool uses multithreading to process files concurrently, making it suitable for large codebases.

### Excluded Folders

To maintain accuracy on source code while avoiding dependency bloat, the following folders are automatically excluded:

**Dependencies**: `node_modules`, `vendor`, `packages`  
**Version Control**: `.git`, `.svn`, `.hg`  
**Build Outputs**: `bin`, `obj`, `dist`, `build`, `out`, `target`  
**Virtual Environments**: `venv`, `env`, `.venv`, `__pycache__`, `.pytest_cache`

This ensures 100% accuracy on your source code while skipping thousands of third-party files.
