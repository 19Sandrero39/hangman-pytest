'''
TC - Test Case
M - Matrix
'''

import pytest
from student_result import get_result

OTLICHNO = "Отлично"
HOROSHO = "Хорошо"
ZACHET = "Зачёт"
NEZACHET = "Незачёт"
BAD_SCORE = "Некорректный балл"
BAD_ATT = "Некорректная посещаемость"

MSG_SCORE_TYPE = "Баллы должны быть числом"
MSG_ATT_TYPE = "Посещаемость должна быть числом"


# ---------------------------------------------------------------------------
# 1. Неправильный тип данных -> TypeError (pytest.raises)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, attendance, message",
    [
        pytest.param("90", 80, MSG_SCORE_TYPE, id="TC-01 score=str"),
        pytest.param(None, 80, MSG_SCORE_TYPE, id="TC-02 score=None"),
        pytest.param([90], 80, MSG_SCORE_TYPE, id="TC-03 score=list"),
        pytest.param(90, "80", MSG_ATT_TYPE, id="TC-04 attendance=str"),
        pytest.param(90, None, MSG_ATT_TYPE, id="TC-05 attendance=None"),
        pytest.param(90, [80], MSG_ATT_TYPE, id="TC-06 attendance=list"),
        
        # оба аргумента неверного типа -> сначала проверяется score
        pytest.param("90", "80", MSG_SCORE_TYPE, id="TC-07 оба=str, приоритет score"),
        
        # проверка типа выполняется раньше проверки диапазона
        pytest.param(
            150, "80", MSG_ATT_TYPE, id="TC-08 score вне диапазона + attendance=str"
        ),
    ],
)
def test_wrong_type_raises_type_error(score, attendance, message):
    with pytest.raises(TypeError, match=message):
        get_result(score, attendance)


# ---------------------------------------------------------------------------
# 2. Значения вне допустимого диапазона
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        pytest.param(-1, 80, BAD_SCORE, id="TC-09 score=-1"),
        pytest.param(101, 80, BAD_SCORE, id="TC-10 score=101"),
        pytest.param(-0.1, 80, BAD_SCORE, id="TC-11 score=-0.1"),
        pytest.param(100.1, 80, BAD_SCORE, id="TC-12 score=100.1"),
        pytest.param(float("inf"), 80, BAD_SCORE, id="TC-13 score=+inf"),
        pytest.param(float("-inf"), 80, BAD_SCORE, id="TC-14 score=-inf"),
        pytest.param(80, -1, BAD_ATT, id="TC-15 attendance=-1"),
        pytest.param(80, 101, BAD_ATT, id="TC-16 attendance=101"),
        pytest.param(80, -0.1, BAD_ATT, id="TC-17 attendance=-0.1"),
        pytest.param(80, 100.1, BAD_ATT, id="TC-18 attendance=100.1"),
        
        # оба неверны -> сообщение про балл (score проверяется первым)
        pytest.param(-1, 101, BAD_SCORE, id="TC-19 оба вне диапазона"),
    ],
)
def test_out_of_range(score, attendance, expected):
    assert get_result(score, attendance) == expected


# ---------------------------------------------------------------------------
# 3. Граничные значения score (attendance = 100, чтобы не влиять на результат)
#    Значение 100 для attendance проверяется здесь же (TC-26)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, expected",
    [
        pytest.param(0, NEZACHET, id="TC-20 score=0"),
        pytest.param(49, NEZACHET, id="TC-21 score=49"),
        pytest.param(50, ZACHET, id="TC-22 score=50"),
        pytest.param(69, ZACHET, id="TC-23 score=69"),
        pytest.param(70, HOROSHO, id="TC-24 score=70"),
        pytest.param(89, HOROSHO, id="TC-25 score=89"),
        pytest.param(90, OTLICHNO, id="TC-26 score=90, attendance=100"),
        pytest.param(100, OTLICHNO, id="TC-27 score=100, attendance=100"),
    ],
)
def test_score_boundaries(score, expected):
    assert get_result(score, 100) == expected


# ---------------------------------------------------------------------------
# 4. Граничные значения attendance (score = 100)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "attendance, expected",
    [
        pytest.param(0, NEZACHET, id="TC-28 attendance=0"),
        pytest.param(59, NEZACHET, id="TC-29 attendance=59"),
        pytest.param(60, ZACHET, id="TC-30 attendance=60"),
        pytest.param(69, ZACHET, id="TC-31 attendance=69"),
        pytest.param(70, HOROSHO, id="TC-32 attendance=70"),
        pytest.param(79, HOROSHO, id="TC-33 attendance=79"),
        pytest.param(80, OTLICHNO, id="TC-34 attendance=80"),
    ],
)
def test_attendance_boundaries(attendance, expected):
    assert get_result(100, attendance) == expected


