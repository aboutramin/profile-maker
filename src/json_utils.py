import json
import re
from pathlib import Path
from typing import Any


def extract_json_text(content: str) -> str:
    if not content:
        return ""

    text = str(content).strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()

    first = text.find("{")
    last = text.rfind("}")

    if first == -1 or last == -1 or last <= first:
        return text

    return text[first:last + 1]


def parse_json(content: str) -> Any:
    return json.loads(extract_json_text(content))


def write_json(path: str, data: Any) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
