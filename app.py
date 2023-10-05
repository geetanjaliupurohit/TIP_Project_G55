from flask import Flask,render_template,request,redirect,url_for
from flask.wrappers import Request #imported flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)#syntax to initialize app

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///BasicDetails.db"
app.config['SQLALCHEMY_BINDS']={'EducationDetails':"sqlite:///EducationDetails.db",
                                'WorkExperience':"sqlite:///WorkExperience.db",
                                'OtherDetails':"sqlite:///OtherDetails.db"}
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/timetable')
def timetable():
    return render_template('facultyTimetable.html')

    


#BASIC DETAILS TABLE
class BasicDetails(db.Model): #table column defination
    sno=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    designation=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    addressa=db.Column(db.String(100),nullable=False)
    addressb=db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    zip=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(10),nullable=False)
    relation_staus=db.Column(db.String(20),nullable=False)
    

#returns an object which prints details
    def __repr__(self) ->str:
        return f'{self.sno} - {self.first_name}'

#EDUCATION DETAILS TABLE
class EducationDetails(db.Model):
    __bind_key__ = 'EducationDetails'
    sno=db.Column(db.Integer,primary_key=True)
    sscboard=db.Column(db.String(200),nullable=False)
    sscyear=db.Column(db.String(200),nullable=False)
    sscpercent=db.Column(db.String(200),nullable=False)
    hscboard=db.Column(db.String(200),nullable=False)
    hscyear=db.Column(db.String(200),nullable=False)
    hscpercent=db.Column(db.String(200),nullable=False)
    bachelorboard=db.Column(db.String(200),nullable=False)
    bacheloryear=db.Column(db.String(200),nullable=False)
    bachelorpercent=db.Column(db.String(200),nullable=False)
    mastersboard=db.Column(db.String(200),nullable=False)
    mastersyear=db.Column(db.String(200),nullable=False)
    masterspercent=db.Column(db.String(200),nullable=False)

#returns an object which prints details
    def __repr__(self) ->str:
        return f'{self.sno} - {self.sscboard}'

#WORK EXPERIENCE TABLE
class WorkExperience(db.Model):
    __bind_key__ = 'WorkExperience'
    sno=db.Column(db.Integer,primary_key=True)
    companyName1=db.Column(db.String(200),nullable=False)
    designation1=db.Column(db.String(200),nullable=False)
    startDate1=db.Column(db.String(200),nullable=True)
    endDate1=db.Column(db.String(200),nullable=True)
    companyName2=db.Column(db.String(200),nullable=False)
    designation2=db.Column(db.String(200),nullable=False)
    startDate2=db.Column(db.String(200),nullable=True)
    endDate2=db.Column(db.String(200),nullable=True)

#returns an object which prints details
    def __repr__(self) ->str:
        return f'{self.sno} - {self.companyName1}'

#OTHER DETAILS TABLE
class OtherDetails(db.Model):
    __bind_key__ = 'OtherDetails'
    sno=db.Column(db.Integer,primary_key=True)
    Hindi_R=db.Column(db.String(200),nullable=True)
    Hindi_W=db.Column(db.String(200),nullable=True)
    Hindi_S=db.Column(db.String(200),nullable=True)
    English_R=db.Column(db.String(200),nullable=True)
    English_W=db.Column(db.String(200),nullable=True)
    English_S=db.Column(db.String(200),nullable=True)
    Gujarati_R=db.Column(db.String(200),nullable=True)
    Gujarati_W=db.Column(db.String(200),nullable=True)
    Gujarati_S=db.Column(db.String(200),nullable=True)
    PHP=db.Column(db.String(200),nullable=False)
    MySql=db.Column(db.String(200),nullable=False)
    Larvae=db.Column(db.String(200),nullable=False)
    Oracle=db.Column(db.String(200),nullable=False)
    RefName1=db.Column(db.String(200),nullable=False)
    RefContact1=db.Column(db.String(200),nullable=False)
    RefRelation1=db.Column(db.String(200),nullable=False)
    RefName2=db.Column(db.String(200),nullable=False)
    RefContact2=db.Column(db.String(200),nullable=False)
    RefRelation2=db.Column(db.String(200),nullable=False)

    #returns an object which prints details
    def __repr__(self) ->str:
        return f'{self.sno} - {self.Hindi_R}'


