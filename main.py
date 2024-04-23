from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Subject:
    def __init__(self, name, credits, marks, is_125_marks):
        self.name = name
        self.credits = credits
        self.marks = marks
        self.is_125_marks = is_125_marks

    def calculate_grade_points(self):
        normalized_marks = self.marks * 100 / 125 if self.is_125_marks else min(self.marks, 100)
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

class Semester:
    def __init__(self):
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
        if total_credits == 0:
            return 0
        return total_grade_points / total_credits

class Student:
    def __init__(self, branch):
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
        if total_credits == 0:
            return 0
        cgpa = ((sgpa_sem1 * total_credits_sem1) + (sgpa_sem2 * total_credits_sem2)) / total_credits 
        return cgpa

@app.route('/', methods=['GET', 'POST'])
def index():
    sgpa = None
    cgpa = None
    count = 0

    if request.method == 'POST':
        branch = request.form['branch']
        count = int(request.form.get('count', 0))

        subjects_sem1 = []
        subjects_sem2 = []

        semester = request.form.get('semester')
        if semester is not None:
            semester = int(semester)

        for i in range(count):
            sub_name = request.form.get('subject_name' + str(i))
            credits = request.form.get('credits' + str(i))
            marks = request.form.get('marks' + str(i))
            is_125_marks = request.form.get('is_125_marks' + str(i))

            if sub_name and credits and marks and is_125_marks:
                credits = int(credits)
                marks = int(marks)
                is_125_marks = is_125_marks == 'y'

                subject = Subject(sub_name, credits, marks, is_125_marks)
                if semester == 1:
                    subjects_sem1.append(subject)
                else:
                    subjects_sem2.append(subject)

        student = Student(branch)
        student.add_subjects_semester1(subjects_sem1)
        student.add_subjects_semester2(subjects_sem2)

        if request.form['action'] == 'Generate Result':
            sgpa = student.semester1.calculate_sgpa() if semester == 1 else student.semester2.calculate_sgpa()
        elif request.form['action'] == 'Generate CGPA':
            cgpa = student.calculate_cgpa()

        return redirect(url_for('result', sgpa=sgpa or 0, cgpa=cgpa or 0, count=count))

    return render_template('index.html', count=count)

@app.route('/result', methods=['GET'])
def result():
    sgpa = request.args.get('sgpa')
    cgpa = request.args.get('cgpa')
    count = int(request.args.get('count', 0))
    return render_template('result.html', sgpa=sgpa, cgpa=cgpa, count=count)

if __name__ == "__main__":
    app.run(debug=True)
