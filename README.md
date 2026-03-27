# Async Portscanner 🚀

![Version](https://img.shields.io/badge/version-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A high-performance, asynchronous Python port scanner designed for speed and service identification. Unlike traditional scanners, `Async PortScanner` utilizes **Python's Asyncio** to handle thousands of concurrent connections and includes a **Banner Grabbing** engine to identify the software versions running on open ports.

---

## ✨ Features

* **Asynchronous Engine:** Uses `asyncio` for extreme speed without the overhead of heavy threads.
* **Banner Grabbing:** Automatically attempts to identify service versions (e.g., SSH, FTP, Apache).
* **Network Support:** Scan single IPs or entire CIDR networks (e.g., `192.168.1.0/24`).
* **Concurrency Control:** Adjustable semaphore to manage system resources and scan intensity.
* **Clean CLI:** Real-time feedback and formatted output for security assessments.

---

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hawaxgit/Async_Portscanner.git
    
    cd Async_Portscanner
    ```

2.  **Requirements:**
    This script uses the Python Standard Library. Ensure you have **Python 3.7+** installed. No external pip packages are required for the core functionality.

---

## 🛠 Usage

To run a basic scan against a target:

```bash
python Async_Portscanner.py 192.168.1.1

