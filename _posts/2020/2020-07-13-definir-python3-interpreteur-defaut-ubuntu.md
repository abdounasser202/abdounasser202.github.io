---
layout: post
title: Comment définir Python 3 comme interpréteur Python par défaut en lieu et place de Python 2 sur Ubuntu
description: Découvrez comment définir Python 3 comme interpréteur par défaut sur Ubuntu.
permalink: /definir-python3-interpreteur-defaut-ubuntu
author: Nasser
date: 2020-07-13 12:11:00 +0200
tags: [dev, Python, Ubuntu]
---

Hello! Aujourd'hui je vais vous montrer comment définir l'interpréteur de Python 3 (version 3.6) comme interpréteur Python par défaut.

Pour le faire c'est simple: tapez tout simplement les commandes suivantes

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

sudo update-alternatives --config python
```

Enfin choisissez le numéro représentant la version de Python que vous voulez définir par défaut (dans notre cas il s'agit du 2)
