class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}  # {course: [list of grades]}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise TypeError("Оценивать можно только лекторов (Lecturer).")
        if course not in lecturer.courses_attached:
            raise ValueError(f"Лектор не ведёт курс '{course}'.")
        if course not in self.courses_in_progress:
            raise ValueError(f"Студент не учится на курсе '{course}'.")
        if not (0 <= grade <= 10):
            raise ValueError("Оценка должна быть в диапазоне от 0 до 10.")

        if course not in lecturer.grades:
            lecturer.grades[course] = []
        lecturer.grades[course].append(grade)

        return None

    def _average_grade(self):
        """Вычисляет среднюю оценку за домашние задания."""
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0.0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        courses_in_progress_str = ", ".join(self.courses_in_progress) if self.courses_in_progress else ""
        finished_courses_str = ", ".join(self.finished_courses) if self.finished_courses else ""
        avg = self._average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg:.1f}\n"
            f"Курсы в процессе изучения: {courses_in_progress_str}\n"
            f"Завершенные курсы: {finished_courses_str}"
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() <= other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # {course: [list of grades]}

    def _average_lecture_grade(self):
        """Средняя оценка за лекции (по всем курсам)."""
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0.0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg = self._average_lecture_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg:.1f}"
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_lecture_grade() < other._average_lecture_grade()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_lecture_grade() <= other._average_lecture_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_lecture_grade() == other._average_lecture_grade()


class Reviewer(Mentor):
    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# --- Функции для подсчёта средних оценок по курсу ---

def average_student_grade_by_course(students, course):
    """
    Считает среднюю оценку за ДЗ по конкретному курсу среди списка студентов.
    :param students: список объектов Student
    :param course: название курса (строка)
    :return: float (средняя оценка) или 0.0, если оценок нет
    """
    all_grades = []
    for student in students:
        if course in student.grades and student.grades[course]:
            all_grades.extend(student.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


def average_lecturer_grade_by_course(lecturers, course):
    """
    Считает среднюю оценку за лекции по конкретному курсу среди списка лекторов.
    :param lecturers: список объектов Lecturer
    :param course: название курса (строка)
    :return: float (средняя оценка) или 0.0, если оценок нет
    """
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades and lecturer.grades[course]:
            all_grades.extend(lecturer.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


# --- Создание экземпляров (по 2 каждого класса) ---

# Студенты
student1 = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Борис', 'Борисов', 'М')

# Лекторы
lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Анна', 'Смирнова')

# Проверяющие
reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Елена', 'Ельцова')

# --- Настройка курсов ---

student1.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'C++']

lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'Java']

reviewer1.courses_attached += ['Python', 'Java']
reviewer2.courses_attached += ['C++', 'Python']

# --- Выставление оценок за ДЗ (имитация работы Reviewer) ---
# У нас нет метода rate_homework в классах, но мы можем напрямую положить оценки,
# чтобы продемонстрировать работу функции average_student_grade_by_course.
student1.grades['Python'] = [8, 9, 10]
student1.grades['Java'] = [7, 8]

student2.grades['Python'] = [6, 7, 8]
student2.grades['C++'] = [9, 10]

# --- Выставление оценок студентам за лекции (через student.rate_lecture) ---
student1.rate_lecture(lecturer1, 'Python', 7)
student1.rate_lecture(lecturer2, 'Java', 8)

student2.rate_lecture(lecturer1, 'C++', 9)
student2.rate_lecture(lecturer1, 'Python', 8)
student2.rate_lecture(lecturer2, 'Python', 10)

# --- Демонстрация __str__ ---
print("=== Student 1 ===")
print(student1)
print("\n=== Student 2 ===")
print(student2)

print("\n=== Lecturer 1 ===")
print(lecturer1)
print("\n=== Lecturer 2 ===")
print(lecturer2)

print("\n=== Reviewer 1 ===")
print(reviewer1)
print("\n=== Reviewer 2 ===")
print(reviewer2)

# --- Демонстрация сравнений (полиморфизм через магические методы) ---
print("\n=== Сравнение студентов ===")
print(f"student1 < student2: {student1 < student2}")
print(f"student1 == student2: {student1 == student2}")

print("\n=== Сравнение лекторов ===")
print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")
print(f"lecturer1 == lecturer2: {lecturer1 == lecturer2}")

# --- Демонстрация функций подсчёта средних по курсу ---
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]

avg_python_students = average_student_grade_by_course(students_list, 'Python')
avg_java_students = average_student_grade_by_course(students_list, 'Java')
avg_cpp_students = average_student_grade_by_course(students_list, 'C++')

avg_python_lecturers = average_lecturer_grade_by_course(lecturers_list, 'Python')
avg_java_lecturers = average_lecturer_grade_by_course(lecturers_list, 'Java')
avg_cpp_lecturers = average_lecturer_grade_by_course(lecturers_list, 'C++')

print("\n=== Средние оценки по курсам (студенты) ===")
print(f"Python: {avg_python_students:.2f}")
print(f"Java: {avg_java_students:.2f}")
print(f"C++: {avg_cpp_students:.2f}")

print("\n=== Средние оценки по курсам (лекторы) ===")
print(f"Python: {avg_python_lecturers:.2f}")
print(f"Java: {avg_java_lecturers:.2f}")
print(f"C++: {avg_cpp_lecturers:.2f}")