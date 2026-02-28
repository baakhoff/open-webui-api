# Open WebUI API Wrapper

A simple Python wrapper for interacting with the Open WebUI API. It currently supports authenticating, uploading files, and adding them directly to a Knowledge Base while correctly waiting for processing to complete.

## Setup

1. **Clone the repository:**
   (Or navigate to your project directory if already cloned).

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and set your `OPEN_WEBUI_BASE_URL` (e.g., `http://localhost:3000`) and `OPEN_WEBUI_TOKEN` (your JWT token or API key).

## Usage

You can use the `OpenWebUIClient` to interact with the API. You can import and use the client in your own scripts. See `example.py` for a working runnable demo.

### Available Methods

- `get_knowledge_bases()`: Lists all available knowledge bases.
- `get_files()`: Lists all uploaded files accessible to the authenticated user.
- `upload_and_add_to_knowledge(file_path, knowledge_id, timeout=300)`: Uploads a file, waits for it to become processed, and attaches it to the specified knowledge base.

### Example

Here's a basic example showcasing the client's capabilities:

```python
from open_webui_client import OpenWebUIClient

# Initialize the client (automatically loads credentials from .env)
client = OpenWebUIClient()

# 1. List all Knowledge Bases
kbs = client.get_knowledge_bases()
print("Knowledge Bases:", kbs)

# 2. List all available Files
files = client.get_files()
print("Files:", files)

# 3. Upload a file and add it to a Knowledge Base
file_to_upload = "path/to/your/document.pdf"

# You can get this ID from the get_knowledge_bases output
knowledge_base_id = "your-knowledge-id"

try:
    result = client.upload_and_add_to_knowledge(file_to_upload, knowledge_base_id)
    print("Operation successful!")
    print(result)
except Exception as e:
    print(f"Failed to upload file or add to knowledge base: {e}")
```

### Important Notes
- The upload process automatically polls the server every 0.1 seconds to check if the uploaded document has finished processing before attempting to add it to the knowledge base.
- If processing fails or times out (default 300 seconds), an exception is raised explaining the exact error.
- All endpoints automatically handle trailing slash redirects and gracefully fallback to returning raw text inside a JSON wrapper if the server returns non-JSON responses.
