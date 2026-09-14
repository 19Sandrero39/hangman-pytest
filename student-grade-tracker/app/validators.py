def validate_subject_name(name: str) -> None:
    if not name.strip():
        raise ValueError("Subject name cannot be empty")


def validate_grade(grade: int) -> None:
    if not 0 <= grade <= 100:
        raise ValueError("Grade must be between 0 and 100")
