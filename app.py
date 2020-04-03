from flask import Flask, render_template,request, session, redirect, url_for
import pyrebase

app = Flask(__name__)
app.config["SECRET_KEY"] = "covid_19"

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

# Test route til að setja gögn í db
@app.route('/')
def index():
    #db.child("user").push({"usr":"dsg", "pwd":1234}) 
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    login = False
    if request.method == "POST":


        usr = request.form["uname"]
        pwd = request.form["psw"]


        u = db.child("user").get().val()
        lst = list(u.items())
        for i in lst:
            if usr == i[1]["usr"] and pwd == i[1]["pwd"]:
                login = True
                break
        if login:
            session["logged_in"] = usr
            return redirect("/topsecret")
        else:
            return render_template("nologin.html")

# Test route til að sækja öll gögn úr db
#@app.route('/register')
#def register():

@app.route("/doregister", methods=["GET","POST"])
def doregister():
    usernames = []
    if request.method == "POST":

        usr = request.form["uname"]
        pwd = request.form["psw"]

        u = db.child("user").get().val()
        lst = list(u.items())
        for i in lst:
            usernames.append(i[1]["usr"])

        if usr not in usernames:
            db.child("user").push({"usr":usr, "pwd":pwd})
            return render_template("registered.html")
        else:
            return render_template("userexists.html")
@app.route("/topsecret")
def topsecret():
    if "logged_in" in session:
        return render_template("topsecret.html")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return render_template("index.html")
if __name__ == "__main__":
	app.run(debug=True)

@app.route('/register')
def register():
	return render_template("register.html")

# gott að sjá debug í vafranum -- taka út (debug=True) á heroku

if __name__ == "__main__":
	app.run(debug=True)

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())