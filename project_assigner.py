import re

class Student:

    def __init__(self, code: str, preference: list, grade: int):
        self.code = code
        self.preference = preference
        self.grade = grade
        self.isMatched = False

    def getPreference(self):
        return self.preference.pop(0)
    
    def match(self):
        self.isMatched = True
    
    def unmatch(self):
        self.isMatched = False

    def __str__(self):
        return self.code

class Project:

    def __init__(self, code: str, availability: int, minGrade: int):
        self.code = code
        self.availability = availability
        self.minGrade = minGrade
        self.enrolledStudents = []

    def checkAvailability(self):
        if len(self.enrolledStudents) > self.availability:
            self.enrolledStudents.sort(key=lambda student: student.grade, reverse=True)
            return self.enrolledStudents.pop()
        return 0

    def displayStudents(self):
        names = []
        for i in self.enrolledStudents:
            names.append(i.code)
        return names
    
def enrollStudent(project: Project, student: Student, students: list):
    if student.grade >= project.minGrade:
        student.match()
        project.enrolledStudents.append(student)
        removed = project.checkAvailability()
        if removed and removed.code != student.code:
            print(f"{student.code} foi matriculado em {project.code}")
            print(f"{removed.code} foi removido de {project.code}")
        elif not removed:
            print(f"{student.code} foi matriculado em {project.code}")
        if removed:
            index = students.index(removed)
            students[index].unmatch()
            

def read_file(filename, students, projects):
    with open(filename, "r") as input:
        for _ in range(3):
            next(input)
        for line in input:
            if line.isspace():
                break
            data = line.strip("()\n").split(", ")
            projects.append(Project(data[0], int(data[1]), int(data[2])))
        for _ in range(2):
            next(input)
        for line in input:
            data = re.split(r'[()]', line)
            students.append(Student(data[1], data[3].split(", "), int(data[5])))
        

def main():
    students = []
    projects = []
    read_file("input.txt", students, projects)

    every_student_matched = False
    count = 1
    while(not every_student_matched):
        print(f"CICLO {count}")
        count += 1
        every_student_matched = True
        for student in students:
            if student.isMatched or student.preference == []:
                continue
            every_student_matched = False
            preference = student.getPreference()
            enrollStudent(projects[int(preference[1:]) - 1], student, students)

    for project in projects:
        print(project.displayStudents())

main()