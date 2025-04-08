# د اړینو ماډلونو واردول
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import mysql.connector

# د اپلیکیشن او ډېټابېس تنظیم
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # د اپلوډ شویو فایلونو لپاره فولډر

# د ډېټابېس اړیکه جوړولو فنکشن
import os
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    return conn

# -----------------------------------
# 1. د استادانو برخه (Teachers)
# -----------------------------------
# د استادانو جدول جوړول
def init_teachers_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15)
        )
    """)
    conn.commit()
    conn.close()

# د استاد اضافه کولو فنکشن
def add_teacher(name, email, phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teachers (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    conn.commit()
    conn.close()

# د ټولو استادانو لېست راوړل
def get_all_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return teachers

# د استادانو روټ (GET او POST)
@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        add_teacher(name, email, phone)
        return jsonify({'success': True, 'message': 'استاد په بریالیتوب سره اضافه شو'})
    teachers_list = get_all_teachers()
    return render_template('teachers.html', teachers=teachers_list)

# -----------------------------------
# 2. د شاګردانو برخه (Students)
# -----------------------------------
# د شاګردانو جدول جوړول
def init_students_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15)
        )
    """)
    conn.commit()
    conn.close()

# د شاګرد اضافه کولو فنکشن
def add_student(name, email, phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
    conn.commit()
    conn.close()

# د ټولو شاګردانو لېست راوړل
def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

# د شاګردانو روټ
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        add_student(name, email, phone)
        return jsonify({'success': True, 'message': 'شاګرد په بریالیتوب سره اضافه شو'})
    students_list = get_all_students()
    return render_template('students.html', students=students_list)

# -----------------------------------
# 3. د کورسونو برخه (Courses)
# -----------------------------------
# د کورسونو جدول جوړول
def init_courses_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)
    conn.commit()
    conn.close()

# د کورس اضافه کولو فنکشن
def add_course(course_name, department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (course_name, department_id) VALUES (%s, %s)", (course_name, department_id))
    conn.commit()
    conn.close()

# د ټولو کورسونو لېست راوړل
def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, course_name, department_id FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

# د کورسونو روټ
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        course_name = request.form['course_name']
        department_id = request.form['department_id']
        add_course(course_name, department_id)
        return jsonify({'success': True, 'message': 'کورس په بریالیتوب سره اضافه شو'})
    courses_list = get_all_courses()
    return render_template('courses.html', courses=courses_list)

# -----------------------------------
# 4. د څانګو برخه (Departments)
# -----------------------------------
# د څانګو جدول جوړول
def init_departments_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# د څانګې اضافه کولو فنکشن
def add_department(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

# د ټولو څانګو لېست راوړل
def get_all_departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM departments")
    departments = cursor.fetchall()
    conn.close()
    return departments

# د څانګو روټ
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'POST':
        name = request.form['name']
        add_department(name)
        return jsonify({'success': True, 'message': 'څانګه په بریالیتوب سره اضافه شوه'})
    departments_list = get_all_departments()
    return render_template('departments.html', departments=departments_list)

# -----------------------------------
# 5. د داخلې برخه (Enrollments)
# -----------------------------------
# د داخلې جدول جوړول
def init_enrollments_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            enrollment_date DATE,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    conn.commit()
    conn.close()

# د داخلې اضافه کولو فنکشن
def add_enrollment(student_id, course_id, enrollment_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)", 
                   (student_id, course_id, enrollment_date))
    conn.commit()
    conn.close()

# د ټولو داخلې لېست راوړل
def get_all_enrollments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, s.name, c.course_name, e.enrollment_date 
        FROM enrollments e 
        JOIN students s ON e.student_id = s.id 
        JOIN courses c ON e.course_id = c.id
    """)
    enrollments = cursor.fetchall()
    conn.close()
    return enrollments

# د داخلې روټ
@app.route('/enrollments', methods=['GET', 'POST'])
def enrollments():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        enrollment_date = request.form['enrollment_date']
        add_enrollment(student_id, course_id, enrollment_date)
        return jsonify({'success': True, 'message': 'داخله په بریالیتوب سره ثبت شوه'})
    enrollments_list = get_all_enrollments()
    students_list = get_all_students()
    courses_list = get_all_courses()
    return render_template('enrollments.html', enrollments=enrollments_list, students=students_list, courses=courses_list)

# -----------------------------------
# 6. د نمرو برخه (Grades)
# -----------------------------------
# د نمرو جدول جوړول
def init_grades_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            grade DECIMAL(5,2),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    conn.commit()
    conn.close()

# د نمرې اضافه کولو فنکشن
def add_grade(student_id, course_id, grade):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)", 
                   (student_id, course_id, grade))
    conn.commit()
    conn.close()

# د ټولو نمرو لېست راوړل
def get_all_grades():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.id, s.name, c.course_name, g.grade 
        FROM grades g 
        JOIN students s ON g.student_id = s.id 
        JOIN courses c ON g.course_id = c.id
    """)
    grades = cursor.fetchall()
    conn.close()
    return grades

