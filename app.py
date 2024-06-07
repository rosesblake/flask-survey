from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'abcd1234'
toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def servey_home():
    responses.clear()
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/answer', methods=['POST'])
def answer():
    answer = request.form.get('answer')
    if answer:
        responses.append(answer)
    else:
        flash('Please select an answer!', 'error')
    next_question_idx = len(responses)
    if next_question_idx < len(satisfaction_survey.questions):
        return redirect(f'/questions/{next_question_idx}')
    else:
        return redirect('/check-responses')

@app.route('/questions/<int:question_idx>')
def show_question(question_idx):
    if len(responses) == question_idx:
        if question_idx < len(satisfaction_survey.questions):
            question = satisfaction_survey.questions[question_idx].question
            choice1 = satisfaction_survey.questions[question_idx].choices[0]
            choice2 = satisfaction_survey.questions[question_idx].choices[1]
            return render_template('questions.html', question=question, question_idx=question_idx, choice1=choice1, choice2=choice2, satisfaction_survey=satisfaction_survey)
        else:
            return redirect(f'/questions/{len(responses)}')
    else:
        flash("You're trying to access an invalid question!", 'error')
        return redirect(f'/questions/{len(responses)}')    

@app.route('/check-responses')
def check_responses():
    return f"<h1>THANK YOU!</h1>"

