# District-9 Personal Assistant

## Requirements

- **Python**: 3.13.7
- **pip**: 25.2

## Setup

### Create and activate virtual environment

```bash
# Create venv (run once)
python3 -m venv venv
```

#### Activate venv

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (cmd):**
  ```cmd
  venv\Scripts\activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

## Running Commands

You can run each command separately as shown below.

### Install dependencies

- **macOS/Linux:**
  ```bash
  make install
  ```
- **Windows (no Make):**
  ```cmd
  pip3 install -r requirements.txt
  ```

### Run tests

- **macOS/Linux:**
  ```bash
  make test
  ```
- **Windows (no Make):**
  ```cmd
  python3 -m unittest discover -s tests
  ```

### Lint code

- **macOS/Linux:**
  ```bash
  make pylint
  ```
- **Windows (no Make):**
  ```cmd
  pylint .
  ```

### Fix code formatting

- **macOS/Linux:**
  ```bash
  make fix_formatting
  ```
- **Windows (no Make):**
  ```cmd
  black .
  ```

### Run the application

- **macOS/Linux:**
  ```bash
  make run
  ```
- **Windows (no Make):**
  ```cmd
  python3 main.py
  ```