# د نمرو روټ
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        grade = request.form['grade']
        add_grade(student_id, course_id, grade)
        return jsonify({'success': True, 'message': 'نمره په بریالیتوب سره ثبت شوه'})
    grades_list = get_all_grades()
    return render_template('grades.html', grades=grades_list)

# -----------------------------------
# 7. د کارونکو برخه (Users)
# -----------------------------------
# د کارونکو جدول جوړول
def init_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'Teacher', 'Student') NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# د کارن اضافه کولو فنکشن
def add_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                   (username, password, role))
    conn.commit()
    conn.close()

# د ټولو کارونکو لېست راوړل
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# د کارونکو روټ
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        add_user(username, password, role)
        return jsonify({'success': True, 'message': 'کارن په بریالیتوب سره اضافه شو'})
    users_list = get_all_users()
    return render_template('users.html', users=users_list)

# -----------------------------------
# 8. د حاضرۍ برخه (Attendance)
# -----------------------------------
# د حاضرۍ جدول جوړول
def init_attendance_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            date DATE,
            status ENUM('Present', 'Absent') NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    conn.commit()
    conn.close()

# د حاضرۍ اضافه کولو فنکشن
def add_attendance(student_id, course_id, date, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, course_id, date, status) VALUES (%s, %s, %s, %s)", 
                   (student_id, course_id, date, status))
    conn.commit()
    conn.close()

# د ټولو حاضرۍ لېست راوړل
def get_all_attendance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, s.name, c.course_name, a.date, a.status 
        FROM attendance a 
        JOIN students s ON a.student_id = s.id 
        JOIN courses c ON a.course_id = c.id
    """)
    attendance = cursor.fetchall()
    conn.close()
    return attendance

# د حاضرۍ روټ
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        date = request.form['date']
        status = request.form['status']
        add_attendance(student_id, course_id, date, status)
        return jsonify({'success': True, 'message': 'حاضري په بریالیتوب سره ثبت شوه'})
    attendance_list = get_all_attendance()
    return render_template('attendance.html', attendance=attendance_list)

# -----------------------------------
# 9. د مهال‌وېش برخه (Schedule)
# -----------------------------------
# د مهال‌وېش جدول جوړول
def init_schedule_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_id INT,
            teacher_id INT,
            day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            start_time TIME,
            end_time TIME,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    conn.commit()
    conn.close()

# د مهال‌وېش اضافه کولو فنکشن
def add_schedule(course_id, teacher_id, day, start_time, end_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedule (course_id, teacher_id, day, start_time, end_time) VALUES (%s, %s, %s, %s, %s)", 
                   (course_id, teacher_id, day, start_time, end_time))
    conn.commit()
    conn.close()

# د ټولو مهال‌وېش لېست راوړل
def get_all_schedule():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sch.id, c.course_name, t.name, sch.day, sch.start_time, sch.end_time 
        FROM schedule sch 
        JOIN courses c ON sch.course_id = c.id 
        JOIN teachers t ON sch.teacher_id = t.id
    """)
    schedule = cursor.fetchall()
    conn.close()
    return schedule

# د مهال‌وېش روټ
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        course_id = request.form['course_id']
        teacher_id = request.form['teacher_id']
        day = request.form['day']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        add_schedule(course_id, teacher_id, day, start_time, end_time)
        return jsonify({'success': True, 'message': 'مهال‌وېش په بریالیتوب سره ثبت شو'})
    schedule_list = get_all_schedule()
    return render_template('schedule.html', schedule=schedule_list)

# -----------------------------------
# 10. د کورنۍ دندو برخه (Assignments)
# -----------------------------------
# د کورنۍ دندو جدول جوړول
def init_assignments_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            assigned_date DATE,
            due_date DATE,
            file_path VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

# د کورنۍ دندې اضافه کولو فنکشن
def add_assignment(title, description, assigned_date, due_date, file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO assignments (title, description, assigned_date, due_date, file_path) VALUES (%s, %s, %s, %s, %s)", 
                   (title, description, assigned_date, due_date, file_path))
    conn.commit()
    conn.close()

