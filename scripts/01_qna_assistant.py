import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    with open("assistant_config.json", "r") as f:
        config = json.load(f)

    vector_store_id = config.get("vector_store_id")
    if not vector_store_id:
        raise ValueError("vector_store_id missing from assistant_config.json")

    user_question = "Explain the difference between a definite and an indefinite integral in one paragraph."

    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_question,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store_id],
                "max_num_results": 2
            }
        ],
        include=["file_search_call.results"]
    )

   
    print("\n🧠 Assistant answer:\n")
    print(response.output[0].content[0].text)

    metadata = getattr(response, "metadata", None)
    if metadata:
        print("\n📎 Citations:")
        print(response.output[0].content[0].annotations
)

if __name__ == "__main__":
    main()
