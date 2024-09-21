from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
#     os.path.join(basedir, 'app.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://udgsctq7d3q26p:pa80bb310463d1abb919fc59389bd6d278e475d1a8521d0e89dda393ee9aae70c@c6sfjnr30ch74e.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d57u2v1ujuup0p"

db = SQLAlchemy(app)
app.app_context().push()

ma = Marshmallow(app)
CORS(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    progress = db.Column(db.Integer, nullable=False)

    def __init__(self, title, progress):
        self.title = title
        self.progress = progress


class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'progress')


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)



@app.route('/todos', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)


@app.route('/todo/<id>', methods=["GET"])
def get_todo(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)


@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    progress = request.json['progress']
    new_todo = Todo(title, progress)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)


@app.route('/todo/<id>', methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get(id)
    title = request.json['title']
    progress = request.json['progress']
    todo.title = title
    todo.progress = progress
    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)


if __name__ == '__main__':
    app.run(debug=True)
