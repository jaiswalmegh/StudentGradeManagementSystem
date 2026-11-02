
# GradeFlow - Student Grade Management System

GradeFlow is a desktop-based Student Grade Management System developed using Python and PyQt5. It provides a centralized platform to manage student records, academic subjects, examination marks and academic performance.

The application uses SQLite for data storage and integrates Pandas and Matplotlib for academic analytics and visualization.

---

## Features

### 1. Student Management
- Add new student records.
- Update student information.
- Delete student records.
- Search students by name, roll number or email.
- Filter students by class.
- Manage student details including roll number, email and section.

### 2. Subject Management
- Add and manage academic subjects.
- Assign unique subject codes.
- Configure maximum marks.
- Configure subject credits.
- Edit and delete subject records.
- Search subjects by name or code.

### 3. Marks Management
- Record examination marks.
- Associate students with subjects.
- Manage different examination types.
- Maintain academic session records.
- Update and delete marks.
- Calculate obtained marks percentages.
- Prevent marks from exceeding maximum marks.

### 4. Grade Calculation
- Automatic percentage calculation.
- Letter grade assignment.
- Grade point calculation.
- Credit-weighted GPA calculation.
- Pass and fail status evaluation.
- Individual student performance summaries.

### 5. Academic Analytics
- Overall academic performance overview.
- Class performance analysis.
- Subject-wise performance comparison.
- Grade distribution visualization.
- Top performer identification.
- Academic statistics and graphical reports.

### 6. Admin Interface
- Dedicated administrator login interface.
- Dark-themed desktop interface.
- Sidebar-based navigation.
- Centralized application dashboard.
- Reusable tables and UI components.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| PyQt5 | Desktop application interface |
| SQLite | Database management |
| Pandas | Data processing |
| Matplotlib | Charts and visualizations |
| QtAwesome | Icon support |

---

## Project Structure

```text
StudentGradeManagementSystem/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── db_setup.py
│   └── student_grades.db
│
├── models/
│   ├── __init__.py
│   ├── student.py
│   ├── subject.py
│   └── grade.py
│
├── controllers/
│   ├── __init__.py
│   ├── student_controller.py
│   ├── subject_controller.py
│   └── grade_controller.py
│
├── services/
│   ├── __init__.py
│   ├── grade_calculator.py
│   ├── analytics_service.py
│   └── report_service.py
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── dashboard.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── header.py
│   │   ├── stat_card.py
│   │   └── data_table.py
│   │
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── students_page.py
│   │   ├── subjects_page.py
│   │   ├── marks_page.py
│   │   └── analytics_page.py
│   │
│   └── dialogs/
│       ├── __init__.py
│       ├── login_dialog.py
│       ├── add_student_dialog.py
│       ├── edit_student_dialog.py
│       └── marks_dialog.py
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── styles/
│       └── dark_theme.qss
│
└── utils/
    ├── __init__.py
    ├── constants.py
    ├── validators.py
    └── helpers.py
```

---

## Installation and Setup

### Prerequisites

- Python 3.10 or above
- pip package manager

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Directory

```bash
cd StudentGradeManagementSystem
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python main.py
```

---

## Database

GradeFlow uses SQLite as its database engine.

The database manages the following entities:

- Users
- Students
- Subjects
- Grades

Database tables use primary keys, foreign key relationships and constraints to maintain data integrity.

The database setup module handles table creation and schema initialization.

---

## Application Design

The application follows a modular architecture:

- **Models:** Define the application's data structures.
- **Controllers:** Handle database operations and business logic.
- **Services:** Manage grade calculations and academic analytics.
- **UI:** Provides the desktop interface and navigation.
- **Database:** Handles persistent data storage.
- **Utilities:** Provide reusable validation and helper functions.

---

## Future Enhancements

- Advanced academic reporting.
- Downloadable academic reports.
- Additional performance comparison tools.
- Enhanced administrator management.
- More detailed student performance insights.

---

## Project Information

**Project Name:** GradeFlow  
**Project Type:** Desktop Application  
**Domain:** Student and Academic Management  
**Language:** Python  
**Interface:** PyQt5  
**Database:** SQLite  
**Version:** 1.0.0

---

## License

This project is developed for educational and academic purposes.
