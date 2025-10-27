

# 🧾 COMPTE-RENDU : Exploration des fonctionnalités avancées de Docker

### 🎯 **Objectif du TP**

Ce TP a pour but de se familiariser avec les fonctionnalités avancées de Docker :

* manipulation de conteneurs en mode interactif,
* installation de logiciels à l’intérieur,
* transfert de fichiers entre hôte et conteneur,
* création d’images personnalisées,
* et monitoring en temps réel des conteneurs.

---

## ⚙️ **1️⃣ Lancez un conteneur Ubuntu en mode interactif**

#### 🔹 Commande :

```bash
docker run -it --name myubuntu ubuntu
```

#### 🔹 Explication :

* `-i` : mode interactif
* `-t` : attache un pseudo-terminal
* `--name myubuntu` : nom du conteneur
* `ubuntu` : image officielle d’Ubuntu

#### 🔹 Résultat attendu :



```resultal
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
4b3ffd8ccb52: Pull complete
Digest: sha256:66460d557b25769b102175144d538d88219c077c678a49af4afca6fbfc1b5252
Status: Downloaded newer image for ubuntu:latest
```

Le terminal change de prompt :
```
root@a1b2c3d4e5f6:/#
```

---

## ⚙️ **2️⃣ Installez curl et vim dans le conteneur**

#### 🔹 Commandes :

```bash
apt update
apt install -y curl vim
```

#### 🔹 Explication :

* `apt update` met à jour la liste des paquets.
* `apt install` installe les outils demandés (`curl`, `vim`).
* L’option `-y` confirme automatiquement l’installation.

#### 🔹 Vérification :

```bash
curl --version
vim --version
```

```curl
curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.7
Release-Date: 2023-12-06, security patched: 8.5.0-2ubuntu10.6
Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd

```
```vim
curl 8.5.0 (x86_64-pc-linux-gnu)
```

---

## ⚙️ **3️⃣ Créez un fichier test.txt avec du contenu**

#### 🔹 Commande :

```bash
echo "Bonjour Docker avancé !" > test.txt
cat test.txt
```

#### 🔹 Résultat attendu :

```
Bonjour Docker avancé !
```

---

## ⚙️ **4️⃣ Sortez du conteneur sans l’arrêter**

#### 🔹 Raccourci clavier :

```
Ctrl + P  puis  Ctrl + Q
```

#### 🔹 Explication :

* Permet de **détacher** du conteneur sans le **stopper**.
* Le conteneur continue de tourner en arrière-plan.

#### 🔹 Vérification :

```bash
docker ps
```

Résultat :

```
CONTAINER ID   IMAGE     STATUS         NAMES
a7acc97e8d08   ubuntu    Up 6 minutes   myubuntu
```

---

## ⚙️ **5️⃣ Copiez le fichier test.txt du conteneur vers votre machine**

#### 🔹 Commande :

```bash
docker cp myubuntu:/test.txt ./test.txt
```
```
Successfully copied 2.05kB to C:\Users\DADAS\Desktop\Docker & Docker Compose\TP1 - Docker & Docker Compose\Exercice 2 - Manipulation avancée des conteneurs\test.txt
```

#### 🔹 Explication :

* `docker cp` copie un fichier ou dossier entre conteneur et hôte.
* Ici, on copie `/test.txt` depuis le conteneur vers le répertoire courant de la machine locale.

#### 🔹 Vérification :

```bash
cat test.txt
```

➡️ Contenu visible sur votre machine :

```
Bonjour Docker avancé !
```

---

## ⚙️ **6️⃣ Modifiez le fichier sur votre machine et recopiez-le dans le conteneur**

#### 🔹 Modification locale :

```bash
echo "Contenu modifié depuis l’hôte" >> test.txt
cat test.txt
```

Résultat :

```
Bonjour Docker avancé !
Contenu modifié depuis l’hôte
```

#### 🔹 Copie vers le conteneur :

```bash
docker cp ./test.txt myubuntu:/test.txt
```

---

## ⚙️ **7️⃣ Reconnectez-vous au conteneur et vérifiez les modifications**

#### 🔹 Commande :

```bash
docker exec -it myubuntu bash
cat /test.txt
```

