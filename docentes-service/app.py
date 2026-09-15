from flask import Flask
from src.errors import register_error_handlers
from src.routes import docentes_bp
from db import init_db


app = Flask(__name__)

# Registramos las rutas del módulo docentes
app.register_blueprint(docentes_bp)

# Aqui registro el manejador global de los errores
register_error_handlers(app)

# Con esto lo que hago es ejecutar las tablas al crear la aplicacion
init_db()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)


