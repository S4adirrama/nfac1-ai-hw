import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    with open("assistant_config.json", "r") as f:
        config = json.load(f)

    assistant_id = config.get("assistant_id")
    vector_store_id = config.get("vector_store_id")

    if not assistant_id or not vector_store_id:
        raise ValueError("Missing assistant_id or vector_store_id in assistant_config.json")

    user_question = input()
    # Create a thread
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_question
    )

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        tool_choice="auto",  
        additional_instructions=None
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            raise Exception(f"Run {run_status.status}")
        else:
            import time
            time.sleep(1)

    # Get messages 
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    last_message = messages.data[0]

    print("\n🧠 Assistant answer:\n")
    print(last_message.content[0].text.value)

    annotations = last_message.content[0].text.annotations
    if annotations:
        print("\n📎 Citations:")
        for ann in annotations:
            print(ann)

if __name__ == "__main__":
    main()
