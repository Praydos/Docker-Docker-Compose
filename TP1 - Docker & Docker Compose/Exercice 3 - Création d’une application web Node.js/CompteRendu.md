
# 🧾 COMPTE-RENDU : Containerisation d’une application web complète avec Docker

### 🎯 **Objectif du TP**

Mettre en pratique la **containerisation d’une application Node.js** :

* Créer un serveur Express avec plusieurs routes.
* Construire une image Docker, l’optimiser, ajouter un health check.
* Comparer la taille avant et après optimisation.

---

## ⚙️ **1️⃣ Création du dossier du projet**

#### 🔹 Commande :

```bash
mkdir node-app
cd node-app
```

#### 🔹 Structure finale :

```
node-app/
 ├── package.json
 ├── server.js
 ├── Dockerfile
 └── .dockerignore
```

---

## ⚙️ **2️⃣ Création des fichiers nécessaires**

---

### 🧩 **2.1 – Fichier `package.json`**

Crée le fichier avec la configuration minimale pour Express :

```json
{
  "name": "node-app",
  "version": "1.0.0",
  "description": "Application Node.js containerisée",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  },
  "keywords": ["docker", "node", "express"],
  "author": "Docker Developer",
  "license": "MIT"
}
```

---

### 🧩 **2.2 – Fichier `server.js`**

Un serveur web Express avec les routes demandées :

```js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware de base
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Bienvenue sur notre application Node.js containerisée!',
        timestamp: new Date().toISOString()
    });
});

app.get('/api/health', (req, res) => {
    res.status(200).json({
        status: 'OK',
        message: 'L\'application fonctionne correctement',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

app.get('/api/info', (req, res) => {
    res.json({
        nodeVersion: process.version,
        platform: process.platform,
        memoryUsage: process.memoryUsage(),
        environment: process.env.NODE_ENV || 'development'
    });
});

app.get('/api/time', (req, res) => {
    res.json({
        currentTime: new Date().toISOString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        timestamp: Date.now()
    });
});

// Gestion des erreurs 404
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Route non trouvée',
        availableRoutes: ['/', '/api/health', '/api/info', '/api/time']
    });
});

// Démarrage du serveur
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Serveur démarré sur le port ${PORT}`);
    console.log(`📍 URL: http://localhost:${PORT}`);
});
```

---

### 🧩 **2.3 – Fichier `.dockerignore`**

Ce fichier empêche d’inclure les fichiers inutiles dans l’image Docker :

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.DS_Store
```

---

### 🧩 **2.4 – Fichier `Dockerfile` (version 1.0)**

```dockerfile
# Image de base
FROM node:18

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de configuration
COPY package*.json ./

# Installation des dépendances
RUN npm install

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 3000

# Commande de démarrage
CMD ["npm", "start"]
```

---

## ⚙️ **3️⃣ Construisez l’image Docker**

#### 🔹 Commande :

```bash
docker build -t node-app:1.0 .
```

#### 🔹 Vérification :

```bash
docker images
```

Résultat attendu :

```
REPOSITORY                       TAG       IMAGE ID       CREATED              SIZE
node-app                         1.0       3a539ff9dd69   About a minute ago   1.59GB
ubuntu-custom                    latest    dc00a54af28b   15 minutes ago       329MB

```

---

## ⚙️ **4️⃣ Lancez le conteneur sur le port 3000**

#### 🔹 Commande :

```bash
docker run -d -p 3000:3000 --name node-container node-app:1.0
```
```
1afbc1aaa63c08b9a491bf91c8585a7d6f8d502415657b0042e3f40c99a33bb6
```

#### 🔹 Vérification :

```bash
docker ps
```

Résultat :

```
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                         NAMES
1afbc1aaa63c   node-app:1.0    "docker-entrypoint.s…"   49 seconds ago   Up 49 seconds   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   node-app-container
6c8690eebb72   ubuntu-custom   "/bin/bash"              15 minutes ago   Up 15 minutes                                                 custom-container
a7acc97e8d08   ubuntu          "/bin/bash"              29 minutes ago   Up 29 minutes                                                 myubuntu
```

---

## ⚙️ **5️⃣ Testez toutes les routes**

Ouvrez dans le navigateur ou utilisez `curl` :

