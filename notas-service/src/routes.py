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

    if not body:
        return jsonify({'error': 'Debe llenar los campos por favor.'}), 400
    
    result = create_new_grade(body)
    
    if result == 'enrollment_not_found':
        return jsonify({
            'error': 'La matrícula no existe'
        }), 400
    
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
    if not body:
        return jsonify({'error': 'Debe llenar los campos por favor.'}), 400

    result = update_grade_by_id(id, body)

    if result == 'enrollment_not_found':
        return jsonify({
            'error': 'La matrícula no existe'
        }), 400

    if not result:
        return jsonify({'mensaje': 'La nota no está en la base de datos'}), 404

    return jsonify({'mensaje': 'La nota se actualizó correctamente', 'id': id}), 200

@notasbp.route('/notas/<id>', methods=['DELETE'])
def delete_grade(id):
    deleted = delete_grade_by_id(id)
    if not deleted:
        return jsonify({'mensaje': 'La nota no está en la base de datos'}), 404
    return jsonify({'mensaje': 'La nota se eliminó correctamente', 'id': id}), 200