from flask import Flask, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from mysql.connector.errors import IntegrityError
import mysql.connector
import traceback
from flask_mail import Mail,Message   
import uuid
import random
import string


connection=mysql.connector.connect(host="Localhost",user="root",password="",database="online_quiz_system")

if connection.is_connected():
    print("connected succeesfully..")

else:
    print("Failed to connect...")

app = Flask(__name__)
# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ananahd1000@gmail.com'  
app.config['MAIL_PASSWORD'] = 'sqxb fzvr lonm oojx'  
mail=Mail(app)
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

@app.route('/generateQuiz')
def generateQuiz():
    return render_template('generateQuiz.html')

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

@app.route('/defaultStuDashContent')
def defaultStuDashContent():
    return render_template('defaultStudentDashContent.html')

@app.route('/adminCreateAccount')
def adminCreateAccount():
    return render_template('adminAccountCreate.html')

@app.route('/ProfileUpdate')
def ProfileUpdate():
    return render_template('profileUpdate.html')

@app.route('/loadGuidelines')
def loadGuidelines():
    return render_template('guidelines.html')

@app.route('/manageUsers')
def manageUsers():
    return render_template('manageUser.html')

@app.route('/logout')
def loggedOut():
    return render_template('logout.html')

@app.route('/forgotpwd')
def forgotpwd():
    return render_template('forgotpassword.html')

@app.route('/manageQuiz')
def manageQuiz():
    return render_template('manageQuiz.html')

@app.route('/updateQuestions')
def updateQuestions():
    return render_template('updateQuestions.html')

@app.route('/firstYearFirstSem')
def firstYearFirstSem():
    return render_template('quizFirstYearFirstSem.html')

@app.route('/firstYearSecondSem')
def firstYearSecondSem():
    return render_template('quizFirstYearSecondSem.html')

@app.route('/SecondYearFirstSem')
def SecondYearFirstSem():
    return render_template('quizSecondYearFirstSem.html')

@app.route('/SecondYearSecondSem')
def SecondYearSecondSem():
    return render_template('quizSecondYearSecondSem.html')


@app.route('/attemptQuiz')
def attemptQuiz():
    return render_template('attemptQuiz.html')



# display year when student login
def get_user_data(email):
    cursor = connection.cursor()
    cursor.execute("SELECT year FROM student_details WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    cursor.close()
    return  int(user_data[0]) 


#close icon
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
        sql = "INSERT INTO student_details(email,index_no,username,password,semester,year,status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (s_email, s_index, s_name, s_password, semester, year, "active")
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        flash("Account Created Successfully !!!", "success")
        return redirect(url_for('log'))

    except IntegrityError as e:
        flash("Account  or Index already available!", "error")
        return redirect(url_for('register'))
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('register'))
    





# create admin account
@app.route('/createAdminAccount', methods=['POST'])
def createAdminAccount():
    try:
        s_email = request.form.get('email')
        s_name = request.form.get('name')
        s_password = request.form.get('password')
        s_confirmpassword = request.form.get('confirmpassword')  # corrected variable name
        
        # Perform validation
        if not s_email or not s_password or not s_name:
            flash("All fields are required", "error")
            return redirect(url_for('adminCreateAccount'))
        elif s_password != s_confirmpassword:
            flash("Passwords do not match", "error")
            return redirect(url_for('adminCreateAccount'))
        else:
            # Hash the password
            hashed_password =generate_password_hash(request.form.get('confirmpassword'), method='pbkdf2:sha256')  # Hash password

            cursor = connection.cursor()
            sql = "INSERT INTO admin_details(email, username, password, status) VALUES (%s, %s, %s, %s)"
            val = (s_email, s_name,hashed_password, "active")
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
            flash("Admin Account created successfully", "success")
            return redirect(url_for('adminCreateAccount'))

    except IntegrityError as e:
        flash("Account already available!", "error")
        return redirect(url_for('adminCreateAccount'))
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('adminCreateAccount'))






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
                # Call get_user_data function to fetch user's year and store it in session
                user_year = get_user_data(s_email)
                if user_year:
                        session['user_year'] = user_year
                else:
                        session.pop('user_year', None)

                return redirect(url_for('stuLogin'))  # Redirect to student dashboard

        cursor.close()

        # If no match is found in either table, show error message and redirect to login page
        flash("Invalid email or password", "error")
        return redirect(url_for('log'))
    
    # If it's a GET request, render the login page
    return render_template('login.html')



#signout
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


#update Account
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

  

