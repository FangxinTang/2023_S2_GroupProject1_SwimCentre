
from flask import render_template,request,redirect,url_for,session,flash,Blueprint
# from db import get_cursor,USER_ROLES,is_authenticated,get_user_role
from db import *
import re
import bcrypt
import constance
from datetime import datetime, date, time, timedelta

member_page = Blueprint("member", __name__, static_folder="static", template_folder="templates")

#---------------------------------------------------------#
#--------------------Member Dashboard---------------------#
#---------------------------------------------------------#

@member_page.route('/member_dashboard')
def member_dashboard():
    if not is_authenticated():
        return redirect(url_for('home'))
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return redirect(url_for('home'))
    
    # Retrieve the member's ID from the session

    connection = get_cursor()
    connection.execute("SELECT member_id FROM Members WHERE user_id = %s;", (session['user_id'],))
    member_id = connection.fetchone()[0]

    # Get the current date
    current_date = datetime.now().date()

    # Establish a database connection
    connection = get_cursor()

    # Fetch the end_date from the Subscriptions table
    query = "SELECT end_date FROM Subscriptions WHERE member_id = %s"
    connection.execute(query, (member_id,))
    end_date = connection.fetchone()


    # Calculate the remaining days until expiration
    if end_date:
        end_date = end_date[0]  # Extract the end_date from the result tuple
        remaining_days = (end_date - current_date).days
    else:
        remaining_days = None
    
    return render_template('members/member_dashboard.html', username=session['username'], remaining_days=remaining_days)

#---------------------------------------------------------#
#--------------------Member Profile-----------------------#
#---------------------------------------------------------#

@member_page.route('/member_profile')
def display_profile_member():

    if not is_authenticated():
        return redirect(url_for('home'))
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return redirect(url_for('home'))
    
    user_id = session['user_id']
    msg=""
    connection = get_cursor()
    connection.execute('SELECT * FROM Members JOIN Users \
                       ON Members.user_id = Users.user_id \
                       WHERE Members.user_id =%s;', (user_id,))
    account = connection.fetchone()
    return render_template('members/member_profile.html', account=account)

#---------------------------------------------------------#
#----------------Update Member Profile--------------------#
#---------------------------------------------------------#