# ---------------------------------------------------------------------------
# 5. Оба аргумента на границе одновременно (проверка условий с «and»)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        pytest.param(90, 80, OTLICHNO, id="TC-35 90/80"),
        pytest.param(90, 79, HOROSHO, id="TC-36 90/79"),
        pytest.param(89, 80, HOROSHO, id="TC-37 89/80"),
        pytest.param(70, 70, HOROSHO, id="TC-38 70/70"),
        pytest.param(70, 69, ZACHET, id="TC-39 70/69"),
        pytest.param(69, 70, ZACHET, id="TC-40 69/70"),
        pytest.param(50, 60, ZACHET, id="TC-41 50/60"),
        pytest.param(50, 59, NEZACHET, id="TC-42 50/59"),
        pytest.param(49, 60, NEZACHET, id="TC-43 49/60"),
        pytest.param(0, 0, NEZACHET, id="TC-44 0/0"),
        pytest.param(100, 100, OTLICHNO, id="TC-45 100/100"),
    ],
)
def test_both_on_boundary(score, attendance, expected):
    assert get_result(score, attendance) == expected


# ---------------------------------------------------------------------------
# 6. Матрица классов эквивалентности: по одному представителю от класса
#    score: 25 (0-49), 60 (50-69), 80 (70-89), 95 (90-100)
#    attendance: 30 (0-59), 65 (60-69), 75 (70-79), 90 (80-100)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        pytest.param(25, 30, NEZACHET, id="M-01 25/30"),
        pytest.param(25, 65, NEZACHET, id="M-02 25/65"),
        pytest.param(25, 75, NEZACHET, id="M-03 25/75"),
        pytest.param(25, 90, NEZACHET, id="M-04 25/90"),
        pytest.param(60, 30, NEZACHET, id="M-05 60/30"),
        pytest.param(60, 65, ZACHET, id="M-06 60/65"),
        pytest.param(60, 75, ZACHET, id="M-07 60/75"),
        pytest.param(60, 90, ZACHET, id="M-08 60/90"),
        pytest.param(80, 30, NEZACHET, id="M-09 80/30"),
        pytest.param(80, 65, ZACHET, id="M-10 80/65"),
        pytest.param(80, 75, HOROSHO, id="M-11 80/75"),
        pytest.param(80, 90, HOROSHO, id="M-12 80/90"),
        pytest.param(95, 30, NEZACHET, id="M-13 95/30"),
        pytest.param(95, 65, ZACHET, id="M-14 95/65"),
        pytest.param(95, 75, HOROSHO, id="M-15 95/75"),
        pytest.param(95, 90, OTLICHNO, id="M-16 95/90"),
    ],
)
def test_equivalence_class_matrix(score, attendance, expected):
    assert get_result(score, attendance) == expected


# ---------------------------------------------------------------------------
# 7. Дробные числа (float допустим по условию isinstance(..., (int, float)))
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        pytest.param(90.0, 80.0, OTLICHNO, id="TC-46 float 90.0/80.0"),
        pytest.param(89.99, 100, HOROSHO, id="TC-47 score=89.99"),
        pytest.param(49.99, 100, NEZACHET, id="TC-48 score=49.99"),
        pytest.param(100, 79.99, HOROSHO, id="TC-49 attendance=79.99"),
        pytest.param(100, 59.99, NEZACHET, id="TC-50 attendance=59.99"),
    ],
)
def test_float_values(score, attendance, expected):
    assert get_result(score, attendance) == expected


# ---------------------------------------------------------------------------
# 8. Найденные особенности реализации (ожидаемое поведение НЕ выполняется).
#    xfail(strict=True): если дефект исправят, тест «упадёт» и напомнит
#    убрать метку xfail.
# ---------------------------------------------------------------------------
@pytest.mark.xfail(
    strict=True, reason="BUG: NaN проходит проверки диапазона и даёт «Незачёт»"
)
@pytest.mark.parametrize(
    "score, attendance, expected",
    [
        pytest.param(float("nan"), 100, BAD_SCORE, id="TC-51 score=NaN"),
        pytest.param(100, float("nan"), BAD_ATT, id="TC-52 attendance=NaN"),
    ],
)
def test_nan_should_be_invalid(score, attendance, expected):
    assert get_result(score, attendance) == expected


@pytest.mark.xfail(
    strict=True, reason="BUG: bool является подклассом int, TypeError не возникает"
)
@pytest.mark.parametrize(
    "score, attendance, message",
    [
        pytest.param(True, 80, MSG_SCORE_TYPE, id="TC-53 score=True"),
        pytest.param(90, True, MSG_ATT_TYPE, id="TC-54 attendance=True"),
    ],
)
def test_bool_should_raise_type_error(score, attendance, message):
    with pytest.raises(TypeError, match=message):
        get_result(score, attendance)
