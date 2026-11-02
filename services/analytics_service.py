
from collections import defaultdict

from database.connection import fetch_all, fetch_one
from services.grade_calculator import GradeCalculator


class AnalyticsService:
    """
    Provides academic analytics and dashboard statistics.
    """

    @staticmethod
    def _get_records(
        class_name=None,
        exam_type=None,
        academic_session=None
    ):
        """Fetch academic records with optional filters."""

        query = """
            SELECT
                g.grade_id,
                g.student_id,
                g.subject_id,
                g.marks_obtained,
                g.exam_type,
                g.academic_session,

                s.roll_number,
                s.name AS student_name,
                s.class_name,
                s.section,

                sub.subject_code,
                sub.subject_name,
                sub.max_marks,
                sub.credits

            FROM grades g

            INNER JOIN students s
                ON g.student_id = s.student_id

            INNER JOIN subjects sub
                ON g.subject_id = sub.subject_id

            WHERE 1 = 1
        """

        parameters = []

        if class_name and class_name.strip():
            query += " AND s.class_name = ?"
            parameters.append(class_name.strip())

        if exam_type and exam_type.strip():
            query += " AND g.exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session and academic_session.strip():
            query += " AND g.academic_session = ?"
            parameters.append(academic_session.strip())

        query += " ORDER BY s.name ASC, sub.subject_name ASC"

        rows = fetch_all(query, tuple(parameters))

        return [dict(row) for row in rows]

    @staticmethod
    def _group_by_student(records):
        """Group academic records by student."""

        grouped = defaultdict(list)

        for record in records:
            grouped[record["student_id"]].append(record)

        return grouped

    @staticmethod
    def _calculate_student_results(records):
        """Calculate performance for every student."""

        grouped = AnalyticsService._group_by_student(records)

        results = []

        for student_id, student_records in grouped.items():

            first_record = student_records[0]

            performance = GradeCalculator.calculate_student_performance(
                student_records
            )

            results.append({
                "student_id": student_id,
                "roll_number": first_record["roll_number"],
                "student_name": first_record["student_name"],
                "class_name": first_record["class_name"],
                "section": first_record["section"],
                **performance
            })

        return results

    @staticmethod
    def get_dashboard_summary(
        class_name=None,
        exam_type=None,
        academic_session=None
    ):
        """Generate the main dashboard statistics."""

        total_students_row = fetch_one("""
            SELECT COUNT(*) AS total
            FROM students
        """)

        total_subjects_row = fetch_one("""
            SELECT COUNT(*) AS total
            FROM subjects
        """)

        total_students = (
            total_students_row["total"]
            if total_students_row else 0
        )

        total_subjects = (
            total_subjects_row["total"]
            if total_subjects_row else 0
        )

        records = AnalyticsService._get_records(
            class_name,
            exam_type,
            academic_session
        )

        student_results = (
            AnalyticsService._calculate_student_results(records)
        )

        total_entries = len(records)

        if not student_results:

            return {
                "total_students": total_students,
                "total_subjects": total_subjects,
                "students_with_results": 0,
                "total_grade_entries": 0,
                "class_average": 0.0,
                "highest_percentage": 0.0,
                "lowest_percentage": 0.0,
                "pass_percentage": 0.0,
                "passed_students": 0,
                "failed_students": 0,
                "top_performer": None,
                "lowest_performer": None,
                "grade_distribution": {},
            }

        percentages = [
            item["percentage"]
            for item in student_results
        ]

        passed_students = sum(
            1 for item in student_results
            if item["result"] == "Pass"
        )

        failed_students = (
            len(student_results) - passed_students
        )

        class_average = sum(percentages) / len(percentages)

        top_performer = max(
            student_results,
            key=lambda item: item["percentage"]
        )

        lowest_performer = min(
            student_results,
            key=lambda item: item["percentage"]
        )

        grade_distribution = (
            AnalyticsService.get_grade_distribution(
                class_name,
                exam_type,
                academic_session
            )
        )

        return {
            "total_students": total_students,
            "total_subjects": total_subjects,
            "students_with_results": len(student_results),
            "total_grade_entries": total_entries,
            "class_average": round(class_average, 2),
            "highest_percentage": round(max(percentages), 2),
            "lowest_percentage": round(min(percentages), 2),
            "pass_percentage": round(
                (passed_students / len(student_results)) * 100,
                2
            ),
            "passed_students": passed_students,
            "failed_students": failed_students,
            "top_performer": {
                "name": top_performer["student_name"],
                "roll_number": top_performer["roll_number"],
                "percentage": top_performer["percentage"],
                "gpa": top_performer["gpa"]
            },
            "lowest_performer": {
                "name": lowest_performer["student_name"],
                "roll_number": lowest_performer["roll_number"],
                "percentage": lowest_performer["percentage"],
                "gpa": lowest_performer["gpa"]
            },
            "grade_distribution": grade_distribution
        }

    @staticmethod
    def get_grade_distribution(
        class_name=None,
        exam_type=None,
        academic_session=None
    ):
        """Calculate the distribution of subject letter grades."""

        records = AnalyticsService._get_records(
            class_name,
            exam_type,
            academic_session
        )

        distribution = {
            "A+": 0,
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0
        }

        for record in records:

            percentage = GradeCalculator.calculate_percentage(
                record["marks_obtained"],
                record["max_marks"]
            )

            letter_grade = GradeCalculator.calculate_letter_grade(
                percentage
            )

            distribution[letter_grade] += 1

        return distribution

    @staticmethod
    def get_subject_performance(
        class_name=None,
        exam_type=None,
        academic_session=None
    ):
        """Calculate average performance for each subject."""

        records = AnalyticsService._get_records(
            class_name,
            exam_type,
            academic_session
        )

        grouped = defaultdict(list)

        for record in records:
            grouped[record["subject_id"]].append(record)

        results = []

        for subject_id, subject_records in grouped.items():

            first_record = subject_records[0]

            obtained_total = sum(
                item["marks_obtained"]
                for item in subject_records
            )

            maximum_total = sum(
                item["max_marks"]
                for item in subject_records
            )

            average_marks = (
                obtained_total / len(subject_records)
            )

            average_percentage = (
                (obtained_total / maximum_total) * 100
                if maximum_total else 0
            )

            results.append({
                "subject_id": subject_id,
                "subject_code": first_record["subject_code"],
                "subject_name": first_record["subject_name"],
                "average_marks": round(average_marks, 2),
                "average_percentage": round(
                    average_percentage, 2
                ),
                "student_count": len(subject_records)
            })

        return sorted(
            results,
            key=lambda item: item["average_percentage"],
            reverse=True
        )

    @staticmethod
    def get_top_performers(
        limit=5,
        class_name=None,
        exam_type=None,
        academic_session=None
    ):
        """Return top-performing students."""

        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        records = AnalyticsService._get_records(
            class_name,
            exam_type,
            academic_session
        )

        results = AnalyticsService._calculate_student_results(
            records
        )

        results.sort(
            key=lambda item: (
                item["percentage"],
                item["gpa"]
            ),
            reverse=True
        )

        return results[:limit]

    @staticmethod
    def get_class_performance(
        exam_type=None,
        academic_session=None
    ):
        """Compare academic performance across classes."""

        rows = fetch_all("""
            SELECT DISTINCT class_name
            FROM students
            ORDER BY class_name
        """)

        results = []

        for row in rows:

            class_name = row["class_name"]

            summary = AnalyticsService.get_dashboard_summary(
                class_name=class_name,
                exam_type=exam_type,
                academic_session=academic_session
            )

            results.append({
                "class_name": class_name,
                "total_students": summary["total_students"],
                "students_with_results": summary[
                    "students_with_results"
                ],
                "class_average": summary["class_average"],

                # Compatibility key used by AnalyticsPage.
                "average_percentage": summary["class_average"],

                "pass_percentage": summary["pass_percentage"],
                "highest_percentage": summary[
                    "highest_percentage"
                ]
            })

        return results

    @staticmethod
    def get_student_analytics(
        student_id,
        exam_type=None,
        academic_session=None
    ):
        """Return detailed analytics for one student."""

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID.")

        student = fetch_one("""
            SELECT *
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        if student is None:
            raise ValueError("Student record not found.")

        query = """
            SELECT
                g.grade_id,
                g.student_id,
                g.subject_id,
                g.marks_obtained,
                g.exam_type,
                g.academic_session,
                sub.subject_code,
                sub.subject_name,
                sub.max_marks,
                sub.credits

            FROM grades g

            INNER JOIN subjects sub
                ON g.subject_id = sub.subject_id

            WHERE g.student_id = ?
        """

        parameters = [student_id]

        if exam_type and exam_type.strip():
            query += " AND g.exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session and academic_session.strip():
            query += " AND g.academic_session = ?"
            parameters.append(academic_session.strip())

        query += " ORDER BY sub.subject_name"

        records = [
            dict(row)
            for row in fetch_all(query, tuple(parameters))
        ]

        performance = GradeCalculator.calculate_student_performance(
            records
        )

        return {
            "student": dict(student),
            "performance": performance
        }
