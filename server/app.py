# from crypt import methods
# from datetime import datetime
# from flask import Flask, request, make_response, jsonify
# from flask_cors import CORS
# from flask_migrate import Migrate
#
# from models import db, Message
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False
#
# CORS(app)
# migrate = Migrate(app, db)
#
# db.init_app(app)
#
# @app.route('/messages', methods=['GET', 'POST'])
# def messages():
#
#     if request.method == 'GET':
#         messages = []
#         for message in Message.query.all():
#             message_dict = message.to_dict()
#             messages.append(message_dict)
#
#         response = make_response(
#             messages,
#             200
#         )
#         return response
#
#     elif request.method == 'POST':
#         data = request.get_json()
#
#         if not data.get("body") or not data.get("username"):
#             return jsonify({"error": "Missing required fields: body or username"}), 400
#
#
#         new_message = Message(
#             body = data["body"],
#             username=data["username"],
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow()
#
#         )
#
#         db.session.add(new_message)
#         db.session.commit()
#
#         message_dict = new_message.to_dict()
#
#         response = make_response(
#             message_dict,
#             201
#         )
#         return response
#
# @app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
# def messages_by_id(id):
#     messages = Message.query.filter(Message.id == id).first()
#
#     if request.method == 'GET':
#         messages_list = []
#         for message in messages:
#             message_dict = message.to_dict()
#             messages_list.append(message_dict)
#
#         response = make_response(
#             messages_list,
#             200
#         )
#
#         return response
#
#
#     elif request.method == 'PATCH':
#         data = request.get_json()
#
#         for attr, value in data.items():
#             if hasattr(messages, attr):
#                 setattr(messages,attr,value)
#
#         db.session.commit()
#
#         message_dict = messages.to_dict()
#
#         response = make_response(
#             message_dict,
#             200
#         )
#
#         return response
#
#     elif request.method == 'DELETE':
#         db.session.delete(messages)
#         db.session.commit()
#
#         response_body = {
#             "deleted_successfully" : True,
#             "message" : "Message deleted."
#         }
#
#         response = make_response(
#             response_body,
#             200
#         )
#
#         return response
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_message = Message(
            username=data['username'],
            body=data['body']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        message.body = data['body']

    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=4000)