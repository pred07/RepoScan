# RepoScan: Developer & Testing Guide

This document explains the three core utilities of the `RepoScan` toolkit, how to run them, and how to interpret their outputs.

---

## 1. Static Scanner (`main.py`)
This is the entry point for static analysis. It scans your source code for inline JavaScript and CSS.

### **How to Run**
```bash
python main.py --root "C:\Path\To\Your\SourceCode" --output "output_scan"
```

### **Purpose**
To identify where inline code exists (e.g., `<script>...</script>`, `onclick="..."`, `<style>...</style>`) so it can be moved to external files for Content Security Policy (CSP) compliance.

### **Output**
- **Excel Report** (`Analysis.xlsx`): Lists every file and line number containing inline code.
- **Extracted Code Folder** (`extracted_code/`): Contains the actual JS/CSS code extracted from your source files.
    - `inline_javascript/`: Extracted scripts.
    - `inline_css/`: Extracted styles.
- **Assessment Tracker** (`Refactoring_Assessment.xlsx`): A checklist for tracking which items have been refactored.

---

## 2. AJAX Crawler (`crawl.py`)
This utility crawls your running application to find resources loaded dynamically (e.g., via AJAX or generated scripts) and correlates them with the static scan findings.

### **How to Run**
1. Ensure your application is running (e.g., `http://localhost:8080`).
2. Run the crawler:
```bash
python crawl.py --url "http://localhost:8080" --scan-report "output_scan\InlineCode_Scan_Report.xlsx" --output "output_crawl"
```

### **Purpose**
Static scanning might miss code that is dynamically loaded or constructed. The crawler verifies what actually loads in the browser and points out any "Missing" items that static analysis found but the crawler didn't see (or vice versa).

### **Output**
- **Correlation Report** (`AJAX_Correlation.xlsx`):
    - **Verified**: Items found by both Static Scan and Crawler.
    - **New Findings**: Dynamic assets found by Crawler that Static Scan missed.
    - **Missing**: Static items that were not detected during the crawl (might require manual check).
    - **External URLs**: List of 3rd-party scripts/styles found.

---

## 3. Refactoring Tool (`refactoring_utility/refactor.py`)
This tool attempts to automatically refactor your code by replacing inline blocks with references to the extracted files.

### **How to Run**
```bash
python refactoring_utility/refactor.py --root "C:\Path\To\Your\SourceCode" --extracted "output_scan\extracted_code" --output "Refactored_App"
```

### **Purpose**
To speed up remediation by "applying" the extracted code back to the project. It creates a **copy** of your project and modifies the HTML/Razor files to link to the new external `.js` / `.css` files.

### **Output**
- A full copy of your application in the `output` folder (e.g., `Refactored_App`).
- **Modified files**: HTML files now have `<script src="...">` and `<link href="...">` tags instead of inline blocks.

---

## Analysis of the Setup

### **Merits**
- **Automation**: Drastically reduces manual effort in finding thousands of inline code snippets.
- **Safety**: The refactoring tool works on a *copy*, ensuring the original source is never touched.
- **Completeness**: Combining Static Analysis (Main) and Dynamic Analysis (Crawler) gives a high-confidence view of the attack surface.
- **Audit Trail**: The Excel reports provide a clear artifacts for security audits.

### **Drawbacks & Limitations**
- **Refactoring Precision**: The refactoring tool uses regex/line-based replacement. It handles standard blocks well but may struggle with complex, multi-line inline strings or mixed server-side code (e.g., heavily nested Razor syntax). **Always manual review the refactored code.**
- **Crawler Coverage**: The crawler can only find pages it can navigate to. Deep states requiring complex user interaction sequences might be missed.

---

## Guide for Developers (How to Test)

1.  **Run the Scan**: Point `main.py` to your codebase.
2.  **Review the Report**: Open `Refactoring_Assessment.xlsx`. Use this as your "To-Do" list.
3.  **Test Refactoring**:
    - Run the `refactoring_utility`.
    - Compare a few "Before" vs "After" files in the `Refactored_App` folder.
    - Check if the logic still holds (e.g., are variables passed correctly to the external script?).
4.  **Run the App**: Launch the `Refactored_App`. Does it still work?
5.  **Crawl**: Run `crawl.py` against the `Refactored_App`. It should ideally show fewer "inline" findings or confirm the external resources are loading.
