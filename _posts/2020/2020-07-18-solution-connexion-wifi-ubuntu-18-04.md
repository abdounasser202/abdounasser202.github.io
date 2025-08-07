---
layout: post
title: Ma machine HP Ubuntu 18.04 ne se connecte plus au WIFI - voici la solution
description: Découvrez comment résoudre le problème de connexion WiFi sur une machine HP avec Ubuntu 18.04.
permalink: /solution-connexion-wifi-ubuntu-18-04
author: Nasser
date: 2020-07-18 12:11:00 +0200
tags: [tech, Ubuntu, WiFi]
---

Bonjour!

J'ai installé Ubuntu 18.04 LTS sur le PC en dual Boot (avec Windows 10) et je n'arrivais plus à détecter la carte WiFi. Mais en démarrant sur Windows, tout fonctionnait bien.

La carte WiFi en question était une BCM43228.

Le souci était au niveau du pilote qui était absent. En effet cette carte étant un peu plus récente, son pilote ne se trouve pas encore dans les dépôts officiels de Ubuntu (à ce qu'il paraît au moment où j'ai rencontré ce problème).

Pour la solution, il fallait taper cette ligne de commande dans son terminal en utilisant bien évidemment une connexion Internet:

```bash
sudo apt-get autoremove --purge ; sudo apt-get clean ; sudo apt-get update ; sudo apt-get install linux-headers-generic ; sudo apt-get install --reinstall bcmwl-kernel-source && sudo service network-manager restart
```

Elle servira peut-être un jour : ceci est la solution à un problème qu'a rencontré mon stagiaire Gael. Il me l'a envoyé après résolution.
