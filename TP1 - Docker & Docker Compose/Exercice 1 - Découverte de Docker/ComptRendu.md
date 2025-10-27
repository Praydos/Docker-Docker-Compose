

## 🧾 **COMPTE-RENDU : Première prise en main de Docker Desktop**

### **Contexte**

Ce travail a pour objectif de se familiariser avec **Docker Desktop**, un outil permettant de créer, exécuter et gérer des conteneurs.
Nous allons exécuter une série d’exercices pour comprendre les **commandes Docker de base**, la **gestion des images** et des **conteneurs**.

---

## ⚙️ **Exercices et solutions**

### **1️⃣ Vérifiez que Docker Desktop est bien installé et démarré**

#### 🔹 Commande :

```bash
docker --version
```

#### 🔹 Explication :

* `docker --version` : vérifie que Docker CLI est bien installé.

#### 🔹 Résultat attendu :

Une sortie similaire à :

```
Docker version 28.5.1, build e180ab8
```

---

### **2️⃣ Exécutez votre premier conteneur avec l’image hello-world**

#### 🔹 Commande :

```bash
docker run hello-world
```

#### 🔹 Explication :

* Télécharge automatiquement l’image `hello-world` depuis Docker Hub si elle n’existe pas localement.
* Crée et exécute un conteneur qui affiche un message de bienvenue.

#### 🔹 Résultat attendu :

Un message confirmant que Docker fonctionne :

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

### **3️⃣ Téléchargez l’image nginx:alpine sans la lancer**

#### 🔹 Commande :

```bash
docker pull nginx:alpine
```

#### 🔹 Explication :

* `docker pull` télécharge une image depuis Docker Hub sans créer de conteneur.
* L’image `nginx:alpine` est une version légère de Nginx basée sur Alpine Linux.

#### 🔹 Résultat attendu :

```
alpine: Pulling from library/nginx
76c9bcaa4163: Pull complete
e2d0ea5d3690: Pull complete
83ce83cd9960: Pull complete
f80aba050ead: Pull complete
621a51978ed7: Pull complete
7fb80c2f28bc: Pull complete
03e63548f209: Pull complete
Digest: sha256:61e01287e546aac28a3f56839c136b31f590273f3b41187a36f46f6a03bbfe22
Status: Downloaded newer image for nginx:alpine
docker.io/library/nginx:alpine
```

---

### **4️⃣ Listez toutes les images présentes sur votre système**

#### 🔹 Commande :

```bash
docker images
```

#### 🔹 Explication :

* Affiche toutes les images téléchargées avec leurs **nom**, **tag**, **ID**, **taille**, et **date de création**.

#### 🔹 Exemple de résultat :

```
REPOSITORY                       TAG       IMAGE ID       CREATED        SIZE
prom/prometheus                  latest    23031bfe0e74   4 days ago     507MB
grafana/grafana                  latest    35c41e0fd029   6 days ago     971MB
exo4-web                         latest    8276d3cbcdd1   7 days ago     235MB
flask-app                        latest    e7f3b2947db6   7 days ago     208MB
nginx                            alpine    61e01287e546   2 weeks ago    79.7MB
mirror.gcr.io/library/redis      alpine    59b6e6946534   3 weeks ago    100MB
mirror.gcr.io/library/postgres   latest    073e7c8b84e2   4 weeks ago    643MB
hello-world                      latest    56433a6be3fd   2 months ago   20.3kB
apache/hadoop                    3.3.6     62a22627f35a   2 years ago    2.64GB
confluentinc/cp-kafka            7.3.0     06e5d17d6c51   3 years ago    1.3GB
confluentinc/cp-zookeeper        7.3.0     3ace7c3475a5   3 years ago    1.3GB
```

---

### **5️⃣ Lancez un conteneur nginx en arrière-plan sur le port 8080**

#### 🔹 Commande :

```bash
docker run -d -p 8080:80 --name mynginx nginx:alpine
```

```resultat
cc043a0256e950ddf8f38bc076d6ef060928acdabf17aee03fd3776495f4c8bf
```

#### 🔹 Explication :

* `-d` : exécution en **arrière-plan** (détaché).
* `-p 8080:80` : redirige le port **8080** de la machine hôte vers le port **80** du conteneur.
* `--name mynginx` : nomme le conteneur “mynginx”.

#### 🔹 Vérification :

```bash
docker ps
```

Résultat attendu :

```
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                     NAMES
cc043a0256e9   nginx:alpine   "/docker-entrypoint.…"   55 seconds ago   Up 54 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   mynginx
```

---

### **6️⃣ Vérifiez que le serveur web est accessible dans votre navigateur**

#### 🔹 Étapes :

Ouvrez votre navigateur et tapez :

```
http://localhost:8080
```

#### 🔹 Résultat attendu :

Une page Nginx par défaut avec le message :

<img width="681" height="292" alt="image" src="https://github.com/user-attachments/assets/19c3a928-2e56-4c3d-bf80-bbc7edb8c58e" />


---

### **7️⃣ Affichez les logs du conteneur nginx**

#### 🔹 Commande :

```bash
docker logs mynginx
```

#### 🔹 Explication :

* Affiche la sortie standard (stdout/stderr) du conteneur.

#### 🔹 Exemple de résultat :

