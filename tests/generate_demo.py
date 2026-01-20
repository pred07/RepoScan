import subprocess
import time
import sys
import glob
import os

def run_demo():
    print("=== Starting Demo Generation ===")
    
    # 1. Start HTTP Server
    print("[1/3] Starting Local Server...")
    server = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        time.sleep(2)
        
        # 2. Preparation
        output_dir = "output_demo_latest"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        static_report = glob.glob('output_demo/InlineCode_Scan_*.xlsx')[0]
        
        # 3. Running Utility
        print(f"[2/3] Running Crawler Utility against {static_report}...")
        cmd = [
            sys.executable, "crawl.py",
            "--url", "http://localhost:8080/ajax_demo.html",
            "--scan-report", static_report,
            "--output", output_dir
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"[3/3] ✅ Success! Report generated at: {os.path.abspath(output_dir)}\AJAX_Correlation_Report.xlsx")
        else:
            print("❌ Error during crawl:")
            print(result.stderr)
            
    finally:
        server.kill()

if __name__ == "__main__":
    run_demo()
