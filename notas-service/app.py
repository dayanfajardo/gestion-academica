from flask import Flask
from src.routes import notasbp
from src.errors import register_error_handlers
from db import init_db

app = Flask(__name__)

# Registramos las rutas del módulo notas
app.register_blueprint(notasbp)

register_error_handlers(app)

init_db()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5005, debug=True)


