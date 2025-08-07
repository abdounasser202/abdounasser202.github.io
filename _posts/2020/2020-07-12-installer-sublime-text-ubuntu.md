---
layout: post
title: Comment installer Sublime Text sur Ubuntu
description: Guide pour installer Sublime Text sur Ubuntu avec quelques lignes de commande.
permalink: /installer-sublime-text-ubuntu
author: Nasser
date: 2020-07-12 12:11:00 +0200
tags: [Sublime Text, Ubuntu, installation]
---

[Sublime Text](https://www.sublimetext.com/) est un éditeur de texte léger qui permet de coder tout type d'applications. Aujourd'hui, **je vais vous montrer comment installer Sublime Text sur Ubuntu** avec juste quelques petites lignes de commandes !

## Pour l'installer

### Télécharger la clé publique et l'ajouter dans les sources

```bash
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
```

### Mettre à jour les paquets

```bash
sudo apt-get update
```

### Faire l'installation proprement dite

```bash
sudo apt-get install sublime-text
```

## Pour désinstaller Sublime Text

```bash
sudo apt-get remove sublime-text && sudo apt-get autoremove
```
