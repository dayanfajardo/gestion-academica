from flask import Blueprint, jsonify, request
from src.services import (
    fetch_all_courses,
    create_new_course,
    fetch_course_by_id,
    update_course_by_id,
    delete_course_by_id
)

cursos_bp = Blueprint('cursos', __name__)

#* Ruta para todos los cursos
@cursos_bp.route('/cursos', methods=['GET'])
def get_courses():
    return jsonify(fetch_all_courses()), 200

#* Ruta para crear un curso
@cursos_bp.route('/cursos', methods=['POST'])
def create_course():
    body = request.get_json()
    create_new_course(body)
    return jsonify({'Mensaje': 'Curso creado con éxito'}), 201

#* Ruta para buscar un curso por id
@cursos_bp.route('/cursos/<id>', methods=['GET'])
def get_course(id):
    course = fetch_course_by_id(id)
    if not course:
        return jsonify({'error': 'Curso no encontrado'}), 404
    return jsonify(course), 200

#* ruta para actualizar un curso
@cursos_bp.route('/cursos/<id>', methods=['PUT'])
def update_course(id):
    body = request.get_json()
    update_course_by_id(id, body)
    return jsonify({'mensaje': 'Curso actualizado con éxito', 'id': id}), 200

#* ruta para eliminar un curso
@cursos_bp.route('/cursos/<id>', methods=['DELETE'])
def delete_course(id):
    delete_course_by_id(id)
    return jsonify({'mensaje': 'Curso eliminado con éxito', 'id': id}), 200
    
    
    
    
    
