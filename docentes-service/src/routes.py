from flask import Blueprint, jsonify, request, abort
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

@docentes_bp.route('/docentes', methods=['POST'])
def create_teacher():
    body = request.get_json()    
    # Validamos los campos
    if not body or not body.get('cedula') or not body.get('correo'):
        abort(400, description='Los campos de cedula y correo son obligatorios')    
    create_new_teacher(body)
    return jsonify({'mensaje': 'Docente creado con éxito'}), 201

@docentes_bp.route('/docentes/<id>', methods=['GET'])
def get_teacher(id):
    teacher = fetch_teacher_by_id(id)
    if not teacher:
        abort(404, description=f'Docente con ID {id} no fue encontrado.')
    return jsonify(teacher), 200

@docentes_bp.route('/docentes/<id>', methods=['PUT'])
def update_teacher(id):
    body = request.get_json()    
    if not body:
        abort(400, description='Debe llenar los campos por favor.')
    updated = update_teacher_by_id(id, body)
    if not updated:
         abort(404, description=f'No se encontro ningun docente con ID {id} para actualizar.')   
    return jsonify({'mensaje': 'Docente actualizado con éxito', 'id': id}), 200

@docentes_bp.route('/docentes/<id>', methods=['DELETE'])
def delete_teacher(id):
    deleted = delete_teacher_by_id(id)    
    if not deleted:
        abort(404, description=f'Docente con ID {id} no fue encontrado')    
    return jsonify({'mensaje': 'Docente eliminado con éxito', 'id': id}), 200