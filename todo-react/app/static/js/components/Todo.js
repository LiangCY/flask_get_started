var $ = require('jquery');
var React = require('react');
var TodoForm = require('./TodoForm');

var Todo = React.createClass({
    addTodo: function (content) {
        console.log(content);
    },
    render: function () {
        return (
            <div>
                <TodoForm addTodo={this.addTodo}/>
            </div>
        );
    }
});

module.exports = Todo;