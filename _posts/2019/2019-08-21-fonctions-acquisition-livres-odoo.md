---
layout: post
title: Mise en place des fonctions d'acquisition de livres
description: Apprenez à gérer les dépendances, les variantes de produits et à établir des liens entre deux modèles dans Odoo.
permalink: /fonctions-acquisition-livres-odoo
author: Nasser
date: 2019-08-21 18:17:00 +0200
tags: [Odoo, Développement, Gestion de bibliothèque]
---

Bonjour et bienvenue !

Dernièrement, je vous présentais comment implémenter les fonctionnalités de consultation des livres. En gros, il s'agissait d'écrire un modèle qui enregistre des livres et sur lequel on peut faire des éditions et des suppressions. [Vous pouvez consulter l'article en question ici !](https://blog.nasser.cm/2019/01/mise-en-place-des-menus-et-des-vues-du.html)

**Si vous êtes débutant et venez tout juste de nous rejoindre, [je vous invite plutôt à commencer ici !](https://blog.nasser.cm/p/apprendre-odoo.html)**

OK ! Aujourd'hui, nous allons **commencer la mise en place des fonctions d'acquisition des livres**. Pour vous permettre de comprendre, mettez-vous à la place d'un libraire qui, après avoir enregistré les livres qu'il va vendre dans sa bibliothèque, décide maintenant de les acquérir. Pour ce faire, il doit enregistrer ses produits ou articles (livres), puis ses fournisseurs. Ensuite, il devra passer par un bon de commande pour passer sa commande auprès du fournisseur avant de les recevoir dans son stock.

Maintenant, et si je vous disais qu'actuellement, Odoo me permet de faire cette opération, sans aucune difficulté, comme ça de manière native ? Et oui ! c'est vrai. Rien qu'en installant les modules Achats (**purchase**) et Inventaire (**stock**), je peux le faire.

*Vous allez me demander : mais pourquoi dois-je alors développer une telle fonctionnalité ?*

*Et à moi de vous répondre :*

1. Vous faites un module personnalisé de gestion de bibliothèque, votre client ne doit faire aucune autre action. Il doit ouvrir son logiciel, aller sur son module et faire ses manipulations.
2. Vous faites une intégration ERP ; et qui dit intégration ERP dit respect des procédures clients. Votre client vous demande de l'aider à exécuter les tâches qu'il fait tous les jours via son poste de travail.
3. L'ergonomie et la personnalisation. Odoo fait tout et vous devrez le personnaliser selon les besoins de votre client, rien de plus !

**J'en profite alors pour vous dire ce qu'on fera dans ce tutoriel :**

1. Permettre l'installation des modules Achats (**purchase**) et Inventaire (**stock**) lors de l'installation du module de gestion de librairie (**oo_library**).
2. Joindre les livres qui ont été enregistrés aux articles (**product.product**). J'en profiterai pour vous expliquer la différence qu'il y a entre les modèles **product.product** et **product.template**.

*Passons maintenant aux choses sérieuses.*

## 1. Comment installer les modules Achats (purchase) et Inventaire (stock) lors de l'installation de notre module ?

C'est simple. Ouvrez le fichier `__manifest__.py` qui présente les caractéristiques du module (dans un dictionnaire Python). Vous verrez qu'au niveau de la clé `depends`, il y a une liste comme ceci :

```python
'depends': ['base', 'sale_management', 'purchase', 'stock'],
```

Cette liste est la liste des modules dont dépend notre module personnalisé. Par conséquent, tous ces modules sont installés lors de l'installation du module `oo_library`. Ici, vous verrez les modules suivants :

- **base** : le noyau d'Odoo comportant les modèles avec **res** (*res.users, res.partners, etc...*), ainsi que plusieurs autres fonctionnalités (*suppression, création, modification, import, export, impression, etc...*) et l'affichage.
- **sale_management** : pour la gestion des ventes.
- **purchase** : gestion des achats.
- **stock** : gestion de stock.

## 2. Nous allons maintenant établir un lien entre les articles et les livres qui ont été enregistrés

Avant de continuer, notez d'abord cette différence entre les modèles **product.product** et **product.template** :

- Le modèle **product.product** contient tous les articles stockables qu'on peut manipuler. Ces articles peuvent être attribués à des variantes : on dit qu'il liste les variantes du produit.
- Le modèle **product.template**, lui, permet de contenir les informations qui sont identiques aux variantes.

En effet, il est possible sur Odoo de créer des variantes de produits. Par exemple, le produit **stylo** contient des variantes **stylo rouge** et **stylo bleu**. Du coup, *si vous créez un produit (Stylo) en utilisant le modèle product.template, le même produit (Stylo) sera créé au niveau du modèle product.product, vous permettant ainsi d'enregistrer les variantes rouges et bleues.*

### Comment activer les variantes de produits sur Odoo ?

C'est simple : vous pouvez utiliser les variantes de produit dans Odoo en activant **"Attributs et variantes"** dans le menu Ventes / Configuration.

![Activer les variantes de produits](https://1.bp.blogspot.com/-0vaSiAOwaNg/XV1Z5xwvIQI/AAAAAAAADEg/ncObsrvDbCkX9Q8u9azexH91UGxok_-zQCLcBGAs/s320/odoo-activer-variantes-produits.PNG)

Ainsi, comme on peut avoir plusieurs versions (tome) d'un même livre, nous allons plutôt créer un *product.template*.

Dans le dossier **views**, créez le fichier **oo_product_template.xml**. Ici, **oo** représente les initiales de mon module et **product_template** représente le modèle sur lequel je vais travailler.

> Pour que votre code soit propre et facile à maintenir, optez toujours pour la méthode un modèle pour un fichier.

Le but de cette section est de faire apparaître le menu **Articles** présent dans **Achats** au niveau de **MaLibrairie**. Pour cela, nous allons faire un héritage de vues.

### Comment hériter d'une vue sur Odoo ?

#### Il faut tout d'abord être capable de repérer le xml_id

En effet, le **xml_id** est l'élément qui identifie un composant (**action, menu, vue, etc...**) sur Odoo. Par exemple, pour repérer le xml_id de l'action qui va ouvrir le formulaire des Articles, voici la procédure à suivre et il en est de même ou presque pour tous les autres composants.

1. Activer le mode développeur.
2. Cliquer sur le menu en question (Menu Articles dans le module Achats).
3. Cliquer sur **Ouvrir les outils de développement** (il s'agit du petit insecte situé tout juste à côté de votre nom de profil à l'extrême droite).
4. Cliquer sur modifier l'action et noter la valeur de ID Externe (c'est le xml_id de l'action : **purchase.product_normal_action_purchased**).

![XML ID](https://1.bp.blogspot.com/-jcoizEcJe8w/XV1ctsM__JI/AAAAAAAADE4/8zkFMPu5obIm48ua2FUYBuUd5IbZzr-TACLcBGAs/s320/xml_id.PNG)

Maintenant, nous allons récupérer le xml_id de la vue (l'ID de la vue formulaire du menu Articles).

1. Cliquer sur le bouton **create**.
2. Cliquer sur **Ouvrir les outils de développement**.
3. Cliquer sur Modifier la vue formulaire et noter la valeur de l'ID externe (**product.product_template_only_form_view**).

![View Form XML ID](https://1.bp.blogspot.com/-H93MvB-rQW4/XV1dqSiKXmI/AAAAAAAADFA/TGQXzpbnMnYJ56Aw7wyS7diCRgnB0HmSgCLcBGAs/s320/view_form_xml_id.PNG)

On peut alors passer au code.

### Nous allons surcharger le modèle product.template (par héritage) et faire le lien avec nos livres présents dans le modèle oo.consultation

```python
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    oo_consultation_id = fields.Many2one(
        'oo.consultation',
        string="Livre",
        required=False,
    )
```

N'oubliez pas d'importer ce nouveau fichier dans le dossier `models/__init__.py`.

```python
from . import oo_product_template
```

Ensuite, nous allons surcharger la vue proprement dite et afficher le livre après le champ **Catégorie**.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="product_template_only_form_view_inherit" model="ir.ui.view">
        <field name="name">product.template.only.form.view.inherit</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_only_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='categ_id']" position="after">
                <field name="oo_consultation_id"/>
            </xpath>
        </field>
    </record>
</odoo>
```

N'oubliez pas d'inclure le fichier dans `__manifest__.py`.

```python
'data': [
    'data/menu.xml',
    'views/oo_consultation_view.xml',
    'views/oo_product_template.xml'
],
```

Je vais m'arrêter ici. Prenez la peine de mieux assimiler tout ce qui a été dit jusqu'à aujourd'hui.

Sur ce,
A+!
