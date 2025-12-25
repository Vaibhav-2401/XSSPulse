# XSSProbe

🚀 **XSSProbe** is an advanced Cross-Site Scripting (XSS) detection tool built for
bug bounty hunters and penetration testers.

It combines **Katana-powered crawling**, multiple **scan modes**, real-time payload
progress, and **keyboard hotkeys** to make XSS testing faster and more practical
in real-world scenarios.

---

## ✨ Features

- Katana-based URL crawling
- Automatic discovery of parameterized URLs
- Ultra Fast / Fast / Medium / Full scan modes
- Real-time payload execution counter
- Hotkeys to skip URLs during scanning
- Designed for bug bounty & VAPT workflows
- Clean and readable CLI output

---

## ✨ Usage


XSSProbe supports scanning a **single domain** or **multiple domains from a file**.

---

### 🔹 Scan a Single Domain

Use this mode when you want to test one target at a time.

```bash
python3 main.py example.com

```

Use this mode when testing multiple targets in bulk.

```bash
python3 main.py -l domains.txt
````




## 📦 Installation

Clone the repository and install Python dependencies:

```bash
git clone https://github.com/Vaibhav-2401/XSSProbe.git
cd XSSProbe
pip3 install -r requirements.txt

#⚠️ Katana is REQUIRED for XSSProbe to work

#XSSProbe relies on Katana (by ProjectDiscovery) to crawl and collect URLs before testing them for XSS.

#Install Katana
go install github.com/projectdiscovery/katana/cmd/katana@latest
