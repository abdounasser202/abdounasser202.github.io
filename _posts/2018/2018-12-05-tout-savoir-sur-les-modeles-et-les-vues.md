---
layout: post
title: Odoo, Tout savoir sur les modèles et les vues
description: Apprenez à tout modifier sur Odoo en manipulant les modèles et les vues.
permalink: /odoo-tout-savoir-sur-les-modeles-et-les-vues
author: Nasser
date: 2018-12-05 12:11:00 +0200
tags: dev
---

Bonjour ! Aujourd'hui, nous allons passer aux choses sérieuses. Il s'agit ici d'un article très important qui fera de vous une personne **capable de tout modifier sur Odoo**. Oui, oui ! J'ai bien dit tout modifier car mettez bien dans votre tête qu'**avec Odoo, on peut tout faire** (Yvan Yelizariev) ! Je vous prie de vous concentrer et de faire les manipulations que je vais vous montrer ! En ce moment, ce que vous allez faire, c'est créer un module Odoo puis démarrer votre instance. Ensuite, **installez le module point_of_sale** et **cliquez sur le menu Products**. Le reste, on le fera ensemble !

## Passons à la manipulation des modèles

Les modèles représentent une abstraction de votre base de données à travers l'ORM d'Odoo. Dans un article précédent, je vous ai expliqué [comment fonctionnent les modèles](2018-09-18-odoo-cest-quoi-au-juste.md). Ici, je vais m'attarder sur leurs manipulations.

### Comment cibler un modèle sur Odoo ?

Le principe est simple :

Regardez au niveau de l'URL dans la barre d'adresse. En jetant un coup d'œil à cet URL (**localhost:8069/web?debug#id=334&view_type=form&model=product.product&menu_id=564&action=806**), on se rend compte que nous sommes sur le modèle **product.product**. Maintenant, considérons que vous voulez avoir le nom d'un champ dans le modèle.

### Comment faites-vous ?

Il suffit d'[activer le mode développeur](2018/11/installer-un-module-comprendre-les.html) et mettre le curseur sur le champ que vous désirez. Dans mon cas, je viens de mettre mon curseur sur le champ **Sale Price**, et les informations que je peux tirer de ce champ sont :

- **Field:** lst_price
- **Object:** product.product
- **Type:** float
- **Widget:** monetary
- **Modifiers:** Readonly, etc...

Je vous présente l'aperçu sur cette image :

