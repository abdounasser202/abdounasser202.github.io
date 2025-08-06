---
layout: post
title: Comment créer, sauvegarder, supprimer et restaurer une base de donnée Odoo
description: Apprenez à manipuler votre base de données Odoo, y compris la création, la sauvegarde, la suppression et la restauration via l'interface d'Odoo.
permalink: /comment-creer-sauvegarder-supprimer-et-restaurer-une-base-de-donnee-odoo
author: Nasser
date: 2018-11-24 12:11:00 +0200
tags: dev
---

Bonjour ! Aujourd'hui, je vais vous montrer comment manipuler votre base de données Odoo. Il s'agira principalement de la **création, sauvegarde, suppression et restauration** à travers l'interface d'Odoo. Je ne manquerai également pas de vous briefer un tout petit peu sur PostgreSQL.

## Création de la base de données

Normalement, après avoir installé et démarré Odoo, un formulaire de création de la base de données s'affiche via l'URL **localhost/web/database/manager** tel qu'indiqué sur la figure suivante.

[![Création de la base de données](https://1.bp.blogspot.com/-VGUnxX-1QOM/W_iB9q6l4zI/AAAAAAAACxY/xvevHylEA-sbpH9iE-j70Xly91uC020JwCLcBGAs/s320/1.png)](https://1.bp.blogspot.com/-VGUnxX-1QOM/W_iB9q6l4zI/AAAAAAAACxY/xvevHylEA-sbpH9iE-j70Xly91uC020JwCLcBGAs/s1600/1.png)

Entrez le nom de la BD, votre email et votre mot de passe. Ce formulaire vous donne aussi la possibilité de choisir une langue et votre pays. Si vous voulez tester Odoo, vous avez également la possibilité de cocher le champ **"load demonstration data"**. En cochant ce champ, Odoo chargera toutes les données qui vous seront nécessaires pour voir comment il fonctionne.

## Sauvegarder une base de données

La sauvegarde dont je vais vous parler ici consiste en quelque sorte à faire le dump de la BD pour la partager par exemple avec un collègue ou faire un test sur un autre environnement. Là également, Odoo a tout prévu sur une vue.

[![Sauvegarder une base de données](https://3.bp.blogspot.com/-jqHFUa5lXjU/W_iEYGS9nHI/AAAAAAAACxw/lsTYanepalo1XVMCGhU_S80wPmLljMLNACLcBGAs/s320/2.png)](https://3.bp.blogspot.com/-jqHFUa5lXjU/W_iEYGS9nHI/AAAAAAAACxw/lsTYanepalo1XVMCGhU_S80wPmLljMLNACLcBGAs/s1600/2.png)

Sur la figure ci-dessus, vous pouvez constater que j'ai 3 BD sur cette instance d'Odoo (Version 10 en l’occurrence). Donc, si vous avez besoin de sauvegarder l'une de ces BD, cliquez juste sur le lien **"Backup"** de la BD correspondante et sélectionnez le champ **"zip (include filestore)"** afin de récupérer tous les fichiers statiques. Contrairement à ce dernier, le champ **"pg_dump custom format (without filestore)"** récupère uniquement les données sans fichiers statiques.

## Supprimer une base de données

La suppression est simple mais faites très attention : ne supprimez jamais une BD tant que vous ne l'avez pas sauvegardée. Si vous avez retenu la leçon, je vous dirai de supprimer votre BD en cliquant tout simplement sur le lien **"Delete"**.

## Restaurer une base de données

Pour restaurer une BD que vous avez au préalable sauvegardée, cliquez sur le bouton **"Restore Database"**, renseignez les informations qui s'affichent à l'écran et chargez la BD en question.

[![Restaurer une base de données](https://1.bp.blogspot.com/-e1XGC7xeAJQ/W_iHwSWzvdI/AAAAAAAACyI/Y8OyGR3jHOMMBNUcpjc6pxrFz9mdUWJiwCLcBGAs/s320/4.png)](https://1.bp.blogspot.com/-e1XGC7xeAJQ/W_iHwSWzvdI/AAAAAAAACyI/Y8OyGR3jHOMMBNUcpjc6pxrFz9mdUWJiwCLcBGAs/s1600/4.png)

**Attention !** Sur cette instance, vous pouvez voir que je n'ai pas renseigné le **"Master password"** pourtant il est très important ! Ceci est une manière de vous dire de ne jamais déployer une instance d'Odoo en production sans avoir renseigné ce **"Master Password"** car c'est lui qui protège votre BD en cas de manipulations malveillantes !

Enfin, si vous avez installé Odoo à partir du code source et vous voulez créer votre BD, reproduisez les étapes suivantes :

```bash
sudo apt-get install postgresql postgresql-contrib # installez postgresql
sudo -i -u postgres # connectez-vous avec l'utilisateur postgres
createdb new_db # créez votre BD
createuser --interactive # créer un utilisateur: de préférence il s'appellera odoo
```

Sur ce, c'est tout pour aujourd'hui. J'espère vous avoir aidé. À plus !