#Main Page
@app.route('/')#what address is the function displayed on
def IndexPage():
    return render_template('index.html')

@app.route('/MentorD')
def men():
    return render_template('MentorDetails.html')    


#BASIC DETAILS
@app.route('/BasicDetails',methods=['GET','POST'])
def BasicDetailsPage():
    if (request.method=='POST'):
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        designation=request.form['designation']
        email=request.form['email']
        addressa=request.form['addressa']
        addressb=request.form['addressb']
        city=request.form['city']
        state=request.form['state']
        zip=request.form['zip']
        gender=request.form['gender']
        relation_staus=request.form['relation_staus']
        insert= BasicDetails(first_name=first_name,last_name=last_name,designation=designation,email=email,addressa=addressa,addressb=addressb,city=city,state=state,zip=zip,gender=gender,relation_staus=relation_staus)
        db.session.add(insert)
        db.session.commit()

    allbasicDetails=BasicDetails.query.all()
    return render_template('BasicDetails.html',allbasicDetails=allbasicDetails)



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

@app.route('/UpdateBasicDetails/<int:sno>', methods=['GET', 'POST'])
def updateBasicDetails(sno):
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        designation=request.form['designation']
        email=request.form['email']
        addressa=request.form['addressa']
        addressb=request.form['addressb']
        city=request.form['city']
        state=request.form['state']
        zip=request.form['zip']
        gender=request.form.get('gender',False)
        relation_staus=request.form['relation_staus']
        insert = BasicDetails.query.filter_by(sno=sno).first()
        insert.first_name = first_name
        insert.last_name = last_name
        insert.designation=designation
        insert.email=email
        insert.addressa=addressa
        insert.addressb=addressb
        insert.city=city
        insert.state=state
        insert.zip=zip
        insert.gender=gender
        insert.relation_status=relation_staus
        
        db.session.add(insert)
        db.session.commit()
        return redirect("/BasicDetailsview")
        
    allBasicDetails = BasicDetails.query.filter_by(sno=sno).first()
    return render_template('UpdateBasicDetails.html', allBasicDetails=allBasicDetails)




#EDUCATION DETAILS 
@app.route('/EducationDetails',methods=['GET','POST'])
def EducationDetailsPage():
    if (request.method=='POST'):
        sscboard=request.form['sscboard']
        sscyear=request.form['sscyear']
        sscpercent=request.form['sscpercent']
        hscboard=request.form['hscboard']
        hscyear=request.form['hscyear']
        hscpercent=request.form['hscpercent']
        bachelorboard=request.form['bachelorboard']
        bacheloryear=request.form['bacheloryear']
        bachelorpercent=request.form['bachelorpercent']
        mastersboard=request.form['mastersboard']
        mastersyear=request.form['mastersyear']
        masterspercent=request.form['masterspercent']
        insert= EducationDetails(sscboard=sscboard,sscyear=sscyear,sscpercent=sscpercent,hscboard=hscboard,hscyear=hscyear,hscpercent=hscpercent,bachelorboard=bachelorboard,bacheloryear=bacheloryear,bachelorpercent=bachelorpercent,mastersboard=mastersboard,mastersyear=mastersyear,masterspercent=masterspercent)
        db.session.add(insert)
        db.session.commit()

    allEducationDetails=EducationDetails.query.all()
    return render_template('EducationDetails.html',allEducationDetails=allEducationDetails)

@app.route('/EducationDetailsview')
def EducationDetailsview():
    allEducationDetails = EducationDetails.query.all()#Displays repr function
    return render_template('EducationDetailsview.html',allEducationDetails=allEducationDetails)

@app.route('/DeleteEducationDetails/<int:sno>')
def deleteEducationDetails(sno):
    delete = EducationDetails.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/EducationDetailsview.html")  

