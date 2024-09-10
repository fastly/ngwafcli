# NGWAF CLI Tool

A Python tool to manage NG WAF deployments on Fastly services, offering features like provisioning, edge security object management, traffic ramping, and backend synchronization.

## Prerequisites

Before running the script, ensure the following are installed and set up:

- Python 3.x
- `requests` library for Python (Installable via `pip3 install requests`)
- Access credentials for NG WAF and Fastly
- **For `--dynamic-backend` or `--premier` flags:** A `.env` file containing the `cookie` value from Voltron

### How to Obtain the Cookie Value for `--dynamic-backend` and `--premier`

Thank you for the clarification! Here's the updated instruction for saving the `.env` file with the correct format:

To use the `--dynamic-backend` or `--premier` flags, you need to create a `.env` file with the full cookie value from Voltron. Here’s how you can do that:

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

#### 2. Create a `.env` File:
- In your project directory, create a `.env` file that includes the cookie string.
  
- The content of the `.env` file will look something like this:

```bash
'_ga=GA1.2.184163117.1724087216; _gid=GA1.2.1553403690.1725903286; _ga_58L9ZE63Z0=GS1.2.1725903286.23.0.1725903286.0.0.0; _DUO_APER_LOCAL_=7569fe783c8d8a108c935eb1b48bdb713a54cd9983746e9cdb2fe3f5125a8d2e; goth-session=MTcyNTk5MDEwM3xEWDhFQVFMX2dBQUJFQUVRQUFELUFucl9nQUFIQm5OMGNtbHVad3dLQUFoT2FXTnJUbUZ0WlFaemRISnBibWNNRWdBUWMzTnBZWEpBWm1GemRHeDVMbU52YlFaemRISnBibWNNQ3dBSlFYWmhkR0Z5VlZKTUJuTjBjbWx1Wnd3Q0FBQUdjM1J5YVc1bkRBMEFDMssFJsYzJOeWFYQjBhVzl1Qm5OMGNtbHVad3dkQUJ0N0ltZGxibVJsY2lJNklpSXNJbUpwY25Sb1pHRjVJam9pSW4wR2MzUnlhVzVuREFnQUJsVnpaWEpKUkFaemRISnBibWNNRmdBVU1EQjFNV1ZuT0hjM1luSldlRXhRWVRJeFpEZ0djM1J5YVc1bkRBNEFER2R2ZEdndGMyVnpjMmx2YmdaemRISnBibWNNX2dGTkFQNEJTWHNpUVhWMGFGVlNUQ0k2SW1oMGRIQnpPaTh2Wm1GemRHeDVMbTlyZEdFdVkyOXRMMjloZFhSb01pOTJNUzloZFhSb2IzSnBlbVVfWTJ4cFpXNTBYMmxrUFRCdllURnBNMlZpYjJkdFVuQlBZVVp3TVdRNFhIVXdNREkyY21Wa2FYSmxZM1JmZFhKcFBXaDBkSEJ6SlROQkpUSkdKVEpHWjJGeWJHbGpMbUpsWldaaGJHOHVjMmxuYzJOcExtNWxkQ1V5Um1GMWRHZ2xNa1p2YTNSaEpUSkdZMkZzYkdKaFkydGNkVEF3TWpaeVpYTndiMjV6WlY5MGVYQmxQV052WkdWY2RUQXdNalp6WTI5d1pUMXZjR1Z1YVdRcmIyWm1iR2x1WlY5aFkyTmxjM01yY0hKdlptbHNaU3RsYldGcGJGeDFNREF5Tm5OMFlYUmxQWE4wWVhSbElpd2lRV05qWlhOelZHOXJaVzRpT2lJaUxDSlNaV1p5WlhOb1ZHOXJaVzRpT2lJaUxDSkZlSEJwY21WelFYUWlPaUl3TURBeExUQXhMVEF4VkRBd09qQXdPakF3V2lKOUJuTjBjbWx1Wnd3R0FBUk9ZVzFsQm5OMGNtbHVad3dMQUFsVGFXNWhJRk5wWVhJR2MzUnlhVzVuREFjQUJVVnRZV2xzQm5OMGNtbHVad3dTQUJCemMybGhja0JtWVhOMGJIa3VZMjl0fGJyxzeBzp0V-3X0T5OHUvSfIf3wKvdQ2ai15SfYL4KR; AWSALB=zbBnqpt5ECV7EoXSvTTJ39nuBGMlXHk6wFLg7XMpFA4dUU7kw/NgtWTDP8i6oeQrBOEjWZdHgK04qohkl+GAaz1ogOrCmqDyIXIfFqZb7nvaSU6rUuU4vFSSXexN'
```
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

