import os
from openai import OpenAI

# Initialize OpenAI client
def openai_login(api_key):
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        raise Exception(f"Couldn't login to OpenAI: {e}")
    
def generate_comment_with_llm(client : OpenAI, caption: str):
    """
    Generates a comment using a Large Language Model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "Write a short, human-like comment for an Instagram post with the caption provided"},
                {"role": "user", "content": caption}
            ],
            stop="\n",
            max_tokens=100,
            temperature=0.9,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating comment: {e}")
        return None

def comment(client, caption):
    """
    Generates a comment based on the post caption.
    """
    generated_comment = generate_comment_with_llm(client, caption)
    return generated_comment if generated_comment else "I'm fast af"  # Fallback comment
