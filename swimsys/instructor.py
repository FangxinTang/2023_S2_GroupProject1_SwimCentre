from flask import render_template,request,redirect,url_for,session,flash,Blueprint,current_app
import os
import time
from db import *
import re
import bcrypt
import constance
from datetime import datetime, date, time, timedelta

instructor_page = Blueprint("instructor", __name__, static_folder="static", template_folder="templates")

########################################### instructor view #############################
@instructor_page.route("/instructor_dashboard")
def instructor_dashboard():
    if not is_authenticated():
        return redirect(url_for('/home'))    
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['member', 'admin']:
        flash('Unauthorised. not instructor', 'warning')
        return redirect(url_for('home'))    
    return render_template('instructors/instructor_dashboard.html',username = session['username'])


@instructor_page.route('/update_instructor_profile', methods=['GET', 'POST'])
def update_instructor_profile():
    if not is_authenticated():
      return redirect(url_for('/home')) 
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role in ['admin', 'member']:
        flash('Unauthorised. not instructor', 'warning')
        return redirect(url_for('home'))
    
    user_id = session['user_id']
    msg = ""       
    connection = get_cursor()
    connection.execute('SELECT * FROM Instructors LEFT JOIN Users on Users.user_id=Instructors.user_id WHERE Instructors.user_id =%s;', (user_id,))
    account = connection.fetchone()
    print(account)
    if (request.method == 'POST'):  
              
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        email = request.form['email']
        phone = request.form['phone']
        instructor_profile = request.form['instructor_profile']
        password=request.form['password'] 
        
        instructor_image = request.files['instructor_image']
        print(f"the original file name is {instructor_image.filename}")
        # Fangxin Tang edits:
        # validate the image and get image filename:
        if instructor_image is not None:
            instructor_image_filename = instructor_image.filename 
        connection = get_cursor()
        connection.execute('SELECT * FROM Instructors WHERE email = %s AND Instructors.user_id != %s', (email,user_id))
        email_entry = connection.fetchone()

        if email_entry:
                msg = 'Email already exists!'
        elif not re.match(r'^[A-Za-z\s.]+$', title):
            msg = 'Invalid title. Please use letters and spaces only.'
        elif not re.match(r'^[A-Za-z\s]+$', first_name):
            msg = 'Invalid first name. Please use letters and spaces only.'
        elif not re.match(r'^[A-Za-z\s]+$', last_name):
            msg = 'Invalid last name. Please use letters and spaces only.'
        elif not re.match(r'^[A-Za-z\s]+$', position):
            msg = 'Invalid position. Please use letters and spaces only.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'^[\d\s+\-().]+$', phone):
            msg = 'Invalid phone number. Please use digits, spaces, hyphens, and parentheses only.'
        elif password:
            if 'instructor_image' in request.files and instructor_image_filename:
                # Define upload directory; if it doesn't exist, create it
                upload_dir = os.path.join(current_app.root_path, 'static', 'images', 'instructors')
                os.makedirs(upload_dir, exist_ok=True)

                # Get file extension
                _, file_extension = os.path.splitext(instructor_image_filename)

                # Create a new unique file name with current timestamp + file extension
                new_filename = str(time.time()) + file_extension
                print(f"new_filename is {new_filename}")

                # Create file path to store this image in our computer
                computer_file_path = os.path.join(upload_dir, new_filename)
                print(f"this is the file path to be saved in the database: {file_path}")

                # ***** Create the file path str which is used for updating database *****
                file_path = f"static/images/instructors/{new_filename}"
                print(f"this is the file path to be saved in the database: {file_path}")

                # save the image as a file to the directory in our computer
                instructor_image.save(computer_file_path)
            
            else:    
                file_path = account[9]
                

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            connection = get_cursor()
            connection.execute('UPDATE Instructors SET title=%s,first_name=%s, last_name=%s, position=%s, phone=%s, email=%s, instructor_profile=%s,image_url=%s WHERE user_id=%s', 
                  (title, first_name, last_name, position, phone, email,instructor_profile,file_name,session['user_id']))
            connection = get_cursor()
            connection.execute('UPDATE Users SET password=%s, role=%s WHERE user_id=%s ',(hashed,user_role,session['user_id']))
            flash('You have successfully updated your profile!', 'success')
            return redirect(url_for('instructor.update_instructor_profile'))
            
        else:
            hashed=account[11]
            
            # define image path, rename image and save it to defined directory
            if 'instructor_image' in request.files and instructor_image_filename:
                # Define upload directory; if it doesn't exist, create it
                upload_dir = os.path.join(current_app.root_path, 'static', 'images', 'instructors')
                os.makedirs(upload_dir, exist_ok=True)

                # Get file extension
                _, file_extension = os.path.splitext(instructor_image_filename)

                # Create a new unique file name with current timestamp + file extension
                new_filename = str(time.time()) + file_extension
                print(f"new_filename is {new_filename}")

                # Create file path to store this image in our computer
                computer_file_path = os.path.join(upload_dir, new_filename)
                print(f"this is the file path to be saved in the database: {computer_file_path}")

                # ***** Create the file path str which is used for updating database *****
                file_path = f"static/images/instructors/{new_filename}"
                print(f"this is the file path to be saved in the database: {file_path}")

                # save the image as a file to the directory in our computer
                instructor_image.save(computer_file_path)
            
            else:    
                file_path = account[9]
            
            connection = get_cursor()
            connection.execute('UPDATE Instructors SET title=%s,first_name=%s, last_name=%s, position=%s, phone=%s, email=%s, instructor_profile=%s ,image_url=%s WHERE user_id=%s', 
                  (title, first_name, last_name, position, phone, email,instructor_profile, file_path, session['user_id'])) # Fangxin edits
            connection = get_cursor()
            connection.execute('UPDATE Users SET password=%s, role=%s WHERE user_id=%s ',(hashed,user_role,session['user_id']))
            flash('You have successfully updated your profile!', 'success')
            return redirect(url_for('instructor.update_instructor_profile'))

    return render_template("instructors/update_instructor_profile.html", account=account, msg=msg)

