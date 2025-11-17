# District-9 Personal Assistant

_A command-line personal assistant for managing contacts, addresses, phones, emails, notes, and birthdays. 
The assistant provides interactive flows for adding, editing, searching, and organizing your personal information._

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

#### Deactivate venv

- **macOS/Linux:**
  ```bash
  deactivate
  ```
- **Windows (cmd):**
  ```cmd
  deactivate
  ```
- **Windows (PowerShell):**
  ```powershell
  deactivate
  ```
  
## Install pre-commit hooks (mandatory once per repository clone)

- **macOS/Linux:**
  ```bash
  pre-commit install
  ```
- **Windows (cmd):**
  ```cmd
  pre-commit install
  ```
- **Windows (PowerShell):**
  ```powershell
  pre-commit install
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

### Check code formatting

- **macOS/Linux:**
  ```bash
  make check_formatting
  ```
- **Windows (no Make):**
  ```cmd
  flake8 .
  ```

### Fix code formatting

- **macOS/Linux:**
  ```bash
  make fix_formatting
  ```
- **Windows (no Make):**
  ```cmd
  autopep8 --in-place --aggressive --aggressive --recursive .
  ```

### Run the assistant

- **macOS/Linux:**
  ```bash
  make run
  ```
- **Windows (no Make):**
  ```cmd
  python3 main.py
  ```

## Commands Without Active Contact

These commands are available when you are not working with a specific contact (book-level):

- **add_contact**  
  Add a new contact to the address book.

- **find_contact**  
  Search for a contact by name.

- **select_active_contact**  
  Select a contact to make them the active contact.

- **edit_contact**  
  Edit the details of an existing contact.

- **delete_contact**  
  Remove a contact from the address book.

- **show_contacts**  
  List all contacts in the address book.

- **find_birthdays_this_week**  
  Show all contacts with birthdays in the current week.

- **exit**  
  Exit the application and save data.

- **help**  
  Show help information about available commands.

- **back_to_book**  
  Return to the main address book view.

---

## Commands With Active Contact

These commands are available when a contact is selected (contact-level):

### Phone Management
- **add_phone**  
  Add a phone number to the active contact.

- **edit_phone**  
  Edit a phone number for the active contact.

- **delete_phone**  
  Delete a phone number from the active contact.

- **show_phones**  
  List all phone numbers for the active contact.

- **set_main_phone**  
  Set the main phone number for the active contact.

### Email Management
- **add_email**  
  Add an email address to the active contact.

- **edit_email**  
  Edit an email address for the active contact.

- **delete_email**  
  Delete an email address from the active contact.

- **show_emails**  
  List all email addresses for the active contact.

- **set_main_email**  
  Set the main email address for the active contact.

### Notes Management
- **add_note**  
  Add a note to the active contact.

- **edit_note**  
  Edit a note for the active contact.

- **delete_note**  
  Delete a note from the active contact.

- **show_notes**  
  List all notes for the active contact.

- **find_note**  
  Search for a note by text, tag, or title for the active contact.

- **find_by_tag**  
  Find notes by tag for the active contact.

### Address Management
- **add_address**  
  Add an address to the active contact.

- **edit_address**  
  Edit an address for the active contact.

- **delete_address**  
  Delete an address from the active contact.

- **show_addresses**  
  List all addresses for the active contact.

- **set_main_address**  
  Set the main address for the active contact.

- **open_in_google_maps**  
  Open the main address of the active contact in Google Maps.

### Birthday Management
- **add_birthday**  
  Add a birthday to the active contact.

- **show_birthday**  
  Show the birthday of the active contact.

### Shared/General
- **exit**  
  Exit the application and save data.

- **help**  
  Show help information about available commands.

- **back_to_book**  
  Return to the main address book view.
