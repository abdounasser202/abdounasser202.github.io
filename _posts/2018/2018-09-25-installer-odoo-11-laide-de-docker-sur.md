---
layout: post
title: "Installer Odoo 11 à l'aide de Docker sur Ubuntu 18.04 LTS"
description: "Guide complet pour installer Odoo 11 avec Docker sur Ubuntu 18.04. Découvrez comment containeriser votre environnement de développement Odoo facilement."
permalink: /installer-odoo-11-a-l-aide-de-docker-sur-ubuntu-18-04-lts
author: Nasser
date: 2018-09-25 12:11:00 +0200
tags: [dev, docker, odoo, ubuntu, containerisation, tutorial]
image: "/assets/images/docker-odoo-banner.jpg"
---

Docker est un outil de déploiement d'applications dans des containers. Ces containers pourront alors partager une grande partie de leurs ressources avec le système hôte, ils auront accès aux fichiers du système d'exploitation en lecture seule et pourront se mettre en place. 

Quant au système hôte, ce dernier utilisera les mêmes ressources pour un ou plusieurs containers. Ainsi, l'un des avantages qu'offre Docker est **l'uniformité des environnements** en ce sens que l'environnement de développement d'une application sera identique à celui de production.

## Prérequis

Avant de commencer, assurez-vous d'avoir :
- Ubuntu 18.04 LTS installé
- Accès administrateur (sudo)
- Connexion internet active

## Installation de Docker et Docker Compose

L'installation d'Odoo est très facile : le principe est simple. Tout ce que vous aurez à faire c'est de taper les commandes suivantes :

```bash
sudo apt install docker.io
sudo pip install docker-compose
```

### Vérification de l'installation

Pour vérifier que l'installation a réussi :

```bash
# Pour voir votre version de docker
sudo docker --version

# Pour consulter tous vos containers
sudo docker ps -a 
```

### Utiliser Docker sans sudo (optionnel)

Si vous voulez utiliser la commande docker sans sudo :

```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
```

> **Note** : Vous devrez vous déconnecter et vous reconnecter pour que les changements prennent effet.

## Installation d'Odoo 11 avec Docker Compose

Ensuite vous pourrez installer votre environnement Odoo. Pour plus de facilité, j'ai créé un dossier nommé **odoo-docker** que vous pourrez trouver [ici sur GitHub](https://github.com/abdounasser202/my-workspace/tree/main/odoo-docker).

### Étapes d'installation :

1. **Clonez le repository** :
   ```bash
   git clone https://github.com/abdounasser202/my-workspace.git
   cd my-workspace/odoo-docker
   ```

2. **Lancez l'installation** :
   ```bash
   docker-compose up
   ```

PostgreSQL et Odoo vont s'installer automatiquement. À la fin de l'installation, vous pourrez lancer votre navigateur et accéder à Odoo via `http://localhost:8069`.

## Outils de développement recommandés

Maintenant que tout est configuré, je vous invite à installer tous les outils de développement qui vous seront nécessaires.

### Mes recommandations personnelles :

- **Éditeur de texte** : Atom avec plugins Git
- **Gestion de version** : GitKraken ou Git en ligne de commande
- **Base de données** : DBeaver pour l'administration PostgreSQL
- **Navigateurs** : Google Chrome et Firefox pour les tests
- **Hébergement du code** : GitHub ou GitLab

### Configuration de l'environnement de développement

```bash
# Installation des outils essentiels
sudo apt update
sudo apt install git curl wget vim

# Installation d'un éditeur moderne (VS Code par exemple)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
```

## Prochaines étapes

La prochaine fois, nous allons entrer plus en détails dans cet environnement et vous saurez comment utiliser Docker pour tous vos projets Odoo.

### Ce que vous apprendrez :
- Configuration avancée de Docker Compose
- Personnalisation de l'environnement Odoo
- Gestion des modules personnalisés
- Déploiement en production

## Conclusion

Docker simplifie considérablement l'installation et la gestion d'Odoo. Avec cette configuration, vous disposez maintenant d'un environnement de développement portable et reproductible.

---

## Ressources utiles

- [Documentation officielle Docker](https://docs.docker.com/)
- [Documentation Odoo](https://www.odoo.com/documentation/)
- [Repository GitHub du projet](https://github.com/abdounasser202/my-workspace/tree/main/odoo-docker)
