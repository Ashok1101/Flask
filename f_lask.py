from flask import Flask, render_template

app = Flask(__name__) # making a variable named ‘app’ which takes a string argument
# app = Flask(“filename”) 
print(type(app))
print(app)

@app.route("/")    # route is a decorator
def hello_world():
    return "<p>Hello, World!</p>"
# app.run()    # to execute
@app.route("/arvind")
def hello_arvind():
    return "<p>Hello, Arvindab!</p>"
# app.run(debug=True)   # 'debug=True'--> it is used to automatically restart the app whenever we make changes

@app.route("/about")
def about():
    name = "rohan das"
    return render_template('about.html', name2 = name)

@app.route("/index")
def hello():
    return render_template('index.html')
app.run(debug=True)