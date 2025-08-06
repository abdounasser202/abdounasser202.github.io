---
layout: post
title: Quelques commandes qu'il est impératif de connaître pour maîtriser Docker
description: Découvrez quelques commandes Docker essentielles pour gérer vos projets.
permalink: /commandes-docker
author: Nasser
date: 2019-07-15 11:21:00 +0200
tags: [Docker, DevOps, Développement]
---

Hello!

Aujourd'hui, je partage avec vous quelques commandes Docker qu'il est bon de connaître lorsque vous travaillez sur un projet utilisant Docker. Avant tout, il est important que vous téléchargiez *Docker* et *Docker Compose*. Ensuite, vous serez libre d'utiliser les commandes suivantes à votre convenance en fonction de vos besoins.

Mais avant de commencer, je suppose que vous savez ce qu'est Docker, une image et un conteneur. Sinon :

- **Docker** est un outil de déploiement d’applications dans des conteneurs. Ces conteneurs pourront alors partager une grande partie de leurs ressources avec le système hôte, ils auront accès aux fichiers du système d’exploitation en lecture seule et pourront se mettre en place.
- Une instance d'une image s'appelle un **conteneur**. Une image est donc un ensemble de calques que vous décrivez. Si vous démarrez cette image, vous avez un conteneur en cours d'exécution de cette image. Vous pouvez avoir plusieurs conteneurs en cours d'exécution de la même image.

Maintenant que tout est clair, voici les commandes que je juge importantes :

```bash
cd projet    # entrer dans un dossier projet
ifconfig docker0    # pour connaître l'adresse IP du projet
docker pull project    # télécharger un projet Docker sur sa machine
docker-compose up    # démarrer le serveur et afficher les logs
docker-compose stop    # arrêter le serveur
docker-compose restart    # redémarrer un serveur
docker-compose start    # démarrer un serveur sans afficher les logs
docker-compose build    # reconstruire une image
docker ps -a    # afficher tous les conteneurs
docker ps    # afficher les conteneurs qui fonctionnent à l'instant t (conteneurs actifs)
docker images    # afficher toutes les images
docker rm conteneur_id    # supprimer le conteneur ayant pour ID conteneur_id
docker rmi image_id    # supprimer l’image ayant pour ID image_id
```
