import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import bs4

class CodeSnippet:
    def __init__(self, file_path: str, start_line: int, end_line: int, category: str, snippet: str, code_type: str, full_code: str = "", ajax_detected: bool = False, source_type: str = "INLINE"):
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line
        self.category = category  # 'JS', 'CSS', 'External', 'Internal'
        self.snippet = snippet
        self.code_type = code_type # e.g., 'Script Block', 'onclick', 'External Script'
        self.full_code = full_code if full_code else snippet
        self.ajax_detected = ajax_detected
        self.source_type = source_type # 'INLINE', 'LOCAL', 'REMOTE'
        # AJAX-specific fields
        self.ajax_pattern = ""
        self.endpoint_url = ""
        self.has_server_deps = False
        self.is_inline_ajax = False
        self.bundled_file = ""  # Populated by Reporter


class Parser:
    def __init__(self):
        # Event handler attributes to scan for
        self.event_handlers = {
            # Mouse
            'onclick', 'ondblclick', 'onmousedown', 'onmouseup', 'onmouseover', 'onmousemove', 
            'onmouseout', 'onmouseenter', 'onmouseleave', 'oncontextmenu',
            # Keyboard
            'onkeydown', 'onkeypress', 'onkeyup',
            # Form
            'onsubmit', 'onreset', 'onchange', 'oninput', 'onfocus', 'onblur', 'onselect',
            # Window
            'onload', 'onunload', 'onbeforeunload', 'onresize', 'onscroll',
            # Media/Other
            'onerror', 'onabort', 'onplay', 'onpause', 'onvolumechange', 'ontimeupdate',
            'ondrag', 'ondragstart', 'ondragend', 'ondrop'
        }
        self.ajax_keywords = ['XMLHttpRequest', 'fetch', '$.ajax', 'axios', 'hxr']

    def parse(self, file_path: str, content: str) -> List[CodeSnippet]:
        all_findings = []
        
        # 1. Regex approach
        all_findings.extend(self._scan_regex(file_path, content))
        
        # 2. DOM Parsing
        # Prefer html.parser as it reliably supports sourceline in recent BS4 versions.
        # lxml often returns None for sourceline unless configured specifically with XML.
        try:
            soup = BeautifulSoup(content, 'html.parser')
        except:
            # Fallback for really broken HTML
            soup = BeautifulSoup(content, 'lxml')
            
        all_findings.extend(self._scan_dom(file_path, soup, content))
        
        # 3. Deduplicate
        unique_findings = []
        seen = set()
        
        for finding in all_findings:
            # Create a unique signature for the finding
            # Using start_line and a hash of the code to avoid storing massive strings
            # We strip the code to ignore minor whitespace diffs between Regex and DOM
            key = (finding.start_line, finding.code_type, finding.full_code.strip())
            
            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)
        
        # 4. AJAX Detection (for JavaScript snippets only)
        from . import ajax_detector
        for finding in unique_findings:
            if finding.category == 'JS':
                ajax_detector.detect_ajax_patterns(finding)
                
        return unique_findings

    def _scan_regex(self, file_path: str, content: str) -> List[CodeSnippet]:
        findings = []
        lines = content.splitlines()
        
        # Regex for 'javascript:' protocol
        js_proto_pattern = re.compile(r'href=["\']\s*javascript:', re.IGNORECASE)
        
        for i, line in enumerate(lines):
            line_num = i + 1
            if js_proto_pattern.search(line):
                findings.append(CodeSnippet(file_path, line_num, line_num, 'JS', line.strip(), 'jsuri', full_code=line.strip(), source_type='INLINE'))
        return findings

    def _scan_dom(self, file_path: str, soup: BeautifulSoup, raw_content: str) -> List[CodeSnippet]:
        findings = []
        
        # --- JavaScript ---
        # 1. Inline Script Blocks
        for script in soup.find_all('script'):
            line_num = self._get_line_number(script, raw_content, str(script))
            
            if script.has_attr('src'):
                # External or Internal Script
                src = script['src']
                end_line = line_num  
                
                if src.lower().startswith(('http:', 'https:', '//')):
                    # Remote
                    findings.append(CodeSnippet(file_path, line_num, end_line, 'External', src, 'External Script', full_code=str(script), source_type='REMOTE'))
                else:
                    # LOCAL / Internal
                    findings.append(CodeSnippet(file_path, line_num, end_line, 'Internal', src, 'Internal Script', full_code=str(script), source_type='LOCAL'))
            else:
                if script.string or script.contents:
                    code = script.string if script.string else "".join([str(c) for c in script.contents])
                    full_code = code.strip()
                    snippet = full_code[:200]
                    ajax = self._detect_ajax(full_code)
                    
                    # Calculate end line
                    line_count = full_code.count('\n')
                    end_line = line_num + line_count
                    
                    findings.append(CodeSnippet(file_path, line_num, end_line, 'JS', snippet, 'scriptblock', full_code=full_code, ajax_detected=ajax, source_type='INLINE'))

        # 2. Event Handlers
        for tag in soup.find_all(True):
            for attr in tag.attrs:
                attr_lower = attr.lower()
                if attr_lower in self.event_handlers:
                    val = tag[attr]
                    full_code = str(val)
                    line_num = self._get_line_number(tag, raw_content, full_code)
                    
                    # Event handlers are attributes, usually start/end on same tag line or close. 
                    # Approximate end line by counting newlines in the attribute value.
                    line_count = full_code.count('\n')
                    end_line = line_num + line_count
                    
                    snippet = f'{attr}="{full_code}"'
                    ajax = self._detect_ajax(full_code)
                    findings.append(CodeSnippet(file_path, line_num, end_line, 'JS', snippet, attr_lower, full_code=full_code, ajax_detected=ajax, source_type='INLINE'))
                
                if attr_lower in ['href', 'src']:
                    val = tag[attr]
                    if isinstance(val, str) and val.lower().strip().startswith('javascript:'):
                        line_num = self._get_line_number(tag, raw_content, val)
                        end_line = line_num + val.count('\n')
                        findings.append(CodeSnippet(file_path, line_num, end_line, 'JS', val, 'jsuri', full_code=val, source_type='INLINE'))

        # --- CSS ---
        # 1. Inline Style Blocks
        for style in soup.find_all('style'):
            content = style.string if style.string else ""
            line_num = self._get_line_number(style, raw_content, content)
            
            if content and '@import' in content:
                end_line = line_num + content.strip().count('\n')
                findings.append(CodeSnippet(file_path, line_num, end_line, 'External', content.strip()[:100], 'External Style (@import)', full_code=content.strip(), source_type='REMOTE'))
            
            end_line = line_num + content.strip().count('\n')
            findings.append(CodeSnippet(file_path, line_num, end_line, 'CSS', content.strip()[:200], 'styleblock', full_code=content.strip(), source_type='INLINE'))

        # 2. Style Attributes
        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                val = tag['style']
                line_num = self._get_line_number(tag, raw_content, val)
                end_line = line_num + str(val).count('\n')
                if '<%' in str(val):
                     findings.append(CodeSnippet(file_path, line_num, end_line, 'CSS', f'style="{val}"', 'ASP.NET Style', full_code=val, source_type='INLINE'))
                else:
                     findings.append(CodeSnippet(file_path, line_num, end_line, 'CSS', f'style="{val}"', 'inlinestyle', full_code=val, source_type='INLINE'))

        # 3. External Stylesheets
        for link in soup.find_all('link'):
            rels = link.get('rel', [])
            if 'stylesheet' in (rels if isinstance(rels, list) else [rels]):
                if link.has_attr('href'):
                    line_num = self._get_line_number(link, raw_content, str(link))
                    end_line = line_num # Single line typically
                    href = link['href']
                    if href.lower().startswith(('http:', 'https:', '//')):
                        findings.append(CodeSnippet(file_path, line_num, end_line, 'External', href, 'External Style', full_code=str(link), source_type='REMOTE'))
                    else:
                        findings.append(CodeSnippet(file_path, line_num, end_line, 'Internal', href, 'Internal Style', full_code=str(link), source_type='LOCAL'))

        return findings

    def _get_line_number(self, tag: bs4.Tag, raw_content: str = "", search_snippet: str = "") -> int:
        # 1. Try BS4 logic
        if tag.sourceline:
            return tag.sourceline
            
        # 2. Fallback: Search in raw content
        # This is a basic search and might pick the first occurrence, but better than 0.
        if raw_content and search_snippet:
            # Try exact match first
            index = raw_content.find(search_snippet)
            if index != -1:
                return raw_content[:index].count('\n') + 1
            
            # Try trimmed snpped (some parsers might normalize whitespace)
            index = raw_content.find(search_snippet.strip())
            if index != -1:
                return raw_content[:index].count('\n') + 1
                
        return 0

    def _detect_ajax(self, code: str) -> bool:
        for keyword in self.ajax_keywords:
            if keyword in code:
                return True
        return False