@instructor_page.route('/upcoming_lessons')
def upcoming_lessons():
    if not is_authenticated():
        return redirect(url_for('home'))

    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. Not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role != 'instructor':
        flash('Unauthorised. Not instructor', 'warning')
        return redirect(url_for('home'))

    connection = get_cursor()
    connection.execute('SELECT instructor_id from Instructors LEFT JOIN Users on Instructors.user_id = Users.user_id WHERE Users.user_id = %s',(session['user_id'],))
    instructor_id = connection.fetchone()[0]

    connection = get_cursor()
    connection.execute('SELECT * FROM IndividualLessons LEFT JOIN Pools ON IndividualLessons.pool_id = Pools.pool_id LEFT JOIN Members on IndividualLessons.member_id = Members.member_id WHERE IndividualLessons.instructor_id = %s AND IndividualLessons.lesson_status = %s', (instructor_id, 'booked'))
    upcoming_lessons = connection.fetchall()

    return render_template('instructors/upcoming_lessons.html', lessons=upcoming_lessons)

###################################### Aqua Aerobics Routes ########################
@instructor_page.route('/instructor/aqua')
def instructor_view_aqua_schedule():
    if "loggedin" in session:

        user_id = session['user_id']

        connection = get_cursor()
        # sql = 'SELECT * FROM Courses JOIN Instructors ON Courses.instructor_id = Instructors.instructor_id;'

        sql = """
            SELECT * 
            FROM Courses 
            JOIN Instructors ON Courses.instructor_id = Instructors.instructor_id
            JOIN Pools ON Courses.pool_id = Pools.pool_id;
        """
        #
        connection.execute(sql)
        classList = connection.fetchall()
        # get instructor account 
        
        return render_template('instructors/instructor_aqua_view_schedule.html',
                                classlist=classList,
                                time_slots=constance.TIME_SLOTS, 
                                days=constance.DAYS)
    return redirect(url_for('login'))

