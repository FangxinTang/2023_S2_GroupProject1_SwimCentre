from flask import Flask,render_template

#Blueprint imports
from admin import admin_page
from member import member_page
from instructor import instructor_page
from public import public_page
from datetime import datetime


app = Flask(__name__)
app.secret_key = '123456'

#Blueprint register
app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(member_page, url_prefix="/member")
app.register_blueprint(instructor_page, url_prefix="/instructor")
app.register_blueprint(public_page, url_prefix="/public")

@app.route("/")
def home():
    return render_template("public/home.html")


if __name__=="__main__":
    app.run(debug=True)
