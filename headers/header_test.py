import requests
import urllib3
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def retry_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def extract_metadata(response):
    """Extract metadata from the HTML response."""
    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tags = soup.find_all('meta')
    metadata = {}
    for tag in meta_tags:
        if tag.get('name') or tag.get('property'):
            name = tag.get('name') or tag.get('property')
            content = tag.get('content', '')
            metadata[name] = content
    return metadata

def test_security_headers(url):
    print(f"\nTesting Security Headers for: {url}\n")
    
    # Make request
    session = retry_session()
    response = session.get(url, verify=False)
    
    # Headers to check
    security_headers = {
        'Strict-Transport-Security': 'HSTS',
        'Content-Security-Policy': 'CSP',
        'X-Frame-Options': 'Clickjacking Protection',
        'X-Content-Type-Options': 'MIME-type Protection',
        'X-XSS-Protection': 'XSS Protection',
        'Referrer-Policy': 'Referrer Policy',
        'Permissions-Policy': 'Permissions Policy'
    }
    
    # Check each security header
    print("Security Headers Analysis:")
    print("-" * 50)
    
    missing_headers = []
    for header, description in security_headers.items():
        value = response.headers.get(header)
        if value:
            print(f"✅ {description}")
            print(f"   {header}: {value}\n")
        else:
            print(f"❌ {description}")
            print(f"   {header}: Missing!\n")
            missing_headers.append(header)
    
    # Analysis of all headers
    print("Response Headers Analysis:")
    print("-" * 50)
    for header, value in response.headers.items():
        if header not in security_headers:
            print(f"{header}: {value}")
    
    # Metadata extraction
    print("\nMetadata Analysis:")
    print("-" * 50)
    metadata = extract_metadata(response)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    # Additional test results
    if missing_headers:
        print("\nSummary: Missing critical security headers:")
        for header in missing_headers:
            print(f" - {header}")
    else:
        print("\nAll critical security headers are present.")

def concurrent_testing(urls):
    """Perform concurrent testing for a list of URLs."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(test_security_headers, urls)

if __name__ == "__main__":
    start_time = time.time()
    test_urls = [
        "https://localhost:8443",
        "https://example.com",
        "https://google.com",
        "https://github.com",
        "https://yahoo.com",
        "https://www.ucdavis.edu"
    ]
    concurrent_testing(test_urls)
    end_time = time.time()
    print(f"\nTesting completed in {end_time - start_time:.2f} seconds.")
