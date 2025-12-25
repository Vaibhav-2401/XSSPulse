# XSSProbe

🚀 **XSSProbe** is an advanced Cross-Site Scripting (XSS) detection tool designed for
bug bounty hunters and penetration testers.

It combines fast crawling, multiple payload modes, real-time progress, and
keyboard hotkeys for efficient testing.

---

## ✨ Features

- Katana-powered URL crawling
- Ultra Fast / Fast / Medium / Full scan modes
- Real-time payload progress
- Hotkeys to skip URLs (Ctrl+N / Ctrl+S)
- Reflected XSS detection
- Clean CLI output
- Designed for bug bounty workflows

---

## ⚙️ Installation

```bash
git clone https://github.com/Vaibhav-2401/XSSProbe.git
cd XSSProbe
pip3 install -r requirements.txt

## 🔧 External Dependencies

XSSProbe requires the following external tools:

##**Katana** (by ProjectDiscovery) – used for crawling URLs

### Install Katana

```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
