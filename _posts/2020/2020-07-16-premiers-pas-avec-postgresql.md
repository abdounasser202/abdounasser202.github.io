---
layout: post
title: Premiers pas avec PostgreSQL
description: Découvrez comment commencer avec PostgreSQL, un SGBD SQL open source.
permalink: /premiers-pas-avec-postgresql
author: Nasser
date: 2020-07-16 12:11:00 +0200
tags: [dev, PostgreSQL, Base de données]
---

Hello! Aujourd'hui je vais vous aider à entrer en contact avec [PostgreSQL](https://www.postgresql.org/). En effet, PostgreSQL est un SGBD SQL open source. Publié sous licence [BSD](https://fr.wikipedia.org/wiki/Licence_BSD), il s'agit de la base de données open source la plus avancée au monde. **Ce programme écrit en C et sorti le 8 juillet 1996 a été créé par Michael Stonebraker.**

> Si vous recherchez un tutoriel complet sur PostgreSQL, voici la bonne adresse [https://www.postgresqltutorial.com/](https://www.postgresqltutorial.com/)

## Comment installer PostgreSQL sur Ubuntu?

C'est simple, il suffit de taper les commandes suivantes

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

## Comment créer un utilisateur de manière interactive avec PostgreSQL?

Pour cela, tapez tout simplement

```bash
sudo -u postgres createuser --interactive
```

## Quelle est la commande pour créer une base de données avec PostgreSQL?

```bash
sudo -u postgres createdb nom_de_votre_bd
```

## Comment se connecter à une base de données PostgreSQL en ligne de commande?

```bash
sudo -u postgres psql
\l # pour lister vos BD
\c nom_de_votre_bd # pour vous connecter à votre BD
```

## Comment modifier le mot de passe d'un utilisateur sur PostgreSQL?

```bash
ALTER USER nom_utilisateur PASSWORD 'nouveau_mot_de_passe';
```