```
docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/10/27 09:07:09 [notice] 1#1: using the "epoll" event method
2025/10/27 09:07:09 [notice] 1#1: nginx/1.29.2
2025/10/27 09:07:09 [notice] 1#1: built by gcc 14.2.0 (Alpine 14.2.0)
2025/10/27 09:07:09 [notice] 1#1: OS: Linux 6.6.87.2-microsoft-standard-WSL2
2025/10/27 09:07:09 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2025/10/27 09:07:09 [notice] 1#1: start worker processes
2025/10/27 09:07:09 [notice] 1#1: start worker process 30
2025/10/27 09:07:09 [notice] 1#1: start worker process 31
2025/10/27 09:07:09 [notice] 1#1: start worker process 32
2025/10/27 09:07:09 [notice] 1#1: start worker process 33
2025/10/27 09:07:09 [notice] 1#1: start worker process 34
2025/10/27 09:07:09 [notice] 1#1: start worker process 35
2025/10/27 09:07:09 [notice] 1#1: start worker process 36
2025/10/27 09:07:09 [notice] 1#1: start worker process 37
2025/10/27 09:07:09 [notice] 1#1: start worker process 38
2025/10/27 09:07:09 [notice] 1#1: start worker process 39
2025/10/27 09:07:09 [notice] 1#1: start worker process 40
2025/10/27 09:07:09 [notice] 1#1: start worker process 41
172.17.0.1 - - [27/Oct/2025:09:08:33 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0" "-"
172.17.0.1 - - [27/Oct/2025:09:08:34 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost:8080/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0" "-"
2025/10/27 09:08:34 [error] 30#30: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 172.17.0.1, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080", referrer: "http://localhost:8080/"
...
```

---

### **8️⃣ Listez tous les conteneurs (en cours et arrêtés)**

#### 🔹 Commande :

```bash
docker ps -a
```

#### 🔹 Explication :

* `-a` affiche **tous** les conteneurs, y compris ceux arrêtés.

#### 🔹 Exemple de résultat :

```
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS                     PORTS                                     NAMES
cc043a0256e9   nginx:alpine             "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   mynginx
f249aec6c5f6   hello-world              "/hello"                 8 minutes ago   Exited (0) 8 minutes ago                                             loving_ardinghelli
13db0e0255b8   grafana/grafana:latest   "/run.sh"                3 days ago      Exited (0) 2 days ago                                                grafana
b9c3bb384dbb   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago      Exited (143) 2 days ago                                              datanode
6ea2649f6860   prom/prometheus:latest   "/bin/prometheus --c…"   3 days ago      Exited (0) 2 days ago                                                prometheus
68d534375a9c   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago      Exited (143) 2 days ago                                              bigdatatp-nodemanager-1
0ca9e9efba92   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago      Exited (143) 2 days ago                                              namenode
0336e4fb72fb   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago      Exited (143) 2 days ago                                              bigdatatp-resourcemanager-1
```

---

### **9️⃣ Arrêtez et supprimez le conteneur nginx**

#### 🔹 Commandes :

```bash
docker stop mynginx
docker rm mynginx
```

#### 🔹 Explication :

* `stop` arrête le conteneur.
* `rm` supprime le conteneur arrêté.

#### 🔹 Vérification :

```bash
docker ps -a
```

```resultat
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                      PORTS     NAMES
f249aec6c5f6   hello-world              "/hello"                 10 minutes ago   Exited (0) 10 minutes ago             loving_ardinghelli
13db0e0255b8   grafana/grafana:latest   "/run.sh"                3 days ago       Exited (0) 2 days ago                 grafana
b9c3bb384dbb   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago       Exited (143) 2 days ago               datanode
6ea2649f6860   prom/prometheus:latest   "/bin/prometheus --c…"   3 days ago       Exited (0) 2 days ago                 prometheus
68d534375a9c   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago       Exited (143) 2 days ago               bigdatatp-nodemanager-1
0ca9e9efba92   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago       Exited (143) 2 days ago               namenode
0336e4fb72fb   apache/hadoop:3.3.6      "/usr/local/bin/dumb…"   3 days ago       Exited (143) 2 days ago               bigdatatp-resourcemanager-1
```

---

### **🔟 Nettoyez les images inutilisées**

#### 🔹 Commande :

```bash
docker image prune -a
```

#### 🔹 Explication :

* Supprime toutes les images **non utilisées par un conteneur**.
* L’option `-a` permet de supprimer toutes les images inutilisées (non seulement les “dangling”).

#### 🔹 Attention :

Vous serez invité à confirmer :

```
WARNING! This will remove all images not used by any container.
Are you sure you want to continue? [y/N]
```

---

## 💭 **Questions de réflexion**

### **🧩 Quelle est la différence entre une image et un conteneur ?**

| Élément       | Description                                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Image**     | Un modèle (template) immuable qui contient tout le nécessaire pour exécuter une application : code, dépendances, configurations, etc. |
| **Conteneur** | Une **instance en cours d’exécution** d’une image. Il est créé à partir de l’image, mais peut avoir un état ou des fichiers propres.  |

➡️ **Analogie :**
Une *image* = recette de cuisine 🍰
Un *conteneur* = gâteau préparé 🎂

---

### **🧩 Pourquoi utiliser l’option `-d` lors du lancement d’un conteneur ?**

* L’option `-d` (**detached mode**) permet d’exécuter un conteneur **en arrière-plan**.
* Cela libère le terminal et permet de continuer à exécuter d’autres commandes.
* Utile pour les services continus comme Nginx, PostgreSQL, etc.

Sans `-d`, le conteneur prend le contrôle du terminal et affiche ses logs en direct.

---

## ✅ **Conclusion**

Dans ce premier TP Docker :

* Nous avons manipulé les commandes de base (`run`, `pull`, `ps`, `stop`, `rm`, etc.).
* Nous avons compris la différence entre **image** et **conteneur**.
* Nous avons appris à exécuter un service web dans un conteneur Nginx accessible sur notre machine.

🧠 **Compétences acquises :**

* Gestion d’images et conteneurs Docker
* Exécution de services en arrière-plan
* Nettoyage et maintenance du système Docker


