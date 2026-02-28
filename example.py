import os
from open_webui_client import OpenWebUIClient

def main():
    # 1. Initialize the client.
    # It automatically reads OPEN_WEBUI_BASE_URL and OPEN_WEBUI_TOKEN from your .env file.
    try:
        client = OpenWebUIClient()
        print(f"Successfully initialized client for: {client.base_url}\n")
    except ValueError as e:
        print(f"Error initializing client: {e}")
        print("Make sure you have created a .env file with the required variables and replaced dummy values.")
        return

    # 2. List all available Knowledge Bases
    print("--- 📚 Listing Knowledge Bases ---")
    try:
        kbs = client.get_knowledge_bases()
        print("Knowledge Bases:")
        print(kbs)
    except Exception as e:
        print(f"Failed to retrieve knowledge bases: {e}")
    print("\n")

    # 3. List all accessible files
    print("--- 📄 Listing All Files ---")
    try:
        files = client.get_files()
        print("Files:")
        print(files)
    except Exception as e:
        print(f"Failed to retrieve files: {e}")
    print("\n")

    # 4. Prepare a file to upload.
    # We will create a temporary test file if you don't provide one.
    file_to_upload = "example_document.txt"
    if not os.path.exists(file_to_upload):
        print(f"Creating a sample file '{file_to_upload}' for testing...")
        with open(file_to_upload, "w") as f:
            f.write("This is a simple text document containing some knowledge. OpenAI is an AI research laboratory.")

    # You need a valid knowledge ID from your Open WebUI instance for this to work completely:
    # (You can get this ID from the get_knowledge_bases() output)
    knowledge_base_id = "your-knowledge-id"

    # 5. Upload the file and add it to the knowledge base.
    print(f"--- ☁️ Uploading '{file_to_upload}' and attaching to knowledge base '{knowledge_base_id}' ---")
    try:
        # The upload_and_add_to_knowledge method handles uploading, waiting for processing, and attaching it
        result = client.upload_and_add_to_knowledge(file_to_upload, knowledge_base_id)
        
        print("\n✅ Operation Successful!")
        print("-" * 20)
        print("Server Response:")
        print(result)
        print("-" * 20)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
