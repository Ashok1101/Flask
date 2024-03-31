from flask import Flask,session,render_template,request
app = Flask(__name__)
app.secret_key= 'super-secret-key'
@app.rote('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session.pop('user',None)
        if request.form['password'] == 'pasword':
            session['user'] = request.form['username']
            return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)