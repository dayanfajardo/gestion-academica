from flask import Flask
from src.routes import estudiantes_bp

app = Flask(__name__)

# Registramos las rutas del módulo estudiantes
app.register_blueprint(estudiantes_bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5003, debug=True)


