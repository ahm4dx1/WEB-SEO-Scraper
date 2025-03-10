import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin, urlparse
import tldextract
import json
import os

# List of common social media domains
SOCIAL_MEDIA = ["linkedin.com", "facebook.com", "twitter.com"]

# Fetch available SEO analysis sections
response = requests.get('https://fes-analysis.ssc-app-services.com/report/sections?fields=key,title,description,relevance')
results = json.loads(response.text)

all_results = []
for r in results.values():
    all_results.extend(r)
tests = [res['key'] for res in all_results]

# Additional SEO tests
additional_tests = [
    'title-tag', 'description-tag', 'google-preview', 'social-media-meta-tags', 'common-keywords', 'common-keywords-usage',
    'keywords-cloud', 'headings-tags', 'robots.txt', 'sitemap', 'url-seo-friendly', 'img-alt', 'image-size',
    'image-aspect-ratio', 'inline-css', 'deprecated-tags', 'google-anlytics', 'favicon', 'js-errors', 'console-errors',
    'meta-charset', 'social-media', 'html-size', 'dom-size', 'html-compressed', 'loading-speed', 'js-execution-time',
    'page-objects', 'page-cache', 'flash', 'cdn-usage', 'next-gen-image-format', 'img-metadata', 'image-caching',
    'js-caching', 'css-caching', 'js-minification', 'css-minification', 'render-blocking-resources', 'nested-tables',
    'frameset', 'doctype', 'http-redirects', 'web-vitals-ttfb', 'web-vitals-fcp', 'web-vitals-lcp', 'web-vitals-cls',
    'url-canonicalization', 'https-encryption', 'mixed-content-type', 'http2', 'hsts', 'safe-browsing', 'server-signature',
    'directory-browsing', 'plaintext-emails', 'cross-origin-links', 'viewport', 'media-queries', 'mobile-snapshot',
    'structured-data', 'custom-404', 'noindex-tags', 'canoical-tags', 'nofollow-tags', 'disallow-tags', 'meta-refresh',
    'spf-record', 'ads.txt'
]

tests.extend(additional_tests)
tests = list(set(tests))  # Remove duplicates

# Read URLs from file
with open("websites.txt", "r") as file:
    urls = file.readlines()

# Function to scrape contact & social media links
def get_info(url):
    url = url.strip()
    if "https" not in url:
        url = f"https://{url}"
    print(f"Fetching data from: {url}")

    headers = {'User-Agent': UserAgent().random}
    
    try:
        response = requests.get(url, headers=headers)
    except:
        print(f"Error navigating to: {url}. Skipping...")
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    all_a_tags = soup.find_all("a")

    all_urls = {'emails': [], 'phones': [], 'socials': [], 'others': []}
    domain = tldextract.extract(url).domain

    for tag in all_a_tags:
        href = tag.get('href')
        if href is None:
            continue
        if href.startswith("mailto:"):
            all_urls['emails'].append(href.replace("mailto:", ""))
        elif href.startswith("telto:"):
            all_urls['phones'].append(href.replace("telto:", ""))
        elif any(s in href.lower() for s in SOCIAL_MEDIA):
            all_urls['socials'].append(href)
        else:
            if "https" not in href and domain not in href:
                href = urljoin(url, href)
            all_urls['others'].append(href)

    return all_urls

# Function to fetch SEO data
def get_seo_info(url):
    if "https" not in url:
        url = f"https://{url}"

    json_data = {
        'url': url,
        'sections': [],
        'source': 'public_ssc',
    }

    domain = tldextract.extract(url).domain

    response = requests.post('https://fes-analysis.ssc-app-services.com/report', json=json_data)
    json_response = json.loads(response.text)

    try:
        guid = json_response['guid']
    except:
        print(f"Error fetching SEO data for: {url}")
        return None

    print(f"SEO Report GUID: {guid}")

    # Create directory for the website
    if domain not in os.listdir():
        os.mkdir(domain)

    for test in tests:
        seo_response = requests.get(f'https://fes-analysis.ssc-app-services.com/report/{guid}/{test}')
        seo_data = json.loads(seo_response.text)

        with open(f"{domain}/seo_data.json", "a", encoding='utf-8') as file:
            json.dump(seo_data, file, indent=4, ensure_ascii=False)

# Main execution loop
data_urls = []
for url in urls[:5]:  # Limit to first 5 URLs for testing
    domain = tldextract.extract(url).domain
    data = get_info(url)
    
    if data is None:
        continue
    
    data_urls.append(url)
    
    if domain not in os.listdir():
        os.mkdir(domain)

    with open(f"{domain}/site_urls.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Fetch SEO data
for url in data_urls:
    get_seo_info(url)

print("Scraping Completed.")

