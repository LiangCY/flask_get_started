var $ = require('jquery');
var React = require('react');
var TodoForm = require('./TodoForm');
var TodoTable = require('./TodoTable');

var Todo = React.createClass({
    getInitialState: function () {
        return {
            todos: []
        }
    },
    listTodo: function () {
        $.ajax({
            url: '/list'
        }).done(function (resp) {
            if (resp.status = 'success') {
                this.setState({
                    todos: resp.todos
                });
            }
        }.bind(this));
    },
    addTodo: function (content) {
        $.ajax({
            type: 'post',
            url: '/add',
            data: {content: content}
        }).done(function (resp) {
            if (resp.status == 'success') {
                var todos = [];
                todos.push(resp.todo);
                this.state.todos.forEach(function (todo) {
                    todos.push(todo);
                });
                this.setState({
                    todos: todos
                });
            }
        }.bind(this));
    },
    updateTodo: function (id, status) {
        $.ajax({
            type: 'post',
            url: '/update',
            data: {id: id, status: status}
        }).done(function (resp) {
            if (resp.status == 'success') {
                var todos = [];
                this.state.todos.forEach(function (todo) {
                    if (todo.id == resp.id) {
                        todo.status = resp.todo_status;
                    }
                    todos.push(todo);
                });
                this.setState({
                    todos: todos
                });
            }
        }.bind(this));
    },
    deleteTodo: function (id) {
        $.ajax({
            url: '/delete/' + id
        }).done(function (resp) {
            if (resp.status == 'success') {
                var todos = [];
                this.state.todos.forEach(function (todo) {
                    if (todo.id != resp.id) {
                        todos.push(todo);
                    }
                });
                this.setState({
                    todos: todos
                });
            }
        }.bind(this));
    },
    componentDidMount: function () {
        this.listTodo();
    },
    render: function () {
        return (
            <div>
                <TodoForm addTodo={this.addTodo}/>
                <TodoTable todos={this.state.todos}
                           updateTodo={this.updateTodo}
                           deleteTodo={this.deleteTodo}/>
            </div>
        );
    }
});

module.exports = Todo;