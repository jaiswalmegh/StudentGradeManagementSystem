
from datetime import datetime, date
from pathlib import Path


def format_date(value, output_format="%d %b %Y"):
    """Convert a date or datetime value into a readable string."""

    if value is None:
        return ""

    if isinstance(value, (datetime, date)):
        return value.strftime(output_format)

    if isinstance(value, str):

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y"
        ]

        for input_format in formats:

            try:
                parsed_date = datetime.strptime(
                    value,
                    input_format
                )

                return parsed_date.strftime(output_format)

            except ValueError:
                continue

    return str(value)


def calculate_percentage(obtained_marks, maximum_marks):
    """Calculate percentage safely."""

    try:
        obtained_marks = float(obtained_marks)
        maximum_marks = float(maximum_marks)

        if maximum_marks <= 0:
            return 0.0

        return round(
            (obtained_marks / maximum_marks) * 100,
            2
        )

    except (TypeError, ValueError):
        return 0.0


def safe_float(value, default=0.0):
    """Convert a value into float without raising an error."""

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    """Convert a value into integer without raising an error."""

    try:
        return int(value)

    except (TypeError, ValueError):
        return default


def format_number(value, decimal_places=2):
    """Format a numeric value with fixed decimal places."""

    try:
        return f"{float(value):,.{decimal_places}f}"

    except (TypeError, ValueError):
        return "0"


def truncate_text(text, max_length=30):
    """Shorten long text while preserving readability."""

    if text is None:
        return ""

    text = str(text)

    if len(text) <= max_length:
        return text

    if max_length <= 3:
        return "." * max_length

    return text[:max_length - 3] + "..."


def get_initials(name):
    """Generate initials from a person's name."""

    if not name or not str(name).strip():
        return ""

    words = str(name).strip().split()

    if len(words) == 1:
        return words[0][0].upper()

    return (
        words[0][0] + words[-1][0]
    ).upper()


def ensure_directory(directory_path):
    """Create a directory if it does not already exist."""

    path = Path(directory_path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def get_current_academic_session():
    """Return the current academic session in YYYY-YY format."""

    today = date.today()

    if today.month >= 7:
        start_year = today.year
    else:
        start_year = today.year - 1

    end_year = (start_year + 1) % 100

    return f"{start_year}-{end_year:02d}"


def calculate_grade_status(percentage, pass_percentage=50):
    """Return PASS or FAIL based on the percentage."""

    try:
        percentage = float(percentage)
        pass_percentage = float(pass_percentage)

        return (
            "PASS"
            if percentage >= pass_percentage
            else "FAIL"
        )

    except (TypeError, ValueError):
        return "INVALID"


def format_student_name(name):
    """Normalize student name capitalization."""

    if not name:
        return ""

    return " ".join(
        word.capitalize()
        for word in str(name).strip().split()
    )
