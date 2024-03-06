from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, db


app = Flask(__name__)
app.secret_key = 'AmaanAhmed'

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate("D:\\final_project\\json\\serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://quiz-system-6c1ff-default-rtdb.firebaseio.com/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/defaultAdmin')
def defaultAdmin():
    return render_template('defaultAdminDashContent.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admindashboard')
def adminLogin():
    return render_template('admindashboard.html')

# Inserting data into Firebase Realtime Database
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

    # Push data to Firebase Realtime Database
    users_ref = ref.child('users')
    users_ref.push({
        'email': s_email,
        'index': s_index,
        'name': s_name,
        'semester': semester,
        'year': year,
        'password': s_password
    })

    flash("Data inserted successfully into Firebase Realtime Database", "success")
    return redirect(url_for('log'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s_email = request.form['email']
        s_password = request.form['password']
        
        # Retrieve user data from Firebase Realtime Database based on email
        users_ref = ref.child('users')
        query = users_ref.order_by_child('email').equal_to(s_email).get()
        
        # Check if user with provided email exists
        if query:
            user_key = list(query.keys())[0]  # Get the user key
            user_data = query[user_key]  # Get user data
            
            # Check if password matches
            if check_password_hash(user_data['password'], s_password):
                # Store user data in session for future use
                session['user'] = user_data
                
                # Redirect to dashboard.html
                return redirect(url_for('adminLogin'))
        
        # If user does not exist or password is incorrect, show error message
        flash("Incorrect username or password", "error")
        print(user_key)
        print(user_data)
        return redirect(url_for('log'))
    
    # If it's a GET request, render the login page
    return render_template('login.html')




@app.route('/result')
def result():
    # Fetch data from the Firebase Realtime Database
    users_ref = ref.child('users')
    users_data = users_ref.get()

    # Render the 'result.html' template with the retrieved data
    return render_template('result.html', users=users_data)

if __name__ == '__main__':
    app.run(debug=True)
