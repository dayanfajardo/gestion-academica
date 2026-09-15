from flask import Blueprint, jsonify, request, abort
from src.services import (
    create_new_student,
    fetch_all_students,
    fetch_student_by_id,
    update_student_by_id,
    delete_student_by_id
)

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/estudiantes', methods=['GET'])
def get_students():
    return jsonify(fetch_all_students()), 200

@estudiantes_bp.route('/estudiantes', methods=['POST'])
def create_student():
    body = request.get_json()
    if not body or not body.get('cedula') or not body.get('correo'):
        abort(400, description='Los campos de cedula y correo son obligatorios')
    create_new_student(body)
    return jsonify({'mensaje': 'Estudiante creado con éxito'}), 201

@estudiantes_bp.route('/estudiantes/<id>', methods=['GET'])
def get_student(id):
    student = fetch_student_by_id(id)
    if not student:
        abort(404, description=f'Estudiante con ID {id} no fue encontrado.')
    return jsonify(student), 200

@estudiantes_bp.route('/estudiantes/<id>', methods=['PUT'])
def update_student(id):
    body = request.get_json()
    if not body:
        abort(400, description='Debe llenar los campos por favor.')
    updated = update_student_by_id(id, body)
    if not updated:
        abort(404, description=f'No se encontró ningún estudiante con ID {id} para actualizar.')
    return jsonify({'mensaje': 'Estudiante actualizado con éxtito', 'id':id}), 200
    
@estudiantes_bp.route('/estudiantes/<id>', methods=['DELETE'])
def delete_student(id):
    deleted = delete_student_by_id(id)
    if not deleted:
        abort(404, description=f'Estudiante con ID {id} no fue encontrado.')
    return jsonify({'mensaje': 'Estudiante eliminado con éxtito', 'id':id}),200
        
