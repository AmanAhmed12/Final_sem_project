from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feed')
def quiz():
    return render_template('feedback.html')

@app.route('/register')
def register():
    return render_template('register.html')



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
