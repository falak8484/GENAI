
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def generate_response(user_prompt, system_prompt):

    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    # Gemini provider
    if provider == "gemini":

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError(
                "Please add your Gemini API key to the .env file."
            )

        client = genai.Client(api_key=api_key)

        model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        # Try up to 3 times for temporary server errors
        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )

                return response.text

            except Exception as error:

                error_message = str(error).lower()

                temporary_error = any(
                    message in error_message
                    for message in [
                        "503",
                        "unavailable",
                        "429",
                        "resource_exhausted",
                        "internal server error"
                    ]
                )

                # Do not retry permanent errors
                if not temporary_error:
                    raise

                # Stop after the third attempt
                if attempt == 2:
                    raise

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds... "
                    f"(Attempt {attempt + 2}/3)"
                )

                time.sleep(wait_time)

    # Groq provider
    elif provider == "groq":

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "Please add your Groq API key to the .env file."
            )

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": os.getenv(
                    "GROQ_MODEL",
                    "llama-3.3-70b-versatile"
                ),
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "temperature": 0.3
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    else:
        raise ValueError(
            "Unsupported LLM provider. Choose 'gemini' or 'groq'."
        )
