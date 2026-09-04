from flask import Flask
from src.routes import cursos_bp
from db import init_db

app = Flask(__name__)

app.register_blueprint(cursos_bp)

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)