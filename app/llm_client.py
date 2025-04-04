from groq import Groq
from app.system_prompt import SYSTEM_PROMPT

# Initialize the Groq client with your API key
client = Groq(api_key="")

def get_llm_response(user_input):
    # Check if the input is empty or irrelevant
    if not user_input.strip():
        return "still in the development phase."

    # Prepare messages for the chat model
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\nOnly provide answers based on the question asked. Do not add extra information."},  
        {"role": "user", "content": user_input}
    ]

    # Call the Groq API
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    # Extract response
    response = completion.choices[0].message.content if completion.choices else ""

    # Handle empty responses
    if not response.strip():
        return "Unable to find data in  my database , Still in the development phase."

    return response