[![Odoo Sale Price Field](https://4.bp.blogspot.com/-slZMds7L-LY/XAezGbCVfxI/AAAAAAAACyo/OIudcwiYohIqa4qcyuV9XHIBIxgVx-JmwCLcBGAs/s320/odoo1.PNG)](https://4.bp.blogspot.com/-slZMds7L-LY/XAezGbCVfxI/AAAAAAAACyo/OIudcwiYohIqa4qcyuV9XHIBIxgVx-JmwCLcBGAs/s1600/odoo1.PNG)

En d'autres termes, le champ **Sale Price** (**lst_price**) est un champ de la table **product_product** de type **réel**, donc le formatage est de type **devise**. Une autre information que je retiens est que ce champ est **accessible en lecture seule**. Dans un prochain article, nous reviendrons plus en détail sur l'accessibilité des champs.

OK, j'ai ciblé mon champ **Sale Price** et j'aimerais ajouter un tout nouveau champ que j'appelle **Earnings**, c'est-à-dire bénéfice. Comment je fais ?

On va utiliser le principe d'**héritage des classes**. Notez très bien que sur Odoo, il y a 3 mécanismes que l'on peut utiliser pour l'héritage des classes. Pour en savoir plus, [je vous renvoie sur cet article](2018/11/installer-un-module-comprendre-les.html). Passons maintenant à la rédaction de notre code pour ajouter notre champ personnalisé.

Vous allez commencer par créer votre module dans les règles de l'art avec un fichier `__manifest__` et des packages Python.

Créez le fichier **product_product.py** et insérez-y le code suivant :

```python
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    earnings = fields.Float(string="Earnings")
```

Après avoir enregistré votre fichier et redémarré votre serveur Odoo, le champ que vous venez de créer sera bel et bien présent dans votre BD. Pour vérifier, allez sur **Settings --> Technical --> Database Structure --> Models**. Tapez dans la barre de recherche **product.product**, sélectionnez votre modèle et déroulez un peu, vous verrez le champ "**earnings**".

## Nous pouvons alors passer à la manipulation de la vue pour positionner notre champ

Nous allons rester sur la même vue et allons positionner notre champ "**earnings**" **après le champ Sale Price**. Pour cela, vous devez rester en mode développeur, puis vous allez ouvrir votre vue et cliquer sur l'**icône représentant un petit "scarabé"**.

[![Odoo Edit View](https://3.bp.blogspot.com/-QFqEFtfFv1s/XAe0GcQHSPI/AAAAAAAACy0/nJ-CQa13SWAXx74L3e4rC5gOZUzJAULJgCLcBGAs/s320/odoo2.PNG)](https://3.bp.blogspot.com/-QFqEFtfFv1s/XAe0GcQHSPI/AAAAAAAACy0/nJ-CQa13SWAXx74L3e4rC5gOZUzJAULJgCLcBGAs/s1600/odoo2.PNG)

En déroulant, vous verrez le bouton "**Edit form view**" sur lequel vous cliquerez. La fenêtre suivante s'affichera.

[![Odoo Form View](https://4.bp.blogspot.com/-8zBHcNFYmjM/XAe0Ex2updI/AAAAAAAACyw/J9dRkEE3L_Ex4HK55lw4zbQD5DCN_uHKwCLcBGAs/s320/odoo3.PNG)](https://4.bp.blogspot.com/-8zBHcNFYmjM/XAe0Ex2updI/AAAAAAAACyw/J9dRkEE3L_Ex4HK55lw4zbQD5DCN_uHKwCLcBGAs/s1600/odoo3.PNG)

Regardez très bien les champs qui ont été surlignés en jaune : ces champs nous permettront de positionner notre champ personnalisé via l'**héritage des vues**. Oui, oui, vous avez très bien lu, il s'agit de l'**héritage des vues**. Tout à l'heure, nous avons parlé de l'héritage des classes.

### Il s'agit de quoi concrètement ?

En effet, **l'héritage des vues consiste à surcharger une vue dans le but d'ajouter, modifier, cacher ou changer le comportement d'un champ**. Les éléments principaux qui entrent dans l'héritage d'une vue sont l'**external ID qui représente l'ID de la balise XML où sera placé le nouveau champ et un champ cible à partir duquel notre champ personnalisé sera positionné**. Dans notre cas, j'ai surligné ces éléments en jaune.

Pour la suite, créez un document XML et ajoutez-y ce bout de code :

```xml
<record id="your_new_view_id" model="ir.ui.view">
    <field name="name">your_new_view_id.form</field>
    <field name="model">product.product</field>
    <field name="inherit_id" ref="product.product_normal_form_view"/>
    <field name="arch" type="xml">
        <field name="lst_price" position="after">
            <field name="earnings"/>
        </field>
    </field>
</record>
```

### Je vous propose ici un petit commentaire de ce code

- **ligne 1** : on déclare notre balise (record) et on lui affecte un ID unique
- **ligne 2** : on donne un nom à notre record
- **ligne 3** : on définit le nom du modèle sur lequel pointe notre record
- **ligne 4** : on définit l'ID de la vue qui sera surchargée.
- **ligne 6** : on indique où sera placé notre champ personnalisé. Dans notre cas, après (**after**) le champ **lst_price**
- **ligne 7** : on place notre champ proprement dit.

Mettez à jour votre module et admirez le fruit des efforts que vous avez fournis. Pendant ce temps, je vais aller bidouiller quelques packages sur Odoo !

Sur ce, à plus !
