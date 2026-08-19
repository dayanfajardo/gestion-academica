from flask import Blueprint, jsonify, request
from src.services import (
    fetch_all_teachers, 
    fetch_teacher_by_id, 
    create_new_teacher, 
    update_teacher_by_id, 
    delete_teacher_by_id
)

docentes_bp = Blueprint('docentes', __name__)

@docentes_bp.route('/docentes', methods=['GET'])
def get_teachers():
    return jsonify(fetch_all_teachers()), 200

@docentes_bp.route('/docentes/<id>', methods=['GET'])
def get_teacher(id):
    teacher = fetch_teacher_by_id(id)
    if not teacher:
        return jsonify({'error': 'Docente no encontrado'}), 404
    return jsonify(teacher), 200

@docentes_bp.route('/docentes', methods=['POST'])
def create_teacher():
    body = request.get_json()
    create_new_teacher(body)
    return jsonify({'mensaje': 'Docente creado con éxito'}), 201

@docentes_bp.route('/docentes/<id>', methods=['PUT'])
# Este id es el parámetro que recibe el valor que estaba en <id> de la URL.
def update_teacher(id):
    body = request.get_json()
    update_teacher_by_id(id, body)
    return jsonify({'mensaje': 'Docente actualizado con éxito', 'id': id}), 200

@docentes_bp.route('/docentes/<id>', methods=['DELETE'])
def delete_teacher(id):
    delete_teacher_by_id(id)
    return jsonify({'mensaje': 'Docente eliminado con éxito', 'id': id}), 200