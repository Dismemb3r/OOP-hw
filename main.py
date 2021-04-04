class Student:
    students_list = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.students_list.append(self)

    def mean_grade(self):
        return sum([sum(x) for x in self.grades.values()]) / len(
            [sum(x) for x in self.grades.values()])

    def lecture_score(self, lecture, course, grade):
        if isinstance(lecture, Lecture) and course in \
                self.courses_in_progress and course \
                in lecture.courses_attached:
            if course in lecture.grades:
                lecture.grades[course] += [grade]
            else:
                lecture.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Студент\nИмя: {self.name} \nФамилия: {self.surname} \n' \
               f'Средняя оценка за домашнее задание:  ' \
             f'{average_mark(sum(self.grades.values(), []))} ' \
             f'\nКурсы в процессе изучения:  ' \
             f'{", ".join(self.courses_in_progress)} ' \
             f'\nЗавершенные курсы:  {", ".join(self.finished_courses)}'

    def __lt__(self, other):
        return self.mean_grade() < other.mean_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecture(Mentor):
    lectures_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.lectures_list.append(self)

    def overall_average(self):
        average_mark(sum(self.grades.values(), []))
        return

    def mean_grade(self):
        return int(sum(self.grades)) / int(len(self.grades))

    def __str__(self):
        return f'Лектор\nИмя: {self.name}\nФамилия: {self.surname} ' \
             f'\nСредняя оценка за лекции:' \
             f'{average_mark(sum(self.grades.values(), []))}'

    def __lt__(self, other):
        return self.courses_attached < other.courses_attached


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached \
               and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return str('Рецензент\nИмя: ' + self.name + '\n' + 'Фамилия: ' +
                   self.surname)


def average_mark(marks: list):
    if marks:
        return sum(marks) / len(marks)


def mark_hw_course(students: list, course: str):
    marks_hw = []
    for student in students:
        marks_hw.append(average_mark(student.grades[course]))
    return average_mark(marks_hw)


def average_rate(lectures: list, course: str):
    marks_l = []
    for lecture in lectures:
        marks_l.append(average_mark(lecture.grades[course]))
    return average_mark(marks_l)


student_1 = Student('Вячеслав', 'Сороконожкин', 'gender')
student_1.courses_in_progress += ['Git', 'Python']
student_1.finished_courses += ['ООП: объекты и классы. '
                               'Взаимодействие между ними',
                               'Git — система контроля версий']

student_2 = Student('Алексей', 'Мешалкин', 'gender')
student_2.courses_in_progress += ['Git', 'Python']
student_2.finished_courses += ['ООП: объекты и классы. '
                               'Взаимодействие между ними',
                               'Git — система контроля версий']

expert_1 = Reviewer('Фёдор', 'Баянов')
expert_1.courses_attached += ['Git', 'Python']
expert_1.rate_hw(student_1, 'Git', 10)
expert_1.rate_hw(student_1, 'Python', 9)

expert_2 = Reviewer('Станислав', 'Стругатский')
expert_2.courses_attached += ['Git', 'Python']
expert_2.rate_hw(student_2, 'Git', 8)
expert_2.rate_hw(student_2, 'Python', 7)

Lecturer_1 = Lecture('Юрий', 'Томпсон')
Lecturer_1.courses_attached += ['Git', 'Python']
Lecturer_2 = Lecture('Константин', 'Кинг')
Lecturer_2.courses_attached += ['Git', 'Python']

student_1.lecture_score(Lecturer_1, 'Git', 8)
student_1.lecture_score(Lecturer_1, 'Python', 9)
student_2.lecture_score(Lecturer_2, 'Git', 9)
student_2.lecture_score(Lecturer_2, 'Python', 10)

print(f'{expert_1} \n\n{expert_2} \n')
print(f'{Lecturer_1} \n\n{Lecturer_2} \n')

if Lecturer_1.__lt__(Lecturer_2):
    print('Лучший лектор: ', Lecturer_1.name, Lecturer_1.surname)
else:
    print('Лучший лектор: ', Lecturer_2.name, Lecturer_2.surname)

print(f'\n{student_1} \n\n{student_2} \n')

if student_1.__lt__(student_2):
    print('Лучший студент:\n', student_2.name, student_2.surname)
else:
    print('Лучший студент: ', student_1.name, student_1.surname)

print('\n' + "Подсчет средней оценки за домашние задания по всем "
             "студентам в рамках конкретного курса:")
print('Git', (mark_hw_course(Student.students_list, 'Git')))
print('Python', (mark_hw_course(Student.students_list, 'Python')))

print('\n' + "Подсчет средней оценки за лекции всех "
             "лекторов в рамках конкретного курса:")
print('Git', (average_rate(Lecture.lectures_list, 'Git')))
print('Python', (average_rate(Lecture.lectures_list, 'Python')))
