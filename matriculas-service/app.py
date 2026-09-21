from flask import Flask
from src.routes import matriculas_bp
from src.errors import register_error_handlers
from db import init_db

app = Flask(__name__)

# Registramos las rutas del módulo matriculas
app.register_blueprint(matriculas_bp)

register_error_handlers()

init_db()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5004, debug=True)


