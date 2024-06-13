from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'abcd1234'
toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def servey_home():
    session.pop('responses', None)
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

# add session 
@app.route('/start-survey', methods=['POST'])
def start_survey():
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def answer():
    answer = request.form.get('answer')
    if answer:
        # having to do this three step process tripped me up 
        responses = session['responses']
        responses.append(answer)
        session['responses'] = responses
    else:
        flash('Please select an answer!', 'error')

    next_question_idx = len(session['responses'])

    if next_question_idx < len(satisfaction_survey.questions):
        return redirect(f'/questions/{next_question_idx}')
    else:
        return redirect('/check-responses')
    

@app.route('/questions/<int:question_idx>')
def show_question(question_idx):
    # if 'responses' not in session:
    #     return redirect('/')
    if len(session['responses']) == question_idx:
        if question_idx < len(satisfaction_survey.questions):
            question = satisfaction_survey.questions[question_idx].question
            choice1 = satisfaction_survey.questions[question_idx].choices[0]
            choice2 = satisfaction_survey.questions[question_idx].choices[1]
            return render_template('questions.html', question=question, question_idx=question_idx, choice1=choice1, choice2=choice2, satisfaction_survey=satisfaction_survey)
        else:
            return redirect(f'/questions/{len(session["responses"])}')
    else:
        flash("You're trying to access an invalid question!", 'error')
        return redirect(f'/questions/{len(session["responses"])}')    

@app.route('/check-responses')
def check_responses():
    return "<h1>THANK YOU!</h1>"