@member_page.route('/update_profile', methods=['GET', 'POST'])
def update_profile_member():
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return render_template("public/home.html")
    
    if (request.method == 'POST' 
        # and request.form.get('title') 
        and request.form.get('first_name') 
        and request.form.get('last_name') 
        # and request.form.get('position') 
        and request.form.get('email')
        and request.form.get('phone')
        # and request.form.get('address')
        and request.form.get('birthdate')
        and request.form.get('username')
        # and request.form.get('health_info')
        ):

        # title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        # position = request.form['position']
        email = request.form['email']
        phone = request.form['phone']
        # address = request.form['address']
        birthdate = request.form['birthdate']
        username = request.form['username']
        # health_info=request.form['health_info']

        connection = get_cursor()
        connection.execute('SELECT username FROM Users;')
        accounts = connection.fetchall()
        usernames = []
        for users in accounts:
            usernames.append(users[0])
        


        if not re.match(r'^[a-zA-Z0-9]+$', username):
            flash('Invalid username. Usernames only contain letters and numbers.', 'warning') 
        elif username != session['username'] and username in usernames:
            flash('Username already existed. Please choose another username.','warning')
        
        else:
            print('username looks good')

            # if not re.match(r'^[A-Za-z\s]+$', title):
            #     flash('Invalid title.', 'warning')
            if not re.match(r'^[A-Za-z\s]+$', first_name):
                flash('Invalid first name.', 'warning')
            elif not re.match(r'^[A-Za-z\s]+$', last_name):
                flash('Invalid last name.', 'warning')
            # elif not re.match(r'^[A-Za-z\s]+$', position):
            #     flash('Invalid position.', 'warning')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address.','warning')
            elif not re.match(r'^[\d\s+\-().]+$', phone):
                flash('Invalid phone number.', 'warning')
            
            else:
                password = request.form.get('password')
                title = request.form.get('title')
                position = request.form.get('position')
                address = request.form.get('address')
                health_info = request.form.get('health_info')

                print('all optional info fetched')

                # Define default values
                default_title = None
                default_position = None
                default_address = None
                default_health_info = None

                if password:
                    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                else:
                    user_id = session['user_id']
                    connection = get_cursor()
                    connection.execute('SELECT * FROM Users WHERE user_id = %s;', (user_id,))
                    hashed = connection.fetchone()[1]
                
                if title:
                    if not re.match(r'^[A-Za-z\s]+$', title):
                        flash('Invalid title.', 'warning')
                    else:
                        default_title = title

                if position:
                    if not re.match(r'^[A-Za-z\s]+$', position):
                        flash('Invalid position.', 'warning')
                    else:
                        default_position = position
                
                if address:
                        if not re.match(r'^[A-Za-z0-9\s,.-]+$', address):
                            flash('Invalid address.', 'warning')
                        else:
                            default_address = address

                if health_info:
                    pattern = r'^[A-Za-z0-9\s!@#$%^&*(),.?":{}|<>]+$'
                    if re.match(pattern, health_info):
                        default_health_info = health_info
                    else:
                        flash('Invalid health information.', 'warning')


                connection = get_cursor()
                connection.execute('UPDATE Members SET title=%s, \
                                first_name=%s, last_name=%s, \
                                position=%s, email=%s, phone=%s, \
                                address=%s, birthdate=%s, health_info=%s \
                                WHERE user_id=%s;', 
                                (default_title, first_name, last_name, default_position, email, phone, default_address, birthdate, default_health_info, session['user_id'],))
                connection.execute('UPDATE Users SET password=%s, username =%s WHERE user_id=%s;', 
                                (hashed, username, session['user_id'],)) 
                flash('You have successfully updated your profile!','success')
        
    elif request.method == 'POST':
        flash('Please fill out the form.', 'warning')
    
    user_id = session['user_id']
    connection = get_cursor()
    connection.execute('SELECT * FROM Members JOIN Users \
                       ON Members.user_id = Users.user_id \
                       WHERE Members.user_id =%s;', (user_id,))
    account = connection.fetchone()
    return render_template('members/member_profile.html', account=account)

# member view instructors available and booked slots
@member_page.route('/view_lesson_slots')
def view_lesson_slots():
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return render_template("public/home.html")
    
    user_id = session['user_id']
    member_account = get_member_account_by_user_id(user_id)
    member_id = member_account[0]

    weekday_list = get_weekday_list()
    date_list = get_date_list()
    lesson_list = update_lesson_list()

    weekday_date_list = zip(weekday_list, date_list)
    print(weekday_date_list)

    # print(weekday_list)
    # print(date_list)
    current_datetime = datetime.now()
    current_date = current_datetime.date() # ,<class 'datetime.date'>


    midnight = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = current_datetime - midnight # current time as time delt
    print(f"current time as time delta is {current_time}")


    # for row in lesson_list:
    #     print(row[:-6])

        # can not book on the same day
        # can not book if the day has passed

    today = datetime.today().date()
    two_weeks_later = today + timedelta(days=14)
    date_list = []
    while today < two_weeks_later:
        date_list.append(today)
        today += timedelta(days=1)

    return render_template('members/member_view_lesson_slots.html',\
                           lesson_list=lesson_list,
                           time_slots=constance.TIME_SLOTS,
                           weekday_date_list=weekday_date_list,
                           member_id = member_id,
                           current_date = current_date,
                           current_time = current_time,
                           date_list = date_list)
                          


    # current_user_id = session['user_id']
    # current_member_account = get_member_account_by_user_id(current_user_id)
    # current_member_id = current_member_account[0]
    # print(current_member_id)
    # print(type(current_member_id))

    # connection = get_cursor()
    # sql = 'SELECT * FROM IndividualLessons JOIN Instructors \
    #         ON IndividualLessons.instructor_id = \
    #         Instructors.instructor_id;'
    # connection.execute(sql)
    # lesson_slots = connection.fetchall()
    # # print(lesson_slots)

@member_page.route('/view_instructors')
def view_instructors():
    if not is_authenticated():
        return render_template("public/home.html")
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return render_template("public/home.html")
    connection = get_cursor()
    connection.execute('SELECT * FROM Instructors')
    instructors = connection.fetchall()
    return render_template('members/view_instructors.html', instructors=instructors)

