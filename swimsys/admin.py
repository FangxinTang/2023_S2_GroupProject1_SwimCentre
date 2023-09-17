from flask import render_template,request,redirect,url_for,session,flash,Blueprint
from db import *
import re
import bcrypt
import constance
from datetime import datetime, date
from datetime import timedelta
import json

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

# display admin dashboard
@admin_page.route('/admin/dashboard')
def admin_dashboard():

    if not is_authenticated():
        return redirect(url_for('home'))
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return redirect(url_for('home'))
    return render_template('admins/admin_dashboard.html', username = session['username'])

# display admin profile
@admin_page.route('/admin/profile')
def display_profile():

    if not is_authenticated():
        return redirect(url_for('home'))
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return redirect(url_for('home'))
    
    user_id = session['user_id']
    connection = get_cursor()
    connection.execute('SELECT * FROM Admins JOIN Users \
                       ON Admins.user_id = Users.user_id \
                       WHERE Admins.user_id =%s;', (user_id,))
    account = connection.fetchone()
    return render_template('admins/admin_profile.html', account=account)

# update admin profile
@admin_page.route('/update_profile', methods=['GET', 'POST'])
def update_admin_profile():
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")
    
    if (request.method == 'POST' 
        # and request.form.get('title') 
        and request.form.get('first_name') 
        and request.form.get('last_name') 
        # and request.form.get('position') 
        and request.form.get('email')
        and request.form.get('phone')
        and request.form.get('username')):

        # title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        # position = request.form['position']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']

        print('all required info fetched')

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
                print('all other required info looks good')

                password = request.form.get('password')
                title = request.form.get('title')
                position = request.form.get('position')
               

                print('all optional info fetched')

                # Define default values
                default_title = None
                default_position = None

                # Update the variables based on the conditions
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

                print('all set to update db')

                connection = get_cursor()
                connection.execute('UPDATE Admins SET title=%s, \
                                    first_name=%s, last_name=%s, \
                                    position=%s, email=%s, phone=%s \
                                    WHERE user_id=%s;', 
                                    (default_title, first_name, last_name, default_position, email, phone, session['user_id'],))
                connection.execute('UPDATE Users SET password=%s, \
                                    username=%s WHERE user_id=%s;', 
                                    (hashed, username, session['user_id'],)) 
                flash('You have successfully updated your profile!', 'success')
            
   
    elif request.method == 'POST':
        flash('Please fill out the form.', 'warning')

    user_id = session['user_id']
    connection = get_cursor()
    connection.execute('SELECT * FROM Admins JOIN Users \
                       ON Admins.user_id = Users.user_id \
                       WHERE Admins.user_id =%s;', (user_id,))
    account = connection.fetchone()
    return render_template('admins/admin_profile.html', account=account)

@admin_page.route('/admin/member_list')
def admin_member_list():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")
    
    connection = get_cursor()
    connection.execute('SELECT * FROM Members WHERE status=1;')
    member_list = connection.fetchall()
    return render_template('admins/admin_memberlist.html', member_list=member_list)

@admin_page.route('/admin/member_form')
def admin_member_form():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")

    return render_template('admins/admin_member_form.html')

