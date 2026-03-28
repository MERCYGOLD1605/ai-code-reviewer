import os
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Load .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

client = OpenAI(api_key=api_key)


def generate_ai_docstring(code):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Generate a Python docstring:\n{code}"}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
       return '''"""AI unavailable (quota exceeded).

Args:
    parameters

Returns:
    output
"""'''