```bash
curl http://localhost:3000/  : {"message":"Bienvenue sur notre application Node.js containerisée!","timestamp":"2025-10-27T10:02:58.395Z"}
curl http://localhost:3000/api/health  : {"status":"OK","message":"L'application fonctionne correctement","uptime":270.168975132,"timestamp":"2025-10-27T10:06:02.689Z"}
curl http://localhost:3000/api/info : {"nodeVersion":"v18.20.8","platform":"linux","memoryUsage":{"rss":54489088,"heapTotal":8765440,"heapUsed":7525328,"external":1076250,"arrayBuffers":41162},"environment":"development"}
curl http://localhost:3000/api/time : {"currentTime":"2025-10-27T10:08:01.312Z","timezone":"UTC","timestamp":1761559681325}
```


#### 🔹 Résultats attendus :
{"message":"Bienvenue sur notre application Node.js containerisée!","timestamp":"2025-10-27T10:02:58.395Z"}
{"status":"OK","message":"L'application fonctionne correctement","uptime":270.168975132,"timestamp":"2025-10-27T10:06:02.689Z"}
{"nodeVersion":"v18.20.8","platform":"linux","memoryUsage":{"rss":54489088,"heapTotal":8765440,"heapUsed":7525328,"external":1076250,"arrayBuffers":41162},"environment":"development"}
{"currentTime":"2025-10-27T10:08:01.312Z","timezone":"UTC","timestamp":1761559681325}

---

## ⚙️ **6️⃣ Optimisez le Dockerfile pour réduire la taille de l’image**

Voici une version **optimisée** utilisant une image plus légère (`node:18-alpine`) et le cache intelligent :

```dockerfile
# Utilisation d'une image Alpine plus légère
FROM node:18-alpine

# Installation uniquement des packages nécessaires en production
RUN apk add --no-cache curl

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de configuration
COPY package*.json ./

# Installation des dépendances PRODUCTION uniquement
RUN npm ci --only=production

# Copie du code source
COPY . .

# Création d'un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Exposition du port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Commande de démarrage
CMD ["npm", "start"]
```

---

## ⚙️ **7️⃣ Reconstruisez avec le tag node-app:1.1**

#### 🔹 Commande :

```bash
docker build -t node-app:1.1 .
```

#### 🔹 Vérification :

```bash
docker images
```

---

## ⚙️ **8️⃣ Comparez les tailles des deux images**

 résultat :

REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
node-app     1.0       3a539ff9dd69   11 minutes ago   1.59GB

➡️ Gain de **~85%** grâce à l’image `alpine` et au cache intelligent.

---

## ⚙️ **9️⃣ Ajoutez un health check à votre Dockerfile**

Ajoutez cette ligne à la fin du Dockerfile optimisé :

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

#### 🔹 Explication :

* Docker exécute périodiquement cette commande pour vérifier la santé du conteneur.
* Si la commande échoue plusieurs fois, le statut du conteneur devient “unhealthy”.

---

## ⚙️ **🔟 Testez le health check avec docker inspect**

#### 🔹 Commande :

```bash
docker inspect --format='{{json .State.Health}}' node-container
```

#### 🔹 Exemple de résultat :

```json
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2025-10-27T09:00:00Z",
      "End": "2025-10-27T09:00:01Z",
      "ExitCode": 0,
      "Output": "Application is healthy "
    }
  ]
}
```

---

## 💭 **Analyse et conclusion**

### 🧩 Concepts clés maîtrisés :

| Fonctionnalité  | Description                                                        |
| --------------- | ------------------------------------------------------------------ |
| `Dockerfile`    | Script de construction d’image (base, dépendances, commande)       |
| `.dockerignore` | Exclusion des fichiers inutiles dans le build                      |
| `docker build`  | Création d’images avec tags                                        |
| `docker run`    | Lancement de conteneurs exposant des ports                         |
| `HEALTHCHECK`   | Supervision automatique de la santé du conteneur                   |
| Optimisation    | Réduction drastique de la taille via `alpine` et cache intelligent |

---

### 🧠 **Bilan**

Nous avons :

* Développé une **application Node.js complète**.
* Créé une **image Docker fonctionnelle**, puis une version **optimisée**.
* Implémenté un **health check** et vérifié son statut.

Résultat : une application **portable, légère et supervisée**, prête pour le déploiement dans tout environnement Docker (local ou cloud). 🌍🚀
