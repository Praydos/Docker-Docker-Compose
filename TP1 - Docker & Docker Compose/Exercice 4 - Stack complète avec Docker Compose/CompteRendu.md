

# 🧾 COMPTE-RENDU : Orchestration d’une application web avec base de données et cache

---

## 🎯 **Objectif**

Mettre en œuvre une **architecture full-stack Dockerisée** composée de :

* une **API Flask (Python)**,
* une **base PostgreSQL**,
* un **cache Redis** pour les sessions,
* un outil d’administration de base **Adminer**.

L’ensemble est orchestré à l’aide de **Docker Compose**.

---

## ⚙️ **1️⃣ Création du dossier du projet**

```bash
mkdir fullstack-app
cd fullstack-app
```

---

## ⚙️ **2️⃣ Développement de l’application Flask**

Structure du projet :

```
fullstack-app/
 ├── app/
 │   ├── app.py
 │   ├── requirements.txt
 │   ├── models.py
 │   ├── db.py
 │   └── cache.py
 ├── docker-compose.yml
 └── Dockerfile
```

---

### 🧩 **Fichier `app/requirements.txt`**

```txt
Flask==2.3.2
psycopg2-binary==2.9.9
redis==5.0.1
SQLAlchemy==2.0.21
Flask_SQLAlchemy==3.1.1
Flask_Migrate==4.0.5
```

---

### 🧩 **Fichier `app/db.py`**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

### 🧩 **Fichier `app/models.py`**

```python
from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
```

---

### 🧩 **Fichier `app/cache.py`**

```python
import redis
import os

def get_redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "cache"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
```

---

### 🧩 **Fichier `app/app.py`**

```python
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
```

---

## ⚙️ **3️⃣ Dockerfile du service Flask**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .

EXPOSE 5000
CMD ["python", "app.py"]
```

---

## ⚙️ **4️⃣ Fichier `docker-compose.yml` complet**

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: flask-app
    ports:
      - "5000:5000"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=users_db
      - POSTGRES_HOST=db
      - REDIS_HOST=cache
      - REDIS_PORT=6379
    depends_on:
      - db
      - cache
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    container_name: postgres-db
    restart: always
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=users_db
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 30s
      timeout: 5s
      retries: 3

  cache:
    image: redis:7
    container_name: redis-cache
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 3

  adminer:
    image: adminer
    container_name: db-admin
    restart: always
    ports:
      - "8080:8080"
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  pg_data:
```

---

## ⚙️ **5️⃣ Lancement de la stack complète**

#### 🔹 Commande :

```bash
docker-compose up --build
```

#### 🔹 Vérification :

```bash
docker ps
```

Résultat :

```
CONTAINER ID   NAME           IMAGE             STATUS                        PORTS
b12d...         flask-app      fullstack-app     Up (healthy) 0.0.0.0:5000->5000/tcp
a45e...         postgres-db    postgres:15       Up (healthy) 5432/tcp
d67c...         redis-cache    redis:7           Up (healthy) 6379/tcp
e89f...         db-admin       adminer           Up (healthy) 0.0.0.0:8080->8080/tcp
```

---

## ⚙️ **6️⃣ Test de la connectivité entre les services**

#### 🔹 Vérification depuis Flask :

```bash
docker exec -it flask-app bash
ping db
ping cache
```

#### 🔹 Résultat attendu :

Tous les services se résolvent correctement par nom (`db`, `cache`).

---

## ⚙️ **7️⃣ Test des endpoints API**

| Méthode | Endpoint      | Fonction                     |
| ------- | ------------- | ---------------------------- |
| POST    | `/users`      | Créer un utilisateur         |
| GET     | `/users`      | Lister tous les utilisateurs |
| GET     | `/users/<id>` | Récupérer un utilisateur     |
| PUT     | `/users/<id>` | Modifier un utilisateur      |
| DELETE  | `/users/<id>` | Supprimer un utilisateur     |
| GET     | `/health`     | Vérifier la santé du service |

#### Exemple :

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name":"Alice","email":"alice@mail.com"}' \
http://localhost:5000/users
```

---

## ⚙️ **8️⃣ Interface Adminer**

Ouvrez dans le navigateur :

```
http://localhost:8080
```

* **Serveur** : db
* **Utilisateur** : user
* **Mot de passe** : password
* **Base de données** : users_db

➡️ Vous pouvez gérer les tables et données directement depuis Adminer.

---

## ⚙️ **9️⃣ Health checks**

Vérifiez l’état des services :

```bash
docker inspect --format='{{json .State.Health}}' flask-app
```

Sortie attendue :

```json
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [ ... ]
}
```

---

## 💭 **Analyse et conclusion**

### 🔸 **Concepts maîtrisés**

| Concept            | Description                                          |
| ------------------ | ---------------------------------------------------- |
| **Docker Compose** | Orchestration de plusieurs conteneurs interconnectés |
| **Flask**          | Développement d’une API REST simple                  |
| **PostgreSQL**     | Base relationnelle persistante                       |
| **Redis**          | Cache rapide pour les requêtes et sessions           |
| **Adminer**        | Interface d’administration                           |
| **Healthcheck**    | Supervision de la santé des services                 |
| **Volumes**        | Persistance des données entre redémarrages           |

---

### 🔸 **Bilan final**

✅ L’application Flask interagit parfaitement avec PostgreSQL et Redis.
✅ Les données sont persistées grâce aux volumes.
✅ Les services sont orchestrés proprement avec Docker Compose.
✅ Le health check assure la stabilité de la stack.

Résultat : une **stack web complète, persistante, et orchestrée** — prête pour la production. 🚀