@admin_page.route('/admin/add_member', methods=['GET', 'POST'])
def admin_add_member():
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
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
        and request.form.get('password')
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

        print('all form info fetched')

        connection = get_cursor()
        connection.execute('SELECT username FROM Users;')
        accounts = connection.fetchall()
        usernames = []
        for users in accounts:
            usernames.append(users[0])

        if username in usernames:
            flash('Username already existed. Please choose another username.','warning')
        else:
            if not re.match(r'^[a-zA-Z0-9]+$', username):
                flash('Invalid username. Usernames only contain letters and numbers.', 'warning')
            # elif not re.match(r'^[A-Za-z\s]+$', title):
            #     flash('Invalid title.', 'warning')
            elif not re.match(r'^[A-Za-z\s]+$', first_name):
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
                # Extract values from the request form if they exist
                password = request.form.get('password')
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                title = request.form.get('title')
                position = request.form.get('position')
                address = request.form.get('address')
                health_info = request.form.get('health_info')
     
                # Define default values
                default_title = None
                default_position = None
                default_address = None 
                default_health_info = None

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

                # Validate health_info
                if health_info:
                    # Define a regex pattern that allows letters, numbers, symbols, and spaces
                    pattern = r'^[A-Za-z0-9\s!@#$%^&*(),.?":{}|<>]+$'
                    if re.match(pattern, health_info):
                        default_health_info = health_info
                    else:
                        flash('Invalid health information.', 'warning')


                connection = get_cursor()
                connection.execute('INSERT INTO Users (password, username, \
                                   role) VALUES (%s, %s, %s);', (hashed, \
                                    username, 'member')) 
                
                print('user added')

                # get user_id
                connection.execute('SELECT * FROM Users WHERE username = %s;', (username,))
                user_id = connection.fetchone()[0]

                connection.execute('INSERT INTO Members (title, first_name, \
                                   last_name, position, email, phone, address, \
                                   birthdate, health_info, user_id, status) VALUES (%s, %s, %s,\
                                    %s, %s, %s, %s, %s, %s, %s, %s);', (default_title, first_name, \
                                    last_name, default_position, email, phone, default_address, \
                                    birthdate, default_health_info, user_id, 1))
                
                print('member added')

                connection.execute('SELECT member_id FROM Members WHERE user_id=%s;', (user_id,))
                member_id = connection.fetchone()[0]

                connection.execute('INSERT INTO Subscriptions (member_id, subscription_type, subscription_status) VALUES (%s, %s, %s)',\
                               (member_id, 'Monthly', 'inactive',))
                
                print('subs added')
                
                flash('You have successfully added a member!','success')
        
    elif request.method == 'POST':
        flash('Please fill out the form.', 'warning')
  
    return redirect(url_for('admin.admin_member_list'))

@admin_page.route('/admin/member_info/<user_id>')
def admin_member_info(user_id):
    connection = get_cursor()                 
    connection.execute('SELECT * FROM Members JOIN Users \
                       ON Members.user_id = Users.user_id \
                       WHERE Members.user_id =%s;', (user_id,))
    account = connection.fetchone()
    # print(account)
    return render_template('admins/admin_member_info.html', account=account)

@admin_page.route('/admin/update_member/<user_id>/<user_name>', methods=['GET', 'POST'])
def admin_update_member(user_id, user_name):
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
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
        # and request.form.get('password')
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

        print('all form info fetched')

        connection = get_cursor()
        connection.execute('SELECT username FROM Users;')
        accounts = connection.fetchall()
        usernames = []
        for users in accounts:
            usernames.append(users[0])


        if not re.match(r'^[a-zA-Z0-9]+$', username):
            flash('Invalid username. Usernames only contain letters and numbers.', 'warning') 
        elif username != user_name and username in usernames:
            flash('Username already existed. Please choose another username.','warning')
        
        else: 
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
                # Extract values from the request form if they exist
                password = request.form.get('password')
                title = request.form.get('title')
                position = request.form.get('position')
                address =  request.form.get('address')
                health_info = request.form.get('health_info')

                # Define default values
                default_title = None
                default_position = None
                default_address = None
                default_health_info = None


                # Update the variables based on the conditions
                if password:
                    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                else:
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

                    # Validate health_info
                if health_info:
                    # Define a regex pattern that allows letters, numbers, symbols, and spaces
                    pattern = r'^[A-Za-z0-9\s!@#$%^&*(),.?":{}|<>]+$'
                    if re.match(pattern, health_info):
                        default_health_info = health_info
                    else:
                        flash('Invalid health information.', 'warning')


                connection = get_cursor()
                connection.execute('UPDATE Users SET password=%s, username=%s \
                                    WHERE user_id=%s;',(hashed, username, user_id)) 
                
                print('user updated')

                connection.execute('UPDATE Members SET title=%s, first_name=%s, \
                                    last_name=%s, position=%s, email=%s, phone=%s, address=%s, \
                                    birthdate=%s, health_info=%s WHERE user_id=%s;', (default_title, first_name, \
                                    last_name, default_position, email, phone, default_address, \
                                    birthdate, default_health_info, user_id))
                
                print('member updated')

                flash('You have successfully updated a member!','success')

    elif request.method == 'POST':
        flash('Please fill out the form.', 'warning')
    

    return redirect(url_for('admin.admin_member_info', user_id=user_id))


