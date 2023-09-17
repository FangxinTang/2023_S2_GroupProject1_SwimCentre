from flask import render_template,request,redirect,url_for,session,flash,Blueprint
from db import get_cursor,USER_ROLES,is_authenticated,get_user_role
import re
import bcrypt
import constance
from db import *

public_page = Blueprint("public", __name__, static_folder="static", template_folder="templates")

#-------------------------------------------------#
#--------------------  Login ---------------------#
#-------------------------------------------------#

@public_page.route("/login/", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        provided_username = request.form.get("username")
        provided_password = request.form.get("password")

        # get user info from db by username:
        cursor = get_cursor()
        cursor.execute('SELECT * FROM Users WHERE username = %s', (provided_username,))
        user_info = cursor.fetchone()

        # check if user info is found
        if user_info is None:
            flash("User not found",'warning')
            return redirect(request.url)   
        else:
            # if user exist, compare provided values and database values
            hashed_pass_in_db = user_info[1] # get the hased pass from database
                
            # check provided pass matches the hashed pass
            if bcrypt.checkpw(provided_password.encode('utf-8'), hashed_pass_in_db.encode('utf-8')):
                # if match, store user info into session variables
                session["username"] = user_info[2]
                session['user_id'] = user_info[0]
                session['user_role'] = user_info[3]
                session['loggedin'] = True

                flash("Welcome back.", "success")

                # check the role in the session, and assign to different dashboards
                if session['user_role'] == "admin":
                    return redirect(url_for("admin.admin_dashboard"))
                elif session['user_role'] == "member":
                    return redirect(url_for("member.member_dashboard"))
                elif session['user_role'] == "instructor":
                    print ("test print")
                    return redirect(url_for("instructor.instructor_dashboard"))
            else:
                flash("Password incorrect","warning")
                return redirect(request.url)     
    else:
        print ("test")  
        return render_template("public/login.html")
    
#-------------------------------------------------#
#-------------------- Logout ---------------------#
#-------------------------------------------------#

@public_page.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

#-------------------------------------------------#
#--------------------Register---------------------#
#-------------------------------------------------#

@public_page.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data from the request
        username = request.form["username"]
        password = request.form["password"]
        role = "member"
        title = request.form["title"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        position = request.form["position"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]
        birthdate = request.form["birthdate"]
        health_info = request.form["health_info"]

        # Create a cursor for the database connection
        db_cursor = get_cursor()

        # Check if the username already exists in the database
        db_cursor.execute("SELECT COUNT(*) FROM users WHERE UserName = %s", (username,))
        user_count = db_cursor.fetchone()[0]
        if user_count > 0:
            flash("Username already exists. Please choose a different username.", "warning")
            return redirect(url_for("public.register"))

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert the new user data into the 'users' table
        db_cursor.execute("INSERT INTO users (UserName, Password, Role) VALUES (%s, %s, %s)",
                          (username, hashed_password, role))

        # Get the new user_id to be ready to insert into the three role table 
        db_cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user_id = db_cursor.fetchone()[0]

        # Insert into the Members table
        db_cursor.execute("INSERT INTO Members (title, first_name, last_name, position, phone, email, address, birthdate, health_info, user_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                              (title, first_name, last_name, position, phone, email, address, birthdate, health_info, user_id, 1))
            
        # Get the newly inserted member_id
        db_cursor.execute('SELECT member_id FROM Members WHERE user_id=%s;', (user_id,))
        member_id = db_cursor.fetchone()[0]

        # Generate the next available payment_id
        db_cursor.execute('SELECT MAX(payment_id) FROM Payment;')
        max_payment_id = db_cursor.fetchone()[0] or 0
        next_payment_id = max_payment_id + 1

        # Insert into the Payment table
        db_cursor.execute('INSERT INTO Payment (payment_id, member_id, payment_type) VALUES (%s, %s, %s)',
                          (next_payment_id, member_id, 'subscription'))

        # Calculate start date (current date) and end date (30 days from start date)
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
        payment_date = start_date

        # Insert into the Subscription table with the calculated details
        db_cursor.execute('INSERT INTO Subscriptions (member_id, subscription_type, start_date, end_date, payment_amount, payment_date, subscription_status, payment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                          (member_id, 'Monthly', start_date, end_date, 70.00, payment_date, 'active', next_payment_id))
                
        flash("You have successfully registered!", "success")
        return redirect(url_for("home"))

    # If the request method is 'GET', render the registration form
    return render_template("public/register.html")