@member_page.route('/view_instructor_detail/<int:instructor_id>')
def view_instructor_detail(instructor_id):
    print(instructor_id)
    if not is_authenticated():
        return render_template("public/home.html")
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return render_template("public/home.html")
    connection = get_cursor()
    connection.execute('SELECT * FROM Instructors WHERE instructor_id =%s;', (instructor_id,))
    instructor = connection.fetchone()
    return render_template('members/view_instructor_detial.html', instructor=instructor, username = session['username'])

############################## Aqua Aerobics Routes ########################

#view aqua aerobics schedule 
@member_page.route('/view_aqua')
def member_view_aqua_schedule():
    if "loggedin" in session:
        user_id = session['user_id']
        connection = get_cursor()
        # sql = 'SELECT * FROM Courses JOIN Instructors ON Courses.instructor_id = Instructors.instructor_id;'
       
       # Fangxin edits - need pool information as well
        sql = """
            SELECT * 
            FROM Courses 
            JOIN Instructors ON Courses.instructor_id = Instructors.instructor_id
            JOIN Pools ON Courses.pool_id = Pools.pool_id;
        """
        #
        connection.execute(sql)
        classList = connection.fetchall()
        # get member account from db    
        member_account = get_member_account_by_user_id(user_id)
        # Get the existing booked courses as a list
        if member_account[11] == '':
            existing_booked_courses = []

        elif member_account[11] is None:
            existing_booked_courses = []

        else:

            existing_booked_courses = member_account[11].split(',')
            print(f"before formatting: {existing_booked_courses}")
            existing_booked_courses = [int(num_str) for num_str in existing_booked_courses]
            print(f"after formatting: {existing_booked_courses}")

        return render_template('members/member_aqua_view_schedule.html',
                                    classlist=classList,
                                    time_slots=constance.TIME_SLOTS,
                                    days=constance.DAYS,
                                    booked_courses=existing_booked_courses)
        
    return redirect (url_for('public.login'))

# book a aqua aerobics class
@member_page.route('book_group_class', methods=['POST', 'GET'])
def book_group_class():
    if request.method == "POST":
        if not is_authenticated():
            return redirect(url_for('home'))
        
        user_role = get_user_role()
        if user_role not in USER_ROLES:
            flash('Unauthorised. not in roles', 'warning')
            return redirect(url_for('home'))
        elif user_role in ['admin', 'instructor']:
            flash('Unauthorised. not member', 'warning')
            return redirect(url_for('home'))
        

        user_id = session['user_id'] 
        # get member account from db    
        member_account = get_member_account_by_user_id(user_id)
        if member_account is None:
            flash('Member account not found', 'warning')
        else:
            # get hold of member id from member account
            current_member_id = member_account[0]

        # check member subscription status by member_id
        current_member_subscription = get_subscription_info_by_member_id(current_member_id)
        if current_member_subscription[7] == "inactive":
            flash("Your subscription status is inactive, please pay monthly subscription", "danger")
            return redirect(url_for('member.member_dashboard'))
        
        elif current_member_subscription[7] == "active":
            # Get the existing booked courses as a list
            if member_account[11] == '':
                existing_booked_courses = []
            elif member_account[11] is None:
                existing_booked_courses = []
            else:
                existing_booked_courses = member_account[11].split(',')


            # Get chosen course_id from the form
            chosen_course_id = request.form.get('course_id')
            # get chosen course account from db
            chosen_course_account = get_course_account_by_course_id(chosen_course_id)

            # validate for adding a new course to member's booked courses
            if chosen_course_id not in existing_booked_courses:                
                current_booked_count = chosen_course_account[8]
                chosen_course_max_capacity = chosen_course_account[7]

                if current_booked_count < chosen_course_max_capacity:
                    # Append the new course ID to the member's booked
                    existing_booked_courses.append(chosen_course_id)
                    # Add one count to course count
                    current_booked_count += 1

                    #update database:members-booked_courses, courses-booked_count
                    update_member_booked_courses(existing_booked_courses, current_member_id)
                    update_course_booked_count(current_booked_count, chosen_course_id)
                    flash("You have successully booked this class", "success")
                    return redirect(url_for('member.member_view_aqua_schedule'))

                else:
                    flash("This class is fully booked", "danger")
                    return redirect(url_for('member.member_view_aqua_schedule'))
            else:
                flash("Already booked. Not able to book agian", "warning")
                return redirect(url_for('member.member_view_aqua_schedule'))

    return redirect(url_for("member.my_bookings"))
            
