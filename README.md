# **LfiDump - Local File Inclusion (LFI) Vulnerability Scanner**

**LfiDump** is a Python-based Local File Inclusion (LFI) vulnerability scanner that helps security professionals detect potential LFI vulnerabilities in web applications. This tool uses a set of predefined payloads to manipulate URLs and checks for vulnerable file inclusion points that could potentially be exploited. The scanner uses multithreading for efficient scanning of multiple URLs simultaneously and provides a detailed output of the results.

---

## **Features**
- **LFI Vulnerability Testing**: Detects LFI vulnerabilities by injecting payloads into URL parameters.
- **Multithreading Support**: Fast testing of multiple URLs in parallel with adjustable thread count.
- **Payloads from JSON File**: Easily load custom payloads from a JSON file to target specific vulnerabilities.
- **Results Logging**: Detected vulnerabilities are saved in `LFi.txt`, while errors are logged in `errors.log`.
- **Customizable URL Testing**: Choose between using a single URL or a list of URLs to scan.

---

## **Installation**

### **1. Clone the repository**

To get started with LfiDump, clone the repository to your local machine:

```bash
git clone https://github.com/HackfutSec/LfiDump.git
cd LfiDump
```

### **2. Install Dependencies**

Make sure you have Python 3.x installed. You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### **3. Prepare Payloads File**

Before running the script, make sure you have a valid `payloads.json` file. This file contains the payloads that will be used for testing LFI vulnerabilities.

Example of `payloads.json` format:

```json
[
  "../etc/passwd",
  "/proc/self/environ",
  "/var/log/apache2/access.log"
]
```

---

## **Usage**

### **1. Running the Script**

After cloning the repository and installing dependencies, run the `lfi.py` script:

```bash
python lfi.py
```

### **2. Configuration Options**

The script will prompt you to choose several options during execution:

1. **Select URL Input Type**:
   - **Option 1**: Enter a single URL.
   - **Option 2**: Provide a file containing a list of URLs (one URL per line).
   
2. **Choose URL Option**:
   - **Option 1**: Keep the original URL structure.
   - **Option 2**: Replace the URL with `?file=`.

3. **Set Number of Threads**:
   - Set the number of threads to run concurrently (default is 10).

### **3. Example Input**

```bash
[✘] Do you want to test:
    (1) Single URL
    (2) List of URLs
[<<] Choose (1/2): 1
[✘] Enter the single URL to test: http://example.com/page?id=1
[✓] Choose option:
    1: Keep URL
    2: Replace with ?file=
[<<] Your choice: 1
[✓] Number of Threads (default 10): 10
```

---

## **Output**

1. **LFi.txt**: This file contains the URLs that are vulnerable to LFI.
2. **errors.log**: This file logs any errors that occurred during the requests.

Example of a vulnerable URL:

```bash
[>>] http://example.com/page?id=../../../../etc/passwd --> [Vuln]
```

Example of a non-vulnerable URL:

```bash
[x] http://example.com/page?id=1 --> [Not Vuln]
```

---

## **Example**

Let's test the following URLs from a list:

```bash
python lfi.py
```

- **URLs File**: `urls.txt` containing a list of URLs:
  
```txt
http://example.com/page?id=1
http://example.com/page?id=2
http://example.com/page?id=3
```

The tool will automatically test all URLs with the configured payloads and display results in the terminal.

---

## **Disclaimer**

**LfiDump** is intended for ethical hacking and security testing only. Ensure you have explicit permission to test the websites or applications you're scanning. Unauthorized access to computer systems is illegal and unethical.

---

## **Contributing**

We welcome contributions to **LfiDump**. If you find any bugs or have suggestions for new features, feel free to open an issue or submit a pull request.

---

## **License**

**LfiDump** is open-source software licensed under the **MIT License**.

---

## **Contact**

For any questions or assistance, feel free to reach out to us:

- **Telegram**: [@HackfutSec](https://t.me/HackfutSec)
- **GitHub**: [https://github.com/HackfutSec/LfiDump](https://github.com/HackfutSec/LfiDump)

---

## **Support Us**

If you find this tool useful, consider starring the repository and sharing it with others in the security community. Thank you!
