from app import app
from flask import render_template
from models import Todo


@app.route('/')
def index():
    print('123')
    todos = Todo.objects.all()

    print(todos)
    return render_template('index.html', todos=todos)
