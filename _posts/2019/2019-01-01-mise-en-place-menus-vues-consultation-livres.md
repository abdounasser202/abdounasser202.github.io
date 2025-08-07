---
layout: post
title: Mise en place des menus et des vues du module de consultation des livres
description: Découvrez comment mettre en place les menus et les vues pour le module de consultation des livres.
permalink: /mise-en-place-menus-vues-consultation-livres
author: Nasser
date: 2019-01-01 00:59:00 +0200
tags: [dev, Odoo, Installation]
---

Hello!

Dans [l'article précédent](../2018/2018-12-26-oolibrary-developpement-du-module-de.md), nous avons mis en place les modèles du module sur lequel nous travaillons en ce moment: **la consultation des livres**. En gros, nous allons à ce niveau développer nos vues XML et y joindre des menus. Maintenant, allons tout droit au but:

On définit l’architecture globale de nos vues dans le fichier **oo_library/views/oo_consultation_view.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <data>

  </data>
</odoo>
```

Par la suite, tout ce que nous allons écrire sera dans l'attribut `data`, sachant que l'attribut `xml` permet de définir l'encodage.

## Ensuite on écrit la vue formulaire pour obtenir ce résultat

| Vue formulaire avant enregistrement | Vue formulaire après enregistrement |
|------------------------------------|-------------------------------------|
| ![Vue formulaire avant enregistrement](https://1.bp.blogspot.com/--DFdshh2J68/XCqqquAeUkI/AAAAAAAAC1c/KpefF-vOmRAIyi2ee3P6uG0W66XmBZQCwCLcBGAs/s320/b1.png) | ![Vue formulaire après enregistrement](https://3.bp.blogspot.com/-WP5cX_5as9g/XCqqrlkUGvI/AAAAAAAAC1o/sP78UCUp5kgrvP5OASGzSK82jbi7Wl94gCLcBGAs/s320/b4.png) |

```xml
<record id="oo_consultation_view_form" model="ir.ui.view">
  <field name="name">oo.consultation.view.form</field>
  <field name="model">oo.consultation</field>
  <field name="arch" type="xml">
    <form string="">
      <sheet>
        <group>
          <field name="titre"/>
          <field name="auteur_id"/>
          <field name="genre_id"/>
          <field name="code_isbn"/>
        </group>
        <group>
          <field name="editeur_id"/>
          <field name="collection_id"/>
          <field name="resume"/>
        </group>
      </sheet>
    </form>
  </field>
</record>
```

**Petit commentaire:**

1. `<record id="oo_consultation_view_form" model="ir.ui.view">`: ici nous définissons l'ID de la vue qui sera stockée dans la table **ir.ui.view**.
2. `<field name="name">oo.consultation.view.form</field>`: on définit le nom de la vue; généralement pour faciliter le débogage, je préfère utiliser la nomenclature **oo.consultation.view.form** comme pour dire la vue formulaire du module consultation.
3. Pour la suite, nous définissons dans l’architecture **xml** un formulaire (**form**) dans lequel nous définissons une feuille (**sheet**) et les différents champs que nous allons disposer dans les attributs **group**. À ce niveau, il est important de noter que l'attribut **group** joue le rôle de la **div** de classe **row** sur **bootstrap**.

## Maintenant nous pouvons implémenter la vue tree qui fonctionne à peu près comme la vue form et on obtiendra ceci

| Vue tree avant enregistrement | Vue tree après enregistrement |
|------------------------------|-------------------------------|
| ![Vue tree avant enregistrement](https://3.bp.blogspot.com/-drYrYlfyQAc/XCqqq1SEItI/AAAAAAAAC14/32546IsiQ4k60J5G8eQVBM0jiQr6GJ3qQCEwYBhgL/s320/b2.png) | ![Vue tree après enregistrement](https://2.bp.blogspot.com/-GB52IisnCrQ/XCqqsDAYq8I/AAAAAAAAC2A/M-vD_vSJKD4i-Nin0jcbeiMMUjI0fDllQCEwYBhgL/s320/b5.png) |

```xml
<record id="oo_consultation_view_tree" model="ir.ui.view">
  <field name="name">oo.consultation.view.tree</field>
  <field name="model">oo.consultation</field>
  <field name="arch" type="xml">
    <tree string="">
      <field name="titre"/>
      <field name="auteur_id"/>
      <field name="editeur_id"/>
      <field name="genre_id"/>
    </tree>
  </field>
</record>
```

## Nous définissons l'action qui sera liée au menu présenté ci-dessous

![Menu Bibliothèque dont module MaLibrairie](https://3.bp.blogspot.com/-oGjgmwDZXKg/XCqqqv8g6sI/AAAAAAAAC1w/8GY6PEmncNIdzArIC0lae8TaZ5BjLXR9gCEwYBhgL/s1600/b3.png)

### L'action

```xml
<record id="oo_consultation_action" model="ir.actions.act_window">
  <field name="name">Bibliothèque</field>
  <field name="type">ir.actions.act_window</field>
  <field name="res_model">oo.consultation</field>
  <field name="view_mode">tree,form</field>
  <field name="help" type="html">
    <p class="oe_view_nocontent_create">
      Créer vos livres
    </p>
    <p>
      Enregistrer toutes les informations relatives aux livres que vous souhaiter repertoriés
    </p>
  </field>
</record>
```

**Commentaire:**

1. `<record id="oo_consultation_action" model="ir.actions.act_window">`: on définit l'ID de l'action qui sera stocké dans la table **ir.actions.act_window**.
2. `<field name="name">Bibliothèque</field>`: le nom de l'action.
3. `<field name="res_model">oo.consultation</field>`: le modèle vers lequel pointe cette action.
4. `<field name="view_mode">tree,form</field>`: les vues que cette action devra ouvrir.
5. Et le reste sont des messages de présentation lorsque le modèle.

### Enfin le menu

```xml
<menuitem
  id="menu_oo_consultation"
  name="Bibliothèque"
  parent="oo_library_menu_root"
  action="oo_consultation_action"/>
```

Dans cette balise nous avons défini son **ID**, son nom (**name**), l'**ID de son parent** et l'**ID de l'action** qui sera exécutée.

## Mais où se trouve le menu parent me direz-vous?

Allez dans le fichier **oo_library/data/menu.xml** écrire le code suivant qui représente le menu principal du module

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <data>

    <menuitem name="MaLibrairie" id="oo_library_menu_root"/>

  </data>
</odoo>
```

Pour que tous vos changements soient pris en compte sur Odoo, allez dans le fichier **__manifest__.py** et ajoutez-y le chemin vers vos vues au niveau de la clé **data** comme suit:

```python
'data': [
  'data/menu.xml',
  'views/oo_consultation_view.xml'
],
```

Maintenant vous pouvez redémarrer votre instance et mettre à jour le module pour voir les changements qui ont été apportés. Désormais vous pouvez enregistrer tous vos livres favoris!

## En résumé:

1. Notez qu'il existe plusieurs vues XML sur Odoo (**tree**, **form**, **kanban**, etc...) Nous aurons l'occasion de revenir sur chacune de ces vues.
2. Chaque vue est définie dans un bout de code qui lui est spécifique.
3. Lors de l'implémentation d'une vue, il est important d'adopter des standards précis pour faciliter le débogage!

Si vous avez des questions ou des suggestions, n'hésitez surtout pas à les mettre en commentaire.

Sur ce, A+!
