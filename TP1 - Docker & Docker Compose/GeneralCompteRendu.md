

# 🧾 COMPTE-RENDU GÉNÉRAL : Initiation à Docker et Docker Compose

### **Auteur :** CHAFIK Anas

### **Date :** 27/10/2025

### **Contexte :**

Ce projet regroupe quatre exercices visant à :

1. Découvrir Docker Desktop et les commandes de base.
2. Explorer les fonctionnalités avancées des conteneurs.
3. Containeriser une application Node.js complète.
4. Orchestrer une stack full-stack avec Flask, PostgreSQL et Redis.

---

## **EXERCICE 1 : Première prise en main de Docker Desktop**

**Objectif :** Se familiariser avec les commandes de base et l’exécution d’un conteneur simple.

**Commandes clés :**

```bash
docker --version
docker run hello-world
docker pull nginx:alpine
docker images
docker run -d -p 8080:80 --name mynginx nginx:alpine
docker logs mynginx
docker ps -a
docker stop mynginx
docker rm mynginx
docker image prune -a
```

**Résultats :**

* Docker Desktop fonctionne correctement.
* Un conteneur Nginx est lancé et accessible sur le port 8080.
* Gestion des images et conteneurs maîtrisée.

**Concepts clés :**

* Différence **image vs conteneur**
* Mode détaché (`-d`) pour exécuter en arrière-plan.

---

## **EXERCICE 2 : Exploration des fonctionnalités avancées**

**Objectif :** Maîtriser les conteneurs interactifs, copier/modifier des fichiers et créer des images personnalisées.

**Commandes clés :**

```bash
docker run -it --name myubuntu ubuntu
apt update && apt install -y curl vim
echo "Bonjour Docker avancé !" > test.txt
Ctrl+P, Ctrl+Q   # détacher sans stopper
docker cp myubuntu:/test.txt ./
docker cp ./test.txt myubuntu:/test.txt
docker exec -it myubuntu bash
docker commit myubuntu ubuntu-custom
docker run -it --name custom-container ubuntu-custom
docker stats
```

**Résultats :**

* Fichier créé, copié entre hôte et conteneur, modifié et vérifié.
* Création d’une image personnalisée réutilisable.
* Surveillance des conteneurs en temps réel.

**Concepts clés :**

* Mode interactif (`-it`) et détachement
* Copie de fichiers (`docker cp`)
* Création d’images (`docker commit`)
* Statistiques en temps réel (`docker stats`)

---

## **EXERCICE 3 : Containerisation d’une application Node.js**

**Objectif :** Dockeriser une application web Node.js/Express avec routes multiples et optimisation d’image.

**Structure du projet :**

```
node-app/
 ├── package.json
 ├── server.js
 ├── Dockerfile
 └── .dockerignore
```

**Commandes clés :**

```bash
docker build -t node-app:1.0 .
docker run -d -p 3000:3000 --name node-container node-app:1.0
docker build -t node-app:1.1 .
```

**Optimisations :**

* Utilisation de `node:alpine` pour réduire la taille de l’image
* Utilisation de `.dockerignore` pour exclure les fichiers inutiles
* Ajout de `HEALTHCHECK` pour vérifier l’état du conteneur

**Résultats :**

* Routes `/`, `/api/health`, `/api/info`, `/api/time` fonctionnelles.
* Réduction de taille de ~1GB → 155MB avec image optimisée.
* Health check opérationnel.

---

## **EXERCICE 4 : Orchestration d’une application full-stack (Flask + PostgreSQL + Redis)**

**Objectif :** Mettre en place une stack complète avec Docker Compose, services interconnectés, volumes persistants et health checks.

**Structure du projet :**

```
fullstack-app/
 ├── app/
 │   ├── app.py
 │   ├── db.py
 │   ├── models.py
 │   ├── cache.py
 │   └── requirements.txt
 ├── Dockerfile
 └── docker-compose.yml
```

**Commandes clés :**

```bash
docker-compose up --build
docker ps
docker exec -it flask-app bash
curl http://localhost:5000/users
```

**Services :**

* `web` : Flask API avec endpoints CRUD `/users` et health check
* `db` : PostgreSQL avec volume persistant
* `cache` : Redis pour cache des sessions
* `adminer` : Interface d’administration de la base

**Résultats :**

* La stack complète fonctionne, les services communiquent correctement.
* Les données utilisateurs sont persistées dans PostgreSQL.
* Health checks et dépendances entre services opérationnels.

**Concepts clés :**

* Orchestration multi-conteneurs avec **Docker Compose**
* Persistance via **volumes**
* Health checks et dépendances (`depends_on`)
* Test et supervision de la stack complète

---

## **Bilan général**

* Maîtrise progressive de **Docker** : images, conteneurs, volumes, health check.
* Création d’images personnalisées et optimisation.
* Gestion de stacks multi-services avec **Docker Compose**.
* Applications web simples et full-stack fonctionnelles et containerisées.
* Compétences acquises transférables pour le déploiement en production.


