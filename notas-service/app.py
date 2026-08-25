from flask import Flask
from src.routes import notasbp

app = Flask(__name__)

# Registramos las rutas del módulo matriculas
app.register_blueprint(notasbp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5005, debug=True)


