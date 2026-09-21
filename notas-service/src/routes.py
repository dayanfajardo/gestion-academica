from flask import Blueprint, request, jsonify, abort
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
    if not body or not body.get('calificacion'):
        abort(400, description='El campo de calificacion es obligatorio.')
    create_new_grade(body)
    return jsonify({'mensaje': 'La nota fue creada con éxito'}),201

@notasbp.route('/notas/<id>', methods=['GET'])
def get_grade(id):
    grade = fetch_grade_by_id(id)
    if not grade:
        abort(404, description=f'Nota con ID {id} no fue encontrado.')
    return jsonify(grade), 200

@notasbp.route('/notas/<id>', methods=['PUT'])
def update_grade(id):
    body = request.get_json()
    if not body:
        abort(400, description='Debe llenar los campos por favor.')        
    updated = update_grade_by_id(id, body)
    if not updated:
        abort(404, description=f'Nota con ID {id} no fue encontrada.')    
    return jsonify({'mensaje': 'La nota se actualizó correctamente', 'id': id}), 200

@notasbp.route('/notas/<id>', methods=['DELETE'])
def delete_grade(id):
    deleted = delete_grade_by_id(id)
    if not deleted:
        abort(404, description=f'Nota con ID {id} no fue encontrada.')
    return jsonify({'mensaje': 'La nota se eliminó correctamente', 'id': id}), 200