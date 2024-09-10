# NGWAF CLI Tool

A Python tool to manage NG WAF deployments on Fastly services, offering features like provisioning, edge security object management, traffic ramping, and backend synchronization.

## Prerequisites

Before running the script, ensure the following are installed and set up:

- Python 3.x
- `requests` library for Python (Installable via `pip3 install requests`)
- Access credentials for NG WAF and Fastly

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/fastly/ngwafcli.git
   cd ngwafcli
   ```

2. **Install Dependencies:**
   ```bash
   pip3 install requests
   ```

## New Features and Improvements

### Advanced Error Handling and Retry Logic

- **Retry Mechanism:** The script now includes a retry mechanism for API calls, automatically retrying up to three times with a waiting period for transient network or server errors.
- **Enhanced Error Messages:** More informative error messages are provided, especially for HTTP 401 Unauthorized errors and specific issues like failing to clone a service on Fastly.

### Edge Security Object Management

- **Automatic Creation:** If a site does not exist on NG WAF, the script now automatically creates an edge security object for it.
- **Mapping to Fastly Service:** Sites can be mapped to Fastly services with options to activate the Fastly service version immediately and to specify the percentage of traffic to be routed through the NG WAF.

### Flexible Deployment Options

- **Activate Version Option:** Control whether the Fastly service version is activated immediately using the `--activate` flag.
- **Traffic Ramping:** Control the percentage of traffic routed through the NG WAF using the `--percent_enabled` argument.

### **New Flags:**
- **`--dynamic-backend`:** Adds the corp to the `sigsci-edge-dynamic-backends` group before mapping the site to Fastly services.
- **`--premier`:** Adds the corp to the `rate-limiting` group before mapping the site to Fastly services.

### Synchronizing Origins with Fastly Backend

- **`--sync-backend` Flag:** Synchronize origins with Fastly after changes, preventing 503 Unknown Wasm backend errors.
- **CSV File Input for Synchronization:** The `--sync-backend` flag works with a CSV file to synchronize multiple sites.

### Mutually Exclusive Flags for Operations

The script enforces mutually exclusive flags `--provision` and `--sync-backend`, ensuring only one operation runs at a time.

## Using `setup_env.zsh` to Update Local Terminal Environment

A script called `setup_env.zsh` helps set up the necessary environment variables in your terminal session.

### Running the `setup_env.zsh` Script

1. **Make the script executable:**
   ```bash
   chmod +x setup-env.zsh
   ```

2. **Run the script:**
   ```bash
   source setup_env.zsh --update-file
   ```

The script will prompt you to enter values for `CORP_NAME`, `NGWAF_TOKEN`, and `FASTLY_TOKEN`.

3. **Reload the terminal environment:**
   After running the script, reload your `.zshrc`:
   ```bash
   source ~/.zshrc
   ```

## CSV File Input

The script processes multiple sites from a CSV file. The CSV should contain two columns: `site_name` and `fastly_sid`.

### Format of the CSV File

```csv
site_name,fastly_sid
site1,serviceID1
site2,serviceID2
```

### Using the CSV File

To provision sites or synchronize origins, provide the CSV file path as a command-line argument:

```bash
python3 ngwafcli.py --ngwaf_user_email 'your_ngwaf_user_email' --ngwaf_token 'your_ngwaf_token' --fastly_token 'your_fastly_token' --corp_name 'your_corp_name' --csv_file 'path/to/sites.csv' --activate true --percent_enabled 100
```

For backend synchronization:
```bash
python3 ngwafcli.py --sync-backend --csv_file 'path/to/sites.csv'
```

## Usage

The script can be executed via command-line arguments or environment variables.

### Command-Line Arguments

Execute the script by passing the required parameters:
```bash
python3 ngwafcli.py --ngwaf_user_email 'your_ngwaf_user_email' --ngwaf_token 'your_ngwaf_token' --fastly_token 'your_fastly_token' --corp_name 'your_corp_name' --site_name 'your_site_name' --fastly_sid 'your_fastly_service_id' [--activate] [--percent_enabled <0-100>]
```

### New Dynamic Backend and Premier Flags

- To add the corp to the `sigsci-edge-dynamic-backends` group:
  ```bash
  python3 ngwafcli.py --provision --csv_file 'path/to/sites.csv' --dynamic-backend
  ```

- To add the corp to the `rate-limiting` group for premier customers:
  ```bash
  python3 ngwafcli.py --provision --csv_file 'path/to/sites.csv' --premier
  ```

### Environment Variables

Set the following environment variables and run the script without additional parameters:

```bash
export NGWAF_USER_EMAIL='your_ngwaf_user_email'
export NGWAF_TOKEN='your_ngwaf_token'
export FASTLY_TOKEN='your_fastly_token'
export CORP_NAME='your_corp_name'
export SITE_NAME='your_site_name' # Required if not using CSV
export FASTLY_SID='your_fastly_service_id' # Required if not using CSV
export ACTIVATE='true' # Optional
export PERCENT_ENABLED='10' # Optional
```

Then, execute the script:
```bash
python3 ngwafcli.py
```

## Example Scenarios

- **Deploying with Partial Traffic Ramping:**
  ```bash
  python3 ngwafcli.py --ngwaf_user_email 'user@example.com' --ngwaf_token 'token123' --fastly_token 'fastlykey123' --corp_name 'MyCorp' --site_name 'MySite' --fastly_sid 'serviceID' --activate --percent_enabled 25
  ```

- **Deploying without Activating the Fastly Service:**
  ```bash
  python3 ngwafcli.py --ngwaf_user_email 'user@example.com' --ngwaf_token 'token123' --fastly_token 'fastlykey123' --corp_name 'MyCorp' --site_name 'MySite' --fastly_sid 'serviceID'
  ```

- **Synchronizing Origins for Multiple Sites:**
  ```bash
  python3 ngwafcli.py --sync-backend --csv_file 'path/to/sites.csv'
  ```

---

## Contributions

Contributions are welcome! Fork the repository and submit pull requests.

## Contact

Sina Siar - [@ssiar](https://linkedin.com/in/ssiar) - ssiar@fastly.com
