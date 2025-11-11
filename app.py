from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__, template_folder='templates')

todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    if todo.strip():
        todos.append({'task': todo, 'done': False})
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if index >= len(todos):
        return redirect(url_for('index'))
    todo = todos[index]
    if request.method == 'POST':
        new_task = request.form['todo']
        if new_task.strip():
            todo['task'] = new_task
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', todo=todo, index=index)

@app.route('/check/<int:index>')
def check(index):
    if index < len(todos):
        todos[index]['done'] = not todos[index]['done']
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    if index < len(todos):
        del todos[index]
    return redirect(url_for('index'))

@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    global todos
    todos = [todo for todo in todos if not todo['done']]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)