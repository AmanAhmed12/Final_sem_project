from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash


import mysql.connector

connection=mysql.connector.connect(host="Localhost",user="root",password="",database="testdb")

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register')
def register():
    return render_template('register.html')

# Inserting data into details table
@app.route('/studentRegistration', methods=['POST'])
def insert_data():
    s_email = request.form['email']
    s_index = request.form['index']
    s_name = request.form['name']
    semester = request.form['semester']
    year = request.form['year']
    s_password = generate_password_hash(request.form['password'])  # Hash password
    
    # Perform validation
    if not s_email or not s_index or not s_name or not semester or not year or not s_password:
        flash("All fields are required", "error")
        return redirect(url_for('register'))

    cursor = connection.cursor()
    sql = "INSERT INTO details(s_index, s_email, s_name, s_password, semester, year) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (s_index, s_email, s_name, s_password, semester, year)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    flash("Data inserted successfully into the details table", "success")
    return redirect(url_for('login'))



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
