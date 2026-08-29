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


# Пример использования
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

student.rate_lecture(lecturer, 'Python', 7)
student.grades['Python'] = [8, 9, 10]  # пример оценок за ДЗ

print(reviewer)
# Имя: Пётр
# Фамилия: Петров

print(lecturer)
# Имя: Иван
# Фамилия: Иванов
# Средняя оценка за лекции: 7.0

print(student)
# Имя: Алёхина
# Фамилия: Ольга
# Средняя оценка за домашние задания: 9.0
# Курсы в процессе изучения: Python, Java
# Завершенные курсы:

# Сравнение
lecturer2 = Lecturer('Анна', 'Смирнова')
lecturer2.grades = {'Python': [9, 10, 10]}
print(lecturer < lecturer2)  # True

student2 = Student('Борис', 'Борисов', 'М')
student2.grades = {'Java': [7, 7, 7]}
print(student > student2)    # True