@admin_page.route('/admin/delete_member/<member_id>')
def admin_delete_member(member_id):
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")
    
    connection = get_cursor()
    connection.execute('UPDATE Members SET status=%s WHERE member_id=%s;', (0, member_id,))
    flash('You have successfully deleted a member!','success')
 
    return redirect(url_for('admin.admin_member_list'))


# admin view instructors available and booked slots
@admin_page.route('/view_lesson_slots')
def view_lesson_slots():
    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")

    weekday_list = get_weekday_list()
    formated_date_list = get_date_list()
    lesson_list = update_lesson_list()

    weekday_date_list = zip(weekday_list, formated_date_list)
    
    today = datetime.today().date()
    two_weeks_later = today + timedelta(days=14)
    date_list = []
    while today < two_weeks_later:
        date_list.append(today)
        today += timedelta(days=1)

    return render_template('admins/admin_view_lesson_slots.html', lesson_list=lesson_list, 
            time_slots=constance.TIME_SLOTS, weekday_date_list=weekday_date_list, date_list=date_list)

#-------------------------------------------------#
#-------- Admin View subscription status ---------#
#-------------------------------------------------#
@admin_page.route('/admin/subscription_status', methods=['GET', 'POST'])
def admin_subscription_status():
    if not is_authenticated():
        return redirect(url_for('home'))

    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return redirect(url_for('home'))

    connection = get_cursor()

    # Check if a search query was submitted
    search_query = request.args.get('search', '')

    # Construct your SQL query with a WHERE clause to filter results based on the search query
    sql = 'SELECT Members.member_id, Members.first_name, Members.last_name, Subscriptions.subscription_type, Subscriptions.subscription_status \
           FROM Members \
           JOIN Subscriptions ON Members.member_id = Subscriptions.member_id \
           WHERE Members.member_id LIKE %s OR Members.first_name LIKE %s OR Members.last_name LIKE %s;'

    # Use the '%' wildcard in the SQL query to perform a partial match
    search_pattern = f'%{search_query}%'

    # Execute the SQL query with the search pattern
    connection.execute(sql, (search_pattern, search_pattern, search_pattern))
    subscription_status_list = connection.fetchall()

    return render_template('admins/admin_subscription_status.html', subscription_status_list=subscription_status_list)



################################## Aqua Aerobics Routes ########################
@admin_page.route('/admin/aqua')
def admin_view_aqua_schedule():
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

      
        return render_template('admins/admin_aqua_view_schedule.html',
                                    classlist=classList,
                                    time_slots=constance.TIME_SLOTS,
                                    days=constance.DAYS)
    return redirect(url_for('public.login'))
  
################################## Admin Track Payments ##########################################  