# cancel a aqua aerobics class
@member_page.route('cancel_group_class', methods=['POST', 'GET'])
def cancel_group_class():

    if request.method == "POST":
        if not is_authenticated():
            return redirect(url_for('home'))
        
        user_role = get_user_role()
        if user_role not in USER_ROLES:
            flash('Unauthorised. not in roles', 'warning')
            return redirect(url_for('home'))
        elif user_role in ['admin', 'instructor']:
            flash('Unauthorised. not member', 'warning')
            return redirect(url_for('home'))
        

        user_id = session['user_id'] 
        # get member account from db    
        member_account = get_member_account_by_user_id(user_id)
        if member_account is None:
            flash('Member account not found', 'warning')
        else:
            # get hold of member id from member account
            current_member_id = member_account[0]
            # Get the existing booked courses as a list
            if member_account[11] == '':
                existing_booked_courses = []
            else:
                existing_booked_courses = member_account[11].split(',')


            # Get chosen course_id from the form
            chosen_course_id = request.form.get('course_id')
            # get chosen course account from db
            chosen_course_account = get_course_account_by_course_id(chosen_course_id)

            # validate for deleting an existing course from member's booked courses
            # if exist, delete it
            if chosen_course_id in existing_booked_courses:
                existing_booked_courses.remove(chosen_course_id)
                # current_booked_count - 1
                current_booked_count = chosen_course_account[8]
                current_booked_count -= 1
                #update database:members-booked_courses, courses-booked_count
                update_member_booked_courses(existing_booked_courses, current_member_id)
                update_course_booked_count(current_booked_count, chosen_course_id)
                flash("You have successully cancelled the booking", "success")
                return redirect(url_for('member.member_view_aqua_schedule'))
            
            else:
                flash("You haven't booked this class", "warning")
                return redirect(url_for('member.member_view_aqua_schedule'))


    return redirect(url_for("member.my_bookings"))


# pay and book an individual lesson
@member_page.route('/pay_and_book_lesson', methods = ['GET','POST'])
def pay_and_book_lesson():

    if request.method == 'POST':

        if not is_authenticated():
            return redirect(url_for('home'))
        
        user_role = get_user_role()
        if user_role not in USER_ROLES:
            flash('Unauthorised. not in roles', 'warning')
            return redirect(url_for('home'))
        elif user_role in ['admin', 'instructor']:
            flash('Unauthorised. not member', 'warning')
            return redirect(url_for('home'))
        
                    #  <input type="hidden" name="lesson_id" value="{{ lesson_list[i+i][0] }}">
                    #             <input type="hidden" name="member_id" value="{{ member_id }}">
                    #             <input type="hidden" name="duration" value="{{ lesson_list[i+i][3] }}">
                    #             <input type="hidden" name="date" value="{{ lesson_list[i+i][4] }}">
                    #             <input type="hidden" name="time" value="{{ lesson_list[i+i][5] }}">
                    #             <input type="hidden" name="tuition" value="{{ lesson_list[i+i][6] }}">
                    #             <input type="hidden" name="lesson_status" value="{{ lesson_list[i+i][7] }}">
                    #             <input type="hidden" name="pool_id" value="{{ lesson_list[i+i][8] }}">
                    #             <input type="hidden" name="instructor"
                    #                 value="{{ lesson_list[i+i][13] }} {{ lesson_list[i+i][14] }}">
                    #             <button type="submit" class="btn btn-sm btn-primary book-btn">Book Now</button>
        
    # get info from request form
    lesson_id = int(request.form.get('lesson_id'))
    member_id = int(request.form.get('member_id'))
    date = request.form.get('date')
    time = request.form.get('time')
    duration =request.form.get('duration')
    tuition = request.form.get('tuition')
    lesson_status = request.form.get('lesson_status')
    pool_id = request.form.get('pool_id')
    instructor = request.form.get('instructor')

    # get pool name by pool id
    cursor = get_cursor()
    query = "select * from Pools where pool_id = %s"
    cursor.execute(query, (pool_id,)) 
    pool_info = cursor.fetchone()
    pool_name = pool_info[1]

    # check member subscription status by member_id
    current_member_subscription = get_subscription_info_by_member_id(member_id)
    if current_member_subscription[7] == "inactive":
        flash("Your subscription status is inactive, please pay monthly subscription", "danger")
        return redirect(url_for('member.member_dashboard'))
    
    else:
        invoice_dict = {} # initialize an empty dict with item name and detail pair for rendering table
        invoice_keys =  ['instructor', 'date', 'time', 'duration', 'pool', 'tuition']
        invoice_values = [instructor, date, time, duration, pool_name, tuition]
        
        for key, val in zip (invoice_keys, invoice_values):
            invoice_dict[key] = val
        print(invoice_dict)

    return render_template("members/pay_and_book_lesson.html",
                            lesson_id=lesson_id,
                            member_id=member_id,
                            lesson_status=lesson_status,
                            invoice_dict=invoice_dict,
                            )

              
