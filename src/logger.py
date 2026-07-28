import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


LOG_DIRECTORY = Path("logs")


def save_json_log(
    data: BaseModel | dict[str, Any] | list[Any],
    prefix: str = "evaluation",
) -> Path:
    """
    Save evaluation data as a timestamped JSON file.
    """

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = LOG_DIRECTORY / f"{prefix}_{timestamp}.json"

    if isinstance(data, BaseModel):
        serializable_data = data.model_dump()
    else:
        serializable_data = data

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            serializable_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return file_path