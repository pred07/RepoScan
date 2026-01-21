"""
AJAX Detection Module for RepoScan

Detects AJAX patterns in JavaScript code, extracts endpoint URLs,
identifies server dependencies, and classifies inline vs external AJAX.
"""

import re
import os
from typing import Optional

# Compile regex patterns once for performance
AJAX_PATTERNS = {
    'xmlhttprequest': re.compile(r'new\s+XMLHttpRequest\s*\(', re.IGNORECASE),
    'jquery_ajax': re.compile(r'[A-Za-z_$]\w*\s*\.\s*(?:ajax|get|post|getJSON|getScript|load|request)\s*\(', re.IGNORECASE),
    'fetch_api': re.compile(r'\bfetch\s*\(|window\.fetch\s*\(', re.IGNORECASE),
    'axios': re.compile(r'\baxios(?:\.\w+)?\s*\(', re.IGNORECASE),
    'xhr_state': re.compile(r'\bonreadystatechange\s*=|' r'\.send\s*\(', re.IGNORECASE),
    'websocket': re.compile(r'new\s+WebSocket\s*\(', re.IGNORECASE),
    'eventsource': re.compile(r'new\s+EventSource\s*\(', re.IGNORECASE),
}

# Server-side dependency patterns
SERVER_PATTERNS = [
    re.compile(r'@Model\.', re.IGNORECASE),
    re.compile(r'@ViewBag\.', re.IGNORECASE),
    re.compile(r'@ViewData\.', re.IGNORECASE),
    re.compile(r'@Url\.Action', re.IGNORECASE),
    re.compile(r'@Url\.Content', re.IGNORECASE),
    re.compile(r'<%=', re.IGNORECASE),
    re.compile(r'<%:', re.IGNORECASE),
    re.compile(r'<%\s', re.IGNORECASE),
    re.compile(r'\{\{.*?\}\}', re.IGNORECASE),  # Template engines
    re.compile(r'\bResponse\.Write\b', re.IGNORECASE),
    re.compile(r'\bRequest\.Form\b', re.IGNORECASE),
]

# URL extraction patterns
URL_PATTERNS = {
    # url: '/api/users' or url: "/api/users"
    'url_property': re.compile(r'''url\s*:\s*['"]([^'"]+)['"]''', re.IGNORECASE),
    # url: baseUrl + '/users'
    'url_concat': re.compile(r'''url\s*:\s*([a-zA-Z_$][a-zA-Z0-9_$]*\s*\+\s*['"][^'"]+['"])''', re.IGNORECASE),
    # url: `${API_URL}/users`
    'url_template': re.compile(r'''url\s*:\s*`([^`]+)`''', re.IGNORECASE),
    # url: variableName
    'url_variable': re.compile(r'''url\s*:\s*([a-zA-Z_$][a-zA-Z0-9_$]*)(?:\s|,|\))''', re.IGNORECASE),
    # fetch('/api/users') or fetch("/api/users")
    'fetch_literal': re.compile(r'''fetch\s*\(\s*['"]([^'"]+)['"]''', re.IGNORECASE),
    # fetch(`${base}/users`)
    'fetch_template': re.compile(r'''fetch\s*\(\s*`([^`]+)`''', re.IGNORECASE),
    # $.get('/api/users', ...) or $.post('/api/users', ...)
    'jquery_literal': re.compile(r'''\$\.(get|post|getJSON|load)\s*\(\s*['"]([^'"]+)['"]''', re.IGNORECASE),
    # axios.get('/api/users')
    'axios_literal': re.compile(r'''axios\.(get|post|put|delete|patch)\s*\(\s*['"]([^'"]+)['"]''', re.IGNORECASE),
}

# Inline file extensions (view/template files)
INLINE_EXTENSIONS = {'.cshtml', '.aspx', '.ascx', '.master', '.html', '.htm', '.php', '.jsp'}


