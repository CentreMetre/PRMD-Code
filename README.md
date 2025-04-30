# PRMD-Code

## Setup

1. **Clone the repository:**

   ```sh
   git clone <repo-url>
   cd PRMD-Code
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment:**

   - **Windows (cmd):**
     ```sh
     .venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```sh
     .venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```sh
     source .venv/bin/activate
     ```

4. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

5. **Set environment variables:**

   - TODO - Discuss obfuscation methods
   - Create a `.env` file (see `.env.example` if available) and add your secrets, e.g.:
     ```
     IOTHUB_DEVICE_CONNECTION_STRING=your-connection-string-here
     ```

6. **Run the main script:**
   ```sh
   TODO
   ```

## Notes

- Do **not** commit your `.env` or `.venv` folders.
- Use [Azure best practices](https://learn.microsoft.com/en-us/azure/developer/python/configure-local-development-environment) for managing secrets.
