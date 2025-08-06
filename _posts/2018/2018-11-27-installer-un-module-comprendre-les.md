---
layout: post
title: Installer un module, comprendre les modèles Odoo et activer le mode développeur
description: Apprenez à installer des modules Odoo, comprendre les modèles Odoo et activer le mode développeur.
permalink: /installer-un-module-comprendre-les-modeles-odoo-et-activer-le-mode-developpeur
author: Nasser
date: 2018-11-27 12:11:00 +0200
tags: dev
---

Bonjour ! Aujourd'hui, nous allons parler de quelques aspects techniques d'Odoo qu'il est important de connaître : il s'agit de l'**installation des modules**, les **modèles Odoo** et l'**activation du mode développeur**.

## L'installation des modules

L'installation d'un module Odoo doit être prise au sérieux, car il ne suffit pas tout simplement de cliquer sur le bouton « Installer ». Pour que cette installation soit optimale et que le module installé ne pose pas de problèmes plus tard, **un ensemble de règles liés au fichier `__manifest__.py` ou `__openerp__.py` (pour ceux qui sont sur les versions 8 et 9) doit être respecté**.

1. Le `__manifest__` doit être très bien renseigné, il devra être cohérent et présenter toutes les informations nécessaires. [Voici un exemple de `__manifest__`](https://github.com/abdounasser202/odoo-addons/blob/8.0/pos_custom/__openerp__.py).
2. Dans le `__manifest__`, il faut absolument éviter les dépendances inutiles. Si vous n'utilisez pas un module, ne le mettez pas en dépendance.
3. Il faut aussi éviter ce que j'appellerai « les boucles de dépendances ». Ainsi, il faut éviter de faire hériter le module A du module B, puis faire hériter le module B du module A. D'autre part, si je considère une instance où j'ai des modules qui dépendent tous des modules qui permettent de personnaliser l'apparence de celle-ci (par exemple web, web_debranding, web_material_custom), **il serait préférable de créer un module web_template qui dépendra des modules web, web_debranding et web_material_custom**.
4. Il est important de savoir qu'avec Odoo, il est possible d'installer, de mettre à jour ou de désinstaller un module à partir de la ligne de commande. Voici une commande qui met à jour un module_A : `odoo.py -r odoo -w odoo -d my_odoo_db -u module_A`. Ici, `-r` représente le nom de l'utilisateur, `-w` son mot de passe, `-d` la base de données sur laquelle est installé le module_A, `-u` pour mettre à jour le module. Pour en savoir plus sur les commandes Odoo, [cliquez ici](https://www.getopenerp.com/tips-tricks-of-odoo-command-line/) et [ici](https://www.odoo.com/documentation/8.0/reference/cmdline.html).

## La compréhension des modèles Odoo

L'ORM d'Odoo présente une cartographie relationnelle des objets parmi lesquelles :

- **Une structure hiérarchique**
- **La cohérence et la validation des contraintes**
- **Le traitement optimisé par requête complexe (plusieurs actions à la fois)**
- **Les valeurs de champ par défaut**
- **Des types de champs variés** :
  - Classique (varchar, entier, booléen, ...)
  - Relationnel (one2many, many2one, many2many)
  - Fonctionnel (champs calculés, onchange)

Odoo propose trois mécanismes différents pour étendre les modèles de manière modulaire : créer un nouveau modèle à partir d'un modèle existant, ajouter de nouvelles informations à la copie tout en laissant le module d'origine tel quel, étendre les modèles définis dans d'autres modules sur place, remplaçant la version précédente.

Il est également important de noter ceci :

1. Le modèle `openerp.models.Model` permet d'instancier la classe sur la base de données lorsque le module de la classe est installé.
2. `openerp.models.TransientModel` permet d'afficher les fenêtres modales (wizard).
3. `openerp.models.AbstractModel` est un modèle abstrait qui permet la création d'une classe abstraite destinée à être héritée par les modèles classiques (`Model` et `TransientModel`). Il est très utilisé dans l'édition des rapports (report).

## Activation du mode développeur

Sur cette partie, j'ai tout simplement envie de partager avec vous une extension (Chrome et Firefox) qui permet d'activer le mode développeur d'Odoo en un clic. Il s'agit de l'extension **Odoo Debug** que vous pouvez retrouver sur [Chrome Web Store](https://chrome.google.com/webstore/detail/odoo-debug/hmdmhilocobgohohpdpolmibjklfgkbi) et [Firefox Add-ons](https://addons.mozilla.org/fr/firefox/addon/odoo-debug/).

Maintenant, j'ai du Python à coder ! Donc, tout en espérant vous avoir aidé, je vous dis à plus !