@admin_page.route('/payment',  methods=['GET', 'POST'])
def admin_track_payment():
    if "loggedin" in session:
        connection = get_cursor()
        sql = 'SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name, \
            Subscriptions.payment_amount AS amount, Subscriptions.payment_date, Payment.payment_type \
            FROM Payment\
            JOIN Subscriptions ON Payment.payment_id = Subscriptions.payment_id\
            JOIN Members ON Subscriptions.member_id = Members.member_id\
            UNION\
            SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name,\
            IndividualLessons.lesson_fee AS amount, IndividualLessons.payment_date, Payment.payment_type\
            FROM Payment\
            JOIN IndividualLessons ON Payment.payment_id = IndividualLessons.payment_id\
            JOIN Members ON IndividualLessons.member_id = Members.member_id\
            Order by payment_date desc;'
        
        connection.execute(sql)
        paymentList= connection.fetchall()
        member_name_dict = get_member_names()
        if request.method == 'POST':
            connection = get_cursor()
            # get user input member id
            selected_member = request.form.get('member')
            selected_memberid, selected_member_name = selected_member.split('|')
            sql_search = 'SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name, \
                        Subscriptions.payment_amount AS amount, Subscriptions.payment_date, Payment.payment_type \
                        FROM Payment\
                        JOIN Subscriptions ON Payment.payment_id = Subscriptions.payment_id\
                        JOIN Members ON Subscriptions.member_id = Members.member_id\
                        WHERE Members.member_id = %s \
                        UNION\
                        SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name,\
                        IndividualLessons.lesson_fee AS amount, IndividualLessons.payment_date, Payment.payment_type\
                        FROM Payment\
                        JOIN IndividualLessons ON Payment.payment_id = IndividualLessons.payment_id\
                        JOIN Members ON IndividualLessons.member_id = Members.member_id\
                        WHERE Members.member_id = %s \
                        Order by payment_date desc;'
            
            connection.execute(sql_search, (selected_memberid, selected_memberid,))
            selected_paymentList = connection.fetchall()
            return render_template('admins/admin_search_payment.html', \
                            selected_paymentList = selected_paymentList,\
                            selected_member_name = selected_member_name)
        
        return render_template ('admins/admin_track_payment.html', \
                                    paymentList = paymentList, member_name_dict = member_name_dict)
    return redirect(url_for('public.login'))
         
         
  
################################## Attendance Report ########################################## 


@admin_page.route('admin/select_attendance')
def admin_select_attendance():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")


    member_name_dict = get_member_names()
 


    period_list = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December', 'all periods']

    return render_template('admins/admin_select_attendance.html', member_name_dict=member_name_dict, period_list=period_list)

@admin_page.route('admin/display_attendance', methods=['GET', 'POST'])
def admin_display_attendance():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")
    



    if request.method == 'POST':
        # get hold of form data: member_id and period 
        selected_member = request.form.get('member')
        selected_memberid, selected_member_name = selected_member.split('|')

        selected_period = request.form.get('period')

        available_period = ['June', 'July', 'August', 'September', 'all periods'] 


        if selected_period not in available_period:
            flash('Sorry, data is not available for the selected period.', 'warning')
        else:
            if selected_memberid:
                attendance_data = generate_attendance_data(selected_memberid, selected_period)
            else: 
                attendance_data = generate_attendance_data('all members', selected_period)
     
            activity_data = ['Pool Use', 'Aqua Aerobics', 'Swimming Lesson']

            attendance_data_json = json.dumps(attendance_data)          
            activity_data_json = json.dumps(activity_data)

            member_name_dict = get_member_names()

            period_list = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December', 'all periods']
            
            return render_template('admins/admin_display_attendance.html', 
                                attendance_data_json=attendance_data_json, activity_data_json=activity_data_json, 
                                period_list=period_list, member_name_dict=member_name_dict, 
                                period = selected_period, member=selected_member_name,)

    return redirect(url_for('admin.admin_select_attendance'))






########################  aqua aerobics classes report  ########################

@admin_page.route('admin/select_aerobics')
def admin_select_aerobics():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")

    period_list = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December', 'all periods']
    return render_template('admins/admin_select_aerobics.html', period_list=period_list)

@admin_page.route('admin/display_aerobics_report', methods=['GET', 'POST'])
def admin_display_aerobics_report():

    if not is_authenticated():
        return render_template("public/home.html")
    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return render_template("public/home.html")
    elif user_role in ['member', 'instructor']:
        flash('Unauthorised. not admin', 'warning')
        return render_template("public/home.html")
    

    if request.method == 'POST':

        # get selected peroiod 
        selected_period = request.form.get('period')

        # get attendance data for the selected period 
        available_period = ['June', 'July', 'August', 'September', 'all periods'] 


        if selected_period not in available_period:
            flash('Sorry, data is not available for the selected period.', 'warning')
        else:
            aerobics_attendance_data, all_data = generate_aerobics_data(selected_period)

            # get a list of course names 
            course_names = []
            for entry in all_data:
                course_names.append(entry[2])

            # json.dump course names & attendance data 
            aerobics_attendance_json = json.dumps(aerobics_attendance_data)
            course_names_json = json.dumps(course_names)

            period_list = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December', 'all periods']



            return render_template('admins/admin_display_aerobics.html', 
                                aerobics_attendance_json=aerobics_attendance_json, 
                                course_names_json=course_names_json, 
                                period_list=period_list, 
                                period = selected_period, 
                                # course_tooltip_json=course_tooltip_json
                                )

    return redirect(url_for('admin.admin_select_aerobics'))

  