# Define a route for instructors to manage their lesson slots
@instructor_page.route('/instructor/manage_lesson_slots', methods=['GET', 'POST'])
def manage_lesson_slots():
    if not is_authenticated():
        return redirect(url_for('home'))

    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. Not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role != 'instructor':
        flash('Unauthorised. Not instructor', 'warning')
        return redirect(url_for('home'))
    user_id = session['user_id']
    connection = get_cursor()
    connection.execute('SELECT * FROM Instructors LEFT JOIN Users on Users.user_id=Instructors.user_id WHERE Instructors.user_id =%s;', (user_id,))
    account = connection.fetchone()
    instructor_id = account[0]
    connection = get_cursor()
    connection.execute('SELECT * FROM Instructors LEFT JOIN IndividualLessons on IndividualLessons.instructor_id=Instructors.instructor_id LEFT JOIN Pools ON IndividualLessons.pool_id=Pools.pool_id WHERE Instructors.instructor_id = %s;', (instructor_id,))
    lesson_slots = connection.fetchall()

    # Handle form submissions to add or edit lesson slots
    lesson_list = update_lesson_list()
    lesson_slots.sort(key=lambda slot: (slot[14], slot[15]))
    date_list=get_date_list()
    weekday_list=get_weekday_list()

    weekday_date_list = zip(weekday_list, date_list)

    current_datetime = datetime.now()
    current_date = current_datetime.date() # ,<class 'datetime.date'>
    end_date = current_date + timedelta(days=14)
    date_range = [current_datetime.date() + timedelta(days=i) for i in range(14) if current_datetime.date() + timedelta(days=i) <= end_date]

    midnight = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = current_datetime - midnight # current time as time delt


    if request.method == 'POST':
        # Retrieve and validate form data, then save it to your database
        # Replace the following lines with your actual form handling logic
        date_str = request.form.get('date')
        time = request.form.get('time')
        duration = request.form.get('duration')
        location = request.form.get('location')
        # Parse the date string in the format 'DD/MM' to a datetime object
        parsed_date = datetime.strptime(date_str, '%d/%m')

        # Create a new datetime object with the year '2023' and the parsed month and day
        date_obj = parsed_date.replace(year=2023)
        # Check if duration is empty or not selected
        if not duration:
            flash('Please select a duration (30 or 60 minutes).', 'danger')
            return redirect(url_for('instructor.manage_lesson_slots'))

        if location == 'Olympic':
            pool_id=3
        elif location == 'Hydrotherapy' :
            pool_id=1
        elif location == 'Training':
            pool_id=2
        elif location == 'Family':
            pool_id=4

        if duration == '30':
            lesson_fee=44
        elif duration == '60':
            lesson_fee=80
        
        # Check if the selected time and date already exist in the lesson_slots list
        for slot in lesson_slots:

            if str(slot[14]).strip() == date_obj.strftime('%Y-%m-%d').strip() and str(slot[15]).strip() == time.strip():
                flash('The selected time and date are not available. Please choose another.', 'danger')
                return redirect(url_for('instructor.manage_lesson_slots'))

        connection = get_cursor()
        connection.execute('INSERT INTO IndividualLessons (instructor_id, lesson_duration, date, lesson_time, lesson_status, pool_id,lesson_fee) VALUES (%s, %s, %s, %s, %s, %s,%s)',
                       (instructor_id, duration, date_obj.strftime('%Y-%m-%d'), time, 'available', pool_id,lesson_fee))
        
        flash('New lesson slot added successfully', 'success')
        return redirect(url_for('instructor.manage_lesson_slots'))
    
    return render_template('instructors/manage_lesson_slots.html', lesson_list=lesson_list,
                           time_slots=constance.TIME_SLOTS,date_list=date_list,
                           current_date = current_date,
                           current_time = current_time,lesson_slots=lesson_slots,instructor_id=instructor_id)

@instructor_page.route('/cancel_class/<int:lesson_id>', methods=['GET', 'POST'])
def cancel_class(lesson_id):
    print(lesson_id)
    if not is_authenticated():
        return redirect(url_for('home'))
    user_role = get_user_role()
    if user_role not in USER_ROLES:
        flash('Unauthorised. Not in roles', 'warning')
        return redirect(url_for('home'))
    elif user_role != 'instructor':
        flash('Unauthorised. Not instructor', 'warning')
        return redirect(url_for('home'))
    
    # Check if the request is a POST request (confirmation)
    if request.method == 'POST':
        # Delete the lesson slot from the database
        connection = get_cursor()
        connection.execute('DELETE FROM IndividualLessons WHERE lesson_id = %s;', (lesson_id,))
        
        flash('Lesson slot canceled successfully.', 'success')
        return redirect(url_for('instructor.manage_lesson_slots'))

    # If it's a GET request, retrieve the lesson slot information (if needed)
    connection = get_cursor()
    cursor = connection.execute('SELECT * FROM IndividualLessons WHERE lesson_id = %s;', (lesson_id,))
    lesson_slot = cursor.fetchone()
    connection.close()

    return render_template('instructors/confirm_cancel.html', lesson_slot=lesson_slot)