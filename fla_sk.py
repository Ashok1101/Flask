from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
import json

with open('templates/news hour_minor/config.json', 'r') as c:
    params = json.load(c)["params"]
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/news'
db = SQLAlchemy(app)
app.secret_key = 'super-secret-key'   #require when session is created

class Sign_in(db.Model):        # class name will be table name with 1st letter capital even if it is not capital in database
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
@app.route("/about")
def about():
    return render_template('news hour_minor/about.html',params=params)

@app.route("/")
def index():
    return render_template('news hour_minor/index.html',params=params)

@app.route("/blog")
def blog():
    return render_template('news hour_minor/blog.html',params=params)

@app.route("/contact")
def contact():
    return render_template('news hour_minor/contact.html',params=params)

@app.route("/signin")
def signin():
    return render_template('news hour_minor/sign-in.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if (request.method=='POST'):
        email1 = request.form.get('email')
        password1 = request.form.get('password')
        account = Sign_in.query.filter_by(email=email1, password=password1).first()
        print(account)
        if account:
            return render_template('news hour_minor/fake_news.html',user=email1)
        elif account==None:
            return render_template('news hour_minor/sign-in.html',msg="Invalid Credentials!!!")
    return render_template('news hour_minor/sign-in.html',msg="")

@app.route("/fake_news", methods = ['GET','POST'])
def fake_news():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = Sign_in(name = name, email = email, password = password )
        db.session.add(entry)
        db.session.commit()    
        session['user']=email    # set the session variable
        user=session['user']  
    return render_template('news hour_minor/fake_news.html',user=user)

@app.route("/predict", methods = ['GET','POST'])
def predict():
    import requests,pandas as pd
    import csv,time
    from requests.api import head

    url = 'https://newsapi.org/v2/top-headlines?country=in&sortBy=top&apiKey=8b7f9fe063f74535acbc6a422d7716c7'
    response = requests.request("GET",url,data={})
    myjson = response.json()
    ourdata = []
    df=pd.read_csv('templates/news hour_minor/sample.csv')
    rows=len(df)
    c=0
    csvheader = ['title','author','description','label']
    for x in myjson['articles']:
        for y in range(0,rows):
            if df['title'][y] not in x['title']:
                c=c+1
                if c == rows:
                    listing = [x['title'],x['author'],x['description'],'REAL']
                    ourdata.append(listing)      
        c=0
    if ourdata!=[]:
        with open('templates/news hour_minor/sample.csv','a',encoding='UTF8',newline='') as f:
            writer = csv.writer(f)
            # writer.writerow(csvheader)   // for new dataset file
            writer.writerows(ourdata)



    TxtTitle = request.form.get('TxtTitle')
    TxtAuthor = request.form.get('TxtAuthor')
    TxtContent = request.form.get('TxtContent')
    # print (TxtTitle)
    for z in range(0,rows):
        if df['title'][z]== TxtTitle:
            # print(z+1,df['label'][z])
            res = z+1,df['label'][z]
            break;
        elif TxtTitle in df['title'][z]:
            # print(params['msg'])
            res = "INSUFFICIENT DATA!"
            break;
        elif z == rows-1:
            # print("MAY BE FAKE!!!")
            res = "MAY BE FAKE!!!"
        
    return render_template('news hour_minor/fake_news.html',result=res,title=TxtTitle,author=TxtAuthor,content=TxtContent)
app.run(debug=True)