# د ټولو کورنۍ دندو لېست راوړل
def get_all_assignments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, assigned_date, due_date, file_path FROM assignments")
    assignments = cursor.fetchall()
    conn.close()
    return assignments

# د کورنۍ دندو روټ
@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assigned_date = request.form['assigned_date']
        due_date = request.form['due_date']
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
        add_assignment(title, description, assigned_date, due_date, file_path)
        return jsonify({'success': True, 'message': 'کورنۍ دنده په بریالیتوب سره ثبت شوه'})
    assignments_list = get_all_assignments()
    return render_template('assignments.html', assignments=assignments_list)

# -----------------------------------
# 11. د سپارنو برخه (Submissions)
# -----------------------------------
# د سپارنو جدول جوړول
def init_submissions_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            assignment_id INT,
            submission_date DATE,
            file_path VARCHAR(255),
            grade DECIMAL(5,2) DEFAULT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (assignment_id) REFERENCES assignments(id)
        )
    """)
    conn.commit()
    conn.close()

# د سپارنې اضافه کولو فنکشن
def add_submission(student_id, assignment_id, submission_date, file_path, grade=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO submissions (student_id, assignment_id, submission_date, file_path, grade) VALUES (%s, %s, %s, %s, %s)", 
                   (student_id, assignment_id, submission_date, file_path, grade))
    conn.commit()
    conn.close()

# د ټولو سپارنو لېست راوړل
def get_all_submissions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sub.id, s.name, a.title, sub.submission_date, sub.file_path, sub.grade 
        FROM submissions sub 
        JOIN students s ON sub.student_id = s.id 
        JOIN assignments a ON sub.assignment_id = a.id
    """)
    submissions = cursor.fetchall()
    conn.close()
    return submissions

# د سپارنو روټ
@app.route('/submissions', methods=['GET', 'POST'])
def submissions():
    if request.method == 'POST':
        student_id = request.form['student_id']
        assignment_id = request.form['assignment_id']
        submission_date = request.form['submission_date']
        grade = request.form.get('grade') or None
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
        add_submission(student_id, assignment_id, submission_date, file_path, grade)
        return jsonify({'success': True, 'message': 'سپارنه په بریالیتوب سره ثبت شوه'})
    submissions_list = get_all_submissions()
    students_list = get_all_students()
    assignments_list = get_all_assignments()
    return render_template('submissions.html', submissions=submissions_list, students=students_list, assignments=assignments_list)

# -----------------------------------
# 12. د اعلاناتو برخه (Notifications)
# -----------------------------------
# د اعلاناتو جدول جوړول
def init_notifications_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            target ENUM('Teachers', 'Students', 'All') NOT NULL,
            published_date DATE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# د اعلان اضافه کولو فنکشن
def add_notification(title, message, target, published_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (title, message, target, published_date) VALUES (%s, %s, %s, %s)", 
                   (title, message, target, published_date))
    conn.commit()
    conn.close()

# د ټولو اعلاناتو لېست راوړل
def get_all_notifications():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, message, target, published_date FROM notifications")
    notifications = cursor.fetchall()
    conn.close()
    return notifications

# د اعلاناتو روټ
@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        target = request.form['target']
        published_date = request.form['published_date']
        add_notification(title, message, target, published_date)
        return jsonify({'success': True, 'message': 'اعلان په بریالیتوب سره ثبت شو'})
    notifications_list = get_all_notifications()
    return render_template('notifications.html', notifications=notifications_list)

# -----------------------------------
# 13. د فیډبک برخه (Feedback)
# -----------------------------------
# د فیډبک جدول جوړول
def init_feedback_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            teacher_id INT,
            course_id INT,
            message TEXT NOT NULL,
            feedback_date DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    conn.commit()
    conn.close()

# د فیډبک اضافه کولو فنکشن
def add_feedback(student_id, teacher_id, course_id, message, feedback_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (student_id, teacher_id, course_id, message, feedback_date) VALUES (%s, %s, %s, %s, %s)", 
                   (student_id, teacher_id, course_id, message, feedback_date))
    conn.commit()
    conn.close()

