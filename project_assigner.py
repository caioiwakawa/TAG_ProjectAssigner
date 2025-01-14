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

    def decreaseAvailability(self):
        self.availability -= 1

    def updateStudentOrder(self):
        self.enrolledStudents.sort(key=lambda student: student.grade, reverse=True)

    def enrollStudent(self, student: Student):
        if student.grade < self.minGrade:
            #print(student.code + "'s grade is too low")
            pass
        elif self.availability > 0:
            self.enrolledStudents.append(student)
            self.decreaseAvailability()
            #print("student " + student.code + " enrolled in " + self.code)
        elif student.grade > self.enrolledStudents[-1].grade:
            removed = self.enrolledStudents.pop()
            self.enrolledStudents.append(student)
            student.match()
            self.updateStudentOrder()
            #print("student " + removed.code + " removed from " + self.code)
        else:
            #print("student " + student.code + " rejected from " + self.code)
            pass

    def displayStudents(self):
        names = []
        for i in self.enrolledStudents:
            names.append(i.code)
        return names
    
def enrollStudent(project: Project, student: Student, students: list):
    if student.grade < project.minGrade:
        #print(student.code + "'s grade is too low")
        pass
    elif project.availability > 0:
        project.enrolledStudents.append(student)
        project.decreaseAvailability()
        #print("student " + student.code + " enrolled in " + self.code)
    elif student.grade > project.enrolledStudents[-1].grade:
        removed = project.enrolledStudents.pop()
        index = students.index(removed)
        students[index].unmatch()
        project.enrolledStudents.append(student)
        student.match()
        project.updateStudentOrder()
        #print("student " + removed.code + " removed from " + self.code)
    else:
        #print("student " + student.code + " rejected from " + self.code)
        pass

def main():
    students = []
    projects = []
    with open("input.txt", "r") as input:
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

    every_student_matched = False
    while(not every_student_matched):
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