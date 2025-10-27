from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import User
from cache import get_redis_client
import os

app = Flask(__name__)

# Configuration base de données
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "users_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
redis_client = get_redis_client()

@app.route("/")
def index():
    return jsonify({"message": "Bienvenue dans l’API Flask Dockerisée 🚀"})

# CREATE
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    redis_client.delete("users_cache")  # invalidate cache
    return jsonify(user.to_dict()), 201

# READ ALL
@app.route("/users", methods=["GET"])
def get_users():
    cached_users = redis_client.get("users_cache")
    if cached_users:
        return jsonify({"source": "cache", "data": eval(cached_users)})

    users = [u.to_dict() for u in User.query.all()]
    redis_client.set("users_cache", str(users))
    return jsonify({"source": "database", "data": users})

# READ ONE
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# UPDATE
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    db.session.commit()
    redis_client.delete("users_cache")
    return jsonify(user.to_dict())

# DELETE
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    redis_client.delete("users_cache")
    return jsonify({"message": "Utilisateur supprimé"})

# HEALTH CHECK
@app.route("/health", methods=["GET"])
def health_check():
    try:
        db.session.execute("SELECT 1")
        redis_client.ping()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