@app.route('/UpdateEducationDetails/<int:sno>', methods=['GET', 'POST'])
def updateEducationDetails(sno):
    if request.method=='POST':
        sscboard=request.form['sscboard']
        sscyear=request.form['sscyear']
        sscpercent=request.form['sscpercent']
        hscboard=request.form['hscboard']
        hscyear=request.form['hscyear']
        hscpercent=request.form['hscpercent']
        bachelorboard=request.form['bachelorboard']
        bacheloryear=request.form['bacheloryear']
        bachelorpercent=request.form['bachelorpercent']
        mastersboard=request.form['mastersboard']
        mastersyear=request.form['mastersyear']
        masterspercent=request.form['masterspercent']
        insert = EducationDetails.query.filter_by(sno=sno).first()
        insert.sscboard = sscboard
        insert.sscyear = sscyear
        insert.sscpercent=sscpercent
        insert.hscboard=hscboard
        insert.hscyear=hscyear
        insert.hscpercent=hscpercent
        insert.bachelorboard=bachelorboard
        insert.bacheloryear=bacheloryear
        insert.bachelorpercent=bachelorpercent
        insert.mastersboard=mastersboard
        insert.mastersyear=mastersyear
        insert.masterspercent=masterspercent
        db.session.add(insert)
        db.session.commit()
        return redirect("/EducationDetailsview")
        
    allEducationDetails = EducationDetails.query.filter_by(sno=sno).first()
    return render_template('UpdateEducationDetails.html', allEducationDetails=allEducationDetails)


#WORK EXPERIENCE
@app.route('/WorkExperience',methods=['GET','POST'])
def WorkExperiencePage():
    if (request.method=='POST'):
        companyName1=request.form['companyName1']
        designation1=request.form['designation1']
        startDate1=request.form['startDate1']
        endDate1=request.form['endDate1']
        companyName2=request.form['companyName2']
        designation2=request.form['designation2']
        startDate2=request.form['startDate2']
        endDate2=request.form['endDate2']
        insert= WorkExperience(companyName1=companyName1,designation1=designation1,startDate1=startDate1,endDate1=endDate1,companyName2=companyName2,designation2=designation2,startDate2=startDate2,endDate2=endDate2)
        db.session.add(insert)
        db.session.commit()

    allWorkExperience=WorkExperience.query.all()
    return render_template('WorkExperience.html',allWorkExperience=allWorkExperience)

@app.route('/WorkExperienceview')
def WorkDetailsview():
    allWorkExperience = WorkExperience.query.all()#Displays repr function
    return render_template('WorkExperienceview.html',allWorkExperience=allWorkExperience)

@app.route('/deleteWorkExperience/<int:sno>')
def deleteWorkDetails(sno):
    delete = WorkExperience.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/WorkExperienceview.html")  

@app.route('/UpdateWorkExperience/<int:sno>', methods=['GET', 'POST'])
def updateWorkExperience(sno):
    if request.method=='POST':
        companyName1=request.form['companyName1']
        designation1=request.form['designation1']
        startDate1=request.form['startDate1']
        endDate1=request.form['endDate1']
        companyName2=request.form['companyName2']
        designation2=request.form['designation2']
        startDate2=request.form['startDate2']
        endDate2=request.form['endDate2']
        insert = WorkExperience.query.filter_by(sno=sno).first()
        insert.companyName1 = companyName1
        insert.designation1 = designation1
        insert.startDate1=startDate1
        insert.endDate1=endDate1
        insert.companyName2=companyName2
        insert.designation2=designation2
        insert.startDate2=startDate2
        insert.endDate2=endDate2
        db.session.add(insert)
        db.session.commit()
        return redirect("/WorkExperienceview")
        
    allWorkExpereince = WorkExperience.query.filter_by(sno=sno).first()
    return render_template('UpdateWorkExperience.html', allWorkExpereince=allWorkExpereince)


