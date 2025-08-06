---
layout: post
title: Quelques commandes utiles sous Git que chaque débutant doit connaître
description: Découvrez quelques commandes Git essentielles pour les débutants.
permalink: /commandes-git-debutants
author: Nasser
date: 2019-08-14 00:00:00 +0200
tags: [Git, Développement, Outils]
---

Hello! Aujourd'hui je vais vous parler de Git.

Git est le système de contrôle de version distribué (ou simplement l'outil de collaboration) le plus célèbre et le plus performant jusqu'à présent.

Dans cet article, je partage avec vous une liste (non exhaustive) de commandes Git utiles. Ces commandes ont été initialement postées sur Twitter par [eliaswalyba](https://twitter.com/eliaswalyba).

En effet, Elias est un Senior AI/ML consultant et CoFounder [DopeLab](https://github.com/DopeLab) and [@GalsenAI](https://github.com/GalsenAI). Vous pouvez le retrouver sur [Twitter](https://twitter.com/eliaswalyba), [GitHub](https://github.com/eliaswalyba), [LinkedIn](https://www.linkedin.com/in/eliaswalyba/), et [YouTube](https://www.youtube.com/channel/UCHJfgo-twozt9nNq0XplU_g?view_as=subscriber) (il y publie des tutoriels).

Maintenant, passons aux choses sérieuses!

## Installer Git

Pour installer Git, rendez-vous sur le site [https://git-scm.com/downloads](https://git-scm.com/downloads). Téléchargez la distribution correspondante à votre système et installez-la.

Sur Ubuntu, ouvrez votre terminal et tapez:

```bash
$ sudo apt install git
```

Et le tour est joué. Vous avez Git installé.

Dans la suite de cet article, toutes les commandes que je vous présente s’exécutent sur un terminal (cmd pour Windows). Cependant, il existe des outils graphiques qui vous permettent de manipuler Git. Mais pour un début, je ne vous les conseille pas.

## Premières configurations

Configurer les informations utilisateur pour tous les référentiels locaux:

```bash
$ git config --global user.name "Votre nom"
```

Définit le nom que vous voulez attacher à vos transactions de commit.

```bash
$ git config --global user.email "Votre adresse email"
```

Définit l'email que vous voulez attacher à vos transactions de commit.

```bash
$ git config --global color.ui auto
```

Active la colorisation utile de la sortie en ligne de commande.

## Créer des dépôts

Démarrer un nouveau référentiel ou en obtenir un à partir d'une URL existante:

```bash
$ git init nom_du_projet
```

Crée un nouveau référentiel local avec le nom spécifié.

```bash
$ git clone url
```

Télécharge un projet et l'historique de ses versions.

## Faire des changements

Vérifier les modifications et créer une transaction de validation:

```bash
$ git status
```

Répertorie tous les fichiers nouveaux ou modifiés à valider.

```bash
$ git add nom_du_fichier
```

Capture instantanée du fichier en préparation (ou `.` pour tout ajouter).

```bash
$ git reset [fichier]
```

Décompose le fichier mais conserve son contenu.

```bash
$ git diff
```

Affiche les différences de fichier non encore mises en scène.

```bash
$ git diff --staged
```

Affiche les différences de fichier entre le transfert et la dernière version du fichier.

```bash
$ git commit -m "Une petite description de votre commit"
```

Enregistre les fichiers de manière permanente dans l'historique des versions.

## Regrouper des changements

Nommer une série de commits et combiner les efforts accomplis:

```bash
$ git branch
```

Répertorie toutes les branches locales du référentiel actuel.

```bash
$ git branch nom-branche
```

Crée une nouvelle branche.

```bash
$ git checkout nom-branche
```

Bascule vers la branche spécifiée et met à jour le répertoire de travail.

```bash
$ git merge nom-branche
```

Combine l’historique de la branche spécifiée dans la branche actuelle.

```bash
$ git branch -d nom-branche
```

Supprime la branche spécifiée.

## Modifications sur les fichiers

Déplacer et supprimer les fichiers versionnés:

```bash
$ git rm nom_fichier
```

Supprime le fichier du répertoire de travail.

```bash
$ git rm --cached nom_fichier
```

Supprime le fichier du contrôle de version mais conserve le fichier localement.

```bash
$ git mv ancien_nom_fichier nouveau_nom_fichier
```

Change le nom du fichier et le prépare pour le commit.

## Exclusion de fichier

Exclure les fichiers temporaires et les chemins:

Pour exclure certains fichiers (ne pas les tracker par Git), créez un fichier nommé **.gitignore** et mettez-y tous les fichiers que vous voulez exclure.

```bash
$ git ls-files --other --ignored --exclude-standard
```

Répertorie tous les fichiers exclus dans ce projet.

## Sauvegarder des fragments de fichiers

Doubler et restaurer les modifications incomplètes:

```bash
$ git stash
```

Stocke temporairement tous les fichiers suivis modifiés.

```bash
$ git stash list
```

Répertorie tous les changements cachés.

```bash
$ git stash pop
```

Restaure les derniers fichiers cachés.

```bash
$ git stash drop
```

Ignore le plus récent jeu de modifications stocké.

## Voir l'histoire de votre projet

Parcourir et inspecter l'évolution des fichiers de projet:

```bash
$ git log
```

Répertorie l'historique des versions de la branche actuelle.

```bash
$ git log --follow nom_fichier
```

Répertorie l'historique des versions d'un fichier, renommage compris.

```bash
$ git diff nom-branche-1 ... nom-branche-2
```

Affiche les différences de contenu entre deux branches.

```bash
$ git show hash-du-commit
```

Affiche les métadonnées et les modifications de contenu du commit spécifié.

## Refaire des commits

Effacer les erreurs et l'historique des remplacements:

```bash
$ git reset hash-du-commit
```

Annule tous les commits après [hash-du-commit], en préservant les modifications localement. Le hash-du-commit est un identifiant unique octroyé à chaque commit. Par exemple, `793e57778a8e33ee61044a8255ee3b37368596a7` est un hash-du-commit.

```bash
$ git reset --hard hash-du-commit
```

Ignore tout l'historique et rétablit le commit spécifié.

## Synchroniser vos changements (sur un serveur)

Enregistrer un signet de référentiel et échanger l'historique des versions:

```bash
$ git fetch url
```

Télécharge tout l'historique du signet du référentiel.

```bash
$ git push url nom-branche
```

Télécharge tous les commits des branches vers un serveur.

```bash
$ git pull url nom-branche
```

Télécharge l'historique des signets et intègre les modifications.

Voilà en gros quelques commandes de Git qu'Elias a publiées sur son fil Twitter.

> Après, je ne retiens pas toutes les commandes, mais sur internet vous pouvez trouver plein de ressources pour apprendre à utiliser Git. C'est une technologie incontournable maintenant, surtout dans le milieu professionnel, et malheureusement on en parle jamais dans les universités / instituts de formation.

Enjoy!
A+!
