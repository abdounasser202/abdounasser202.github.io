---
layout: post
title: oo_library, développement du module de consultation - mise en place du modèle
description: Apprenez à développer le module de consultation des livres dans Odoo, incluant l'implémentation des modèles pour enregistrer et visualiser les caractéristiques des livres.
permalink: /oo_library-developpement-du-module-de-consultation-mise-en-place-du-modele
author: Nasser
date: 2018-12-26 12:11:00 +0200
tags: dev
---

Bonjour ! Aujourd'hui, nous allons continuer notre apprentissage avec la mise en place du module de consultation des livres et notamment avec l'implémentation des modèles. Ce module vous permettra d'enregistrer et de visualiser l'ensemble des livres et l'ensemble de leurs caractéristiques : titre, auteur, genre, éditeur, collection, résumé, code ISBN.

Dans l'[article précédent](2018/12/presentation-dun-module-odoo-de-gestion.html), je vous expliquais les fonctionnalités du module que nous sommes en train de développer.

## Commençons par une brève modélisation du module

Grâce aux applications [Dia](http://dia-installer.de/) et [draw.io](https://www.draw.io/), j'ai conçu les diagrammes suivants qui nous permettront de développer notre module.

| ![Diagramme des cas d'utilisation](https://4.bp.blogspot.com/-RX1jXcIX4ik/XCKqyPMYn_I/AAAAAAAAC04/WiiskWOhQcgXBA4pDyTdpRaMEHvTjJGfACLcBGAs/s1600/use-case-consultation-livre.png) |
| Diagramme des cas d'utilisation |

Ce diagramme montre que l'utilisateur (ici le bibliothécaire) pourra enregistrer, consulter et rechercher des livres.

| ![Diagramme des classes](https://4.bp.blogspot.com/-7tKEFnvmzL8/XCKqyfMg5YI/AAAAAAAAC08/rSet_1PIecwlvila6Li3W8KZ71hIQZJZwCLcBGAs/s1600/class-diagram-consultation-livre.png) |
| Diagramme des classes |

Le module que nous allons mettre en place dans cette partie prendra en compte les tables suivantes :

- **oo_consultation** pour les caractéristiques du livre
- **oo_genre** pour le genre de livre (roman, thriller, etc...)
- **oo_editeur** ou bien **res_partner** pour la maison d'édition. Ici, il est à noter que le mieux serait d'utiliser res_partner pour enregistrer les informations de la maison d'édition. Le plus souvent, les erreurs que les gens commettent est de créer de nouvelles tables pour enregistrer des fournisseurs ou des clients pourtant Odoo met à notre disposition les tables res_users et res_partner pour ça. J'ai mis oo_editeur dans ce diagramme pour des besoins d'explications, mais je répète qu'en aucun cas vous ne devrez le mettre en place sauf si vous aimeriez qu'il soit un fils de la table res_partner comme on le verra plus loin.
- **oo_collection** pour l'enregistrement des informations sur la collection du livre (livre de poche, classique, etc...)
- Enfin, **res_partner** et **res_users** pour enregistrer respectivement les informations de l'éditeur et celles de l'auteur

## Passons maintenant au code source qui implémentera ce modèle

### Dans le dossier models, vous allez écrire le code suivant :

#### Fichier oo_collection.py

```python
# coding: utf-8

from odoo import fields, models

class OoCollection(models.Model):
    _name = 'oo.collection'
    _rec_name = 'name'

    name = fields.Char(string="Nom")
```

#### Fichier oo_genre.py

```python
# coding: utf-8

from odoo import fields, models

class OoGenre(models.Model):
    _name = 'oo.genre'
    _rec_name = 'name'

    name = fields.Char(string="Nom")
```

#### Fichier oo_consultation.py

```python
# coding: utf-8

from odoo import fields, models

class OoConsultation(models.Model):
    _name = 'oo.consultation'
    _rec_name = 'titre'

    titre = fields.Char()
    auteur_id = fields.Many2one(
        comodel_name='res.users',
        string='Auteur'
    )
    genre_id = fields.Many2one(
        comodel_name='oo.genre',
        string='Genre'
    )
    editeur_id = fields.Many2one(
        comodel_name='res.partner',
        string='Éditeur'
    )
    collection_id = fields.Many2one(
        comodel_name='oo.collection',
        string='Collection'
    )
    resume = fields.Text(string="Résumé")
    code_isbn = fields.Char(string='Code ISBN')
```

#### Fichier __init__.py

```python
from . import oo_collection
from . import oo_consultation
from . import oo_genre
```

**Notes importantes**

1. L'écriture du code `# coding: utf-8` permet de prendre en compte les accents dans le code source.
2. `_rec_name = 'titre'` affichera le titre du livre lorsque la page correspondante à ce livre sera ouverte.
3. Tous les fichiers Python devront être importés dans `__init__.py`.

#### Pour vérifier que votre code a été implémenté :

1. Redémarrez votre instance.
2. Activez le mode développeur.
3. Lancez Odoo sur votre navigateur.
4. Allez sur Configuration - Techniques - Structure de la base de données - Modèles.
5. Vous pouvez maintenant rechercher vos tables.

Je m'arrête ici pour aujourd'hui. Prenez tout votre temps pour assimiler cette partie et n'hésitez pas à me poser vos questions en commentaires.

Sur ce, à plus !
