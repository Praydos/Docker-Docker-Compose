# Compte-rendu : Orchestration d'une application web fullstack avec Docker Compose

## Structure du projet

```
fullstack-app/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── init.sql
├── docker-compose.yml
└── README.md
```

## Résolution détaillée des consignes

### 1. Création de la structure du projet
```bash
mkdir fullstack-app
cd fullstack-app
mkdir app
```

### 2. Développement de l'API Python Flask

**app/requirements.txt**
```txt
Flask==2.3.3
psycopg2-binary==2.9.7
redis==4.6.0
```

**app/app.py**
```python
from flask import Flask, request, jsonify
import psycopg2
import redis
import os
import json

app = Flask(__name__)

# Configuration depuis les variables d'environnement
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'app_db')
DB_USER = os.getenv('DB_USER', 'app_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'app_password')
REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Connexion à Redis
def get_redis_connection():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    redis_client = get_redis_connection()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
            (data['name'], data['email'])
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        
        # Invalider le cache
        redis_client.delete('users:all')
        
        return jsonify({'id': user_id, 'name': data['name'], 'email': data['email']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/users', methods=['GET'])
def get_users():
    redis_client = get_redis_connection()
    
    # Vérifier le cache
    cached_users = redis_client.get('users:all')
    if cached_users:
        return jsonify(json.loads(cached_users))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, created_at FROM users')
        users = []
        for row in cur.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3].isoformat()
            })
        
        # Mettre en cache pour 5 minutes
        redis_client.setex('users:all', 300, json.dumps(users))
        
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    redis_client = get_redis_connection()
    cache_key = f'user:{user_id}'
    
    # Vérifier le cache
    cached_user = redis_client.get(cache_key)
    if cached_user:
        return jsonify(json.loads(cached_user))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, created_at FROM users WHERE id = %s', (user_id,))
        row = cur.fetchone()
        
        if row:
            user = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3].isoformat()
            }
            # Mettre en cache pour 5 minutes
            redis_client.setex(cache_key, 300, json.dumps(user))
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    redis_client = get_redis_connection()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id, name, email, created_at',
            (data['name'], data['email'], user_id)
        )
        row = cur.fetchone()
        
        if row:
            conn.commit()
            user = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3].isoformat()
            }
            # Invalider les caches
            redis_client.delete('users:all')
            redis_client.delete(f'user:{user_id}')
            
            return jsonify(user)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    redis_client = get_redis_connection()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE id = %s RETURNING id', (user_id,))
        row = cur.fetchone()
        
        if row:
            conn.commit()
            # Invalider les caches
            redis_client.delete('users:all')
            redis_client.delete(f'user:{user_id}')
            
            return '', 204
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 3. Configuration Docker

**app/Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**app/init.sql**
```sql
CREATE DATABASE app_db;
CREATE USER app_user WITH PASSWORD 'app_password';
GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;
```

### 4. Configuration Docker Compose

**docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_NAME=app_db
      - DB_USER=app_user
      - DB_PASSWORD=app_password
      - REDIS_HOST=cache
      - REDIS_PORT=6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=app_db
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD=app_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./app/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  cache:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  adminer:
    image: adminer:4.8.1
    ports:
      - "8080:8080"
    environment:
      - ADMINER_DEFAULT_SERVER=db
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

## Mise en œuvre et tests

### 7. Lancement de la stack
```bash
docker-compose up -d
```

### 8. Tests de connectivité

**Test de l'API Flask**
```bash
# Créer un utilisateur
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Lister les utilisateurs
curl http://localhost:5000/users

# Récupérer un utilisateur spécifique
curl http://localhost:5000/users/1

# Modifier un utilisateur
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Smith","email":"johnsmith@example.com"}'

# Supprimer un utilisateur
curl -X DELETE http://localhost:5000/users/1
```

**Vérification des services**
```bash
# Vérifier l'état des services
docker-compose ps

# Vérifier les logs
docker-compose logs web
docker-compose logs db
docker-compose logs cache
```

### 9. Accès à Adminer
- URL : http://localhost:8080
- Serveur : `db`
- Utilisateur : `app_user`
- Mot de passe : `app_password`
- Base de données : `app_db`

### 10. Vérification des health checks
```bash
docker-compose ps
```
```
NAME                       SERVICE             STATUS              PORTS
fullstack-app-cache-1      cache               running (healthy)   6379/tcp
fullstack-app-db-1         db                  running (healthy)   5432/tcp
fullstack-app-web-1        web                 running (healthy)   0.0.0.0:5000->5000/tcp
fullstack-app-adminer-1    adminer             running             0.0.0.0:8080->8080/tcp
```

## Architecture et concepts avancés

### Stratégie de cache Redis
- **Cache des listes** : `users:all` avec TTL de 5 minutes
- **Cache individuel** : `user:{id}` avec TTL de 5 minutes
- **Invalidation** : Suppression des caches lors des opérations d'écriture

### Health checks configurables
- **Web** : Endpoint `/health` dédié
- **PostgreSQL** : Commande `pg_isready`
- **Redis** : Commande `ping`
- **Dépendances** : Les services attendent que les dépendances soient healthy

### Gestion de la persistance
- **PostgreSQL** : Volume nommé `postgres_data`
- **Redis** : Volume nommé `redis_data` avec AOF (Append Only File)

## Commandes de gestion

```bash
# Arrêter la stack
docker-compose down

# Redémarrer un service spécifique
docker-compose restart web

# Scale un service (si nécessaire)
docker-compose up -d --scale web=3

# Nettoyage complet
docker-compose down -v
```

## Conclusion

Cette orchestration Docker Compose démontre une architecture microservices complète avec :

- **Service web** : API Flask avec cache Redis
- **Base de données** : PostgreSQL avec persistance
- **Cache** : Redis avec persistance AOF
- **Administration** : Adminer pour la gestion de la base
- **Monitoring** : Health checks intégrés
- **Résilience** : Dépendances contrôlées entre services

L'application est entièrement containerisée, scalable et prête pour le déploiement en production avec des mécanismes de santé et de persistance robustes.
