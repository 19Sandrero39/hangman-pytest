import json
from pathlib import Path

from app.models import Subject


def save_subjects(
    subjects: list[Subject],
    file_path: str | Path,
) -> None:
    path = Path(file_path)

    data = [
        {
            "name": subject.name,
            "grade": subject.grade,
        }
        for subject in subjects
    ]

    path.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8",
    )


def load_subjects(
    file_path: str | Path,
) -> list[Subject]:
    path = Path(file_path)

    if not path.exists():
        return []

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    return [
        Subject(
            name=item["name"],
            grade=item["grade"],
        )
        for item in data
    ]