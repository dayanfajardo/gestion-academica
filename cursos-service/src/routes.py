from flask import Blueprint, jsonify, request, abort
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
    if not body or not body.get('codigo'):
        abort(400, description='El campo de codigo es obligatorio.')
        
    create_new_course(body)
    return jsonify({'Mensaje': 'Curso creado con éxito'}), 201

#* Ruta para buscar un curso por id
@cursos_bp.route('/cursos/<id>', methods=['GET'])
def get_course(id):
    course = fetch_course_by_id(id)
    if not course:
        abort(404, description=f'Curso con ID {id} no fue encontrado.')
    return jsonify(course), 200

#* ruta para actualizar un curso
@cursos_bp.route('/cursos/<id>', methods=['PUT'])
def update_course(id):
    body = request.get_json()    
    if not body:
        abort(400, description='Debe llenar los campos por favor.')        
    updated = update_course_by_id(id, body)
    if not updated:
        abort(404, description=f'Curso con ID {id} no fue encontrado.')    
    return jsonify({'mensaje': 'Curso actualizado con éxito', 'id': id}), 200

#* ruta para eliminar un curso
@cursos_bp.route('/cursos/<id>', methods=['DELETE'])
def delete_course(id):
    deleted = delete_course_by_id(id)
    if not deleted:
        abort(404, description=f'Curso con ID {id} no fue encontrado.')
    return jsonify({'mensaje': 'Curso eliminado con éxito', 'id': id}), 200
    

