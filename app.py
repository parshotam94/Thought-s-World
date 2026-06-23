
from flask import *

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)

app.secret_key="mysecretkey"


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///thoughtbox.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)


class User(db.Model):

    id=db.Column(db.Integer,primary_key=True)

    username=db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    email=db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    password=db.Column(
        db.String(200),
        nullable=False
    )


    thoughts=db.relationship(
        'Thought',
        backref='author',
        lazy=True
    )

class Thought(db.Model):

    id=db.Column(
        db.Integer,
        primary_key=True
    )

    user_id=db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    content=db.Column(
        db.Text,
        nullable=False
    )

    created_at=db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


with app.app_context():

    db.create_all()


@app.route("/post",methods=["POST"])

def post():

    if 'user_id' not in session:

        return redirect("/login")


    content=request.form['content']


    if content.strip()=="":

        return redirect("/")


    thought=Thought(

        user_id=session['user_id'],

        content=content

    )


    db.session.add(thought)

    db.session.commit()


    return redirect("/")



@app.route("/register",methods=["GET","POST"])

def register():

    if request.method=="POST":

        username=request.form['username']

        email=request.form['email']

        password=request.form['password']


        user=User.query.filter_by(username=username).first()

        if user:

            return "Username already exists"


        hashed_password=generate_password_hash(password)


        new_user=User(

        username=username,

        email=email,

        password=hashed_password

        )


        db.session.add(new_user)

        db.session.commit()


        return redirect("/login")


    return render_template("register.html")


@app.route("/login",methods=["GET","POST"])

def login():

    if request.method=="POST":


        username=request.form['username']

        password=request.form['password']


        user=User.query.filter_by(

        username=username

        ).first()


        if user and check_password_hash(

        user.password,

        password

        ):


            session['user_id']=user.id

            session['username']=user.username


            return redirect("/")


        return "Invalid Credentials"


    return render_template("login.html")



@app.route("/")

def home():

    if 'user_id' not in session:

        return redirect("/login")


    thoughts=Thought.query.order_by(

        Thought.created_at.desc()

    ).all()


    return render_template(

        "home.html",

        username=session['username'],

        thoughts=thoughts

    )



@app.route("/logout")

def logout():

    session.clear()

    return redirect("/login")


if __name__=="__main__":

    app.run(debug=True)
