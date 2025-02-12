# EmailPicker

## Overview
EmailPicker is a powerful and efficient email reconnaissance tool designed to harvest emails from multiple sources on the internet. It leverages search engine results, public certificate transparency logs, and proxy rotation to gather valid email addresses associated with a target domain.

This tool is ideal for security researchers, penetration testers, and OSINT (Open-Source Intelligence) professionals looking to conduct reconnaissance efficiently.

## Features
- **Multi-Source Email Collection:** Uses Google, Bing, DuckDuckGo, LinkedIn, and crt.sh.
- **Proxy Support:** Enables the use of free proxies for anonymous searches.
- **Threading for Speed:** Supports multi-threading for faster email extraction.
- **Custom Output:** Saves results to a file for further analysis.
- **Error Handling & Retry Mechanism:** Ensures stable execution even with failed requests.

## Prerequisites
Before using EmailPicker, ensure you have the following installed:

- Python 3.x


## Installation
Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Arhmfaculty/EmailPicker.git
cd EmailPicker
```

## Usage
To see the available options and usage instructions, run:

```bash
python EmailPicker.py -h
```

### Basic Usage
To search for emails associated with a specific domain:

```bash
python EmailPicker.py -d example.com
```

### Save Output to a File
To store the results in a text file:

```bash
python EmailPicker.py -d example.com -o emails.txt
```

### Increase Threading for Faster Searches
To adjust the number of concurrent search threads (default is 10):

```bash
python EmailPicker.py -d example.com -t 20
```

### Enable Proxy Rotation
To fetch and use proxies for anonymous searches:

```bash
python EmailPicker.py -d example.com -p
```

## How It Works
1. **Fetches URLs** from major search engines using domain-based queries.
2. **Extracts Emails** from search result pages and linked web pages.
3. **Fetches Public Certificates** from crt.sh for additional email addresses.
4. **Uses Proxies (Optional)** to avoid IP bans while scraping search engines.
5. **Applies Regex Filtering** to extract only domain-specific emails.
6. **Multithreading** is used to speed up the search and extraction process.

## Example Output
```
[*] Starting reconnaissance for domain: example.com
[+] Emails found:
admin@example.com
contact@example.com
support@example.com
[*] Results saved to emails.txt
```

## Troubleshooting
- If you receive **429 errors** from Google, try using the `-p` flag to enable proxies.
- If email results seem low, increase the thread count using `-t`.
- Ensure that Python and dependencies are correctly installed.

## Legal Disclaimer
This tool is intended for educational and security research purposes only. **Unauthorized use of this tool against websites or individuals without consent may violate laws and ethical guidelines.** The author is not responsible for any misuse of this tool.

## Contribution
Contributions are welcome! Feel free to submit issues and pull requests on GitHub.



---
**Author:** Maxwell Bosiako Antwi 
**GitHub:** [Maxwell B. Antwi](https://github.com/Arhmfaculty)  

