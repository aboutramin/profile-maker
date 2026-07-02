import os

from dotenv import load_dotenv

# Safe when this module is used directly, not only through profile_maker.py.
load_dotenv()


DEFAULT_OPENAI_MODEL = "gpt-5.5"
DEFAULT_CLAUDE_MODEL = "claude-fable-5"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name}. Add it to your .env file.")
    return value


def get_openai_model(model: str | None = None) -> str:
    return model or os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)


def get_claude_model(model: str | None = None) -> str:
    return model or os.getenv("ANTHROPIC_MODEL", DEFAULT_CLAUDE_MODEL)


def get_int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got: {raw_value}") from exc

    if value <= 0:
        raise ValueError(f"{name} must be positive, got: {value}")

    return value


def call_openai(prompt: str, model: str | None = None) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError(
            "The openai package is required. Install dependencies with: "
            "pip install -r requirements.txt"
        ) from exc

    client = OpenAI(api_key=require_env("OPENAI_API_KEY"))

    response = client.responses.create(
        model=get_openai_model(model),
        input=prompt,
        max_output_tokens=get_int_env("OPENAI_MAX_OUTPUT_TOKENS", 20000),
    )

    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text

    raise RuntimeError("OpenAI response did not contain output_text.")


def call_claude(prompt: str, model: str | None = None) -> str:
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise ImportError(
            "The anthropic package is required. Install dependencies with: "
            "pip install -r requirements.txt"
        ) from exc

    client = Anthropic(api_key=require_env("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model=get_claude_model(model),
        max_tokens=get_int_env("ANTHROPIC_MAX_TOKENS", 20000),
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text_blocks = [
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    ]

    if text_blocks:
        return "\n".join(text_blocks)

    raise RuntimeError("Claude response did not contain any text blocks.")
