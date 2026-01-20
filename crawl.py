"""
AJAX Crawler & Correlator Utility
Entry point for crawling a target app and correlating with static analysis.
"""
import argparse
import sys
import os
import shutil

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.crawler import config
from src.crawler.crawler import Crawler
from src.crawler.fetcher import Fetcher
from src.crawler.detector import DynamicDetector
from src.crawler.comparer import Comparer
from src.crawler.tracker import CorrelationTracker

def main():
    parser = argparse.ArgumentParser(description="AJAX Crawler & Correlator")
    parser.add_argument("--url", required=True, help="Target URL to crawl (e.g., http://localhost:8080)")
    parser.add_argument("--scan-report", required=True, help="Path to static RepoScan Excel report (InlineCode_Scan_*.xlsx)")
    parser.add_argument("--output", default="output", help="Output folder")
    parser.add_argument("--cookies", help="Auth cookies (key=value;key2=val2)")
    
    args = parser.parse_args()
    
    # 1. Setup
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        
    print(f"=== Starting AJAX Crawler ===")
    print(f"Target: {args.url}")
    print(f"Static Report: {args.scan_report}")
    
    # Parse cookies
    cookies = {}
    if args.cookies:
        for pair in args.cookies.split(';'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                cookies[k.strip()] = v.strip()
    
    # 2. Crawl
    crawler = Crawler(args.url, cookies=cookies)
    crawler.crawl()
    assets = crawler.get_assets()
    print(f"\nDiscovered {len(assets)} assets to scan.")
    
    # 3. Fetch
    fetcher = Fetcher(session=crawler.session) # Reuse session for auth/cookies
    fetched_content = fetcher.fetch_assets(assets)
    
    # 4. Detect
    print("\nAnalyzing fetched assets for AJAX...")
    detector = DynamicDetector()
    dynamic_findings = detector.detect(fetched_content)
    
    # 5. Correlate
    print("\nCorrelating with static analysis...")
    comparer = Comparer(args.scan_report)
    matches, new_findings, missing = comparer.correlate(dynamic_findings)
    
    # 6. Report
    output_file = os.path.join(args.output, "AJAX_Correlation.xlsx")
    external_assets = crawler.get_external_assets()
    tracker = CorrelationTracker()
    tracker.generate_report(matches, new_findings, missing, external_assets, output_file)
    
    print("\n=== Process Complete ===")
    print(f"Stats: {len(matches)} Verified, {len(new_findings)} New, {len(missing)} Missing")
    print(f"External Resources Found: {len(external_assets)}")
    print(f"Report: {output_file}")

if __name__ == "__main__":
    main()
