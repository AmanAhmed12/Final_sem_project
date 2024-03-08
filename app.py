from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from mysql.connector.errors import IntegrityError
import mysql.connector



connection=mysql.connector.connect(host="Localhost",user="root",password="",database="online_quiz_system")

if connection.is_connected():
    print("connected succeesfully..")

else:
    print("Failed to connect...")

app = Flask(__name__)
app.secret_key = 'AmaanAhmed'

# Sample questions
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Rome', 'Berlin'],
        'answer': 'Paris'
    },
    {
        'question': 'What is 2+2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is 3+3?',
        'options': ['3', '4', '5', '6'],
        'answer': '6'
    },
    {
        'question': 'What is 4+4?',
        'options': ['3', '4', '8', '6'],
        'answer': '8'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admindashboard')
def adminLogin():
    return render_template('admindashboard.html')

@app.route('/studentdashboard')
def stuLogin():
    return render_template('studentdashboard.html')

@app.route('/defaultAdminDashContent')
def defaultAdminContent():
    return render_template('defaultAdminDashContent.html')

@app.route('/adminCreateAccount')
def adminCreateAccount():
    return render_template('adminAccountCreate.html')

@app.route('/ProfileUpdate')
def ProfileUpdate():
    return render_template('profileUpdate.html')

@app.route('/manageUsers')
def manageUsers():
    return render_template('manageUser.html')

@app.route('/logout')
def loggedOut():
    return render_template('logout.html')






@app.route('/closeupdate')
def closeupdate():
            if 'student' in session:
                return redirect(url_for('stuLogin'))  # Redirect to the login page
            elif 'admin' in session:
                return redirect(url_for('adminLogin'))  # Redirect to the login page
            else:
                # If the user type is not specified in the session, return an error or handle it accordingly
                flash("User type not specified", "error")
                return redirect(url_for('log'))
    



# Inserting data into details table
@app.route('/studentRegistration', methods=['POST'])
def insert_data():
    try:
        s_email = request.form.get('email')
        s_index = request.form.get('index')
        s_name = request.form.get('name')
        semester = request.form.get('semester')
        year = request.form.get('year')
        s_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')  # Hash password
        
        # Perform validation
        if not s_email or not s_index or not s_name or not semester or not year or not s_password:
            flash("All fields are required", "error")
            return redirect(url_for('register'))

        cursor = connection.cursor()
        sql = "INSERT INTO student_details(email,indexNo,username,password,semester,year,status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (s_email, s_index, s_name, s_password, semester, year, "active")
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        flash("Data inserted successfully into the details table", "success")
        return redirect(url_for('log'))

    except IntegrityError as e:
        flash("Account  or Index already available!", "error")
        return redirect(url_for('register'))
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('register'))

# login 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        s_email = request.form.get('email')
        s_password = request.form.get('password')
        
        cursor = connection.cursor()

        # Check admin_details table
        cursor.execute("SELECT email, password, status FROM admin_details WHERE email = %s", (s_email,))
        admin_data = cursor.fetchone()

        if admin_data:  # If user data exists
            if admin_data[0] == s_email and check_password_hash(admin_data[1], s_password) and admin_data[2] == "active":  # If password matches
                session['user_type'] = 'admin'  # Set session variable to identify user type
                session['admin'] = s_email  # Store the current user's email in the session
                sql = "UPDATE admin_details SET status = %s WHERE email = %s"
                cursor.execute(sql, ('loggedin', s_email))
                connection.commit()
                cursor.close()
                return redirect(url_for('adminLogin'))  # Redirect to admin dashboard

        # Check student_details table
        cursor.execute("SELECT email, password, status FROM student_details WHERE email = %s", (s_email,))
        student_data = cursor.fetchone()
       
        if student_data:  # If user data exists
            if student_data[0] == s_email and check_password_hash(student_data[1], s_password) and student_data[2] == "active":  # If password matches
                session['user_type'] = 'student'  # Set session variable to identify user type
                session['student'] = s_email  # Store the current user's email in the session
                sql = "UPDATE student_details SET status = %s WHERE email = %s"
                cursor.execute(sql, ('loggedin', s_email))
                connection.commit()
                cursor.close()
                return redirect(url_for('stuLogin'))  # Redirect to student dashboard

        cursor.close()

        # If no match is found in either table, show error message and redirect to login page
        flash("Invalid email or password", "error")
        return redirect(url_for('log'))
    
    # If it's a GET request, render the login page
    return render_template('login.html')

@app.route('/signOut', methods=['POST'])
def logOut():
    confirmed = request.form.get('confirmed')
    if confirmed == 'yes':
       
            cursor = connection.cursor()
            if 'student' in session:
                # If the session indicates that the current user is a student, update the student_details table
                sql = "UPDATE student_details SET status = %s WHERE email = %s"
                cursor.execute(sql, ('active', session.get('student')))
                connection.commit()
                cursor.close()
                session.pop('student')  # Remove the user's email from the session
                session.pop('user_type')  # Remove the user's type from the session
                flash("Logged out successfully student", "success")
                return redirect(url_for('log'))  # Redirect to the login page
            elif 'admin' in session:
                # If the session indicates that the current user is an admin, update the admin_details table
                sql = "UPDATE admin_details SET status = %s WHERE email = %s"
                cursor.execute(sql, ('active', session.get('admin')))
                connection.commit()
                cursor.close()
                session.pop('admin')  # Remove the user's email from the session
                session.pop('user_type')  # Remove the user's type from the session
                flash("Logged out successfully admin", "success")
                return redirect(url_for('log'))  # Redirect to the login page
            else:
                # If the user type is not specified in the session, return an error or handle it accordingly
                flash("User type not specified", "error")
                return redirect(url_for('log'))
     

    
    if 'student' in session:
        return redirect(url_for('stuLogin'))  # Redirect to the home page or another appropriate page
    elif 'admin' in session:
        return redirect(url_for('adminLogin'))  # Redirect to the home page or another appropriate page
    else:
        return redirect(url_for('loggedOut'))


@app.route('/updateAccount', methods=['POST'])
def updateAccount():
    newemail = request.form.get('email')
    newname = request.form.get('name')
    newpassword = generate_password_hash(request.form.get('newpass'), method='pbkdf2:sha256')
    cursor = connection.cursor()
    
  
    if 'student' in session:
            # If the session indicates that the current user is a student, update the student_details table
            sql = "UPDATE student_details SET username = %s, password = %s, email = %s, status = %s WHERE email = %s"
            cursor.execute(sql, (newname, newpassword, newemail, 'active', session.get('student')))
            connection.commit()
            cursor.close()
            session.pop('student')  # Remove the user's email from the session
            session.pop('user_type')  # Remove the user's type from the session
            flash("Profile updated successfully student", "success")
           
    elif 'admin' in session:
            # If the session indicates that the current user is an admin, update the admin_details table
            sql = "UPDATE admin_details SET username = %s, password = %s, email = %s, status = %s WHERE email = %s"
            cursor.execute(sql, (newname, newpassword, newemail, 'active', session.get('admin')))
            connection.commit()
            cursor.close()
            session.pop('admin')  # Remove the user's email from the session
            session.pop('user_type')  # Remove the user's type from the session
            flash("Profile updated successfully admin", "success")
          
    else:
           
            return redirect(url_for('log'))
        
    return redirect(url_for('log'))  # Redirect to the logout route

  
        
     

   
       

   
    





@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    for q in questions:
        selected_option = request.form.get(q['question'])
        if selected_option == q['answer']:
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)