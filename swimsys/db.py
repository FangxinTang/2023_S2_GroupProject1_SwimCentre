from flask import session
import mysql.connector
import connect
from datetime import datetime, timedelta, date
import constance

dbconn = None
connection = None

def get_cursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


USER_ROLES = ['admin', 'member', 'instructor']

def is_authenticated():
    return 'user_id' in session

def get_user_role():
    if is_authenticated:
        if session['user_role'] == 'admin':
            return 'admin'
        elif session['user_role'] == 'member':
            return 'member'
        elif session['user_role'] == 'instructor':
            return 'instructor'
    return None




def get_member_account_by_user_id(user_id):    
    m_cursor = get_cursor()
    m_cursor.execute('SELECT * FROM Members where user_id = %s', (user_id,))
    member_account = m_cursor.fetchone()
    if member_account is None:
        return None
    else:
        return member_account

def get_all_courses_info_in_db():
    new_cursor =get_cursor()
    new_cursor.execute('select * from Courses')
    return new_cursor.fetchall()

def get_course_account_by_course_id(course_id):
    c_cursor = get_cursor()
    c_cursor.execute('SELECT * FROM Courses where course_id = %s', (course_id,))
    return c_cursor.fetchone()

def get_subscription_info_by_member_id(member_id):
    s_cursor = get_cursor()
    s_cursor.execute('select * from Subscriptions where member_id = %s', (member_id,))
    return s_cursor.fetchone()

def update_member_booked_courses(new_list_of_course_id, member_id):
    # Join the list back into a comma-separated string
    booked_courses_str = ','.join(new_list_of_course_id)
    # Update the member's booked courses in Members table
    update_m_cursor = get_cursor()
    update_m_cursor.execute('UPDATE Members SET booked_courses = %s WHERE member_id = %s', (booked_courses_str, member_id))

def update_course_booked_count(new_booked_count, course_id):
    update_c_cursor = get_cursor()
    update_c_cursor.execute('UPDATE Courses SET booked_count = %s WHERE course_id = %s', (new_booked_count, course_id))

def update_individual_lesson(new_member_id, new_lesson_status, lesson_id):
    try:
        cursor = get_cursor()
        update_query = """
            UPDATE IndividualLessons
            SET member_id = %s, lesson_status = %s
            WHERE lesson_id = %s
            """
        data = (new_member_id, new_lesson_status, lesson_id)
        cursor.execute(update_query, data)
        return True
    except Exception as e:
        print("Error:", e)
        return False

# for view my-booking page - for displaying group class info
def join_Memebrs_Instructors_Lessons_Pools():
    cursor = get_cursor()
    query = """
        SELECT
            m.member_id,
            il.lesson_id,
            il.date,
            il.lesson_time,
            il.lesson_duration,
            il.payment_date,
            i.first_name AS instructor_first_name,
            i.last_name AS instructor_last_name,
            p.pool_name
        FROM
            Members m
        LEFT JOIN
            IndividualLessons il ON m.member_id = il.member_id
        LEFT JOIN
            Instructors i ON il.instructor_id = i.instructor_id
        LEFT JOIN
            Pools p ON p.pool_id = il.pool_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

# for view my-booking page - for displaying individual lessons info
def join_Courses_Instructors_Pools():
    cursor =get_cursor()
    sql = """
        select 
            c.course_id,
            c.course_name,
            c.instructor_id,
            c.day_of_the_week,
            c.start_time,
            c.end_time,
            c.pool_id,
            i.first_name,
            i.last_name,
            p.pool_name
        from
            Courses c
        left join
            Instructors i ON c.instructor_id = i.instructor_id
        left join Pools p ON c.pool_id = p.pool_id;
"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
    
    

def get_member_booked_lessons(member_id):
    cursor = get_cursor()
    query ="""
        SELECT
            il.lesson_id,
            il.instructor_id,
            il.lesson_duration,
            il.day_of_the_week,
            il.lesson_time,
            il.lesson_fee,
            il.lesson_status
        FROM
            IndividualLessons il
        WHERE
            il.member_id = %s;
    """

    cursor.execute(query, (member_id,))
    all_booked_lessons = cursor.fetchall()
    return all_booked_lessons

# get hold of a list upcoming weekdays 
# for two weeks including today
def get_weekday_list():
    # get hold of the weekday index of today
    weekday_index = datetime.today().weekday()
     
    # get hold of the weekday indext list of the upcoming week 
    weekdays_indexlist = []
    for i in range (0,14):
        if weekday_index == 7:
            weekday_index = 0          
        weekdays_indexlist.append(weekday_index)
        weekday_index += 1
    
    # convert the weekday indext list into the corresponding weekdays 
    weekday_list = []
    for index in weekdays_indexlist:
        if index == 0:
            weekday = constance.DAYS[0]
        elif index == 1:
            weekday = constance.DAYS[1]
        elif index == 2:
            weekday = constance.DAYS[2]
        elif index == 3:
            weekday = constance.DAYS[3]
        elif index == 4:
            weekday = constance.DAYS[4]
        elif index == 5:
            weekday = constance.DAYS[5]
        elif index == 6:
            weekday = constance.DAYS[6]
        weekday_list.append(weekday)
    return weekday_list

# get hold of a list dates 
# for two weeks including today
def get_date_list():
    today = datetime.today()
    two_weeks_later = today + timedelta(days=14)
    date_list = []

    while today < two_weeks_later:
        date_list.append(today.strftime("%d/%m"))
        today += timedelta(days=1)
    
    return date_list

