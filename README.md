# Voltron CLI Tool

A Python tool to manage NG WAF deployments on Fastly services, offering features like provisioning, edge security object management, traffic ramping, and backend synchronization.

## Prerequisites

Before running the script, ensure the following are installed and set up:

- Python 3.x
- `requests` library for Python (Installable via `pip3 install requests`)
- Access credentials for NG WAF and Fastly
- **Cookie file**: A `.voltron_cookie` file containing the `cookie` value from Voltron.

### How to Obtain the Cookie Value for `.voltron_cookie`

To use the tool, you need to create a `.voltron_cookie` file with the full cookie value from Voltron. Here’s how you can do that:

#### 1. Obtain the Cookie Value from Voltron:
1. **Login to the Voltron Dashboard:**
   - Open your browser, navigate to Voltron, and log in.
   
2. **Open the Developer Tools:**
   - Right-click the page, select "Inspect" (or press `F12`), and go to the **Network** tab.
   
3. **Capture a cURL Request:**
   - In the Network tab, perform any action on the Voltron dashboard to trigger a request.
   - Locate a request made to Voltron.
   - Right-click the request and select "Copy as cURL".

4. **Extract the Cookie:**
   - From the copied cURL, find the `-H 'cookie: ...'` section, and copy the entire cookie string.

#### 2. Create a `.voltron_cookie` File:
- In your project directory, create a `.voltron_cookie` file that includes the cookie string.

- The content of the `.voltron_cookie` file will look something like this:

```bash
_ga=GA1.2.184163117.1724087216; _gid=GA1.2.1553403690.1725903286; goth-session=MTcyNTk...
```

### Cookie Expiration Check and Update

The script automatically checks if the `.voltron_cookie` file is out of date (older than one day). If it is, you will be prompted to enter a new cookie value.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/fastly/ngwafcli.git
   cd ngwafcli
   ```

2. **Install Dependencies:**
   ```bash
   pip3 install requests parsel
   ```

## Usage

The script can be executed using command-line arguments to manage corp groups.

### Command-Line Arguments

Execute the script with parameters:

```bash
python3 voltron.py --corp 'your_corp_name' --action 'add' --groups 'group1' 'group2'
```

#### Example:

```bash
python3 voltron.py --corp 'ExampleCorp' --action 'add' --groups 'sigsci-edge-dynamic-backends' 'rate-limiting'
```

### CSV Input

The script supports batch processing with multiple sites from a CSV file. Ensure the CSV contains columns for `site_name` and `fastly_sid`.

#### Example CSV Format:

```csv
site_name,fastly_sid
site1,serviceID1
site2,serviceID2
```

To use a CSV file:
```bash
python3 voltron.py --csv_file 'path/to/sites.csv'
```

## Features

### 1. Cookie Management
- Automatically prompts the user for a new cookie if the `.voltron_cookie` file is older than 1 day.

### 2. Corp Management
- Add a corp to specified groups such as `sigsci-edge-dynamic-backends` or `rate-limiting`.

## Contributions

Contributions are welcome! Fork the repository and submit pull requests.

## Contact

Sina Siar - [@ssiar](https://linkedin.com/in/ssiar) - ssiar@fastly.com
