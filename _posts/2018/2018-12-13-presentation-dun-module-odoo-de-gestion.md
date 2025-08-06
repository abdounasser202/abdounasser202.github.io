---
layout: post
title: Présentation d'un module Odoo de gestion de bibliothèque, comment développer un tel module?
description: Apprenez à développer un module Odoo de gestion de bibliothèque, incluant des modèles et vues personnalisés, des rapports et des workflows.
permalink: /presentation-module-odoo-gestion-bibliotheque-comment-developper-un-tel-module
author: Nasser
date: 2018-12-13 12:11:00 +0200
tags: dev
---

Bonjour ! Aujourd'hui, nous allons continuer notre apprentissage d'Odoo en passant par la phase pratique. Nous allons ensemble **développer un module de gestion de bibliothèque** et donc le code source sera disponible sur un serveur Git. **Le module que nous mettrons en place fera intervenir les modules de gestion de stocks, achats et ventes**. Nous implémenterons entre autres **des modèles et vues personnalisés, des rapports et des workflows**. Bref, ce module vous donnera toutes les techniques et méthodes dont vous aurez besoin pour devenir un développeur Odoo chevronné.

## Commençons par la présentation du module

Le module que nous mettrons en place permettra de :

- Visualiser l'ensemble des livres : livres acquis ou à acquérir, lu ou à lire... et l'ensemble de leurs caractéristiques : titre, auteurs, genre, éditeur, collection, résumé, code ISBN
- Gestion des fournisseurs, achat et approvisionnement du stock
- La possibilité de trier par genre, par auteur, par collection, par éditeur,...
- La recherche des ouvrages suivant divers critères
- Une gestion ultra simple des emprunts (emprunteur, date de prêt) ainsi que la vente
- L'impression sous forme de fiches individuelles ou de tableaux
- L'export des données vers Excel

En gros, nous aurons :

1. Les **fonctions de consultation**
2. Les **fonctions d'acquisition** (suggestions d'achat, des commandes et de la réception des documents, du pré-catalogage, et des fournisseurs).
3. Les **fonctions de gestion des périodiques imprimés** : gestion des abonnements et des états de collection, bulletinage des numéros reçus ; cette fonction est étroitement liée au module acquisitions pour tout ce qui concerne la gestion des abonnements.
4. Les **fonctions de contrôle bibliographique** : gestion de la description des collections (incluant la description des documents, des exemplaires, des entités dites d'autorités, etc.), notamment par import ou catalogage manuel;
5. Les **fonctions de circulation** : gestion des prêts, des prolongations de durée de prêt, des réservations et commandes de documents par les utilisateurs, des retards (relances, suspensions ou amendes pour les lecteurs en retard), des données d'utilisateurs
6. Les **fonctions de statistiques** : génération de rapports sur l'utilisation du système et les données qu'il contient

## Prérequis

Pour être en mesure de mettre en place ce module, vous devez au préalable avoir lu, compris et pratiqué le contenu d'au moins 6 des 7 premiers articles de cette série d'apprentissage d'Odoo à savoir :

1. [Présentation de l’ERP Odoo](2018/09/odoo-cest-quoi-au-juste.html)
2. [Installer Odoo sur Linux](https://formation-odoo.blogspot.com/2018/09/apprendre-odoo.html)
3. [Installer Odoo sur Windows](2018/11/installez-odoo-sur-windows-sans.html)
4. [Bonnes pratiques à suivre](2018/11/les-bonnes-pratiques-suivre-lorsquon.html)
5. [Création, sauvegarde, suppression et restauration d’une BD](2018/11/comment-creer-sauvegarder-supprimer-et.html)
6. [Installer un module, comprendre les modèles Odoo et activer le mode développeur](2018/11/installer-un-module-comprendre-les.html)
7. [En savoir plus sur les modèles et les vues](2018/12/tout-savoir-sur-les-modeles-et-les-vues.html)

Ensuite, avoir des connaissances basiques sur le fonctionnement de Git et GitHub (optionnel)

## Passons à la création de notre module

Nous allons commencer par l'architecture de notre module qu'on appellera **oo_library (Odoo for library)**. Ici, il faut noter que :

- **oo_library est le nom technique du module**, c'est-à-dire qu'il sera le nom de notre dossier ;
- **Odoo for library est le nom proprement dit du module**.

Ainsi, je vous propose ici la structure de notre module, suivi d'une brève explication.

![Structure du module oo_library](https://2.bp.blogspot.com/-cUN_EK6n8u8/XBI12k4cfnI/AAAAAAAACzU/HwW2jY94eFAhpPwN7G23vGnqa9WOURZ_ACEwYBhgL/s1600/oo_library_struct.PNG)

Dans le dossier **oo_library** (notre module), nous avons :

### Les dossiers :

- **data** : c'est ici que toutes les données statiques sont conservées (menus, crons, données à exporter, etc...)
- **models** : le répertoire qui contiendra tous nos modèles Odoo
- **reports** : le code de tous nos rapports (documents à imprimer) sera ici
- **security** : pour la conservation de toutes les règles de sécurité
- **views** : c'est ici que nous allons coder toutes nos vues XML
- **wizard** : toutes les fenêtres popups (modales) seront à ce niveau

### Puis les fichiers :

- **README.md** : un fichier markdown pour la description du projet
- **__manifest__.py** : un fichier obligatoire qui permet à Odoo de reconnaître qu'il s'agit d'un module qui lui est destiné.

Enfin, je vous propose ci-dessous le contenu de notre manifest qui parle de lui-même :

```python
# coding:utf-8

{
    'name': 'Odoo for library',
    'version': '0.1',
    'category': 'Warehouse',
    'description': """
    Odoo for library
    Odoo module for library management.

    Features
    - Consulting functions
    - Acquisition functions (purchase suggestions, orders and receipt of documents, pre-cataloging, and suppliers).
    - The functions of management of printed periodicals: management of subscriptions and states of collection, reception of numbers received; this function is closely related to the acquisitions module for everything related to subscription management.
    - Bibliographic control functions: management of the description of the collections (including the description of documents, copies, so-called authorities entities, etc.), particularly by manual import or cataloging;
    - Circulation functions: loan management, loan extensions, user bookings and orders, delays (reminders, suspensions or fines for late readers), user data
    - Statistics functions: reporting on the use of the system and the data it contains
    """,
    'author': 'Votre Nom',
    'email': 'votre_email@gmail.com',
    'website': 'https://www.siteweb.com/',
    'depends': ['base', 'sale_management', 'purchase', 'stock'],
    'data': [
        # 'data/menu.xml', # not yet ready
        # 'views/library_view.xml' # not yet ready
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

Maintenant, je pense qu'on devrait s'arrêter à ce niveau : prenez le temps de mieux comprendre ce dont il s'agit et posez-moi toutes vos questions.

Sur ce, à plus !
