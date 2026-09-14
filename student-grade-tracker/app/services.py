from app.models import Subject
from app.validators import validate_grade, validate_subject_name


def add_subject(
    subjects: list[Subject],
    name: str,
    grade: int,
) -> Subject:
    validate_subject_name(name)
    validate_grade(grade)

    subject = Subject(
        name=name.strip(),
        grade=grade,
    )

    subjects.append(subject)

    return subject


def remove_subject(
    subjects: list[Subject],
    name: str,
) -> bool:
    for subject in subjects:
        if subject.name == name:
            subjects.remove(subject)
            return True

    return False


def search_subjects(
    subjects: list[Subject],
    query: str,
) -> list[Subject]:
    query = query.strip().lower()

    if not query:
        return subjects.copy()

    return [
        subject
        for subject in subjects
        if query in subject.name.lower()
    ]


def calculate_average(subjects: list[Subject]) -> float:
    if not subjects:
        return 0.0

    total = sum(
        subject.grade
        for subject in subjects
    )

    return total / len(subjects)


def get_min_grade(
    subjects: list[Subject],
) -> int | None:
    if not subjects:
        return None

    return min(
        subject.grade
        for subject in subjects
    )


def get_max_grade(
    subjects: list[Subject],
) -> int | None:
    if not subjects:
        return None

    return max(
        subject.grade
        for subject in subjects
    )


def get_grade_status(grade: int) -> str:
    validate_grade(grade)

    if grade >= 90:
        return "Excellent"

    if grade >= 75:
        return "Good"

    if grade >= 60:
        return "Satisfactory"

    return "Fail"
