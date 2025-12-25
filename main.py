#!/usr/bin/env python3

import sys
import subprocess
import shutil
import requests
import urllib3
import termios
import tty
import select
from colorama import Fore, Style, init
from utils import get_params, inject_payload

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# =============================
# Banner
# =============================
def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
██╗  ██╗ ███████╗ ███████╗   ██████╗ ██╗   ██╗ ██╗     ███████╗ ███████╗
╚██╗██╔╝ ██╔════╝ ██╔════╝   ██╔══██╗██║   ██║ ██║     ██╔════╝ ██╔════╝
 ╚███╔╝  ███████╗ ███████╗   ██████╔╝██║   ██║ ██║     █████╗   ███████╗
 ██╔██╗   ════██║ ╚════██║   ██╔═══╝ ██║   ██║ ██║     ██╔══╝   ╚════██║
██╔╝ ██╗ ███████║ ███████║   ██║     ╚██████╔╝ ███████╗███████╗ ███████║
╚═╝  ╚═╝  ══════╝ ╚══════╝   ╚═╝      ╚═════╝  ╚══════╝╚══════╝ ╚══════╝
""")
    print(Fore.YELLOW + Style.BRIGHT + "        Made by Vaibhav Gaikwad")
    print(Fore.WHITE + "        An Advanced XSS Detection Tool")
    print(Fore.CYAN + "-" * 70 + "\n")


# =============================
# Dependency Check
# =============================
def check_katana():
    if not shutil.which("katana"):
        print(Fore.RED + "[-] Katana not found! Please install Katana first.")
        sys.exit(1)


# =============================
# Helpers
# =============================
def normalize_target(t):
    return t if t.startswith("http") else "https://" + t


def run_katana(target):
    print(Fore.CYAN + f"[i] Crawling target with Katana: {target}")
    r = subprocess.run(
        ["katana", "-u", target, "-d", "3", "-silent"],
        capture_output=True,
        text=True
    )
    urls = list(set(r.stdout.splitlines()))
    print(Fore.CYAN + f"[i] Total URLs discovered: {len(urls)}")
    return urls


def filter_param_urls(urls):
    res = [u for u in urls if "?" in u and "=" in u]
    print(Fore.CYAN + f"[i] Parameterized URLs found: {len(res)}")
    return res


# =============================
# Scan Mode
# =============================
def choose_scan_mode():
    print(Fore.YELLOW + "\nSelect scan mode:")
    print("  [1] Ultra Fast (10 payloads)")
    print("  [2] Fast       (100 payloads)")
    print("  [3] Medium     (500 payloads)")
    print("  [4] Full       (All payloads)\n")

    return {"1": "ultra", "2": "fast", "3": "medium", "4": "full"}.get(
        input("Enter choice (1/2/3/4): ").strip(), "medium"
    )


def load_payloads(mode):
    with open("payloads.txt") as f:
        payloads = [p.strip() for p in f if p.strip()]

    limits = {"ultra": 10, "fast": 100, "medium": 500}
    payloads = payloads[:limits.get(mode, len(payloads))]

    print(Fore.CYAN + f"\n[i] Scan mode selected: {mode.upper()}")
    print(Fore.CYAN + f"[i] Payloads loaded: {len(payloads)}\n")

    return payloads


# =============================
# Hotkey Detection
# =============================
def skip_pressed():
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)
        # Ctrl+N (\x0e) or Ctrl+S (\x13)
        if ch in ("\x0e", "\x13"):
            return True
    return False


# =============================
# XSS Scanner
# =============================
def scan_xss(urls, mode):
    payloads = load_payloads(mode)
    total_urls = len(urls)
    total_payloads = len(payloads)

    print(Fore.YELLOW + "Press Ctrl + N (recommended) or Ctrl + S to skip current URL\n")

    for url_index, url in enumerate(urls, start=1):
        params = get_params(url)
        if not params:
            continue

        print(Fore.BLUE + f"[{url_index}/{total_urls}] Testing: {url}")

        skipped = False

        for param in params:
            for payload_index, payload in enumerate(payloads, start=1):

                if skip_pressed():
                    print(Fore.YELLOW + "\n[!] Skipped by user\n")
                    skipped = True
                    break

                sys.stdout.write(f"\r    Payloads: {payload_index}/{total_payloads}")
                sys.stdout.flush()

                try:
                    test = inject_payload(url, param, payload)
                    r = requests.get(
                        test,
                        timeout=8,
                        verify=False,
                        headers={"User-Agent": "XSSPulse"}
                    )

                    if payload in r.text:
                        print("\n" + Fore.GREEN + "[✓] XSS FOUND")
                        print(Fore.WHITE + f"    URL       : {url}")
                        print(Fore.WHITE + f"    Parameter : {param}")
                        print(Fore.WHITE + f"    Payload   : {payload}")
                        print(Fore.WHITE + f"    PoC       : {test}\n")

                except:
                    pass

            if skipped:
                break

        print()


# =============================
# Main
# =============================
if __name__ == "__main__":
    banner()
    check_katana()

    # ---- Terminal setup ----
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    new_settings = termios.tcgetattr(fd)
    # Disable IXON/IXOFF so Ctrl+S doesn't freeze terminal
    new_settings[3] = new_settings[3] & ~termios.IXON & ~termios.IXOFF

    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    tty.setcbreak(fd)

    try:
        targets = []

        if len(sys.argv) == 2 and sys.argv[1] != "-l":
            targets = [sys.argv[1]]

        elif len(sys.argv) == 3 and sys.argv[1] == "-l":
            with open(sys.argv[2]) as f:
                targets = [line.strip() for line in f if line.strip()]

        else:
            print(Fore.YELLOW + "Usage:")
            print("  python3 main.py example.com")
            print("  python3 main.py -l domains.txt")
            sys.exit(1)

        mode = choose_scan_mode()

        for t in targets:
            t = normalize_target(t)
            print(Fore.MAGENTA + f"\n=== Scanning Target: {t} ===\n")
            urls = filter_param_urls(run_katana(t))
            if urls:
                scan_xss(urls, mode)
            else:
                print(Fore.YELLOW + "[!] No parameterized URLs found.")

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
