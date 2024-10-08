from flask import Flask, render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "We are legends.@#$%"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "vishalsahu012@gmail.com"
app.config["MAIL_PASSWORD"] = "bijebjkyrumlpaxu"

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = datetime.strptime(request.form["date"],"%Y-%m-%d")
        occupation = request.form["occupation"]

        user = User(first_name=first_name,last_name=last_name,email=email,date=date,occupation=occupation)
        db.session.add(user)
        db.session.commit()
        message_body = f"""
                           Thank you for your submission {first_name}
                           name : {first_name}
                           last-name : {last_name}
                           email : {email}
                           date : {date.strftime("%Y-%m-%d")}
                           occupation : {occupation}
                       """
        message = Message(subject="New Form Submission.",sender=app.config["MAIL_USERNAME"],recipients=[email],body=message_body)
        mail.send(message)
        flash(f"{first_name}, Your form is submitted successfully.","success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=4000)