- **Retry Mechanism:** Automatically retries API calls up to three times with a waiting period for transient network or server errors.
- **Enhanced Error Messages:** Informative error messages, especially for HTTP 401 Unauthorized and "failed to clone service" issues.

### Edge Security Object Management

- **Automatic Creation:** The script creates an edge security object if a site doesn’t exist on NG WAF.
- **Mapping to Fastly Service:** Optionally activate the Fastly service version immediately and control traffic routed through NG WAF.

### **New Flags:**
- **`--dynamic-backend`:** Adds the corp to the `sigsci-edge-dynamic-backends` group before mapping the site to Fastly services.
- **`--premier`:** Adds the corp to the `rate-limiting` group for premier customers.

### Synchronizing Origins with Fastly Backend

- **`--sync-backend`:** Synchronizes origins with Fastly after changes, preventing 503 Unknown Wasm backend errors.
- **CSV Input:** Use a CSV file for batch operations.

### Mutually Exclusive Flags for Operations

Enforces the mutually exclusive `--provision` and `--sync-backend` flags to prevent simultaneous operations.

## Using `setup_env.zsh` to Update Local Environment Variables

Use `setup_env.zsh` to set up environment variables.

1. **Make the script executable:**
   ```bash
   chmod +x setup-env.zsh
   ```

2. **Run the script:**
   ```bash
   source setup_env.zsh --update-file
   ```

## CSV File Input

The script processes multiple sites from a CSV file. The CSV should contain two columns: `site_name` and `fastly_sid`.

### CSV Format

```csv
site_name,fastly_sid
site1,serviceID1
site2,serviceID2
```

### Using the CSV File

To provision sites or synchronize origins, pass the CSV file path as a command-line argument:

```bash
python3 ngwafcli.py --ngwaf_user_email 'your_ngwaf_user_email' --ngwaf_token 'your_ngwaf_token' --fastly_token 'your_fastly_token' --corp_name 'your_corp_name' --csv_file 'path/to/sites.csv' --activate true --percent_enabled 100
```

For backend synchronization:
```bash
python3 ngwafcli.py --sync-backend --csv_file 'path/to/sites.csv'
```

## Usage

The script can be executed using command-line arguments or environment variables.

### Using Command-Line Arguments

Execute the script with parameters:

```bash
python3 ngwafcli.py --ngwaf_user_email 'your_ngwaf_user_email' --ngwaf_token 'your_ngwaf_token' --fastly_token 'your_fastly_token' --corp_name 'your_corp_name' --site_name 'your_site_name' --fastly_sid 'your_fastly_service_id' [--activate] [--percent_enabled <0-100>]
```

### Using `--dynamic-backend` and `--premier` Flags

- To add the corp to the `sigsci-edge-dynamic-backends` group:
  ```bash
  python3 ngwafcli.py --provision --csv_file 'path/to/sites.csv' --dynamic-backend
  ```

- To add the corp to the `rate-limiting` group for premier customers:
  ```bash
  python3 ngwafcli.py --provision --csv_file 'path/to/sites.csv' --premier
  ```

### Using Environment Variables

Set the following environment variables, then run the script:

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

Then execute the script:
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