def detect_ajax_patterns(snippet) -> bool:
    """
    Main entry point for AJAX detection.
    Enriches the CodeSnippet object in-place with AJAX metadata.
    
    Args:
        snippet: CodeSnippet object to analyze
        
    Returns:
        bool: True if AJAX detected, False otherwise
    """
    if snippet.category != 'JS':
        return False
    
    code = snippet.full_code
    
    total_ajax = 0
    first_pattern = ""
    
    for name, pattern in AJAX_PATTERNS.items():
        matches = pattern.findall(code)
        if matches:
            if not first_pattern:
                first_pattern = name
            total_ajax += len(matches)
            
    if total_ajax > 0:
        snippet.ajax_detected = True
        snippet.ajax_pattern = first_pattern
        snippet.ajax_count = total_ajax
        snippet.endpoint_url = extract_endpoint_url(code, first_pattern)
        snippet.is_inline_ajax = is_inline_ajax(snippet.file_path)
        
        # Check for server dependencies (e.g. <%= %>, Razor @Model)
        snippet.has_server_deps = False
        for dep_pattern in SERVER_PATTERNS:
            if dep_pattern.search(code):
                snippet.has_server_deps = True
                break
        
        return True
        
    return False


def get_ajax_pattern_name(code: str) -> Optional[str]:
    """
    Identifies which AJAX pattern is present in the code.
    
    Args:
        code: JavaScript code to analyze
        
    Returns:
        str: Pattern name (e.g., 'jquery_ajax', 'fetch_api') or None
    """
    # Search in priority order (most specific first)
    for pattern_name, pattern_regex in AJAX_PATTERNS.items():
        if pattern_regex.search(code):
            return pattern_name
    
    return None


def extract_endpoint_url(code: str, pattern_type: str) -> str:
    """
    Extracts the API endpoint URL from AJAX code.
    
    Args:
        code: JavaScript code containing AJAX call
        pattern_type: Type of AJAX pattern detected
        
    Returns:
        str: Extracted URL or classification (Dynamic/Variable, Server-Generated, Unknown/Dynamic)
    """
    # Limit search to first 1000 chars for performance
    search_code = code[:1000]
    
    # Try pattern-specific extraction first
    if pattern_type.startswith('fetch'):
        # Try template literal
        match = URL_PATTERNS['fetch_template'].search(search_code)
        if match:
            return match.group(1)
        
        # Try literal string
        match = URL_PATTERNS['fetch_literal'].search(search_code)
        if match:
            return match.group(1)
    
    elif pattern_type.startswith('jquery'):
        # Try jQuery shorthand methods
        match = URL_PATTERNS['jquery_literal'].search(search_code)
        if match:
            return match.group(2)  # Group 2 is the URL
    
    elif pattern_type == 'axios':
        # Try axios methods
        match = URL_PATTERNS['axios_literal'].search(search_code)
        if match:
            return match.group(2)  # Group 2 is the URL
    
    # Generic URL property extraction (works for $.ajax, axios, etc.)
    # Try template literal
    match = URL_PATTERNS['url_template'].search(search_code)
    if match:
        return match.group(1)
    
    # Try literal string
    match = URL_PATTERNS['url_property'].search(search_code)
    if match:
        url = match.group(1)
        # Check if it's server-generated
        if '@' in url or '<%' in url:
            return "Server-Generated"
        return url
    
    # Try concatenated URL
    match = URL_PATTERNS['url_concat'].search(search_code)
    if match:
        return match.group(1)
    
    # Try variable
    match = URL_PATTERNS['url_variable'].search(search_code)
    if match:
        return "Dynamic/Variable"
    
    return "Unknown/Dynamic"


def check_server_dependencies(code: str) -> bool:
    """
    Checks if code contains server-side rendering syntax.
    
    Args:
        code: JavaScript code to analyze
        
    Returns:
        bool: True if server dependencies found, False otherwise
    """
    for pattern in SERVER_PATTERNS:
        if pattern.search(code):
            return True
    
    return False


def is_inline_ajax(file_path: str) -> bool:
    """
    Determines if AJAX is inline (in view/template) or external (.js file).
    
    Args:
        file_path: Path to the file containing AJAX code
        
    Returns:
        bool: True if inline (view/template file), False if external (.js file)
    """
    _, ext = os.path.splitext(file_path)
    ext_lower = ext.lower()
    
    # .js files are external
    if ext_lower == '.js':
        return False
    
    # View/template files are inline
    if ext_lower in INLINE_EXTENSIONS:
        return True
    
    # Default to inline for unknown extensions (safer assumption)
    return True