# get hold of a list of individual lessons 
# and update list with new date list 
def update_lesson_list():
    # date_list = get_date_list()
    connection = get_cursor()
    sql = 'SELECT * FROM IndividualLessons JOIN Instructors \
            ON IndividualLessons.instructor_id = \
            Instructors.instructor_id \
            ORDER BY lesson_id;'
    connection.execute(sql)
    lesson_list = connection.fetchall()
    
    return lesson_list

 

# convert date format 
# from db format to nz format 
def convert_date_format(date_str):
    # Convert the input date string to a datetime object using the correct format
    db_date_str = datetime.strptime(date_str, '%Y-%m-%d')
   
    # Convert the datetime object to the New Zealand format
    nz_date_str = db_date_str.strftime('%d/%m/%Y')
    return nz_date_str

#from nz format to db format 
def reverse_convert_date_format(nz_date_str):
    # Convert the input New Zealand date string to a datetime object using the NZ format
    nz_date = datetime.strptime(nz_date_str, '%d/%m/%Y')
   
    # Convert the datetime object to the db format 
    db_date_str = nz_date.strftime('%Y-%m-%d')
    return db_date_str

def get_member_names():
    connection = get_cursor()
    connection.execute('SELECT member_id, first_name, last_name FROM Members;')
    accounts= connection.fetchall()

    member_name_dict = {}
    for account in accounts:
        member_id, first_name, last_name = account
        member_name = first_name + ' ' + last_name
        member_name_dict.update({member_id: member_name})

    member_name_dict.update({'': 'all members'})
    return member_name_dict



# generate attendance chart data 
def generate_attendance_data(member_id, period):
    connection = get_cursor()

    sql_base = "SELECT activity_id, COUNT(activity_id) AS total_attendance FROM Attendance"

    if period == 'June':
        sql = f"{sql_base} WHERE attendance_date >= '2023-06-01' AND attendance_date < '2023-07-01'"
    elif period == 'July':
        sql = f"{sql_base} WHERE attendance_date >= '2023-07-01' AND attendance_date < '2023-08-01'"
    elif period == 'August':
        sql = f"{sql_base} WHERE attendance_date >= '2023-08-01' AND attendance_date < '2023-09-01'"
    elif period == 'September':
        sql = f"{sql_base} WHERE attendance_date >= '2023-09-01' AND attendance_date < '2023-10-01'"
    elif period == 'all periods':
        sql = f"{sql_base}"  # No specific date conditions for 'all periods'

    # Append member_id condition only if a specific member is chosen
    if member_id != 'all members':
        if period == 'all periods':
            sql += " WHERE member_id = %s"
        else:
            sql += " AND member_id = %s"
    

    # Complete the GROUP BY clause
    sql += " GROUP BY activity_id ORDER BY activity_id;"

    if member_id != 'all members':
        connection.execute(sql, (member_id,))
    else:
        connection.execute(sql)
  
    data = connection.fetchall()
    
    attendance_data = []
    for entry in data:
        attendance_data.append(entry[1])
    return attendance_data



def generate_aerobics_data(period):
    sql = "SELECT a.course_id, COUNT(a.course_id) AS total_attendance, \
        c.course_name, c.course_type, c.day_of_the_week, c.start_time, \
        c.end_time, c.instructor_id, i.first_name, i.last_name \
        FROM Attendance a \
        JOIN Courses c ON a.course_id = c.course_id \
        JOIN Instructors i ON c.instructor_id = i.instructor_id \
        WHERE a.activity_id=2"
    if period == 'June':
        sql += " AND attendance_date >= '2023-06-01' AND attendance_date < '2023-07-01'"
    elif period == 'July':
        sql += " AND attendance_date >= '2023-07-01' AND attendance_date < '2023-08-01'"
    elif period == 'August':
        sql += " AND attendance_date >= '2023-08-01' AND attendance_date < '2023-09-01'"
    elif period == 'September':
        sql += " AND attendance_date >= '2023-09-01' AND attendance_date < '2023-10-01'"
    elif period == 'all periods':
        sql = sql
    
    sql += " GROUP BY course_id ORDER BY course_id;"

    connection = get_cursor()
    connection.execute(sql)
    all_data = connection.fetchall()

    # print(all_data)

    aerobics_attendance_data = []
    for entry in all_data:
        aerobics_attendance_data.append(entry[1])

    return aerobics_attendance_data, all_data

  
# get period lists 
def get_month_list():
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
            JOIN Members ON IndividualLessons.member_id = Members.member_id;'
    connection.execute(sql)
    payment_list = connection.fetchall()
    # Create period list 
    month_list = []
    
    for payment in payment_list:

        date_str = str(payment[5])
        date = datetime.strptime(date_str,"%Y-%m-%d")
        payment_month = date.month
        
        if payment_month not in month_list:
            month_list.append(payment_month)
    
    return month_list      

def get_year_list():
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
            JOIN Members ON IndividualLessons.member_id = Members.member_id;'
    connection.execute(sql)
    payment_list = connection.fetchall()
    # Create period list 
    year_list = []
    
    for payment in payment_list:

        date_str = str(payment[5])
        date = datetime.strptime(date_str,"%Y-%m-%d")
        payment_year = date.year
        if payment_year not in  year_list:
            year_list.append(payment_year)     
    return year_list        