#forgot password
@app.route('/forgotpassword', methods=['POST'])
def forgotpassword():        
    try:
        s_email = request.form.get('email')
        s_password = request.form.get('password')
        s_confirmpassword = request.form.get('confirmpassword')  # corrected variable name
       
        
        # Perform validation
        if not s_confirmpassword or not s_password or not s_email:
            flash("All fields are required", "error")
            return redirect(url_for('forgotpwd'))
        elif s_password != s_confirmpassword:
            flash("Passwords do not match", "error")
            return redirect(url_for('forgotpwd'))
        else:
            cursor = connection.cursor()
               # Check student_details table
            cursor.execute("SELECT email FROM student_details WHERE email = %s", (s_email,))
            student_data = cursor.fetchone()
       
            if student_data:  # If user data exists
                  
                    msg = Message('Subject: New Password for Your Account', sender='ananahd1000@gmail.com', recipients=[s_email])  # Replace sender and recipients
                    msg.body =  f"Your new password is: {s_confirmpassword}"
                    mail.send(msg)
                    hashed_password =generate_password_hash(request.form.get('confirmpassword'), method='pbkdf2:sha256')  # Hash password
                    # If the session indicates that the current user is an admin, update the admin_details table
                    sql = "UPDATE student_details SET  password = %s WHERE email = %s"
                    cursor.execute(sql, (hashed_password,s_email))
                    connection.commit()
                    cursor.close()
                    flash("password updated successfully student", "success")
                    return redirect(url_for('log'))
            
            cursor.execute("SELECT email FROM admin_details WHERE email = %s", (s_email,))
            admin_data = cursor.fetchone()
            if admin_data:  # If user data exists 
                    msg = Message('Subject: New Password for Your Account', sender='ananahd1000@gmail.com', recipients=[s_email])  # Replace sender and recipients
                    msg.body =  f"Your new password is: {s_confirmpassword}"
                    mail.send(msg)
                    hashed_password =generate_password_hash(request.form.get('confirmpassword'), method='pbkdf2:sha256')  # Hash password
                    # If the session indicates that the current user is an admin, update the admin_details table
                    sql = "UPDATE admin_details SET  password = %s WHERE email = %s"
                    cursor.execute(sql, (hashed_password,s_email))
                    connection.commit()
                    cursor.close()
                    flash("password updated successfully admin", "success")
                    return redirect(url_for('log'))  # Redirect to the login page
                
              
            flash("Account not found", "error")
            return redirect(url_for('forgotpwd'))  # Redirect to the login page


    except IntegrityError as e:
        flash("Account already available!", "error")
        return redirect(url_for('forgotpwd'))
    
    except Exception as e:
     
        flash(f"An error occurred: {traceback.format_exc()}", "error")
        return redirect(url_for('forgotpwd'))
    

#update user status
@app.route('/update_user_status/<string:email>/<string:action>', methods=['POST'])
def update_user_status(email, action):
    try:
        cursor = connection.cursor()
        if action == 'activate':
            status = 'active'
        elif action == 'deactivate':
            status = 'inactive'
        else:
            flash("Invalid action", "error")
            return redirect(url_for('manageUsers'))

        sql = "UPDATE student_details SET status = %s WHERE email = %s"
        cursor.execute(sql, (status, email))
        connection.commit()
        cursor.close()
        return redirect(url_for('displayUsers'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('manageUsers'))


#display users
@app.route('/displayUsers')
def displayUsers():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT email, index_no, username, password, semester, year, status FROM student_details")
        users_data = cursor.fetchall()
        cursor.close()
        return render_template('manageUser.html', users=users_data)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('adminLogin'))



@app.route('/quizGenerate', methods=['POST'])
def quizGenerate():  
    try:
        # Extract quiz details from the form data
        quiz_id = request.form.get('quizid')
        subject_name = request.form.get('name')
        semester = request.form.get('semester')
        year = request.form.get('year')
        
        cursor = connection.cursor()

       

        # Insert quiz details into the quiz table
        sql_quiz = "INSERT INTO quiz(quiz_id,semester, subject, year) VALUES (%s, %s, %s, %s)"
        val_quiz = (quiz_id, semester, subject_name, year)
        cursor.execute(sql_quiz, val_quiz)

        # Extract questions and answers
        for i in range(1, 21):
            question = request.form.get(f'q{i}')
            answer = request.form.get(f'q{i}a1').lower()
             # Generate a unique qid
            qid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            # Insert each question and answer into the questions table
            sql_question = "INSERT INTO questions(quiz_id, qid, semester, subject, questions, answers) VALUES (%s, %s, %s, %s, %s, %s)"
            val_question = (quiz_id, qid, semester, subject_name, question, answer)
            cursor.execute(sql_question, val_question)

        # Commit the transaction
        connection.commit()
        cursor.close()

        flash("Quiz Generated Successfully!", "success")
        return redirect(url_for('generateQuiz'))  # Redirect to a suitable view after quiz generation

    except IntegrityError as e:
        flash("Quiz details already exist or Integrity error!", "error")
        return redirect(url_for('generateQuiz'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('generateQuiz'))


    

#view quiz
@app.route('/viewQuiz')
def viewQuiz():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT  qid,semester, subject, questions,answers,quiz_id FROM questions")
        quiz_data = cursor.fetchall()
        cursor.close()
        return render_template('manageQuiz.html', quizes=quiz_data)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('manageQuiz'))
    


