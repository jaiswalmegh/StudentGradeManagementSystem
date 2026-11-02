
class GradeCalculator:
    """
    Handles academic grade, percentage and GPA calculations.
    """

    GRADING_SCALE = [
        {"minimum": 90, "grade": "A+", "points": 10},
        {"minimum": 80, "grade": "A", "points": 9},
        {"minimum": 70, "grade": "B", "points": 8},
        {"minimum": 60, "grade": "C", "points": 7},
        {"minimum": 50, "grade": "D", "points": 6},
        {"minimum": 0, "grade": "F", "points": 0},
    ]

    PASS_PERCENTAGE = 50.0

    @staticmethod
    def validate_marks(obtained, maximum):
        """Validate marks before performing calculations."""

        try:
            obtained = float(obtained)
            maximum = float(maximum)
        except (TypeError, ValueError):
            raise ValueError("Marks must be numeric.")

        if maximum <= 0:
            raise ValueError("Maximum marks must be positive.")

        if obtained < 0 or obtained > maximum:
            raise ValueError(
                f"Marks must be between 0 and {maximum}."
            )

        return obtained, maximum

    @staticmethod
    def calculate_total_marks(grades):
        """Calculate total obtained and maximum marks."""

        obtained_total = 0.0
        maximum_total = 0.0

        for record in grades:

            obtained, maximum = GradeCalculator.validate_marks(
                record["marks_obtained"],
                record["max_marks"]
            )

            obtained_total += obtained
            maximum_total += maximum

        return {
            "obtained_marks": round(obtained_total, 2),
            "maximum_marks": round(maximum_total, 2)
        }

    @staticmethod
    def calculate_percentage(obtained, maximum):
        """Calculate percentage."""

        obtained, maximum = GradeCalculator.validate_marks(
            obtained, maximum
        )

        return round((obtained / maximum) * 100, 2)

    @classmethod
    def get_grade_details(cls, percentage):
        """Return letter grade and grade points."""

        try:
            percentage = float(percentage)
        except (TypeError, ValueError):
            raise ValueError("Percentage must be numeric.")

        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")

        for item in cls.GRADING_SCALE:

            if percentage >= item["minimum"]:

                return {
                    "letter_grade": item["grade"],
                    "grade_points": item["points"]
                }

        return {
            "letter_grade": "F",
            "grade_points": 0
        }

    @classmethod
    def calculate_letter_grade(cls, percentage):
        """Return only the letter grade."""

        return cls.get_grade_details(
            percentage
        )["letter_grade"]

    @classmethod
    def calculate_grade_points(cls, percentage):
        """Return grade points."""

        return cls.get_grade_details(
            percentage
        )["grade_points"]

    @classmethod
    def calculate_subject_performance(cls, grades):
        """
        Calculate percentage and grade for every subject.
        """

        results = []

        for record in grades:

            obtained, maximum = cls.validate_marks(
                record["marks_obtained"],
                record["max_marks"]
            )

            percentage = cls.calculate_percentage(
                obtained,
                maximum
            )

            grade_details = cls.get_grade_details(
                percentage
            )

            result = dict(record)

            result.update({
                "marks_obtained": obtained,
                "max_marks": maximum,
                "percentage": percentage,
                "letter_grade": grade_details["letter_grade"],
                "grade_points": grade_details["grade_points"],
                "status": (
                    "Pass"
                    if percentage >= cls.PASS_PERCENTAGE
                    else "Fail"
                )
            })

            results.append(result)

        return results

    @classmethod
    def calculate_gpa(cls, grades):
        """
        Calculate credit-weighted GPA.

        GPA = Sum(Grade Points x Credits) / Sum(Credits)
        """

        if not grades:
            return 0.0

        weighted_points = 0.0
        total_credits = 0.0

        for record in grades:

            obtained, maximum = cls.validate_marks(
                record["marks_obtained"],
                record["max_marks"]
            )

            try:
                credits = float(record["credits"])
            except (KeyError, TypeError, ValueError):
                raise ValueError(
                    "Valid subject credits are required."
                )

            if credits <= 0:
                raise ValueError(
                    "Subject credits must be positive."
                )

            percentage = cls.calculate_percentage(
                obtained,
                maximum
            )

            grade_points = cls.calculate_grade_points(
                percentage
            )

            weighted_points += grade_points * credits
            total_credits += credits

        if total_credits == 0:
            return 0.0

        return round(weighted_points / total_credits, 2)

    @classmethod
    def calculate_student_performance(cls, grades):
        """
        Generate a complete performance summary
        for a student.
        """

        if not grades:

            return {
                "total_subjects": 0,
                "obtained_marks": 0,
                "maximum_marks": 0,
                "percentage": 0.0,
                "gpa": 0.0,
                "letter_grade": "N/A",
                "passed_subjects": 0,
                "failed_subjects": 0,
                "result": "No Records",
                "subject_results": []
            }

        subject_results = cls.calculate_subject_performance(
            grades
        )

        totals = cls.calculate_total_marks(
            subject_results
        )

        percentage = cls.calculate_percentage(
            totals["obtained_marks"],
            totals["maximum_marks"]
        )

        gpa = cls.calculate_gpa(subject_results)

        passed = sum(
            1 for item in subject_results
            if item["status"] == "Pass"
        )

        failed = len(subject_results) - passed

        overall_grade = cls.calculate_letter_grade(
            percentage
        )

        return {
            "total_subjects": len(subject_results),
            "obtained_marks": totals["obtained_marks"],
            "maximum_marks": totals["maximum_marks"],
            "percentage": percentage,
            "gpa": gpa,
            "letter_grade": overall_grade,
            "passed_subjects": passed,
            "failed_subjects": failed,
            "result": "Pass" if failed == 0 else "Fail",
            "subject_results": subject_results
        }
