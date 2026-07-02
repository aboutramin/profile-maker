from src.file_loader import load_text_file
from src.llm_clients import call_openai, call_claude


def build_extraction_prompt(prompt_path: str, source_id: str, document_text: str) -> str:
    base_prompt = load_text_file(prompt_path)

    if not base_prompt.strip():
        raise FileNotFoundError(
            f"Extraction prompt is missing or empty: {prompt_path}. "
            "Stopping before any expensive API call."
        )

    return f"""
{base_prompt}

====================
SOURCE ID
====================
{source_id}

====================
DOCUMENT TEXT
====================
{document_text}
"""


def run_extraction(
    prompt_path: str,
    source_id: str,
    document_text: str,
    provider: str = "openai",
    model: str | None = None,
) -> str:
    prompt = build_extraction_prompt(
        prompt_path=prompt_path,
        source_id=source_id,
        document_text=document_text,
    )

    if provider == "claude":
        return call_claude(prompt, model=model)

    return call_openai(prompt, model=model)
