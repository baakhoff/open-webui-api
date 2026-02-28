import os
import time
import requests
from dotenv import load_dotenv

class OpenWebUIClient:
    """
    A simple Python wrapper for interacting with the Open WebUI API.
    """
    def __init__(self, base_url: str = None, token: str = None):
        """
        Initializes the OpenWebUI API client.
        
        Args:
            base_url (str, optional): The base URL of the Open WebUI server (e.g., 'http://localhost:3000'). 
                                      If not provided, reads 'OPEN_WEBUI_BASE_URL' from environment variables.
            token (str, optional): The JWT token or API key for authentication. 
                                   If not provided, reads 'OPEN_WEBUI_TOKEN' from environment variables.
        """
        load_dotenv()
        
        # Default to localhost:3000 if base_url is not set anywhere
        self.base_url = base_url or os.getenv("OPEN_WEBUI_BASE_URL", "http://localhost:3000")
        self.token = token or os.getenv("OPEN_WEBUI_TOKEN")
        
        if not self.base_url:
            raise ValueError("Base URL must be provided either via arguments or 'OPEN_WEBUI_BASE_URL' environment variable.")
        self.base_url = self.base_url.rstrip("/")
        
        if not self.token or self.token == "your-api-key-here":
            raise ValueError("Authentication token must be provided either via arguments or 'OPEN_WEBUI_TOKEN' environment variable.")

    def _get_headers(self) -> dict:
        """
        Returns the standard headers required for authenticated API requests.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def upload_and_add_to_knowledge(self, file_path: str, knowledge_id: str, timeout: int = 300) -> dict:
        """
        Upload a file and add it to a knowledge base.
        Properly waits for processing to complete before adding.
        
        Args:
            file_path (str): The local path to the file to be uploaded.
            knowledge_id (str): The ID of the knowledge base to add the file to.
            timeout (int): The maximum number of seconds to wait for file processing.
            
        Returns:
            dict: The JSON response obtained from adding the file to the knowledge base.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
            
        headers = self._get_headers()
        
        # Step 1: Upload the file
        print(f"Uploading file: {file_path}")
        with open(file_path, 'rb') as f:
            response = requests.post(
                f'{self.base_url}/api/v1/files/',
                headers=headers,
                files={'file': f}
            )
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")
        
        file_data = response.json()
        file_id = file_data['id']
        print(f"File uploaded with ID: {file_id}")
        
        # Step 2: Wait for processing to complete
        print("Waiting for file processing...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status_response = requests.get(
                f'{self.base_url}/api/v1/files/{file_id}/process/status',
                headers=headers
            )
            
            if status_response.status_code != 200:
                raise Exception(f"Failed to check processing status: {status_response.text}")

            status_data = status_response.json()
            status = status_data.get('status')
            
            if status == 'completed':
                print("File processing completed!")
                break
            elif status == 'failed':
                raise Exception(f"Processing failed: {status_data.get('error')}")
            
            time.sleep(0.5)  # Poll every 0.5 seconds
        else:
            raise TimeoutError("File processing timed out")
        
        # Step 3: Add to knowledge base
        print(f"Adding file to knowledge base: {knowledge_id}")
        add_headers = {**headers, 'Content-Type': 'application/json'}
        add_response = requests.post(
            f'{self.base_url}/api/v1/knowledge/{knowledge_id}/file/add',
            headers=add_headers,
            json={'file_id': file_id}
        )
        
        if add_response.status_code != 200:
            raise Exception(f"Failed to add to knowledge: {add_response.status_code} - {add_response.text}")
        
        print(f"File successfully added to knowledge base!")
        
        try:
            return add_response.json()
        except requests.exceptions.JSONDecodeError:
            return {"status": "success", "response": add_response.text}

    def get_knowledge_bases(self) -> dict:
        """
        List all available knowledge bases.
        Provides comprehensive information about available knowledge bases 
        including document counts and creation timestamps.
        
        Returns:
            dict: The JSON response containing the list of knowledge bases.
        """
        headers = self._get_headers()
        response = requests.get(
            f'{self.base_url}/api/v1/knowledge/',
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get knowledge bases: {response.status_code} - {response.text}")
            
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"status": "success", "response": response.text}

    def get_files(self) -> dict:
        """
        List all uploaded files.
        Returns a comprehensive list of uploaded files accessible to the authenticated user.
        
        Returns:
            dict: The JSON response containing the list of files.
        """
        headers = self._get_headers()
        response = requests.get(
            f'{self.base_url}/api/v1/files/',
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get files: {response.status_code} - {response.text}")
            
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"status": "success", "response": response.text}
