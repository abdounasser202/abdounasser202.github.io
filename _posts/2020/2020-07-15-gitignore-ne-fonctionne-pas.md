---
layout: post
title: Mon .gitignore ne fonctionne pas - comment dois-je faire pour corriger ça
description: Découvrez comment résoudre les problèmes avec votre fichier .gitignore.
permalink: /gitignore-ne-fonctionne-pas
author: Nasser
date: 2020-07-15 12:11:00 +0200
tags: [dev, Git]
---

Hello! Il vous est déjà certainement arrivé de constater que les fichiers que vous avez inséré dans votre .gitignore apparaissent toujours dans votre dépôt. Alors, je vous montre aujourd'hui comment corriger ça avec ces 3 petites commandes:

```bash
git rm -r --cached .
git add .
git commit -m "fixed untracked files"
```
