from flask import request, jsonify, Blueprint
from src.services import (
    fetch_all_enrollments,
    create_new_enrollment,
    fetch_enrollment_by_id,
    update__enrollment_by_id,
    delete_enrollment_by_id
)

matriculas_bp = Blueprint('matriculas', __name__)

@matriculas_bp.route('/matriculas', methods=['GET'])
def get_enrollments():
    return jsonify(fetch_all_enrollments()), 200

@matriculas_bp.route('/matriculas', methods=['POST'])
def create_enrollment():
    body = request.get_json()
    create_new_enrollment(body)
    return jsonify({'mensaje': 'Matricula creada con éxito'}), 201

@matriculas_bp.route('/matriculas/<id>', methods=['GET'])
def get_enrollment(id):
    enrollment = fetch_enrollment_by_id(id) 
    if not enrollment:
        return jsonify({'mensaje': 'Matrícula no se encuentra en la base de datos'}), 404
    return jsonify(enrollment), 200

@matriculas_bp.route('/matriculas/<id>', methods=['PUT'])
def update_enrollemnt(id):
    body = request.get_json()
    update__enrollment_by_id(id, body)
    return jsonify({'mensaje': 'Matricula actualizado con éxtito', 'id':id}), 200

@matriculas_bp.route('/matriculas/<id>', methods=['DELETE'])
def delete_enrollment(id):
    delete_enrollment_by_id(id)
    return jsonify({'mensaje': 'Matrícula eliminada correctamente', 'id':id}), 200
    
