
# ==========================================================
# GRADEFLOW - APPLICATION CONSTANTS
# ==========================================================

# Application Information
APP_NAME = "GradeFlow"
APP_FULL_NAME = "Student Grade Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "GradeFlow Development Team"
APP_DESCRIPTION = (
    "A desktop application for managing student records, "
    "subjects, examination marks and academic performance."
)


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_NAME = "student_grades.db"

DATABASE_TIMEOUT = 10

DATABASE_TABLES = (
    "users",
    "students",
    "subjects",
    "grades"
)


# ==========================================================
# THEME COLORS
# ==========================================================

COLORS = {
    "background": "#101722",
    "surface": "#171D29",
    "surface_secondary": "#202B3B",
    "surface_hover": "#263448",

    "primary": "#0891B2",
    "primary_hover": "#0E7490",

    "accent": "#22D3EE",
    "accent_light": "#67E8F9",

    "text_primary": "#F1F5F9",
    "text_secondary": "#A8B3C7",
    "text_muted": "#8492A6",

    "border": "#293548",
    "border_light": "#344155",

    "success": "#34D399",
    "warning": "#FBBF24",
    "danger": "#F87171",

    "white": "#FFFFFF",
    "black": "#000000"
}


# ==========================================================
# EXAMINATION CONFIGURATION
# ==========================================================

EXAM_TYPES = [
    "Internal Assessment",
    "Mid Term",
    "End Term",
    "Practical",
    "Assignment",
    "Quiz"
]


# ==========================================================
# GRADING CONFIGURATION
# ==========================================================

PASS_PERCENTAGE = 50.0

GRADE_SCALE = [
    {
        "grade": "A+",
        "minimum_percentage": 90,
        "grade_points": 10
    },
    {
        "grade": "A",
        "minimum_percentage": 80,
        "grade_points": 9
    },
    {
        "grade": "B",
        "minimum_percentage": 70,
        "grade_points": 8
    },
    {
        "grade": "C",
        "minimum_percentage": 60,
        "grade_points": 7
    },
    {
        "grade": "D",
        "minimum_percentage": 50,
        "grade_points": 6
    },
    {
        "grade": "F",
        "minimum_percentage": 0,
        "grade_points": 0
    }
]


# ==========================================================
# UI CONFIGURATION
# ==========================================================

WINDOW_MIN_WIDTH = 1100
WINDOW_MIN_HEIGHT = 700

SIDEBAR_EXPANDED_WIDTH = 245
SIDEBAR_COLLAPSED_WIDTH = 76

HEADER_HEIGHT = 82

DEFAULT_TABLE_PAGE_SIZE = 20


# ==========================================================
# VALIDATION CONSTANTS
# ==========================================================

MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 150
MAX_ROLL_NUMBER_LENGTH = 30
MAX_SUBJECT_CODE_LENGTH = 20

MIN_SUBJECT_CREDITS = 0.1
MAX_SUBJECT_CREDITS = 100

MIN_MAXIMUM_MARKS = 1
MAX_MAXIMUM_MARKS = 10000
