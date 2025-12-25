# XSSPulse

🚀 **XSSPulse** is an advanced Cross-Site Scripting (XSS) detection tool built for
bug bounty hunters and penetration testers.

It uses **Katana (ProjectDiscovery)** for crawling, supports multiple scan modes,
shows real-time payload progress, and provides keyboard hotkeys for faster
real-world XSS testing.

---

## ✨ Features

- Katana-powered URL crawling
- Automatic discovery of parameterized URLs
- Ultra Fast / Fast / Medium / Full scan modes
- Real-time payload execution counter
- Hotkeys to skip URLs during scanning
- Designed for bug bounty & VAPT workflows
- Clean and readable CLI output

---

## 📦 Installation

```bash
git clone https://github.com/Vaibhav-2401/XSSPulse.git
cd XSSPulse
pip3 install -r requirements.txt


## 🔧 External Dependencies

XSSProbe requires the following external tools:

- **Katana** (by ProjectDiscovery) – used for crawling URLs

### Install Katana

```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