################################## Financial Reports ##########################################  

@admin_page.route('/financial_report')
def financial_report():
    if 'loggedin' in session:
        # total revenue of the subscription and tuition 
        connection = get_cursor()
        sql_subscription = 'SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name, \
            Subscriptions.payment_amount AS amount, Subscriptions.payment_date, Payment.payment_type \
            FROM Payment\
            JOIN Subscriptions ON Payment.payment_id = Subscriptions.payment_id\
            JOIN Members ON Subscriptions.member_id = Members.member_id\
            Order by payment_date desc;'
          
        sql_tuition = 'SELECT Payment.payment_id, Payment.member_id, Members.first_name, Members.last_name,\
            IndividualLessons.lesson_fee AS amount, IndividualLessons.payment_date, Payment.payment_type\
            FROM Payment\
            JOIN IndividualLessons ON Payment.payment_id = IndividualLessons.payment_id\
            JOIN Members ON IndividualLessons.member_id = Members.member_id\
            Order by payment_date desc;'
        
        connection.execute(sql_subscription)
        subscriptionList = connection.fetchall()
        connection.execute(sql_tuition)
        tuitionList= connection.fetchall()

        # Initialize total subscription and tuition to 0 before the loop
        total_subscription = 0
        total_tuition = 0
        
        for subscription in subscriptionList:
            payment_amount_1 = float(subscription[4])
            total_subscription += payment_amount_1
               
        for tuition in tuitionList:
            payment_amount_2 = float(tuition[4])
            total_tuition += payment_amount_2
        
        total_revenue = total_subscription + total_tuition
        # group by month 
        sql_by_month = 'SELECT\
                    YEAR(payment_date) AS year,\
                    MONTH(payment_date) AS month,\
                    SUM(lesson_fee) AS total_tuition,\
                    SUM(payment_amount) AS total_subscription,\
                    SUM(lesson_fee + payment_amount) AS total\
                    FROM (\
                        SELECT payment_date, lesson_fee, 0 AS payment_amount\
                        FROM IndividualLessons\
                        WHERE payment_date IS NOT NULL AND lesson_fee IS NOT NULL\
                        UNION ALL\
                        SELECT payment_date, 0 AS lesson_fee, payment_amount\
                        FROM Subscriptions\
                        WHERE payment_date IS NOT NULL AND payment_amount IS NOT NULL\
                        ) AS CombinedPayments\
                    GROUP BY YEAR(payment_date), MONTH(payment_date)\
                    ORDER BY year DESC, month DESC;'
        connection.execute(sql_by_month)
        group_by_month_list = connection.fetchall()
        return render_template('admins/admin_financial_report.html', total_subscription = total_subscription,\
                               total_tuition = total_tuition, total_revenue = total_revenue,\
                               group_by_month_list = group_by_month_list
                                )
    return redirect(url_for('public.login'))

                
#-------------------------------------------------#
#----------- Admin create news messages-----------#
#-------------------------------------------------#

@admin_page.route("/admin_news_update", methods=["GET", "POST"])
def admin_news_update():
    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]

        # Create a cursor for the database connection
        db_cursor = get_cursor()

        # Insert the new subject and content into the News updates table
        db_cursor.execute("INSERT INTO NewsUpdates (subject, content) VALUES (%s, %s)",
                          (subject, content))
        
        flash("You have successfully created a news update", "success")
        return redirect(url_for("admin.admin_dashboard"))

    # If the request method is 'GET', render the admin_news_update template
    return render_template("admins/admin_news_update.html")






