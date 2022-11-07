from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "jello"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

satisfaction_survey_instructions = "satisfaction_survey.instructions"

@app.route("/")
def display_start_page():
    """Start page to begin Customer Satisfaction Survey."""
    return render_template("survey_start.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Empty the session responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")
    

@app.route("/answer", methods=["POST"])
def handle_answer():
    """Save answer and redirect to next question."""

    #extract the answer choice
    choice = request.form['answer']

    #add answer to the responses list
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        #survey is complete, redirect to thank you page.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def display_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # Trying to answer questions before starting the survey
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        # Survey complete
        return redirect("/complete")
    if (len(responses) != qid):
        # Answering questions out of order
        flash(f"Invalid question: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question_form.html", question_num=qid, question=question)
    


@app.route("/complete")
def complete():
    """Survey completed. Show thank-you page."""
    return render_template("complete.html")