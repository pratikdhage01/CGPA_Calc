class Subject:
    def _init_(self, name, credits, marks, is_125_marks):
        self.name = name
        self.credits = credits
        self.marks = marks
        self.is_125_marks = is_125_marks

    def calculate_grade_points(self):
        if self.marks <= 100:
            normalized_marks = self.marks * 100 / 125 if self.is_125_marks else self.marks
            if normalized_marks >= 90:
                return 10
            elif 80 <= normalized_marks < 90:
                return 9
            elif 70 <= normalized_marks < 80:
                return 8
            elif 60 <= normalized_marks < 70:
                return 7
            elif 50 <= normalized_marks < 60:
                return 6
            elif 40 <= normalized_marks < 50:
                return 5
            else:
                return 0
        else:
            return 0

class Semester:
    def _init_(self):
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)

    def calculate_sgpa(self):
        total_grade_points = 0
        total_credits = 0
        for subject in self.subjects:
            grade_points = subject.calculate_grade_points()
            total_grade_points += grade_points * subject.credits
            total_credits += subject.credits
        return total_grade_points / total_credits

class Student:
    def _init_(self, branch):
        self.branch = branch
        self.semester1 = Semester()
        self.semester2 = Semester()

    def add_subjects_semester1(self, subjects):
        for subject in subjects:
            self.semester1.add_subject(subject)

    def add_subjects_semester2(self, subjects):
        for subject in subjects:
            self.semester2.add_subject(subject)

    def calculate_cgpa(self):
        sgpa_sem1 = self.semester1.calculate_sgpa()
        sgpa_sem2 = self.semester2.calculate_sgpa()
        total_credits_sem1 = sum(subject.credits for subject in self.semester1.subjects)
        total_credits_sem2 = sum(subject.credits for subject in self.semester2.subjects)
        total_credits = total_credits_sem1 + total_credits_sem2
        cgpa = ((sgpa_sem1 * total_credits_sem1) + (sgpa_sem2 * total_credits_sem2)) / total_credits
        return cgpa

if __name__ == "__main__":
    print("HELLOO!!")
    branch = input("Enter your branch: ")

    subjects_sem1 = []
    subjects_sem2 = []

    option = int(input("Enter your choice (1/2/3/4/5): "))

    if option == 1:
        semester = int(input("Enter 1 for Semester 1 and 2 for Semester 2: "))
        count = int(input("Enter the count of subjects you have in this semester: "))
        
        for i in range(count):
            sub_name = input("Enter your Subject name: ")
            credits = int(input("Enter the credits you received in that subject: "))
            marks = int(input("Enter your marks in this subject: "))
            is_125_marks = input("Enter 'y' for 125 marks subject and 'n' for 50 marks subject: ").lower() == 'y'
            
            subject = Subject(sub_name, credits, marks, is_125_marks)
            if semester == 1:
                subjects_sem1.append(subject)
            else:
                subjects_sem2.append(subject)

    student = Student(branch)
    student.add_subjects_semester1(subjects_sem1)
    student.add_subjects_semester2(subjects_sem2)

    if option == 2:
        sgpa_sem1 = student.semester1.calculate_sgpa()
        print("SGPA for SEMESTER 1:", sgpa_sem1)
    elif option == 3:
        sgpa_sem2 = student.semester2.calculate_sgpa()
        print("SGPA for SEMESTER 2:", sgpa_sem2)
    elif option == 4:
        cgpa = student.calculate_cgpa()
        print("CGPA:", cgpa)
    elif option == 5:
        sgpa_sem1 = student.semester1.calculate_sgpa()
        sgpa_sem2 = student.semester2.calculate_sgpa()
        cgpa = student.calculate_cgpa()
        
        print("SEMESTER 1 SGPA:", sgpa_sem1)
        print("SEMESTER 2 SGPA:", sgpa_sem2)
        print("CGPA:", cgpa)

    print("Thank you")