# confirm tuition payment, update DB
@member_page.route('/update_tuition', methods=['POST'])
def update_tuition():
    if request.method == 'POST':

        if not is_authenticated():
            return redirect(url_for('home'))
        
        user_role = get_user_role()
        if user_role not in USER_ROLES:
            flash('Unauthorised. not in roles', 'warning')
            return redirect(url_for('home'))
        elif user_role in ['admin', 'instructor']:
            flash('Unauthorised. not member', 'warning')
            return redirect(url_for('home'))
        
    # get info from request form
    lesson_id = request.form.get('lesson_id')
    print(f"lesson_id is {lesson_id}, datatype is {type(lesson_id)}")
    lesson_id = int(lesson_id)

    member_id = request.form.get('member_id')
    print(f"member_id is {member_id}, datatype is {type(member_id)}")
    member_id = int(member_id)
    
    payment_type= request.form.get('payment_type')
    lesson_status = request.form.get('lesson_status')

    # to do:
    # 1. add Payment table - need member_id, payment_type = 'tuition'
    cursor = get_cursor()
    insert_query = """
            insert into Payment (member_id, payment_type)
            values (%s, %s)    
            """
    cursor.execute(insert_query,(member_id, payment_type))
    # get the payment id
    payment_id = cursor.lastrowid
    print(f"the new payment id is {payment_id}, datatype is{type(payment_id)}")

    # 2. update IndividualLessons - lesson_id, member_id, change lesson_status - booked, insert payment_id, set payment_date today
    # get payment_date - today
    payment_date = datetime.today()
    # format the date as dd/mm//yy
    payment_date_nz = payment_date.strftime('%d/%m/%Y')
    print(f"payment_date is {payment_date}, datatype is {type(payment_date)}")
    print(f"payment_date_nz is {payment_date_nz}, datatype is {type(payment_date_nz)}")

    payment_cursor = get_cursor()
    update_query = """
        update IndividualLessons
        set member_id=%s, lesson_status=%s, payment_id=%s, payment_date=%s
        where lesson_id=%s
    """
    payment_cursor.execute(update_query, (member_id, lesson_status, payment_id, payment_date, lesson_id))
    flash("You have successully booked the private lesson", "success")

    return redirect(url_for('member.view_lesson_slots'))
    # else:
    #     return redirect(url_for('member.my_bookings'))


