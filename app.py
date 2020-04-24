from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'covid_19'

# tengin við firebase realtime database á firebase.google.com ( db hjá danielsimongalvez@gmail.com )
config = {
    # hér kemur tengingin þín við Firebase gagnagrunninn ( realtime database )
    "apiKey": "AIzaSyBMAv62bCXV8eZMVrP85K7hS1L3CGi_Y7Q",
    "authDomain": "verkefni5-56a52.firebaseapp.com",
    "databaseURL": "https://verkefni5-56a52.firebaseio.com",
    "projectId": "verkefni5-56a52",
    "storageBucket": "verkefni5-56a52.appspot.com",
    "messagingSenderId": "177410401123",
    "appId": "1:177410401123:web:3c9b02b1c15cdd1b9de956",
    "measurementId": "G-H026MVXZL9"
}

fb = pyrebase.initialize_app(config)
db = fb.database()

@app.route('/')
def index():
    #db.child("user").push({"usr":"Johnny","pwd":"bgood"})
    
    return render_template("index.html")

@app.route('/login',  methods=['GET','POST'])
def login():
    login = False
    if request.method == 'POST':

        usr = request.form['uname']
        pwd = request.form['psw']

        # sækjum alla í gagnagrunninn og athugum hvort tiltekið notendanafn og lykilorð sé til
        u = db.child("user").get().val()
        lst = list(u.items())
        for i in lst:
            if usr == i[1]['usr'] and pwd == i[1]['pwd']:
                login = True
                break
        
        if login:  
            # hefur aðgang
            session['logged_in'] = usr
            return redirect("/topsecret")
        else:
            # hefur ekki aðgang
            return render_template("nologin.html")
    else:
        return render_template("no_method.html") 

@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/doregister',  methods=['GET','POST'])
def doregister():
    usernames = []
    if request.method == 'POST':

        usr = request.form['uname']
        pwd = request.form['psw']

        # förum í grunn og athugum hvort notendanafn sé til í grunni
        u = db.child("user").get().val()
        lst = list(u.items())
        for i in lst:
            usernames.append(i[1]['usr'])
        
        if usr not in usernames:
            db.child("user").push({"usr":usr, "pwd":pwd}) # Bætir við nýjum notanda í db á json format ef notendanafn er ekki til
            return render_template("registered.html")
        else:
            # ef notendanafn er til í grunninum nú þegar, viljum ekki hafa sama notendanafn 2 sinnum
            return render_template("userexists.html")
    else:
        return render_template("no_method.html")

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return render_template("index.html")

@app.route('/topsecret')
def topsecret():
    if 'logged_in' in session:
        return render_template("topsecret.html")
    else:
        return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('no_page.html')

if __name__ == "__main__":
	app.run(debug=True)

