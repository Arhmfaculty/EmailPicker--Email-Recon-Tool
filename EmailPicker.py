import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.parse
import concurrent.futures
from fake_useragent import UserAgent
import argparse

# Constants
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
SEARCH_ENGINES = [
    "https://www.google.com/search?q=%40{}&num=100",
    "https://www.bing.com/search?q=%40{}&count=50",
    "https://duckduckgo.com/html/?q=%40{}",
    "https://www.linkedin.com/profile?q=%40{}"
    
]
CRT_SH_URL = "https://crt.sh/?q=%25.{}&output=json"
PROXY_LIST_URL = "https://free-proxy-list.net/"

# Initialize UserAgent
ua = UserAgent()
PROXIES = []


def fetch_proxies():
    """Fetches free proxies from free-proxy-list.net"""
    global PROXIES
    try:
        response = requests.get(PROXY_LIST_URL, headers={"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, 'html.parser')
        proxy_table = soup.find("table", class_="table")
        if proxy_table:
            for row in proxy_table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2 and cols[6].text.strip() == "yes":  # HTTPS proxies only
                    proxy = f"http://{cols[0].text.strip()}:{cols[1].text.strip()}"
                    PROXIES.append(proxy)
    except Exception as e:
        print(f"[!] Failed to fetch proxies: {e}")


def fetch_url(url, retries=3, timeout=15):
    """Fetch URL content with retries and proxy rotation."""
    headers = {"User-Agent": ua.random}
    for attempt in range(retries):
        try:
            proxy = PROXIES[attempt % len(PROXIES)] if PROXIES else None
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(2)
    return None


def extract_emails(text, domain):
    emails = set(re.findall(EMAIL_REGEX, text))
    return {email for email in emails if email.lower().endswith(domain.lower())}


def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if "url?q=" in href:
            href = href.split("url?q=")[1].split("&")[0]
        if href.startswith("http"):
            links.add(href)
    return links


def fetch_crtsh_emails(domain):
    response = fetch_url(CRT_SH_URL.format(domain))
    if response:
        return extract_emails(response, domain)
    return set()


def search_emails(domain, max_workers=10):
    emails = set()
    visited_urls = set()

    def process_url(url, domain):
        if url in visited_urls:
            return set()
        visited_urls.add(url)
        html = fetch_url(url)
        if not html:
            return set()
        return extract_emails(html, domain)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_url, engine.format(urllib.parse.quote(domain)), domain): engine
            for engine in SEARCH_ENGINES
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                emails.update(future.result())
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")

    emails.update(fetch_crtsh_emails(domain))
    return emails


def main():
    # Customizing help output for -h option
    def custom_help():
        tool_name = "\033[1;34m*EmailPicker*\033[0m"
        print(f"\n{tool_name}")
        print("Enhanced Email Harvester - Gathers emails from multiple sources.\n")
        print("Usage: python email_harvester.py -d <domain> [options]")
        print("\nOptions:")
        print("  -d, --domain    Domain to search for emails (e.g., example.com)")
        print("  -o, --output    Output file to save results (e.g., emails.txt)")
        print("  -t, --threads   Number of threads to use (default: 10)")
        print("  -p, --proxies   Enable proxy rotation")
        print("\nExample:")
        print("  python EmailPicker.py -d example.com -o emails.txt -t 20")
        print("\nFor more details, refer to the documentation or the script's README.\n")

    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="Enhanced Email Harvester - Gathers emails from multiple sources.",
        epilog="Example: python EmailPicker.py -d example.com -o emails.txt -t 20"
    )
    parser.add_argument("-d", "--domain", required=True, help="Domain to search for emails (e.g., example.com)")
    parser.add_argument("-o", "--output", help="Output file to save results (e.g., emails.txt)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    parser.add_argument("-p", "--proxies", action="store_true", help="Enable proxy rotation")

    args = parser.parse_args()

    # Check if the help flag is set and display custom help message
    if args.__dict__.get('help', False):
        custom_help()
        return

    if args.proxies:
        print("[*] Fetching proxies...")
        fetch_proxies()
        print(f"[*] {len(PROXIES)} proxies loaded.")

    print(f"[*] Starting reconnaissance for domain: {args.domain}")
    found_emails = search_emails(args.domain, max_workers=args.threads)

    if found_emails:
        print("\n[+] Emails found:")
        for email in found_emails:
            print(email)
        if args.output:
            with open(args.output, "w") as f:
                f.write("\n".join(found_emails))
            print(f"\n[*] Results saved to {args.output}")
    else:
        print("\n[-] No emails found.")



if __name__ == "__main__":
    main()
