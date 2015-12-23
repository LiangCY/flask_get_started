var React = require('react');

var TodoItem = React.createClass({
    handleUpdate: function (id, status) {
        console.log(id, status);
        this.props.updateTodo(id, status);
    },
    handleDelete: function (id) {
        this.props.deleteTodo(id);
    },
    render: function () {
        var item = this.props.todo;
        var updateButton;

        if (item.status == 0) {
            updateButton =
                <button onClick={this.handleUpdate.bind(this,item.id,1)} className="btn btn-success operator">Done</button>
        } else {
            updateButton =
                <button onClick={this.handleUpdate.bind(this,item.id,0)} className="btn btn-primary operator">Undone</button>
        }

        return (
            <tr>
                <td>{item.content}</td>
                <td>{item.status == 0 ? '未完成' : '已完成'}</td>
                <td>{item.time}</td>
                <td>
                    {updateButton}
                    <button onClick={this.handleDelete.bind(this,item.id)} className="btn btn-danger operator">Delete</button>
                </td>
            </tr>
        );
    }
});

module.exports = TodoItem;