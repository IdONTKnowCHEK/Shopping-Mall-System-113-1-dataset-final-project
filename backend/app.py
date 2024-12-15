from flask import Flask, jsonify
from flasgger import Swagger
from models.models import db
import os

from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化資料庫
    db.init_app(app)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app

if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'  # 開發模式
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
