# Projet : Load  Balancing, Test de Charge avec HAProxy et Node.js

## Description

L'objectif de ce projet est de démontrer les principes fondamentaux de l'équilibrage de charge (load balancing) en utilisant HAProxy. Nous allons configurer HAProxy pour répartir les requêtes HTTP entrantes entre deux serveurs web simples basés sur Node.js, le tout fonctionnant sur des conteneurs Docker. Ce projet illustre comment HAProxy peut efficacement gérer le trafic pour assurer une haute disponibilité et une fiabilité accrue des services.

## Déroulement du projet

Dans ce projet, nous allons :

- Configurer un environnement Docker pour héberger notre infrastructure de test.

- Développer deux serveurs web basiques en Node.js.

- Lancer les serveurs sur des ports distincts dans des conteneurs Docker.

- Installer et configurer HAProxy pour équilibrer la charge entre nos serveurs Node.js.

- Tester l'équilibrage de charge et observer la répartition des requêtes.

- Accéder à l'interface de statistiques de HAProxy pour surveiller ses performances et l'état des serveurs backend.

## Technologies utilisées

Node.js : Serveur backend

Express.js : Gestion des API

HAProxy : Load Balancer

Docker : Conteneurisation

JavaScript, HTML, CSS (Frontend) : Interface utilisateur

## Prérequis

Docker installé sur votre machine.

Si vous utilisez Windows, Docker Desktop doit être installé et en cours d’exécution.

Git installé pour cloner le projet.

## Installation

### Utiliser l'application depuis Docker Desktop

```bash
docker run -d -p 8080:8080 -p 8404:8404 ton_nom_utilisateur/haproxy_loadbalancing:latest
```

### Utiliser l'application en local

#### 1. Cloner le projet

```bash
git clone https://github.com/DidouLaMenace/haproxy_loadbalancing.git
cd haproxy_loadbalancing
```

#### 2. Build le container Docker

```bash
docker build -t haproxy_loadbalancing .
```

#### 3. Lancer l'application 

```bash
docker run -d --name haproxy_test -p 8080:8080 -p 8404:8404 haproxy_loadbalancing
```

## Accéder à l'application

Ouvrir http://localhost:8080 pour lancer l'application.

Ouvrir http://localhost:8080/dashboard pour lancer la simulation.

Ouvrir http://localhost:8404/stats pour voir les statistiques HAProxy.


## Personnalisation

Modifier haproxy.cfg pour ajuster les paramètres du load balancer.

Modifier dashboard.js pour adapter la cadence d'envoi des requêtes.

Modifier server1.js et server2.js pour tester différents comportements serveur.
