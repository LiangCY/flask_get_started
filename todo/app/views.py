from app import app
from flask import render_template, request, redirect, url_for
from models import Todo, TodoForm
from datetime import datetime


@app.route('/')
def index():
    form = TodoForm()
    todos = Todo.objects.all()
    return render_template('index.html', todos=todos, form=form)


@app.route('/add', methods=['POST'])
def add():
    form = TodoForm(request.form)
    if form.validate():
        content = form.content.data
        todo = Todo(content=content, time=datetime.now())
        todo.save()
    return redirect(url_for('index'))


@app.route('/done/<string:todo_id>')
def done(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.status = 1
    todo.save()
    return redirect(url_for('index'))


@app.route('/undone/<string:todo_id>')
def undone(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.status = 0
    todo.save()
    return redirect(url_for('index'))


@app.route('/delete/<string:todo_id>')
def delete(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.delete()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
