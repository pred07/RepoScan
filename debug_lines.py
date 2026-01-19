from bs4 import BeautifulSoup

html = """
<html>
<body>
<div style="color:red">Test</div>
<script>console.log('hi')</script>
</body>
</html>
"""

print("--- Testing lxml ---")
try:
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div')
    script = soup.find('script')
    print(f"Div line: {div.sourceline}")
    print(f"Script line: {script.sourceline}")
except Exception as e:
    print(f"lxml failed: {e}")

print("\n--- Testing html.parser ---")
soup2 = BeautifulSoup(html, 'html.parser')
div2 = soup2.find('div')
script2 = soup2.find('script')
print(f"Div line: {div2.sourceline}")
print(f"Script line: {script2.sourceline}")
