
import logging
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger("owaspshield")


def generate_response_with_metrics(user_prompt, system_prompt):
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    start_time = time.perf_counter()

    input_tokens = 0
    output_tokens = 0
    answer = ""

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError(
                "Please add your Gemini API key to the .env file."
            )

        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )

                answer = response.text or ""

                usage = response.usage_metadata

                if usage:
                    input_tokens = usage.prompt_token_count or 0
                    output_tokens = usage.candidates_token_count or 0

                break

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

                if not temporary_error or attempt == 2:
                    raise

                wait_time = 2 ** (attempt + 1)

                logger.warning(
                    "Gemini temporarily unavailable. Retrying in %s seconds.",
                    wait_time
                )

                time.sleep(wait_time)

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
        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        usage = result.get("usage") or {}

        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

    else:
        raise ValueError(
            "Unsupported LLM provider. Choose 'gemini' or 'groq'."
        )

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "llm_metrics provider=%s latency_ms=%.2f input_tokens=%s output_tokens=%s total_tokens=%s",
        provider,
        latency_ms,
        input_tokens,
        output_tokens,
        input_tokens + output_tokens
    )

    return {
        "answer": answer,
        "provider": provider,
        "latency_ms": round(latency_ms, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }


def generate_response(user_prompt, system_prompt):
    result = generate_response_with_metrics(
        user_prompt=user_prompt,
        system_prompt=system_prompt
    )

    return result["answer"]
