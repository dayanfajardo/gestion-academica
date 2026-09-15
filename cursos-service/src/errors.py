from werkzeug.exceptions import HTTPException
from flask import jsonify
import psycopg2.errors
import psycopg2

def register_error_handlers(app):
    
    #  Errores específicos de Postgres
    @app.errorhandler(psycopg2.errors.UniqueViolation)
    def handle_unique_violation(e):
        return jsonify({
            'error': 'Conflict',
            'message': "El código del curso ya existe.",
            'status': 409
        }), 409
        
    @app.errorhandler(psycopg2.errors.ForeignKeyViolation)
    def handle_foreign_key_violation(e):
        return jsonify({
            'error': 'Bad Request',
            'message': 'La operación no puede realizarse porque cursos está relacionado con otros datos.',
            'status': 400
        }), 400
    
    #  Clase base de errores de Postgres
    @app.errorhandler(psycopg2.Error)
    def handle_db_error(e):
        return jsonify({
            'error': 'Database Error',
            'message': 'Ups, problema inesperado al comunicarse con la base de datos.',
            'status': 500
        }), 500
    
    # Excepciones HTTP de Flask 
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            'error': e.name,
            'message': e.description,
            'status': e.code
        }), e.code
    
    # Errores no controlados de Python
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Algo pasó con el servidor, intenta más tarde.',
            'status': 500
        }), 500