---
layout: post
title: La gestion du processus d'achat et l'entrée des produits en stocks
description: Apprenez à gérer le processus d'achat et l'entrée des produits en stock dans Odoo.
permalink: /gestion-processus-achat-stock-odoo
author: Nasser
date: 2019-08-28 16:50:00 +0200
tags: [Odoo, Gestion des stocks, Achats]
---

Hello!

La semaine dernière, je vous montrais comment gérer les dépendances, utiliser les variantes de produits et établir des liens entre modèles.

Nous allons entrer dans le vif du sujet: gérer le processus d'achat et faire entrer nos livres dans le stock! Je vous laisse un petit secret: j'ai comme l'impression que ce tutoriel ne va nécessiter aucune écriture de code :)

Commencez par démarrer votre instance Odoo et assurez-vous d'avoir le module **oo_library**. Sinon, il est disponible à [cette adresse](https://apps.odoo.com/apps/browse?repo_maintainer_id=140338).

## Gestion du processus d'achat

Le principe est simple:

1. Cliquer sur le menu **Achats**.
2. Ensuite, sur le bouton créer situé dans la vue demande de prix.

![Demande de prix](https://1.bp.blogspot.com/-1W9MtP31ods/XWaIRA1uj3I/AAAAAAAADFc/x8CQFL1r_9EojqQIlNn6Pa0VHVSlL6WZgCLcBGAs/s320/demande%2Bde%2Bprix.PNG)

### C'est quoi une demande de prix?

Comme mentionné sur la vue, la demande de prix ou devis contient l'histoire de la discussion/négociation que vous avez eue avec le fournisseur. Dès que c'est confirmé, une demande de devis est convertie en un ordre d'achat. La plupart des propositions d'ordres d'achat sont créées automatiquement par Odoo, basé sur les besoins de l'inventaire, notamment lorsque vous avez configuré les règles d'approvisionnement.

Ici, il faut noter que la demande de prix est fournie par le modèle **purchase.order**.

Autre chose, n'oubliez pas ce que l'on s'est dit la semaine dernière: *Vous faites un module personnalisé de gestion de bibliothèque, votre client ne doit faire aucune autre action. Il doit ouvrir son logiciel, aller sur son module et faire ses manipulations*, ce qui veut dire qu'il doit normalement éditer sa demande de prix sur le menu **MaLibrairie**.

Pour ce faire, nous allons procéder comme la dernière fois, c'est-à-dire faire apparaître le menu **Demande de prix** au niveau de **MaLibrairie**. Ceci dit, il suffit de créer un nouveau document XML qui contient ce code puis ajouter son chemin dans le fichier manifest.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <menuitem id="menu_oo_library_purchase_order" name="Demande de prix" parent="oo_library_menu_root" action="purchase.purchase_rfq"/>
</odoo>
```

Et donc, si jamais il arrive que vous ayez besoin d'ajouter ou modifier un champ, il suffira tout simplement de venir dans ce fichier, créer le `record form view` et hériter de la vue originale (XML ID: **purchase.purchase_order_form**).

Maintenant que tout est bon, on peut éditer notre demande de prix ou devis. Une fois le formulaire enregistré, vous pouvez alors **Confirmer la commande** (cliquer sur le bouton) et attendre que le fournisseur vous livre avant de réceptionner les articles dans votre stock (bouton **Réception par article**).

## L'entrée des produits en stock

Nous passons alors dans le module **stock** (Menu **Inventaire**).

![Module Inventaire](https://1.bp.blogspot.com/-zqLBMh5ffIE/XWaOrAgC35I/AAAAAAAADGA/ZCLhL5VW8R8vVNDL0hvmgdmXH2B3Lzh5wCLcBGAs/s320/module%2Binventaire.PNG)

Lorsque vous l'ouvrez, vous constatez qu'il y a deux éléments principaux (**Réceptions** et **Livraison**) sur la page. Les réceptions vous indiquent qu'il y a des produits en cours de réception (le fournisseur va les livrer) et les livraisons quant à elles indiquent les livraisons en cours que vous allez devoir écouler.

### Cependant, le seul élément qui nous intéresse pour le moment est **Réceptions**.

1. En cliquant sur le bouton **A recevoir**, vous obtenez une vue liste qui vous présente une ligne de transfert incluant la référence, le fournisseur (partenaire), la date de la commande, le document d'origine et l'état du transfert.
2. Cliquez sur cette ligne: le formulaire de réception va s'ouvrir. Tout ce que vous aurez à faire sera de **Valider** (en cliquant sur le bouton), puis **Appliquer** (en cliquant sur le bouton) et le tour est joué! Vous venez de faire entrer votre produit dans le stock.
3. Le menu **Mouvements de stocks** (premier menu après Valorisation de l'inventaire) vous montre les mouvements qui se sont produits. En ouvrant le formulaire, vous pourrez même accéder à l'emplacement où est stocké votre produit comme le montrent ces captures.

![Mouvement de stock](https://1.bp.blogspot.com/-tYOkorA5qa0/XWaSbbknqkI/AAAAAAAADGc/k-4wri7bCD4F9NRwV5i1l7lUEDxyLdA2wCLcBGAs/s320/mouvement%2Bde%2Bstock.PNG)

![Emplacement stock](https://1.bp.blogspot.com/-sIU2yRZ19M0/XWaSbTjpW-I/AAAAAAAADGY/vMxUhadSJTUkTtTDA5O3K-Cb-An_o41HwCEwYBhgL/s320/emplacement%2Bstock.PNG)

Avant de terminer, je vais vous donner un petit exercice pour vous aider à assimiler ce que l'on a vu aujourd'hui:

1. Afficher le menu **Transferts en cours** dans **MaLibrairie**. Ce menu doit afficher les transferts en cours.
2. Afficher le menu **Emplacements** dans **MaLibrairie**.

Sur ce,
A+!
