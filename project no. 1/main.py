from flask import Flask,render_template,request,send_file
from flask_sqlalchemy import SQLAlchemy
import smtplib
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/thenotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FILE_LOCATION'] = 'C:\\Users\\Windows\\Desktop\\perfact project\\static'
db = SQLAlchemy(app)
class Contanct(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    pas = db.Column(db.String)
    date = db.Column(db.String)
    message = db.Column(db.String)
class Subject(db.Model):
    # index branch database
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    slug = db.Column(db.String)
    slug2 = db.Column(db.String,nullable=True)
    line = db.Column(db.String)
    by = db.Column(db.String)
    image = db.Column(db.String)
class Branchsub(db.Model):
    # subject name from branch
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    slug = db.Column(db.String)
    slug1 = db.Column(db.String)
class User(db.Model):
    # user name pas email store
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    pas = db.Column(db.String)
    email = db.Column(db.String)
class Otp1(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String)
    otp = db.Column(db.String)
class Subjectinfo(db.Model):
    # new subject data base 
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    subject = db.Column(db.String)
    image = db.Column(db.String,nullable=True)
    line = db.Column(db.String,nullable=True)
    about = db.Column(db.String)
    slug = db.Column(db.String,nullable=True)
class Sem(db.Model):
    # sno,name,slug1,slug2
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    slug1 = db.Column(db.String)
    slug2 = db.Column(db.String)
class Question(db.Model):
    # database for question
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    question = db.Column(db.String)
    slug = db.Column(db.String)
class Answer(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    answer = db.Column(db.String)
    slug = db.Column(db.String)
class Notes(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    notes = db.Column(db.String)
    by = db.Column(db.String)
    slugsub = db.Column(db.String)
    slug = db.Column(db.String)
    subjectname = db.Column(db.String)
@app.route('/')
def home():
    data = Subject.query.filter_by().all()
    return render_template('index.html',data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['Get','POST'])
def contact():
    if request.method == "POST":
        user = request.form.get('user')
        pas = request.form.get('user')
        msg = request.form.get('user')
    return render_template('contact.html')
@app.route("/sem/<string:slug>")
def sem(slug):
    data = Subject.query.filter_by(slug=slug).first()
    data2 = Sem.query.filter_by(slug2=data.slug2)
    return render_template('sem.html',slug=slug,data=data,data2=data2)
@app.route("/subject/<string:slug1>/<string:slug2>")
def subject(slug1,slug2):
    slug = slug1+slug2
    da = Subject.query.filter_by(slug=slug2).first()
    if slug1 == 'sem1':
        if slug2 == 'comp' or slug2 == 'it' or slug2 == 'civil':
            data = Branchsub.query.filter_by(slug='sem1comp').all()
            return render_template('BranchSub.html',data=data,da=da,slug1=slug1,slug2=slug2)
        else:
            data = Branchsub.query.filter_by(slug='sem2comp').all()
            return render_template('BranchSub.html',data=data,da=da,slug1=slug1,slug2=slug2)
    elif slug1 == 'sem2':
        if slug2 == 'comp' or slug2 == 'it' or slug2 == 'civil':
            data = Branchsub.query.filter_by(slug='sem2comp').all()
            return render_template('BranchSub.html',data=data,da=da,slug1=slug1,slug2=slug2)
        else:
            data = Branchsub.query.filter_by(slug='sem1comp').all()
            return render_template('BranchSub.html',data=data,da=da,slug1=slug1,slug2=slug2)
    data = Branchsub.query.filter_by(slug=slug).all()
    return render_template('BranchSub.html',data=data,da=da,slug1=slug1,slug2=slug2)
@app.route('/add')
def add():
    return render_template('sign.html',a=0)

@app.route('/submit/<string:slug>/<string:slug2>')
def submit(slug,slug2):
    return render_template('submit.html',a=0,slug=slug,slug2=slug2)

@app.route('/login/<string:slug>/<string:slug2>',methods=['GET','POST'])
def login(slug,slug2):
    if request.method == 'POST':
        user = request.form.get('username')
        pas = request.form.get('password')
        try:
            data = User.query.filter_by(username=user).first()
            if data.pas == pas:
                if slug == 'branch':
                    return render_template('subjectinfo.html',user=user,slug2=slug2)
                elif slug == 'year':
                    return render_template('branchsubadd.html',user=user,slug2=slug2,slug = 'branchsub')
                elif slug == 'question':
                    return render_template('ask.html',user = user,slug2 = slug2)
                elif slug2 == 'Notes':
                    return render_template('submitNotes.html',user = user,slug = slug)
                else:
                    return render_template('branchsubadd.html',user=user,slug2=slug2,slug=slug)
            else:
                msg = "passaword is wrong"
                return render_template('submit.html',a=1,msg=msg,slug=slug,slug2=slug2)
        except:
            msg = "This type of user dont exsist"
            return render_template('submit.html',a=1,msg=msg,slug=slug,slug2=slug2)

@app.route('/sign',methods=['GET','POST'])
def sign():
    if request.method == 'POST':
        a = 0
        try:
            email = request.form.get('email')
            content = random.uniform(100000,999999)
            content = int(content)
            content = str(content)
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login('shivammandloi1102@gmail.com','')
            server.sendmail('shivammandloi1102@gmail.com',email,content)
            con = Otp1(email=email,otp=content)
            db.session.add(con)
            db.session.commit()
            return render_template("cheack.html",email=email)
        except:
            a = 1
            msg = "Plesae enter a valid email"
            return render_template('sign.html',msg=msg,a=a)
@app.route('/cheack/<string:email>',methods=['GET','POST'])
def cheack(email):
    if request.method == 'POST':
        try:
            user_otp = request.form.get('otp')
            real_otp = Otp1.query.filter_by(email=email).first()
            user_otp = str(user_otp)
            if user_otp == real_otp.otp:
                data = Otp1.query.filter_by(email=email).first()
                db.session.delete(data)
                db.session.commit()
                return render_template('form.html',email=email)
            else:
                data = Otp1.query.filter_by(email=email).first()
                db.session.delete(data)
                db.session.commit()
                msg = "otp is wrong please enter your email once again"
                return render_template('sign.html',msg=msg,a=1)
        except:
            data = Otp1.query.filter_by(email=email).first()
            db.session.delete(data)
            db.session.commit()
            msg = "somthing is wrong"
            return render_template('sign.html',msg=msg,a=1)
@app.route('/userid/<string:email>',methods=['GET','POST'])
def userid(email):
    if request.method == 'POST':
        name = request.form.get('name')
        user = request.form.get('username')
        if " " in user:
            return render_template('form.html',a=1,msg = 'please select username without space.',email=email)
        pas = request.form.get('password')
        data = User(name=name,username=user,pas=pas,email=email)
        db.session.add(data)
        db.session.commit()
        return render_template('submit.html',a=0)
@app.route('/subjectinfo/<string:user>/<string:slug>/<string:slug2>',methods=['GET','POST'])
def subjectinfo(user,slug,slug2):
    if request.method == 'POST':
        print(slug2)
        data = User.query.filter_by(username = user).first()
        subject = request.form.get('subject')
        if slug == "branch":
            quets = request.form.get('qoutes')
            file = request.files['file']
            file.save(os.path.join(app.config['FILE_LOCATION'] , secure_filename(file.filename)))
            about = "This is for new branch"
            data1 = Subjectinfo(name = data.name,subject = subject,slug='1',username = user,image = file.filename,line=quets,about=about)
        elif slug == 'branchsub':
            about = "This is for new subject in branch"
            data1 = Subjectinfo(name = data.name,subject=subject,username=user,image='image.jpg',about=about,line='Hard work take you to ima',slug=slug2)
        elif slug == 'question':
            about = "This data is for question"
            ques = request.form.get('ques')
            data1 = Subjectinfo(name = data.name,username=user,image='image.jpg',about=about,line=ques,subject='TheNotes',slug='2')
        elif slug2 == 'notes':
            file = request.files['file']
            file.save(os.path.join(app.config['FILE_LOCATION'] , secure_filename(file.filename)))
            about = 'This is for save notes by user'
            subject = Branchsub.query.filter_by(slug1 = slug).first()
            data1 = Subjectinfo(subject = subject.name,name = file.filename,slug=slug,username = user,about=about,line='notes',image='image.jpg')
        else:
            about = 'This is for any sem subject'
            data1 = Subjectinfo(name=data.name,image='image.jpg',slug = slug2+slug,subject = subject,username = user,about=about,line='Hard work take you to ima')
        db.session.add(data1)
        db.session.commit()
        data = Subject.query.filter_by().all()
        return render_template('index.html',data=data)
@app.route('/admin')
def admin():
    return render_template('pass.html',a = 0)
@app.route('/login1',methods = ['GET','POST'])
def login1():
    pas1 = request.form.get('pas1')
    pas2 = request.form.get('pas2')
    pas3 = request.form.get('pas3')
    pas4 = request.form.get('pas4')
    if pas1 == 'ye' and pas2 == 'kya' and pas3 == 'bakchodi' and pas4 == 'he':
        return render_template('admin.html')
    elif pas1 == '1':
        data = Subjectinfo.query.filter_by().all()
        return render_template('admin.html',data=data)
    else:
        return render_template('pass.html',a = 1 ,msg = 'Soory but this only can acces by admin')
@app.route('/subject/<string:name>',methods=['GET','POST'])
def subject1(name):
    data = Subjectinfo.query.filter_by(sno=name).first()
    return render_template('sem1.html',data=data)
@app.route('/allow/<string:subject>',methods=['GET','POST'])
def allow(subject):
    if request.method == 'POST':
        data = Subjectinfo.query.filter_by(sno=subject).first()
        slug = request.form.get('slug')
        if data.slug == '2':
            data1 = Question(name = data.name,username=data.username,slug=slug,question=data.line)
            db.session.add(data1)
            db.session.commit()
            da = Subjectinfo.query.filter_by(sno=subject).first()
            db.session.delete(da)
            db.session.commit()
        elif data.line == 'notes':
            data2 = User.query.filter_by(username=data.username).first()
            data1 = Notes(notes=data.name,by=data2.name,slugsub=data.slug,slug=slug,subjectname=data.subject)
            db.session.add(data1)
            db.session.commit()
            data2 = Subjectinfo.query.filter_by(sno=subject).first()
            db.session.delete(data2)
            db.session.commit()
        elif data.slug == '1':
            slug = request.form.get('slug')
            slug1=slug
            da = Subject(name=data.subject,slug=slug,slug2=slug1,line=data.line,by=data.name,image=data.image)
            db.session.add(da)
            db.session.commit()
            data2 = Subjectinfo.query.filter_by(sno=subject).first()
            db.session.delete(data2)
            db.session.commit()
        elif data.about == 'This is for any sem subject':
            slug1 = request.form.get('slug')
            da = Branchsub(name = data.subject,slug = data.slug,slug1=slug1)
            db.session.add(da)
            db.session.commit()
            data2 = Subjectinfo.query.filter_by(sno=subject).first()
            db.session.delete(data2)
            db.session.commit()
        else:
            data1 = Sem(name=data.subject,slug1=slug,slug2=data.slug)
            db.session.add(data1)
            db.session.commit()
            data2 = Subjectinfo.query.filter_by(sno=subject).first()
            db.session.delete(data2)
            db.session.commit()
            
        data = Subjectinfo.query.filter_by().all()
        return render_template('admin.html',data=data)
@app.route('/question')
def question():
    data = Question.query.filter_by().all()
    return render_template('question.html',data=data)
@app.route('/AddNew')
def AddNew():
    return render_template()
@app.route('/answer/<string:sno>')
def answer(sno):
    data = Question.query.filter_by(slug=sno).first()
    data1 = Answer.query.filter_by(slug=sno).all()
    return render_template('ans.html',data=data,data1=data1,a=0)
@app.route('/submitAns/<string:slug>',methods=['GET','POST'])
def submitans(slug):
    if request.method == 'POST':
        user = request.form.get('user')
        pas = request.form.get('pas')
        data = Question.query.filter_by(slug=slug).first()
        data1 = Answer.query.filter_by(slug=slug).all()
        try:
            data = User.query.filter_by(username=user).first()
            if data.pas==pas:
                ans = request.form.get('ans')
                data1 = Answer(name=data.name,username=data.username,answer=ans,slug=slug)
                db.session.add(data1)
                db.session.commit()
                data = Question.query.filter_by(slug=slug).first()
                data1 = Answer.query.filter_by(slug=slug).all()
                return render_template('ans.html',data=data,data1=data1,a=0,msg="")
            else:
                data = Question.query.filter_by(slug=slug).first()
                msg = "user password is wrong"
                return render_template('ans.html',data=data,data1=data1,a=1,msg=msg)
        except:
            data = Question.query.filter_by(slug=slug).first()
            msg="username do not exist"
            return render_template('ans.html',data=data,data1=data1,a=1,msg=msg)
@app.route('/download/<string:slug>/<string:formate>')
def download(slug,formate):
    data = Branchsub.query.filter_by(slug1 = slug).first()
    if formate == 'Notes':
        try:
            data1 = Notes.query.filter_by(slugsub = slug).all()
        except:
            pass
        subject = Branchsub.query.filter_by(slug1 = slug).first()
        return render_template('notes.html',data1 = data1,why='Notes',subject = subject.name)
    if formate == 'Book':
        return send_file(f'C:\\Users\Windows\Desktop\perfact project\static\{data.book}',as_attachment=True)
@app.route('/store/<string:slug>',methods = ['GET','POST'])
def store(slug):
    data = Notes.query.filter_by(slug=slug).first()
    return send_file(f'C:\\Users\Windows\Desktop\perfact project\static\{data.notes}', as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True,port=5000)