from flask import request, jsonify, Blueprint, abort
from src.services import (
    fetch_all_enrollments,
    create_new_enrollment,
    fetch_enrollment_by_id,
    update_enrollment_by_id,
    delete_enrollment_by_id
)

matriculas_bp = Blueprint('matriculas', __name__)

@matriculas_bp.route('/matriculas', methods=['GET'])
def get_enrollments():
    return jsonify(fetch_all_enrollments()), 200

@matriculas_bp.route('/matriculas', methods=['POST'])
def create_enrollment():
    body = request.get_json()
    
    if not body or not body.get('anio') or not body.get('periodo'):
        abort(400, description='Los campos de año y periodo son obligatorios') 

    result = create_new_enrollment(body)

    if result == 'student_not_found':
        return jsonify({
            'error': 'El estudiante no existe'
        }), 400

    if result == 'course_not_found':
        return jsonify({
            'error': 'El curso no existe'
        }), 400

    return jsonify({
        'mensaje': 'Matricula creada con éxito'
    }), 201

@matriculas_bp.route('/matriculas/<id>', methods=['GET'])
def get_enrollment(id):
    enrollment = fetch_enrollment_by_id(id) 
    if not enrollment:
        abort(404, description=f'Matricula con ID {id} no fue encontrada.')
    return jsonify(enrollment), 200

@matriculas_bp.route('/matriculas/<id>', methods=['PUT'])
def update_enrollemnt(id):
    body = request.get_json()   
    if not body:
        abort(400, description='Debe llenar los campos por favor.')
    updated = update_enrollment_by_id(id, body)

    if updated == 'student_not_found':
        return jsonify({
            'error': 'El estudiante no existe'
        }), 400

    if updated == 'course_not_found':
        return jsonify({
            'error': 'El curso no existe'
        }), 400

    if not updated:
        abort(404, description=f'No se encontró ninguna matricila con ID {id} para actualizar.')
    return jsonify({'mensaje': 'Matricula actualizado con éxtito', 'id':id}), 200

@matriculas_bp.route('/matriculas/<id>', methods=['DELETE'])
def delete_enrollment(id):
    deleted = delete_enrollment_by_id(id)
    if not deleted:
        abort(404, description=f'La matricula con ID {id} no fue encontrada.')
    return jsonify({'mensaje': 'Matrícula eliminada correctamente', 'id':id}), 200
    
    