#### 🔹 Résultat attendu :

```
Bonjour Docker avancé !
Contenu modifié depuis l’hôte
```

---

## ⚙️ **8️⃣ Créez une nouvelle image à partir de ce conteneur modifié**

#### 🔹 Commande :

```bash
docker commit myubuntu ubuntu-custom
```

#### 🔹 Explication :

* `docker commit` crée une **nouvelle image** à partir d’un conteneur existant.
* `ubuntu-custom` : nom de la nouvelle image.

#### 🔹 Vérification :

```bash
docker images
```

Résultat :

```
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
ubuntu-custom                    latest    dc00a54af28b   36 seconds ago   329MB
prom/prometheus                  latest    23031bfe0e74   4 days ago       507MB
grafana/grafana                  latest    35c41e0fd029   6 days ago       971MB
exo4-web                         latest    8276d3cbcdd1   7 days ago       235MB
flask-app                        latest    e7f3b2947db6   7 days ago       208MB
nginx                            alpine    61e01287e546   2 weeks ago      79.7MB
mirror.gcr.io/library/redis      alpine    59b6e6946534   3 weeks ago      100MB
ubuntu                           latest    66460d557b25   3 weeks ago      117MB
mirror.gcr.io/library/postgres   latest    073e7c8b84e2   4 weeks ago      643MB
hello-world                      latest    56433a6be3fd   2 months ago     20.3kB
apache/hadoop                    3.3.6     62a22627f35a   2 years ago      2.64GB
confluentinc/cp-kafka            7.3.0     06e5d17d6c51   3 years ago      1.3GB
confluentinc/cp-zookeeper        7.3.0     3ace7c3475a5   3 years ago      1.3GB
```

---

## ⚙️ **9️⃣ Lancez un nouveau conteneur basé sur votre image personnalisée**

#### 🔹 Commande :

```bash
docker run -it --name custom-container ubuntu-custom
```

#### 🔹 Vérification :

```bash
cat /test.txt
```

#### 🔹 Résultat attendu :

```
Bonjour Docker avancé !
Contenu modifié depuis l’hôte
```

➡️ ✅ Le fichier est bien présent dans le conteneur créé à partir de l’image personnalisée.

---

## ⚙️ **🔟 Testez que vos modifications sont bien présentes**

#### 🔹 Commandes :

```bash
curl --version
vim --version
cat /test.txt
```

#### 🔹 Vérification :

Les outils **curl** et **vim** sont installés, et le fichier modifié existe toujours.

---

## ⭐ **Bonus : Explorez les statistiques en temps réel**

#### 🔹 Commande :

```bash
docker stats
```

#### 🔹 Explication :

* Affiche en **temps réel** la consommation CPU, mémoire, réseau et disque des conteneurs actifs.

#### 🔹 Exemple de sortie :

```
CONTAINER ID   NAME               CPU %     MEM USAGE / LIMIT    MEM %     NET I/O           BLOCK I/O        PIDS
6c8690eebb72   custom-container   0.00%     980KiB / 15.5GiB     0.01%     872B / 126B       549kB / 0B       1
a7acc97e8d08   myubuntu           0.00%     12.71MiB / 15.5GiB   0.08%     87.5MB / 4.96MB   31.1MB / 200MB   2

```

---

## 💭 **Réflexion et conclusion**

### 🔸 **Concepts clés appris :**

* **Mode interactif (-it)** : permet d’utiliser un conteneur comme une machine Linux normale.
* **Détachement (Ctrl+P + Ctrl+Q)** : utile pour quitter un conteneur sans l’arrêter.
* **docker cp** : transfert de fichiers entre conteneur ↔ hôte.
* **docker commit** : création d’images personnalisées à partir d’un conteneur modifié.
* **docker stats** : surveillance en temps réel des performances.

---

### 🔸 **Bilan**

Ce TP nous a permis d’approfondir notre compréhension du cycle de vie d’un conteneur :
de sa création, modification, sauvegarde sous forme d’image, et réutilisation.

Nous avons ainsi construit une **image Ubuntu personnalisée** intégrant des outils et fichiers spécifiques, démontrant la puissance et la flexibilité de Docker.