# د ټولو فیډبک لېست راوړل
def get_all_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, s.name AS student_name, t.name AS teacher_name, c.course_name, f.message, f.feedback_date 
        FROM feedback f 
        JOIN students s ON f.student_id = s.id 
        JOIN teachers t ON f.teacher_id = t.id 
        JOIN courses c ON f.course_id = c.id
    """)
    feedback = cursor.fetchall()
    conn.close()
    return feedback

# د فیډبک روټ
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        student_id = request.form['student_id']
        teacher_id = request.form['teacher_id']
        course_id = request.form['course_id']
        message = request.form['message']
        feedback_date = request.form['feedback_date']
        add_feedback(student_id, teacher_id, course_id, message, feedback_date)
        return jsonify({'success': True, 'message': 'فیډبک په بریالیتوب سره ثبت شو'})
    feedback_list = get_all_feedback()
    students_list = get_all_students()
    teachers_list = get_all_teachers()
    courses_list = get_all_courses()
    return render_template('feedback.html', feedback=feedback_list, students=students_list, teachers=teachers_list, courses=courses_list)

# -----------------------------------
# 14. د کتابتون برخه (Library)
# -----------------------------------
# د کتابتون جدول جوړول
def init_library_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            isbn VARCHAR(13) UNIQUE NOT NULL,
            availability ENUM('Available', 'Unavailable') DEFAULT 'Available'
        )
    """)
    conn.commit()
    conn.close()

# د کتاب اضافه کولو فنکشن
def add_book(title, author, isbn, availability='Available'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO library (title, author, isbn, availability) VALUES (%s, %s, %s, %s)", 
                   (title, author, isbn, availability))
    conn.commit()
    conn.close()

# د ټولو کتابونو لېست راوړل
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, isbn, availability FROM library")
    books = cursor.fetchall()
    conn.close()
    return books

# د کتابتون روټ
@app.route('/library', methods=['GET', 'POST'])
def library():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        availability = request.form['availability']
        add_book(title, author, isbn, availability)
        return jsonify({'success': True, 'message': 'کتاب په بریالیتوب سره ثبت شو'})
    books_list = get_all_books()
    return render_template('library.html', books=books_list)

# -----------------------------------
# 15. د لاګونو برخه (Logs)
# -----------------------------------
# د لاګونو جدول جوړول
def init_logs_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            action TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# د لاګ اضافه کولو فنکشن
def add_log(user_id, action, timestamp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, action, timestamp) VALUES (%s, %s, %s)", 
                   (user_id, action, timestamp))
    conn.commit()
    conn.close()

# د ټولو لاګونو لېست راوړل
def get_all_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, u.username, l.action, l.timestamp 
        FROM logs l 
        JOIN users u ON l.user_id = u.id
    """)
    logs = cursor.fetchall()
    conn.close()
    return logs

# د لاګونو روټ
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']
        timestamp = datetime.now()
        add_log(user_id, action, timestamp)
        return jsonify({'success': True, 'message': 'لاګ په بریالیتوب سره ثبت شو'})
    logs_list = get_all_logs()
    users_list = get_all_users()
    return render_template('logs.html', logs=logs_list, users=users_list)

# -----------------------------------
# 16. د کور پاڼې روټ (Home)
# -----------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -----------------------------------
# د اپلیکیشن چلول او جدولونو جوړول
# -----------------------------------
if __name__ == '__main__':
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
    # لومړی خپلواک جدولونه (چې نورو ته اړتیا نلري)
    init_departments_table()   # 4. څانګې - مخکې له courses
    init_teachers_table()      # 1. استادان - مخکې له schedule او feedback
    init_students_table()      # 2. شاګردان - مخکې له enrollments, grades, attendance, feedback
    init_users_table()         # 7. کارونکي - مخکې له logs
    
    # دویم وابسته جدولونه (چې نورو جدولونو ته اړتیا لري)
    init_courses_table()       # 3. کورسونه - وروسته له departments
    init_enrollments_table()   # 5. داخلې - وروسته له students او courses
    init_grades_table()        # 6. نمرې - وروسته له students او courses
    init_attendance_table()    # 8. حاضري - وروسته له students او courses
    init_schedule_table()      # 9. مهال‌وېش - وروسته له courses او teachers
    init_assignments_table()   # 10. کورنۍ دندې - مخکې له submissions
    init_submissions_table()   # 11. سپارنې - وروسته له students او assignments
    init_notifications_table() # 12. اعلانات - خپلواک
    init_feedback_table()      # 13. فیډبک - وروسته له students, teachers, courses
    init_library_table()       # 14. کتابتون - خپلواک
    init_logs_table()          # 15. لاګونه - وروسته له users
    
    # سرور چلول
    app.run(debug=True)