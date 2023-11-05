from flask import Flask, render_template, request
from gpt_teacher_deploy import gpteacher

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        corrected_text, spelling_errors, grammar_errors = gpteacher(input_text)
        return {'corrected_text': corrected_text, 'spelling_errors': spelling_errors, 'grammar_errors': grammar_errors}
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
