from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

questions = []

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        num_options = int(request.form['num_options'])
        options = request.form.getlist('options')
        answer = request.form['answer'] if 'answer' in request.form else None
        question_type = request.form['question_type']
        
        if question_type == 'likert' and answer is None:
            return "Por favor, forneça um gabarito para a questão Likert.", 400

        question = {'title': title, 'options': options, 'answer': answer, 'type': question_type}
        questions.append(question)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    question = questions[id]
    if request.method == 'POST':
        title = request.form['title']
        num_options = int(request.form['num_options'])
        options = request.form.getlist('options')
        answer = request.form['answer'] if 'answer' in request.form else None
        question_type = request.form['question_type']
        
        if question_type == 'likert' and answer is None:
            return "Por favor, forneça um gabarito para a questão Likert.", 400

        question['title'] = title
        question['options'] = options
        question['answer'] = answer
        question['type'] = question_type
        return redirect(url_for('index'))
    return render_template('update.html', question=question, id=id)

@app.route('/delete/<int:id>')
def delete(id):
    questions.pop(id)
    return redirect(url_for('index'))

@app.route('/view')
def view():
    return render_template('view.html', questions=questions)

@app.template_filter('number_to_letter')
def number_to_letter_filter(number):
    return chr(97 + number)
    
if __name__ == '__main__':
    app.run(debug=True)
