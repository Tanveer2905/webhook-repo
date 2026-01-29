from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo
from dotenv import load_dotenv
import os

load_dotenv() 
def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # 🔐 Use environment variable in real projects (better practice)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    # Prevent JSON sorting (keeps API responses clean)
    app.config["JSON_SORT_KEYS"] = False

    # Initialize Mongo
    mongo.init_app(app)

    # Register Blueprint
    app.register_blueprint(webhook)

    return app