@app.route('/update_quiz_status/<string:qid>/<string:action>', methods=['POST'])
def update_quiz_status(qid, action):
    try:
        cursor = connection.cursor()
        if action == 'Delete':
            sql = "DELETE FROM questions WHERE qid= %s"
            cursor.execute(sql, (qid,))
            connection.commit()
            cursor.close()
            flash("Deleted Successfully!!!", "success")
            return redirect(url_for('viewQuiz'))  # Redirect after deletion
        
        elif action == 'Update':
            # Fetch the details of the question using the qid
            sql = "SELECT * FROM questions WHERE qid = %s"
            cursor.execute(sql, (qid,))
            question_details = cursor.fetchone()
            cursor.close()

            # Pass the question details to the updateQuestions.html template
            return render_template('updateQuestions.html', question_details=question_details)
        
        else:
            flash("Invalid action", "error")
            return redirect(url_for('viewQuiz'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('viewQuiz'))

    


@app.route('/updateQuestionsForm', methods=['POST'])
def updateQuestionsForm():
    try:
        cursor = connection.cursor()
        qid = request.form.get('qid')
        quiz_id = request.form.get('quizid')
        subject = request.form.get('name')
        semester = request.form.get('semester')
        question = request.form.get('q1')
        answer = request.form.get('q1a1')

        sql = "UPDATE questions SET semester = %s, subject = %s, questions = %s, answers = %s, quiz_id = %s WHERE qid = %s"
        cursor.execute(sql, (semester, subject, question, answer, quiz_id, qid))
        connection.commit()
        cursor.close()
        flash("Successfully Updated Question !!!")
        return redirect(url_for('viewQuiz'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('viewQuiz'))



@app.route('/quiz', methods=['GET'])
def quiz():
    try:
        cursor = connection.cursor()
        sql = "SELECT semester FROM student_details WHERE email = %s"
        cursor.execute(sql, (session.get('student'),))
        semester_row = cursor.fetchone()
        cursor.close()

        if semester_row:
            semester = semester_row[0]  # Extract the string value from the tuple
            if semester == "First Year First semester":
                return redirect(url_for('firstYearFirstSem'))
            elif semester == "First Year Second semester":
                return redirect(url_for('firstYearSecondSem'))
            elif semester == "Second Year First semester":
                return redirect(url_for('SecondYearFirstSem'))
            elif semester == "Second Year Second semester":
                return redirect(url_for('SecondYearSecondSem'))
            else:
                flash("Successfully Updated Question !!!")
                return redirect(url_for('viewQuiz'))
        else:
            flash("Semester information not found for the user.")
            return redirect(url_for('viewQuiz'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('viewQuiz'))
    






@app.route('/attemptQuizSubOne', methods=['GET'])
def attemptQuizSubOne():
    try:
        # Assume connection object is defined and imported properly
        cursor = connection.cursor()
        sql = "SELECT questions, answers FROM questions WHERE subject = 'sub1' AND semester = 'First Year First semester' ORDER BY RAND() LIMIT 10"
        cursor.execute(sql)
        question_data = cursor.fetchall()  # Fetch all the questions and correct answers
        cursor.close()
        
        questions = []  # List to store questions
        answers = []  # List to store answers for questions
        
        # Fetch answers for the other questions
        for question, correct_answer in question_data:
            # Fetch two random incorrect answers from other questions
            cursor = connection.cursor()
            sql = "SELECT answers FROM questions WHERE subject = 'sub1' AND semester = 'First Year First semester' AND answers != %s ORDER BY RAND() LIMIT 2"
            cursor.execute(sql, (correct_answer,))
            other_answers = [row[0] for row in cursor.fetchall()]  # Fetch two incorrect answers
            cursor.close()
            
            # Add the correct answer and two other random incorrect answers
            all_answers = [correct_answer] + other_answers
            random.shuffle(all_answers)  # Shuffle the answers
            
            questions.append(question)
            answers.append(all_answers)
        
        return render_template('attemptQuiz.html', questions=questions, answers=answers)

    except Exception as e:
        print(e)
        flash("An error occurred while fetching questions.", "error")
        return redirect(url_for('viewQuiz'))
    



@app.route('/attemptQuizSubTwo', methods=['GET'])
def attemptQuizSubTwo():
    try:
        # Assume connection object is defined and imported properly
        cursor = connection.cursor()
        sql = "SELECT questions, answers FROM questions WHERE subject = 'sub2' AND semester = 'First Year First semester' ORDER BY RAND() LIMIT 10"
        cursor.execute(sql)
        question_data = cursor.fetchall()  # Fetch all the questions and correct answers
        cursor.close()
        
        questions = []  # List to store questions
        answers = []  # List to store answers for questions
        
        # Fetch answers for the other questions
        for question, correct_answer in question_data:
            # Fetch two random incorrect answers from other questions
            cursor = connection.cursor()
            sql = "SELECT answers FROM questions WHERE subject = 'sub2' AND semester = 'First Year First semester' AND answers != %s ORDER BY RAND() LIMIT 2"
            cursor.execute(sql, (correct_answer,))
            other_answers = [row[0] for row in cursor.fetchall()]  # Fetch two incorrect answers
            cursor.close()
            
            # Add the correct answer and two other random incorrect answers
            all_answers = [correct_answer] + other_answers
            random.shuffle(all_answers)  # Shuffle the answers
            
            questions.append(question)
            answers.append(all_answers)
        
        return render_template('attemptQuiz.html', questions=questions, answers=answers)

    except Exception as e:
        print(e)
        flash("An error occurred while fetching questions.", "error")
        return redirect(url_for('viewQuiz'))
    

@app.route('/attemptQuizSubThree', methods=['GET'])
def attemptQuizSubThree():
    try:
        # Assume connection object is defined and imported properly
        cursor = connection.cursor()
        sql = "SELECT questions, answers FROM questions WHERE subject = 'sub3' AND semester = 'First Year First semester' ORDER BY RAND() LIMIT 10"
        cursor.execute(sql)
        question_data = cursor.fetchall()  # Fetch all the questions and correct answers
        cursor.close()
        
        questions = []  # List to store questions
        answers = []  # List to store answers for questions
        
        # Fetch answers for the other questions
        for question, correct_answer in question_data:
            # Fetch two random incorrect answers from other questions
            cursor = connection.cursor()
            sql = "SELECT answers FROM questions WHERE subject = 'sub3' AND semester = 'First Year First semester' AND answers != %s ORDER BY RAND() LIMIT 2"
            cursor.execute(sql, (correct_answer,))
            other_answers = [row[0] for row in cursor.fetchall()]  # Fetch two incorrect answers
            cursor.close()
            
            # Add the correct answer and two other random incorrect answers
            all_answers = [correct_answer] + other_answers
            random.shuffle(all_answers)  # Shuffle the answers
            
            questions.append(question)
            answers.append(all_answers)
        
        return render_template('attemptQuiz.html', questions=questions, answers=answers)

    except Exception as e:
        print(e)
        flash("An error occurred while fetching questions.", "error")
        return redirect(url_for('viewQuiz'))
    



@app.route('/attemptQuizSubFour', methods=['GET'])
def attemptQuizSubFour():
    try:
        # Assume connection object is defined and imported properly
        cursor = connection.cursor()
        sql = "SELECT questions, answers FROM questions WHERE subject = 'sub4' AND semester = 'First Year First semester' ORDER BY RAND() LIMIT 10"
        cursor.execute(sql)
        question_data = cursor.fetchall()  # Fetch all the questions and correct answers
        cursor.close()
        
        questions = []  # List to store questions
        answers = []  # List to store answers for questions
        
        # Fetch answers for the other questions
        for question, correct_answer in question_data:
            # Fetch two random incorrect answers from other questions
            cursor = connection.cursor()
            sql = "SELECT answers FROM questions WHERE subject = 'sub4' AND semester = 'First Year First semester' AND answers != %s ORDER BY RAND() LIMIT 2"
            cursor.execute(sql, (correct_answer,))
            other_answers = [row[0] for row in cursor.fetchall()]  # Fetch two incorrect answers
            cursor.close()
            
            # Add the correct answer and two other random incorrect answers
            all_answers = [correct_answer] + other_answers
            random.shuffle(all_answers)  # Shuffle the answers
            
            questions.append(question)
            answers.append(all_answers)
        
        return render_template('attemptQuiz.html', questions=questions, answers=answers)

    except Exception as e:
        print(e)
        flash("An error occurred while fetching questions.", "error")
        return redirect(url_for('viewQuiz'))




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