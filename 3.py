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
    def rate_homework(self, student, course, grade):
        """Выставить оценку за ДЗ. Метод доступен только у Reviewer."""
        if not isinstance(student, Student):
            raise TypeError("Оценивать можно только студентов (Student).")
        if course not in self.courses_attached:
            raise ValueError(f"Reviewer не закреплён за курсом '{course}'.")
        if course not in student.courses_in_progress:
            raise ValueError(f"Студент не учится на курсе '{course}'.")
        if not (0 <= grade <= 10):
            raise ValueError("Оценка должна быть в диапазоне от 0 до 10.")

        if course not in student.grades:
            student.grades[course] = []
        student.grades[course].append(grade)
        return None

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# --- Функции для подсчёта средних оценок по курсу ---

def average_student_grade_by_course(students, course):
    all_grades = []
    for student in students:
        if course in student.grades and student.grades[course]:
            all_grades.extend(student.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


def average_lecturer_grade_by_course(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades and lecturer.grades[course]:
            all_grades.extend(lecturer.grades[course])
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


# --- Создание экземпляров (по 2 каждого класса) ---

student1 = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Борис', 'Борисов', 'М')

lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Анна', 'Смирнова')

reviewer1 = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Елена', 'Ельцова')

# --- Настройка курсов ---

student1.courses_in_progress += ['Python', 'Java']
student2.courses_in_progress += ['Python', 'C++']
student1.finished_courses += ['Введение в программирование']
student2.finished_courses += ['Введение в программирование', 'Git']

lecturer1.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'Java']

reviewer1.courses_attached += ['Python', 'Java']
reviewer2.courses_attached += ['C++', 'Python']

# --- Reviewer выставляет оценки за ДЗ ---

reviewer1.rate_homework(student1, 'Python', 8)
reviewer1.rate_homework(student1, 'Python', 9)
reviewer1.rate_homework(student1, 'Python', 10)
reviewer1.rate_homework(student1, 'Java', 7)
reviewer1.rate_homework(student1, 'Java', 8)

reviewer1.rate_homework(student2, 'Python', 6)
reviewer1.rate_homework(student2, 'Python', 7)
reviewer1.rate_homework(student2, 'Python', 8)

reviewer2.rate_homework(student2, 'C++', 9)
reviewer2.rate_homework(student2, 'C++', 10)

# --- Студенты оценивают лекторов ---

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

# --- Демонстрация сравнений ---

print("\n=== Сравнение студентов ===")
print(f"student1 < student2: {student1 < student2}")
print(f"student1 == student2: {student1 == student2}")
print(f"student1 > student2: {student1 > student2}")

print("\n=== Сравнение лекторов ===")
print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")
print(f"lecturer1 == lecturer2: {lecturer1 == lecturer2}")
print(f"lecturer1 > lecturer2: {lecturer1 > lecturer2}")

# --- Функции подсчёта средних по курсу ---

students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]

print("\n=== Средние оценки по курсам (студенты) ===")
print(f"Python: {average_student_grade_by_course(students_list, 'Python'):.2f}")
print(f"Java:   {average_student_grade_by_course(students_list, 'Java'):.2f}")
print(f"C++:    {average_student_grade_by_course(students_list, 'C++'):.2f}")

print("\n=== Средние оценки по курсам (лекторы) ===")
print(f"Python: {average_lecturer_grade_by_course(lecturers_list, 'Python'):.2f}")
print(f"Java:   {average_lecturer_grade_by_course(lecturers_list, 'Java'):.2f}")
print(f"C++:    {average_lecturer_grade_by_course(lecturers_list, 'C++'):.2f}")

# --- Случаи отказа (недопустимые действия) ---

print("\n=== Случаи отказа ===")

# 1. Reviewer пытается оценить курс, за которым не закреплён
try:
    reviewer1.rate_homework(student2, 'C++', 5)
except ValueError as e:
    print(f"Отказ: {e}")

# 2. Reviewer пытается оценить студента за курс, который тот не изучает
try:
    reviewer2.rate_homework(student1, 'C++', 5)
except ValueError as e:
    print(f"Отказ: {e}")

# 3. Студент пытается оценить лектора, который не ведёт курс
try:
    student1.rate_lecture(lecturer1, 'Java', 10)
except ValueError as e:
    print(f"Отказ: {e}")

# 4. Студент пытается оценить лектора за курс, который сам не изучает
try:
    student1.rate_lecture(lecturer2, 'C++', 10)
except ValueError as e:
    print(f"Отказ: {e}")

# 5. Попытка использовать rate_lecture на Reviewer (не Lecturer)
try:
    student1.rate_lecture(reviewer1, 'Python', 5)
except TypeError as e:
    print(f"Отказ: {e}")

# 6. Попытка использовать rate_homework на Lecturer (не Reviewer)
try:
    lecturer1.rate_homework(student1, 'Python', 5)
except AttributeError as e:
    print(f"Отказ: у Lecturer нет метода rate_homework — {e}")