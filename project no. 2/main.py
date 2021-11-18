from flask import Flask,render_template,request
import mysql.connector

mydb = mysql.connector.connect(host="localhost",port=3306,user="root",passwd="",database="nerdalert")
mycr = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/email/<string:slug>/<string:slug1>')
def email(slug,slug1):
    return render_template('email.html',slug=slug,slug1=slug1)

@app.route('/otp/<string:slug>/<string:slug1>',methods=['POST','GET'])
def otp(slug,slug1):
    if request.method == 'POST':
        email = request.form.get('email')
        return render_template('otp.html',slug=slug,slug1=slug1,email=email)
    else:
        return render_template('home.html')

@app.route('/import',methods=['POST','GET'])
def impot():
    return render_template('import.html')

@app.route('/book')
def book():
    mycr.execute("select * from book")
    li = []
    for i in mycr:
        li.append(i)
    return render_template('book.html',data = li)

@app.route('/rating/<string:slug>')
def rating(slug):
    sql = 'select * from rating where slug = %s'
    slg = (slug,)
    mycr.execute(sql,slg)
    li = []
    for i in mycr:
        li.append(i)
    try:
        sql = 'select * from comment where slug = %s'
        slg = (slug,)
        mycr.execute(sql,slg)
        li1 = []
        for i in mycr:
            li1.append(i)
    except:
        li1 = []
    return render_template('rating.html',data=li,data1=li1)

@app.route('/rate/<string:slug>/<string:email>',methods=['GET','POST'])
def rate(slug,email):
    if request.method == 'POST':
        return render_template('rate.html',slug=slug,email=email)
    else:
        return render_template('home.html')

@app.route('/rate-book/<string:slug>/<string:email>',methods=['POST','GET'])
def ratebook(slug,email):
    if request.method == 'POST':
        f_name = request.form.get('fname')
        l_name = request.form.get("lname")
        msg = request.form['msg']
        submit = int(request.form['sub'])
        sql = 'insert into comment(fname,lname,msg,star,slug,email) values(%s,%s,%s,%s,%s,%s)'
        data = (f_name,l_name,msg,submit,slug,email)
        mycr.execute(sql,data)
        mydb.commit()
        sql = 'select * from rating where slug = %s'
        slg = (slug,)
        mycr.execute(sql,slg)
        li = []
        for i in mycr:
            li.append(i)
        try:
            sql = 'select * from comment where slug = %s'
            slg = (slug,)
            mycr.execute(sql,slg)
            li1 = []
            for i in mycr:
                li1.append(i)
        except:
            li1 = []
        return render_template('rating.html',data=li,data1=li1)
    else:
        return render_template('home.html')
        
app.run(debug=True)