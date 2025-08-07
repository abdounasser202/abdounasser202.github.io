---
layout: post
title: Git - comment supprimer une branche en local et à distance
description: Découvrez comment supprimer une branche Git en local et à distance.
permalink: /git-supprimer-branche-local-distance
author: Nasser
date: 2020-07-14 12:11:00 +0200
tags: [dev, Git]
---

Hello! Aujourd’hui je vais vous montrer comment supprimer une branche en local et à distance sur Git.

Pour le faire, il suffit de taper les commandes suivantes:

### Pour supprimer la branche distante

```bash
git push -d <remote_name> <branch_name>
```

**Exemple**

```bash
git push -d origin ma-branche
```

### Pour supprimer la branche locale

```bash
git branch -d ma-branche
```

Si vous voulez forcer la suppression de la branche

```bash
git branch -D ma-branche
```
