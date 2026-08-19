from flask import Flask
from src.routes import docentes_bp

app = Flask(__name__)

# Registramos las rutas del módulo docentes
app.register_blueprint(docentes_bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)


