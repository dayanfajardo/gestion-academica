from flask import Blueprint, request, jsonify
from src.services import (
    fetch_all_grades,
    create_new_grade,
    fetch_grade_by_id,
    update_grade_by_id,
    delete_grade_by_id
)

notasbp = Blueprint('notas', __name__)

@notasbp.route('/notas', methods=['GET'])
def get_grades():
    return jsonify(fetch_all_grades()), 200

@notasbp.route('/notas', methods=['POST'])
def create_grade():
    body = request.get_json()
    create_new_grade(body)
    return jsonify({'mensaje': 'La nota fue creada con éxito'}),201

@notasbp.route('/notas/<id>', methods=['GET'])
def get_grade(id):
    grade = fetch_grade_by_id(id)
    if not grade:
        return jsonify({'mensaje': 'La nota no está en la base de datos'}), 404
    return jsonify(grade), 200

@notasbp.route('/notas/<id>', methods=['PUT'])
def update_grade(id):
    body = request.get_json()
    update_grade_by_id(id, body)
    return jsonify({'mensaje': 'La nota se actualizó correctamente', 'id': id}), 200

@notasbp.route('/notas/<id>', methods=['DELETE'])
def delete_grade(id):
    delete_grade_by_id(id)
    return jsonify({'mensaje': 'La nota se eliminó correctamente', 'id': id}), 200