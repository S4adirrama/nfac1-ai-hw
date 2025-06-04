import os
import json
import requests
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_assistant() -> str:
    assistant = client.beta.assistants.create(
        name="Study Q&A Assistant",
        model="gpt-4o-mini",
        instructions="You are a helpful tutor. Use the knowledge in the attached files to answer questions. Cite sources where possible.",
        tools=[{"type": "file_search"}]
    )
    print(f"✅ Created assistant: {assistant.id}")
    return assistant.id

def upload_file(file_path: str) -> str:
    if file_path.startswith("http://") or file_path.startswith("https://"):
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file = client.files.create(
            file=(file_name, file_content),
            purpose="assistants"
        )
    else:
        with open(file_path, "rb") as f:
            file = client.files.create(file=f, purpose="assistants")
    print(f"📄 Uploaded file: {file.id}")
    return file.id

def create_vector_store() -> str:
    vector_store = client.vector_stores.create(name="Study PDF Knowledge Base")
    print(f"🧠 Created vector store: {vector_store.id}")
    return vector_store.id

def add_file_to_vector_store(vector_store_id: str, file_id: str):
    result = client.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    print(f"📎 Added file to vector store: {result.id}")

def save_config(assistant_id: str, file_id: str, vector_store_id: str):
    config = {
        "assistant_id": assistant_id,
        "file_id": file_id,
        "vector_store_id": vector_store_id
    }
    with open("assistant_config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("💾 Saved config to assistant_config.json")

def main():
    try:
        assistant_id = create_assistant()

        # Можно заменить на URL, если нужно
        pdf_path = "../data/calculus_basics.pdf"
        if not Path(pdf_path).exists() and not pdf_path.startswith("http"):
            print(f"⚠️ File not found: {pdf_path}")
            return

        file_id = upload_file(pdf_path)
        vector_store_id = create_vector_store()
        add_file_to_vector_store(vector_store_id, file_id)

        save_config(assistant_id, file_id, vector_store_id)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
