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
    page.theme = ft.Theme(color_scheme_seed="#0F4C5C")
    page.bgcolor = "#F2F5F6"
    page.scroll = ft.ScrollMode.AUTO

    subjects: list[Subject] = load_subjects(DATA_FILE)

    # =========================================================
    # DESIGN TOKENS
    # =========================================================
    # Palette: deep ink-teal as the single brand colour, cool paper
    # background, and semantic colours reserved for grade statuses.

    PRIMARY = "#0F4C5C"  # ink teal
    PRIMARY_LIGHT = "#E3EEF0"  # tinted surface for icon tiles
    BACKGROUND = "#F2F5F6"
    CARD = ft.Colors.WHITE
    SURFACE = "#F7F9FA"  # rows inside a card
    BORDER = "#DDE5E8"
    TRACK = "#E3EAED"  # empty part of progress bars

    TEXT_PRIMARY = "#14232A"
    TEXT_SECONDARY = "#5B6B72"
    TEXT_MUTED = "#8A979D"

    # Status colours: (foreground, background)
    STATUS_EXCELLENT = ("#1E7A4F", "#E4F3EB")
    STATUS_GOOD = (PRIMARY, PRIMARY_LIGHT)
    STATUS_SATISFACTORY = ("#A86200", "#FBEFD9")
    STATUS_LOW = ("#B3372F", "#FBE6E4")

    # Radii by hierarchy: cards > rows/inputs > pills
    RADIUS_CARD = 18
    RADIUS_ROW = 12
    RADIUS_FIELD = 10

    STATUS_COLUMN_WIDTH = 120
    GRADE_COLUMN_WIDTH = 60

    # =========================================================
    # INPUT CONTROLS
    # =========================================================

    field_style = dict(
        border_radius=RADIUS_FIELD,
        filled=True,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=PRIMARY,
        focused_border_width=2,
        cursor_color=PRIMARY,
        text_size=14,
        dense=True,
    )

    subject_name = ft.TextField(
        label="Subject name",
        hint_text="e.g. Programming",
        prefix_icon=ft.Icons.EDIT_OUTLINED,
        expand=True,
        **field_style,
    )

    grade_input = ft.TextField(
        label="Grade",
        hint_text="0-100",
        prefix_icon=ft.Icons.STAR_OUTLINE,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150,
        **field_style,
    )

    search_input = ft.TextField(
        label="Search subjects",
        hint_text="Type subject name...",
        expand=True,
        prefix_icon=ft.Icons.SEARCH,
        **field_style,
    )

    # =========================================================
    # STATISTICS
    # =========================================================

    average_text = ft.Text(
        "0.00",
        size=44,
        weight=ft.FontWeight.W_800,
        color=ft.Colors.WHITE,
    )

    min_text = ft.Text(
        "-",
        size=26,
        weight=ft.FontWeight.W_700,
        color=TEXT_PRIMARY,
    )

    max_text = ft.Text(
        "-",
        size=26,
        weight=ft.FontWeight.W_700,
        color=TEXT_PRIMARY,
    )

    count_text = ft.Text(
        "0",
        size=26,
        weight=ft.FontWeight.W_700,
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
                                    size=18,
                                    color=PRIMARY,
                                ),
                                width=34,
                                height=34,
                                alignment=ft.Alignment.CENTER,
                                border_radius=RADIUS_FIELD,
                                bgcolor=PRIMARY_LIGHT,
                            ),
                            ft.Text(
                                title,
                                size=13,
                                color=TEXT_SECONDARY,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    value_control,
                ],
                spacing=0,
            ),
            padding=18,
            border_radius=RADIUS_CARD,
            bgcolor=CARD,
            border=ft.Border.all(1, BORDER),
            expand=True,
        )

    # =========================================================
    # MESSAGES
    # =========================================================

    error_text = ft.Text(
        "",
        color="#B3372F",
        size=13,
        weight=ft.FontWeight.W_500,
    )

    # =========================================================
    # SUBJECT LIST
    # =========================================================

    subjects_column = ft.Column(
        spacing=8,
    )

    subjects_count_text = ft.Text(
        "0 total",
        size=12,
        weight=ft.FontWeight.W_600,
        color=PRIMARY,
    )

    # =========================================================
    # HELPERS
    # =========================================================

    def get_status_colors(status: str):
        if status == "Excellent":
            return STATUS_EXCELLENT

        if status == "Good":
            return STATUS_GOOD

        if status == "Satisfactory":
            return STATUS_SATISFACTORY

        return STATUS_LOW

    def get_status_color(status: str):
        return get_status_colors(status)[0]

    def section_title(title: str, subtitle: str | None = None):
        controls = [
            ft.Text(
                title,
                size=18,
                weight=ft.FontWeight.W_700,
                color=TEXT_PRIMARY,
            )
        ]

        if subtitle:
            controls.append(
                ft.Text(
                    subtitle,
                    size=12,
                    color=TEXT_SECONDARY,
                )
            )

        return ft.Column(
            controls=controls,
            spacing=2,
        )

    def update_statistics():
        average = calculate_average(subjects)
        minimum = get_min_grade(subjects)
        maximum = get_max_grade(subjects)

        average_text.value = f"{average:.2f}"

        min_text.value = "-" if minimum is None else str(minimum)

        max_text.value = "-" if maximum is None else str(maximum)

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

            page.snack_bar = ft.SnackBar(content=ft.Text(f"'{name}' was deleted."))
            page.snack_bar.open = True

            refresh_subjects()

    # =========================================================
    # SUBJECT CARD
    # =========================================================

    def create_subject_card(subject: Subject):
        status = get_grade_status(subject.grade)
        status_fg, status_bg = get_status_colors(status)

        progress = max(0, min(subject.grade, 100)) / 100

        status_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=7,
                        height=7,
                        border_radius=4,
                        bgcolor=status_fg,
                    ),
                    ft.Text(
                        status,
                        color=status_fg,
                        weight=ft.FontWeight.W_600,
                        size=12,
                    ),
                ],
                spacing=6,
                tight=True,
            ),
            padding=ft.Padding(
                left=10,
                right=12,
                top=5,
                bottom=5,
            ),
            border_radius=20,
            bgcolor=status_bg,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    # Subject icon (tinted by status)
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.BOOK_OUTLINED,
                            size=20,
                            color=status_fg,
                        ),
                        width=42,
                        height=42,
                        alignment=ft.Alignment.CENTER,
                        border_radius=RADIUS_FIELD,
                        bgcolor=status_bg,
                    ),
                    # Subject name + grade bar
                    ft.Column(
                        controls=[
                            ft.Text(
                                subject.name,
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=TEXT_PRIMARY,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.ProgressBar(
                                value=progress,
                                color=status_fg,
                                bgcolor=TRACK,
                                bar_height=4,
                                border_radius=2,
                            ),
                        ],
                        spacing=7,
                        expand=True,
                    ),
                    # Grade
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    str(subject.grade),
                                    size=20,
                                    weight=ft.FontWeight.W_800,
                                    color=status_fg,
                                ),
                                ft.Text(
                                    "/ 100",
                                    size=10,
                                    color=TEXT_MUTED,
                                ),
                            ],
                            horizontal_alignment=(ft.CrossAxisAlignment.CENTER),
                            spacing=0,
                        ),
                        width=GRADE_COLUMN_WIDTH,
                    ),
                    # Status
                    ft.Container(
                        content=status_badge,
                        width=STATUS_COLUMN_WIDTH,
                        alignment=ft.Alignment.CENTER,
                    ),
                    # Delete
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=TEXT_MUTED,
                        icon_size=20,
                        tooltip="Delete subject",
                        on_click=lambda e, name=subject.name: delete_subject(name),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=12,
            border_radius=RADIUS_ROW,
            bgcolor=SURFACE,
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
                message = "No subjects yet.\nAdd your first subject above."
                icon = ft.Icons.INBOX_OUTLINED

            subjects_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    icon,
                                    size=30,
                                    color=PRIMARY,
                                ),
                                width=64,
                                height=64,
                                alignment=ft.Alignment.CENTER,
                                border_radius=32,
                                bgcolor=PRIMARY_LIGHT,
                            ),
                            ft.Text(
                                message,
                                color=TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                                size=13,
                            ),
                        ],
                        horizontal_alignment=(ft.CrossAxisAlignment.CENTER),
                        spacing=12,
                    ),
                    padding=ft.Padding(
                        left=20,
                        right=20,
                        top=32,
                        bottom=32,
                    ),
                    alignment=ft.Alignment.CENTER,
                )
            )

        else:
            for subject in visible_subjects:
                subjects_column.controls.append(create_subject_card(subject))

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
        height=44,
        style=ft.ButtonStyle(
            bgcolor=PRIMARY,
            color=ft.Colors.WHITE,
            elevation=0,
            shape=ft.RoundedRectangleBorder(radius=RADIUS_FIELD),
            padding=ft.Padding(
                left=22,
                right=22,
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
                    size=26,
                    color=ft.Colors.WHITE,
                ),
                width=48,
                height=48,
                alignment=ft.Alignment.CENTER,
                border_radius=14,
                bgcolor=PRIMARY,
            ),
            ft.Column(
                controls=[
                    ft.Text(
                        "Student Grade Tracker",
                        size=24,
                        weight=ft.FontWeight.W_800,
                        color=TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Manage your subjects and grades",
                        size=13,
                        color=TEXT_SECONDARY,
                    ),
                ],
                spacing=2,
                expand=True,
            ),
        ],
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # =========================================================
    # STATISTICS
    # =========================================================
    # The average is the one bold element of the page: a solid
    # ink-teal card with a large number. Everything else stays quiet.

    average_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.TRENDING_UP,
                                size=22,
                                color=ft.Colors.WHITE,
                            ),
                            width=40,
                            height=40,
                            alignment=ft.Alignment.CENTER,
                            border_radius=RADIUS_FIELD,
                            bgcolor=ft.Colors.with_opacity(
                                0.16,
                                ft.Colors.WHITE,
                            ),
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Average grade",
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "Overall performance",
                                    size=11,
                                    color=ft.Colors.with_opacity(
                                        0.7,
                                        ft.Colors.WHITE,
                                    ),
                                ),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                average_text,
                ft.Text(
                    "out of 100",
                    size=11,
                    color=ft.Colors.with_opacity(
                        0.7,
                        ft.Colors.WHITE,
                    ),
                ),
            ],
            spacing=0,
        ),
        padding=20,
        border_radius=RADIUS_CARD,
        bgcolor=PRIMARY,
        expand=True,
    )

    statistics = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=average_card,
                col={
                    "xs": 12,
                    "sm": 12,
                    "md": 12,
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
                    "md": 4,
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
                    "md": 4,
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
                    "md": 4,
                    "lg": 3,
                },
            ),
        ],
        spacing=12,
        run_spacing=12,
    )

    # =========================================================
    # ADD SUBJECT CARD
    # =========================================================

    add_subject_card = ft.Container(
        content=ft.Column(
            controls=[
                section_title(
                    "Add subject",
                    "Enter the subject name and your grade.",
                ),
                ft.Container(height=4),
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
                    spacing=10,
                    run_spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                error_text,
            ],
            spacing=8,
        ),
        padding=22,
        border_radius=RADIUS_CARD,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDER),
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
                    weight=ft.FontWeight.W_600,
                    color=TEXT_MUTED,
                ),
                ft.Text(
                    "Grade",
                    width=GRADE_COLUMN_WIDTH,
                    text_align=ft.TextAlign.CENTER,
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_MUTED,
                ),
                ft.Text(
                    "Status",
                    width=STATUS_COLUMN_WIDTH,
                    text_align=ft.TextAlign.CENTER,
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_MUTED,
                ),
                ft.Container(width=48),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding(
            left=13,
            right=13,
            top=2,
            bottom=2,
        ),
    )

    # =========================================================
    # SUBJECTS CARD (title + search + list)
    # =========================================================

    subjects_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        section_title("Subjects"),
                        ft.Container(
                            content=subjects_count_text,
                            padding=ft.Padding(
                                left=12,
                                right=12,
                                top=5,
                                bottom=5,
                            ),
                            border_radius=20,
                            bgcolor=PRIMARY_LIGHT,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[search_input],
                ),
                table_header,
                subjects_column,
            ],
            spacing=12,
        ),
        padding=22,
        border_radius=RADIUS_CARD,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDER),
    )

    # =========================================================
    # MAIN CONTENT
    # =========================================================
    # Content is centred and capped by responsive column spans,
    # so it stays readable on wide screens.

    content = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        header,
                        ft.Container(height=2),
                        statistics,
                        add_subject_card,
                        subjects_section,
                    ],
                    spacing=16,
                ),
                col={
                    "xs": 12,
                    "md": 11,
                    "lg": 9,
                    "xl": 8,
                },
                padding=ft.Padding(
                    left=16,
                    right=16,
                    top=28,
                    bottom=36,
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(content)

    refresh_subjects()


ft.run(main)
