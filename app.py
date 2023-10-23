from flask import Flask,render_template,request,redirect,url_for
from flask.wrappers import Request #imported flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from twilio.rest import Client
import os
from datetime import datetime, timedelta
from sqlalchemy import text 
from sqlalchemy import func, cast
from sqlalchemy.types import Integer  # Import Integer type
from datetime import datetime, timedelta



app = Flask(__name__)#syntax to initialize app


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///BasicDetails.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#LOGIN
# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)




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




@app.route('/timetable')
def timetable():
    return render_template('facultyTimetable.html')

    


#SESSION BASIC DETAILS TABLE
class BasicDetails(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    session_id=db.Column(db.String(5), nullable=False)
    faculty_id=db.Column(db.String(5), nullable=False)
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
        faculty_id = request.form['faculty_id']
        session_id = request.form['session_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        subject = request.form['subject']
        questions = request.form['questions']
        discussion = request.form['discussion']
        date = request.form['date']
        time = request.form['time']
        NoOfStudents = request.form['NoOfStudents']

        insert = BasicDetails(faculty_id=faculty_id,session_id=session_id,first_name=first_name, last_name=last_name, email=email, subject=subject,
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


@app.route('/dashboard')
def dashboard():

    # Lecture Insights Dashboard
    today = datetime.now().date()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=6)

    # Convert date strings to actual dates for comparison
    last_week_start_str = last_week_start.strftime('%Y-%m-%d')
    last_week_end_str = last_week_end.strftime('%Y-%m-%d')

    # Number Of Lectures last Week
    lectures_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).count()

    # Average Number Of Student Last Week
    avg_students_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(func.avg(cast(BasicDetails.NoOfStudents, db.Integer))).scalar()

    # Faculties Available Last Week
    faculties_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(BasicDetails.faculty_id).distinct().count()

    # Recorded Faculty to Student Ratio
    faculty_student_ratio = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(func.round(func.sum(cast(BasicDetails.NoOfStudents, db.Integer)) / func.count(BasicDetails.faculty_id), 1)).scalar()

    ##Other Dashboard 
    # Number Of Subject Classes Last Week (total count)
    subject_classes_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).count()


    # Average Performance Last Week (Count number of questions in all)
    average_performance_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(func.sum(func.length(BasicDetails.questions) - func.length(func.replace(BasicDetails.questions, '?', ''))).label('question_count')).scalar()
    
    # If you want to calculate the average, you can divide by the total number of records
    total_records_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).count()
    
    # Avoid division by zero
    average_performance_last_week = average_performance_last_week / total_records_last_week if total_records_last_week > 0 else 0

    # Faculties Available Last Week (count)
    faculties_count_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(func.count(func.distinct(BasicDetails.faculty_id)).label('faculties_count')).scalar()

    faculty_student_ratio_last_week = BasicDetails.query.filter(BasicDetails.date.between(last_week_start_str, last_week_end_str)).with_entities(
    BasicDetails.faculty_id,
    (func.sum(cast(BasicDetails.NoOfStudents, db.Integer)) / func.count(BasicDetails.faculty_id)).label('faculty_student_ratio')
    ).group_by(BasicDetails.faculty_id).all()


    return render_template('dashboard.html',
                           lectures_last_week=lectures_last_week,
                           avg_students_last_week=avg_students_last_week,
                           faculties_last_week=faculties_last_week,
                           faculty_student_ratio=faculty_student_ratio,subject_classes_last_week=subject_classes_last_week,average_performance_last_week=average_performance_last_week,faculties_count_last_week =faculties_count_last_week,faculty_student_ratio_last_week=faculty_student_ratio_last_week)


### ATTENDANCE DETAILS AND STUDENT DETAILS 


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



@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('list_students.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    err_msg = 'Student not added'

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Create a new student record
        new_student = Student(first_name=first_name, last_name=last_name, email=email)

        # Add and commit the new student to the database
        db.session.add(new_student)
        db.session.commit()

        message = 'Student added successfully'
        return render_template('add_student.html', message=message)

    # If it's a GET request, or the form hasn't been submitted, render the form
    return render_template('add_student.html', err_msg=err_msg)

# ATTENDANCE CODE

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id=db.Column(db.String(5), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

@app.route('/take_attendance', methods=['GET', 'POST'])
def take_attendance():
    if request.method == 'POST':

        session_id = request.form['session_id']
        date_str = request.form['date']

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Loop through all students and record attendance
        students = Student.query.all()

        for student in students:
            status = request.form.get(f'attendance_{student.id}')  # Use the student ID to get individual status

            new_attendance = Attendance(date=date, status=status, student=student,session_id=session_id)
            db.session.add(new_attendance)

        # Commit the changes to the database
        db.session.commit()

        #return redirect(url_for('BasicDetailsview'))

    # Handle GET request and return a response
    students = Student.query.all()
    return render_template('take_attendance.html', students=students)

@app.route('/attendance_data')
def attendance_data():
    attendances = Attendance.query.all()
    return render_template('attendance_data.html', attendances=attendances)


@app.route('/TwilioForm',methods=['GET','POST'])
def TwilioForm():
    if request.method=="POST":
        account_sid=request.form['sid']
        auth_token=request.form['token']
        twwpfrom=request.form['wpfrom']
        twwpto=request.form['wpto']
        twmsg=request.form['msg']


        client = Client(account_sid, auth_token)

        message = client.messages \
        .create(
            body=twmsg,
            from_='whatsapp:'+twwpfrom,
            to='whatsapp:'+twwpto
        )

        print(message.sid)
        

    return render_template('TwilioForm.html')





if __name__=="__main__":
    with app.app_context():
        #db.session.execute(text("DROP TABLE IF EXISTS basic_details;"))
        #db.session.execute(text("DROP TABLE IF EXISTS Student;"))
        #db.session.execute(text("DROP TABLE IF EXISTS Attendance;"))
        db.create_all()
        print("Database tables created successfully!")
        print("Current Working Directory:", os.getcwd())
    app.run(debug=True)