#OTHER DETAILS
@app.route('/OtherDetails',methods=['GET','POST'])
def OtherDetailsPage():
    if (request.method=='POST'):
        Hindi_R=request.form.get('Hindi_R',False)
        Hindi_W=request.form.get('Hindi_W',False)
        Hindi_S=request.form.get('Hindi_S',False)
        English_R=request.form.get('English_R',False)
        English_W=request.form.get('English_W',False)
        English_S=request.form.get('English_S',False)
        Gujarati_R=request.form.get('Gujarati_R',False)
        Gujarati_W=request.form.get('Gujarati_W',False)
        Gujarati_S=request.form.get('Gujarati_S',False)
        PHP=request.form['PHP']
        MySql=request.form['MySql']
        Larvae=request.form['Larvae']
        Oracle=request.form['Oracle']
        RefName1=request.form['RefName1']
        RefContact1=request.form['RefContact1']
        RefRelation1=request.form['RefRelation1']
        RefName2=request.form['RefName2']
        RefContact2=request.form['RefContact2']
        RefRelation2=request.form['RefRelation2']
        insert= OtherDetails(Hindi_R=Hindi_R,Hindi_W=Hindi_W,Hindi_S=Hindi_S,English_R=English_R,English_W=English_W,English_S=English_S,Gujarati_R=Gujarati_R,Gujarati_W=Gujarati_W,Gujarati_S=Gujarati_S,PHP=PHP,MySql=MySql,Larvae=Larvae,Oracle=Oracle,RefName1=RefName1,RefContact1=RefContact1,RefRelation1=RefRelation1,RefName2=RefName2,RefContact2=RefContact2,RefRelation2=RefRelation2)
        db.session.add(insert)
        db.session.commit()

    allOtherDetails=OtherDetails.query.all()
    return render_template('OtherDetails.html',allOtherDetails=allOtherDetails)

@app.route('/OtherDetailsview')
def OtherDetailsview():
    allOtherDetails = OtherDetails.query.all()#Displays repr function
    return render_template('OtherDetailsview.html',allOtherDetails=allOtherDetails)

@app.route('/DeleteOtherDetails/<int:sno>')
def deleteOtherDetails(sno):
    delete = OtherDetails.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/OtherDetailsview.html")

@app.route('/UpdateOtherDetails/<int:sno>', methods=['GET', 'POST'])
def updateOtherDetails(sno):
    if request.method=='POST':
        Hindi_R=request.form.get('Hindi_R',False)
        Hindi_W=request.form.get('Hindi_W',False)
        Hindi_S=request.form.get('Hindi_S',False)
        English_R=request.form.get('English_R',False)
        English_W=request.form.get('English_W',False)
        English_S=request.form.get('English_S',False)
        Gujarati_R=request.form.get('Gujarati_R',False)
        Gujarati_W=request.form.get('Gujarati_W',False)
        Gujarati_S=request.form.get('Gujarati_S',False)
        PHP=request.form['PHP']
        MySql=request.form['MySql']
        Larvae=request.form['Larvae']
        Oracle=request.form['Oracle']
        RefName1=request.form['RefName1']
        RefContact1=request.form['RefContact1']
        RefRelation1=request.form['RefRelation1']
        RefName2=request.form['RefName2']
        RefContact2=request.form['RefContact2']
        RefRelation2=request.form['RefRelation2']
        insert = OtherDetails.query.filter_by(sno=sno).first()
        insert.Hindi_R = Hindi_R
        insert.Hindi_W = Hindi_W
        insert.Hindi_S=Hindi_S
        insert.English_R=English_R
        insert.English_W=English_W
        insert.English_S=English_S
        insert.Gujarati_R=Gujarati_R
        insert.Gujarati_W=Gujarati_W
        insert.Gujarati_S=Gujarati_S
        insert.PHP=PHP
        insert.MySql=MySql
        insert.Larvae=Larvae
        insert.Oracle=Oracle
        insert.RefName1=RefName1
        insert.RefContact1=RefContact1
        insert.RefRelation1=RefRelation1
        insert.RefName2=RefName2
        insert.RefContact2=RefContact2
        insert.RefRelation2=RefRelation2
        db.session.add(insert)
        db.session.commit()
        return redirect("/OtherDetailsview")
        
    allOtherDetails = OtherDetails.query.filter_by(sno=sno).first()
    return render_template('UpdateOtherDetails.html', allOtherDetails=allOtherDetails)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
