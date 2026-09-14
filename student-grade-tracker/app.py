import flet as ft

from app.models import Subject
from app.services import (
    add_subject,
    calculate_average,
    get_grade_status,
    get_max_grade,
    get_min_grade,
    remove_subject,
    search_subjects,
)
from app.storage import load_subjects, save_subjects


DATA_FILE = "data.json"


def main(page: ft.Page):
    page.title = "Student Grade Tracker"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100
    page.scroll = ft.ScrollMode.AUTO

    subjects: list[Subject] = load_subjects(DATA_FILE)

    # =========================================================
    # COLORS
    # =========================================================

    PRIMARY = ft.Colors.BLUE_700
    PRIMARY_LIGHT = ft.Colors.BLUE_50
    TEXT_PRIMARY = ft.Colors.GREY_900
    TEXT_SECONDARY = ft.Colors.GREY_600
    TEXT_MUTED = ft.Colors.GREY_500
    BORDER = ft.Colors.GREY_200
    CARD = ft.Colors.WHITE

    # =========================================================
    # INPUT CONTROLS
    # =========================================================

    subject_name = ft.TextField(
        label="Subject name",
        hint_text="e.g. Programming",
        expand=True,
        border_radius=10,
        filled=True,
        bgcolor=CARD,
        border_color=ft.Colors.GREY_300,
        dense=True,
    )

    grade_input = ft.TextField(
        label="Grade",
        hint_text="0-100",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150,
        border_radius=10,
        filled=True,
        bgcolor=CARD,
        border_color=ft.Colors.GREY_300,
        dense=True,
    )

    search_input = ft.TextField(
        label="Search subjects",
        hint_text="Type subject name...",
        expand=True,
        prefix_icon=ft.Icons.SEARCH,
        filled=True,
        bgcolor=CARD,
        border_radius=10,
        border_color=ft.Colors.GREY_300,
        dense=True,
    )

    # =========================================================
    # STATISTICS
    # =========================================================

    average_text = ft.Text(
        "0.00",
        size=34,
        weight=ft.FontWeight.BOLD,
        color=PRIMARY,
    )

    min_text = ft.Text(
        "-",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )

    max_text = ft.Text(
        "-",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )

    count_text = ft.Text(
        "0",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )

    def create_stat_card(
        title: str,
        value_control: ft.Text,
        icon: str,
    ):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    icon,
                                    size=19,
                                    color=PRIMARY,
                                ),
                                width=36,
                                height=36,
                                alignment=ft.Alignment.CENTER,
                                border_radius=9,
                                bgcolor=PRIMARY_LIGHT,
                            ),
                            ft.Text(
                                title,
                                size=13,
                                color=TEXT_SECONDARY,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=9,
                    ),
                    ft.Container(height=6),
                    value_control,
                ],
                spacing=0,
            ),
            padding=16,
            border_radius=14,
            bgcolor=CARD,
            border=ft.Border.all(1, BORDER),
            expand=True,
        )

    # =========================================================
    # MESSAGES
    # =========================================================

    error_text = ft.Text(
        "",
        color=ft.Colors.RED_700,
        size=13,
    )

    # =========================================================
    # SUBJECT LIST
    # =========================================================

    subjects_column = ft.Column(
        spacing=8,
    )

    subjects_count_text = ft.Text(
        "0 total",
        size=13,
        color=TEXT_SECONDARY,
    )

    # =========================================================
    # HELPERS
    # =========================================================

    def get_status_color(status: str):
        if status == "Excellent":
            return ft.Colors.GREEN_700

        if status == "Good":
            return PRIMARY

        if status == "Satisfactory":
            return ft.Colors.ORANGE_700

        return ft.Colors.RED_700

    def update_statistics():
        average = calculate_average(subjects)
        minimum = get_min_grade(subjects)
        maximum = get_max_grade(subjects)

        average_text.value = f"{average:.2f}"

        min_text.value = (
            "-" if minimum is None else str(minimum)
        )

        max_text.value = (
            "-" if maximum is None else str(maximum)
        )

        count_text.value = str(len(subjects))

        subjects_count_text.value = (
            f"{len(subjects)} subject"
            if len(subjects) == 1
            else f"{len(subjects)} subjects"
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete_subject(name: str):
        removed = remove_subject(subjects, name)

        if removed:
            save_subjects(subjects, DATA_FILE)

            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"'{name}' was deleted."
                )
            )
            page.snack_bar.open = True

            refresh_subjects()

    # =========================================================
    # SUBJECT CARD
    # =========================================================

    def create_subject_card(subject: Subject):
        status = get_grade_status(subject.grade)

        status_badge = ft.Container(
            content=ft.Text(
                status,
                color=get_status_color(status),
                weight=ft.FontWeight.BOLD,
                size=12,
            ),
            padding=ft.Padding(
                left=10,
                right=10,
                top=5,
                bottom=5,
            ),
            border_radius=20,
            bgcolor=ft.Colors.GREY_100,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    # Subject icon
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.BOOK_OUTLINED,
                            size=21,
                            color=PRIMARY,
                        ),
                        width=42,
                        height=42,
                        alignment=ft.Alignment.CENTER,
                        border_radius=10,
                        bgcolor=PRIMARY_LIGHT,
                    ),

                    # Subject name
                    ft.Column(
                        controls=[
                            ft.Text(
                                subject.name,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_PRIMARY,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                "Subject",
                                size=11,
                                color=TEXT_MUTED,
                            ),
                        ],
                        spacing=1,
                        expand=True,
                    ),

                    # Grade
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    str(subject.grade),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "grade",
                                    size=10,
                                    color=TEXT_MUTED,
                                ),
                            ],
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            spacing=0,
                        ),
                        width=55,
                    ),

                    # Status
                    status_badge,

                    # Delete
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.GREY_600,
                        tooltip="Delete subject",
                        on_click=lambda e, name=subject.name:
                            delete_subject(name),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=12,
            border_radius=12,
            bgcolor=CARD,
            border=ft.Border.all(1, BORDER),
        )

    # =========================================================
    # REFRESH SUBJECT LIST
    # =========================================================

    def refresh_subjects():
        subjects_column.controls.clear()

        query = search_input.value.strip()

        visible_subjects = search_subjects(
            subjects,
            query,
        )

        if not visible_subjects:
            if query:
                message = f"No subjects found for '{query}'."
                icon = ft.Icons.SEARCH_OFF
            else:
                message = (
                    "No subjects yet.\n"
                    "Add your first subject above."
                )
                icon = ft.Icons.INBOX_OUTLINED

            subjects_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                icon,
                                size=40,
                                color=ft.Colors.GREY_400,
                            ),
                            ft.Text(
                                message,
                                italic=True,
                                color=TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                                size=13,
                            ),
                        ],
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        spacing=8,
                    ),
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                )
            )

        else:
            for subject in visible_subjects:
                subjects_column.controls.append(
                    create_subject_card(subject)
                )

        update_statistics()
        page.update()

    # =========================================================
    # SEARCH
    # =========================================================

    def search_subjects_handler(e):
        refresh_subjects()

    search_input.on_change = search_subjects_handler

    # =========================================================
    # ADD SUBJECT
    # =========================================================

    def add_new_subject(e):
        error_text.value = ""

        name = subject_name.value.strip()
        grade_text = grade_input.value.strip()

        if not name:
            error_text.value = "Subject name is required."
            page.update()
            return

        if not grade_text:
            error_text.value = "Grade is required."
            page.update()
            return

        try:
            grade = int(grade_text)

            add_subject(
                subjects,
                name,
                grade,
            )

            save_subjects(
                subjects,
                DATA_FILE,
            )

            subject_name.value = ""
            grade_input.value = ""

            refresh_subjects()

        except ValueError as error:
            error_text.value = str(error)
            page.update()

    # =========================================================
    # ADD BUTTON
    # =========================================================

    add_button = ft.Button(
        "Add Subject",
        icon=ft.Icons.ADD,
        on_click=add_new_subject,
        style=ft.ButtonStyle(
            padding=ft.Padding(
                left=20,
                right=20,
                top=12,
                bottom=12,
            ),
        ),
    )

    # =========================================================
    # HEADER
    # =========================================================

    header = ft.Row(
        controls=[
            ft.Container(
                content=ft.Icon(
                    ft.Icons.SCHOOL,
                    size=28,
                    color=ft.Colors.WHITE,
                ),
                width=50,
                height=50,
                alignment=ft.Alignment.CENTER,
                border_radius=12,
                bgcolor=PRIMARY,
            ),

            ft.Column(
                controls=[
                    ft.Text(
                        "Student Grade Tracker",
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Manage your subjects and grades",
                        size=12,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=2,
                expand=True,
            ),
        ],
        spacing=13,
    )

    # =========================================================
    # ADD SUBJECT CARD
    # =========================================================

    add_subject_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Add subject",
                    size=19,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Enter the subject name and your grade.",
                    size=12,
                    color=TEXT_SECONDARY,
                ),

                ft.Container(height=6),

                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=subject_name,
                            col={
                                "xs": 12,
                                "sm": 12,
                                "md": 6,
                            },
                        ),

                        ft.Container(
                            content=grade_input,
                            col={
                                "xs": 12,
                                "sm": 5,
                                "md": 3,
                            },
                        ),

                        ft.Container(
                            content=add_button,
                            col={
                                "xs": 12,
                                "sm": 7,
                                "md": 3,
                            },
                        ),
                    ],
                    spacing=8,
                    run_spacing=8,
                ),

                error_text,
            ],
            spacing=7,
        ),
        padding=18,
        border_radius=14,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDER),
    )

    # =========================================================
    # SEARCH CARD
    # =========================================================

    search_section = ft.Column(
        controls=[
            ft.Text(
                "Search",
                size=19,
                weight=ft.FontWeight.BOLD,
            ),

            search_input,
        ],
        spacing=8,
    )

    # =========================================================
    # SUBJECTS HEADER
    # =========================================================

    subjects_header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        "Subjects",
                        size=19,
                        weight=ft.FontWeight.BOLD,
                    ),
                    subjects_count_text,
                ],
                spacing=1,
            ),
        ],
    )

    # =========================================================
    # TABLE HEADER
    # =========================================================

    table_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(width=42),

                ft.Text(
                    "Subject",
                    expand=True,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_MUTED,
                ),

                ft.Text(
                    "Grade",
                    width=55,
                    text_align=ft.TextAlign.CENTER,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_MUTED,
                ),

                ft.Text(
                    "Status",
                    width=100,
                    text_align=ft.TextAlign.CENTER,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_MUTED,
                ),

                ft.Container(width=48),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding(
            left=12,
            right=12,
            top=2,
            bottom=2,
        ),
    )

    # =========================================================
    # SUBJECTS LIST
    # =========================================================

    subjects_section = ft.Container(
        content=ft.Column(
            controls=[
                subjects_header,
                ft.Container(height=3),
                table_header,
                subjects_column,
            ],
            spacing=4,
        ),
    )

    # =========================================================
    # STATISTICS
    # =========================================================

    average_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.TRENDING_UP,
                                size=24,
                                color=ft.Colors.WHITE,
                            ),
                            width=44,
                            height=44,
                            alignment=ft.Alignment.CENTER,
                            border_radius=11,
                            bgcolor=PRIMARY,
                        ),

                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Average grade",
                                    size=13,
                                    color=TEXT_SECONDARY,
                                ),
                                ft.Text(
                                    "Overall performance",
                                    size=11,
                                    color=TEXT_MUTED,
                                ),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),

                ft.Container(height=10),

                average_text,

                ft.Text(
                    "out of 100",
                    size=11,
                    color=TEXT_MUTED,
                ),
            ],
            spacing=0,
        ),
        padding=18,
        border_radius=14,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDER),
        expand=True,
    )

    statistics = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=average_card,
                col={
                    "xs": 12,
                    "sm": 12,
                    "md": 6,
                    "lg": 3,
                },
            ),

            ft.Container(
                content=create_stat_card(
                    "Minimum",
                    min_text,
                    ft.Icons.ARROW_DOWNWARD,
                ),
                col={
                    "xs": 12,
                    "sm": 4,
                    "md": 2,
                    "lg": 3,
                },
            ),

            ft.Container(
                content=create_stat_card(
                    "Maximum",
                    max_text,
                    ft.Icons.ARROW_UPWARD,
                ),
                col={
                    "xs": 12,
                    "sm": 4,
                    "md": 2,
                    "lg": 3,
                },
            ),

            ft.Container(
                content=create_stat_card(
                    "Subjects",
                    count_text,
                    ft.Icons.MENU_BOOK,
                ),
                col={
                    "xs": 12,
                    "sm": 4,
                    "md": 2,
                    "lg": 3,
                },
            ),
        ],
        spacing=10,
        run_spacing=10,
    )

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    content = ft.Container(
        content=ft.Column(
            controls=[
                header,

                ft.Container(height=4),

                add_subject_card,

                ft.Container(height=14),

                search_section,

                ft.Container(height=14),

                subjects_section,

                ft.Container(height=18),

                ft.Text(
                    "Statistics",
                    size=19,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(height=3),

                statistics,

                ft.Container(height=20),
            ],
            spacing=0,
        ),
        padding=ft.Padding(
            left=24,
            right=24,
            top=22,
            bottom=30,
        ),
        width=float("inf"),
    )

    page.add(content)

    refresh_subjects()


ft.run(main)
