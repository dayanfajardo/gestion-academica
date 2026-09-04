from flask import Blueprint, jsonify, request
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
    create_new_student(body)
    return jsonify({'mensaje': 'Estudiante creado con éxito'}), 201

@estudiantes_bp.route('/estudiantes/<id>', methods=['GET'])
def get_student(id):
    student = fetch_student_by_id(id)
    if not student:
        return jsonify({'mensaje': 'Estudiante no se encuentra en la base de datos'}), 404
    return jsonify(student), 200

@estudiantes_bp.route('/estudiantes/<id>', methods=['PUT'])
def update_student(id):
    body = request.get_json()
    update_student_by_id(id,body)
    return jsonify({'mensaje': 'Estudiante actualizado con éxtito', 'id':id}), 200
    
@estudiantes_bp.route('/estudiantes/<id>', methods=['DELETE'])
def delete_student(id):
    delete_student_by_id(id)
    return jsonify({'mensaje': 'Estudiante eliminado con éxtito', 'id':id}),200
        