@member_page.route('/my_bookings')
def my_bookings():
    if not is_authenticated():
        return redirect(url_for('home'))
            
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['admin', 'instructor']:
        flash('Unauthorised. not member', 'warning')
        return redirect(url_for('home'))
    
    user_id = session['user_id']
    

    ######### prepare group class data for rendering template my_bookings.html
    member_account = get_member_account_by_user_id(user_id)
    
    if member_account is not None:
        member_booked_courses = member_account[11]
        if member_booked_courses == '':
            member_booked_courses = []
        elif member_booked_courses is None:
            member_booked_courses = []
        else:
            member_booked_courses = member_booked_courses.split(',')
        # format member_booked_courses to a list 
        member_booked_courses_list = [int(course_id_str) for course_id_str in member_booked_courses]

        # get course name, day, time, instructor name, pool name from db
        all_courses_info = join_Courses_Instructors_Pools()

        # sort by day of the week then the time
        weekday_order={}
        days = constance.DAYS
        for i, day in enumerate(days):
            weekday_order[day] = i
        print(weekday_order)

        sorted_all_courses_info = sorted(all_courses_info, key=lambda x: (weekday_order[x[3]], x[4]))
        
        for row in sorted_all_courses_info:
            print(row)

        # to do: iterate the member_booked_courses_list/ids, 
        # if course id in that list, get hold of the info of this couse id, then display


    ######### prepare private lesson data for rendering template my_bookings.html 
    member_id = member_account[0]
    all_booked_lessons = join_Memebrs_Instructors_Lessons_Pools()
    # for row in all_booked_lessons:
    #     print(row)
    # print()


    # date cannot be none
    valid_all_booked_lessons =[]
    for row in all_booked_lessons:
        if row[2] is not None:
            valid_all_booked_lessons.append(row)


    # sort the date then time
    valid_all_booked_lessons = sorted(valid_all_booked_lessons, key=lambda x: (x[2], x[3]))
    # print("valid_all_booked_lessons - sorted by date then time")
    # for row in valid_all_booked_lessons:
    #     print(row)
    # print()


    # select the culumns that will display
    my_lesson_data = []

    for row in valid_all_booked_lessons: 
        if row[0] == member_id:
            
            # check lesson status - upcoming, started or finished
            current_datetime = datetime.now() # ,<class 'datetime.date'>
            current_date = current_datetime.date() # ,<class 'datetime.date'>
            current_time = current_datetime.time() # <class 'datetime.time'>
            lesson_date = row[2] # <class 'datetime.date'>

            # check data type
            # print(f"current datetime is {current_datetime},{type(current_datetime)}")
            # print(f"current date is {current_date},{type(current_date)}")
            # print(f"current time is {current_time},{type(current_time)}")
            # print(f"lesson_date is {lesson_date}, {type(lesson_date)}")
            # print()

            # calc lessen start - end time
            lesson_start_time = row[3] #{<class 'datetime.timedelta'
            duration_minutes = int(row[4]) 
            duration_timedelta = timedelta(minutes=duration_minutes)
            lesson_end_time = lesson_start_time + duration_timedelta #{<class 'datetime.timedelta'>}
            # print("lesson_start_time:", lesson_start_time,  {type(lesson_start_time)})
            # print("lesson_end_time:", lesson_end_time,  {type(lesson_end_time)})
            # print()

            # convert timedelta to datetime
            lesson_start_datetime = datetime.combine(lesson_date, time()) + lesson_start_time
            lesson_end_datetime = datetime.combine(lesson_date, time()) + lesson_end_time

            # compare and get lesson_status
            if current_date == lesson_date:
                if lesson_end_datetime <= current_datetime <= lesson_end_datetime:
                    lesson_status = "Today - Started"
                elif current_datetime < lesson_start_datetime:
                    lesson_status = "Today - Upcomming"
                else:
                    lesson_status = "Today - Finished"
            elif current_date > lesson_date:
                lesson_status = "Finished"
            else:
                lesson_status = "Upcoming"


          # convert datetime format
            date_nz_format = row[2].strftime('%d/%m/%Y') #datetime.date(2023, 9, 5) to nz datetime format dd/mm/yyyy
            hour_min_format = f"{row[3].seconds//3600:02}: {(row[3].seconds//60)%60:02}"
            duration_format = f"{row[4]}mins"

            # convert the list into a new tuple
            each_lesson_data = (f"{row[6]} {row[7]}", date_nz_format, hour_min_format,duration_format, row[8], lesson_status)
            my_lesson_data.append(each_lesson_data)

    print(f"my_lesson_data is {my_lesson_data}")

    # to do: get hold of the member_id and check it in valid all_booked_lessons, then display
                            
    return render_template("members/my_bookings.html",
                           ids = member_booked_courses_list,
                           courses= sorted_all_courses_info,
                           member_id=member_id,
                           all_booked_lessons=my_lesson_data)

