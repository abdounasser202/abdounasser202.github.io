---
layout: post
title: Les bonnes pratiques à suivre lorsqu'on fait du développement Odoo
description: Bonnes pratiques pour structurer et maintenir proprement un projet Odoo.
permalink: /les-bonnes-pratiques-a-suivre-lorsqu-on-fait-du-developpement-odoo
author: Nasser
date: 2018-11-20 12:11:00 +0200
tags: dev
---

Hello !

Aujourd'hui, je vais vous partager quelques bonnes pratiques que j’utilise au quotidien lors de mes développements Odoo. En les appliquant, vous gagnerez en productivité et votre code gagnera en élégance. 💡

## 1. Une classe par fichier

Comme en Java, j'écris toujours **une classe par fichier**. Cela me permet de savoir, à tout moment, quelles fonctionnalités se trouvent où.

## 2. Correspondance entre noms de fichiers et de classes

Chaque classe porte le même nom que son fichier.  
Par exemple, si j’ai une classe `ResPartner` dans laquelle je surcharge le modèle `res.partner`, alors mon fichier s’appellera :

```python
res_partner.py
````

## 3. Préfixe des modèles avec le nom du projet

Les noms de mes modèles commencent toujours par le **nom du projet**.
Par exemple, si mon projet s'appelle **GestPaie**, un modèle pour le virement des salaires s'appellera :

```python
gestpaie.virement.salaire
```

Cela m’aide à rapidement identifier les modèles liés à un projet donné, notamment lors de l’exploration de la base de données ou pendant le débogage.

## 4. Nommage clair des IDs dans les vues XML

### a. Préfixe avec le nom du projet

Les IDs des balises `<record>` commencent toujours par le nom du projet :

```xml
gest_paie_virement_salaire
```

### b. Indiquer le type de vue dans l’ID

Chaque ID inclut également une indication du type de vue ou d'action :

* `gest_paie_virement_salaire_view_tree`
* `gest_paie_virement_salaire_view_form`
* `gest_paie_virement_salaire_action`, etc.

## 5. Ordre des menus dans le XML

Je place **les menus secondaires** de chaque modèle **en fin de fichier XML**, pour garder une structure cohérente et facile à maintenir.

## 6. Versionnage avec Git

Tous mes projets sont **versionnés avec Git**. Après chaque modification majeure, je fais un :

```bash
git push
```

## 7. Mon environnement de développement

Voici mon setup habituel :

* Docker 🐳
* Atom 💻
* Ubuntu 🐧
* Git 🌱

J’espère que ces quelques conseils vous seront utiles.
Bonne chance dans vos développements Odoo, et à bientôt ! 🚀
