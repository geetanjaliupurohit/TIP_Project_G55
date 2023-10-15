from flask import Flask,render_template,request,redirect,url_for
from flask.wrappers import Request #imported flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os






app = Flask(__name__)#syntax to initialize app



app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///BasicDetails.db"
#app.config['SQLALCHEMY_BINDS']={'EducationDetails':"sqlite:///EducationDetails.db",
#                                'WorkExperience':"sqlite:///WorkExperience.db",
#                                'OtherDetails':"sqlite:///OtherDetails.db"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#LOGIN
# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    print("Current Working Directory:", os.getcwd())



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the entered username and password match the predefined values
        if username == "username" and password == "password":
            # Authentication successful, redirect to a protected page
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed, display an error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/timetable')
def timetable():
    return render_template('facultyTimetable.html')

    


#SESSION BASIC DETAILS TABLE
class BasicDetails(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    questions = db.Column(db.String(100), nullable=False)
    discussion = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False) 
    time = db.Column(db.String(5), nullable=False) 
    NoOfStudents = db.Column(db.Integer, nullable=False)
    

#returns an object which prints details
    def __repr__(self) ->str:
        return f'{self.sno} - {self.first_name}'


#Main Page
@app.route('/')#what address is the function displayed on
def IndexPage():
    return render_template('index.html')



#BASIC DETAILS

from flask import render_template, request

@app.route('/BasicDetails', methods=['GET', 'POST'])
def BasicDetailsPage():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        subject = request.form['subject']
        questions = request.form['questions']
        discussion = request.form['discussion']
        date = request.form['date']
        time = request.form['time']
        NoOfStudents = request.form['NoOfStudents']

        insert = BasicDetails(first_name=first_name, last_name=last_name, email=email, subject=subject,
                              questions=questions, discussion=discussion, date=date, time=time,
                              NoOfStudents=NoOfStudents)

        db.session.add(insert)
        db.session.commit()

    all_basic_details = BasicDetails.query.all()
    return render_template('BasicDetails.html', allbasicDetails=all_basic_details)







@app.route('/BasicDetailsview')
def BasicDetailsview():
    allBasicDetails = BasicDetails.query.all()#Displays repr function
    return render_template('BasicDetailsview.html',allBasicDetails=allBasicDetails)


@app.route('/DeleteBasicDetails/<int:sno>')
def deleteBasicDetails(sno):
    delete = BasicDetails.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/BasicDetailsview")

from flask import render_template, request, redirect

@app.route('/UpdateBasicDetails/<int:sno>', methods=['GET', 'POST'])
def updateBasicDetails(sno):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        subject = request.form['subject']
        questions = request.form['questions']
        discussion = request.form['discussion']
        date = request.form['date']
        time = request.form['time']
        NoOfStudents = request.form['NoOfStudents']

        insert = BasicDetails.query.filter_by(sno=sno).first()
        insert.first_name = first_name
        insert.last_name = last_name
        insert.email = email
        insert.subject = subject
        insert.questions = questions
        insert.discussion = discussion
        insert.date = date
        insert.time = time
        insert.NoOfStudents = NoOfStudents

        db.session.add(insert)
        db.session.commit()
        return redirect("/BasicDetailsview")

    all_basic_details = BasicDetails.query.filter_by(sno=sno).first()
    return render_template('UpdateBasicDetails.html', allBasicDetails=all_basic_details)


# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # Add other student details as needed

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Student(id={self.id}, name={self.full_name()}, email={self.email})'


@app.route('/add_student')
def render_add_student():
    return render_template('add_student.html')



@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('list_students.html', students=students)



# Add a new route to handle the form submission and add student to the database
@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Create a new student record
        new_student = Student(first_name=first_name, last_name=last_name, email=email)

        # Add and commit the new student to the database
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('index'))  # You can redirect to any page after adding the student

    return render_template('add_student.html')  # Render the form again if the request is not POST

# ATTENDANCE CODE

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

@app.route('/take_attendance', methods=['GET', 'POST'])
def take_attendance():
    if request.method == 'POST':
        date_str = request.form['date']

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Loop through all students and record attendance
        students = Student.query.all()

        for student in students:
            status = request.form.get(f'attendance_{student.id}')  # Use the student ID to get individual status

            new_attendance = Attendance(date=date, status=status, student=student)
            db.session.add(new_attendance)

        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for('BasicDetailsview'))

    # Handle GET request and return a response
    students = Student.query.all()
    return render_template('take_attendance.html', students=students)

@app.route('/attendance_data')
def attendance_data():
    attendances = Attendance.query.all()
    return render_template('attendance_data.html', attendances=attendances)








if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