########################## Memeber Pay Subscription ##################################
@member_page.route('/renew_subscription', methods=['GET', 'POST'])
def renew_subscription():
    if "loggedin" in session:
        today = date.today()
        # get current subscription details
        connection = get_cursor()
        sql = '''SELECT * FROM Subscriptions 
                JOIN Members ON Subscriptions.member_id = Members.member_id 
                WHERE Members.user_id = %s;'''
        connection.execute(sql, (session['user_id'],))
        subscription_detail = connection.fetchone()
        # get end date out 
        end_date = subscription_detail[4]
        if end_date < today:
            msg = "Your subscription due date was: "
        else:
            msg = "Your subscription due date is: "  
        # convert to nz format 
        converted_end_date = convert_date_format(str(end_date))
        converted_today=convert_date_format(str(today))
       
        return render_template('members/renew_subscription.html', subscription_detail = subscription_detail, \
                               end_date = converted_end_date, today=converted_today, msg = msg )
    return redirect (url_for('public.login'))

@member_page.route('/renew_substription/pay', methods=['GET', 'POST'])
def pay_subscription():
    if "loggedin" in session:
        today = date.today()
        # get current subscription details
        connection = get_cursor()
        sql = '''SELECT * FROM Subscriptions 
                JOIN Members ON Subscriptions.member_id = Members.member_id 
                WHERE Members.user_id = %s;'''
        connection.execute(sql, (session['user_id'],))
        subscription_detail = connection.fetchone()
        subscription_end_date = subscription_detail[4]
        subscription_end_date_nz = convert_date_format(str(subscription_end_date))
        if subscription_end_date < today:
            start_date = today
            end_date = today + timedelta(days=30)
            # convert date format 
            start_date_nz = convert_date_format(str(start_date))
            end_date_nz = convert_date_format(str(end_date))
    
        else:
            start_date = subscription_end_date + timedelta(days=1)
            end_date = start_date + timedelta(days=30)  
            # convert date format 
            start_date_nz = convert_date_format(str(start_date))
            end_date_nz = convert_date_format(str(end_date))
             
        return render_template('members/pay_subscription.html', subscription_detail = subscription_detail, \
                               subscription_end_date = subscription_end_date_nz, \
                                start_date = start_date_nz, end_date = end_date_nz, today = today)
    return redirect (url_for('public.login'))

@member_page.route('/renew_subscription/update', methods=['GET', 'POST'])
def update_subscription():
    if "loggedin" in session:
        # get today's date 
        today = date.today()
        # Get hidden user input start and end date (those are in nz string format and needs to be convert back into db format)
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        # convert them back into db format 
        start_date_nz = reverse_convert_date_format(start_date)
        start_date_db = datetime.strptime(start_date_nz, '%Y-%m-%d').date()
        end_date_nz = reverse_convert_date_format(end_date)
        end_date_db = datetime.strptime(end_date_nz, '%Y-%m-%d').date()
        # Get member id 
        connection = get_cursor()
        connection.execute("SELECT member_id FROM Members WHERE user_id = %s;", (session['user_id'],))
        member_id = connection.fetchone()[0]
        
        # insert payment table 
        sql_payment = "INSERT INTO Payment (member_id, payment_type) VALUES (%s, 'subscription');"
        connection.execute(sql_payment, (member_id,))
       # Get the Last Inserted Payment ID
        connection.execute("SELECT LAST_INSERT_ID();")
        last_payment_id = connection.fetchone()[0]
       
        # update subscription table 
        sql_subscription = "UPDATE Subscriptions SET start_date = %s, \
                        end_date = %s, payment_date = %s, subscription_status = %s, \
                        payment_id = %s WHERE member_id = %s;"
        connection.execute(sql_subscription, (start_date_db, end_date_db, today, 'active', last_payment_id, member_id,))
        flash('You have successfully renewed your subscription!','success')
        return redirect(url_for('member.renew_subscription')) 
    return redirect(url_for('public.login'))

#-------------------------------------------------#
#----------- Display messages for member----------#
#-------------------------------------------------#
                   
@member_page.route("/message")
def message():
    # get current subscription details
    connection = get_cursor()

    # Execute the SQL query to retrieve messages from the NewsUpdates table
    connection.execute("SELECT * FROM NewsUpdates ORDER BY created_at DESC;")

    # Fetch the results from the query
    messages = connection.fetchall()

    return render_template("members/message.html", messages=messages)



    


                    





