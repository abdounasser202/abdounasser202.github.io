---
layout: post
title: Comment joindre un fichier sur Odoo
description: Découvrez comment joindre un fichier sur Odoo à partir de la vue form.
permalink: /joindre-fichier-odoo
author: Nasser
date: 2020-07-17 12:11:00 +0200
tags: [dev, Odoo]
---

Pour joindre un fichier sur Odoo à partir de la vue form, il suffit d'utiliser le champ `fields.Binary` pour sauvegarder le fichier en question et le champ `fields.Char` pour enregistrer le nom du fichier. Ensuite, vous pourrez les insérer dans votre vue form.

Voici un exemple illustratif

### Dans le modèle Python

```python
from odoo import fields, models

class ExempleFichier(models.Model):

    _name = 'exemple.fichier'

    fichier = fields.Binary(string="Joindre votre fichier", track_visibility="onchange")
    nom_fichier = fields.Char(string="Nom du fichier", track_visibility="onchange")
```

### Côté XML

```xml
<field name="fichier" filename="nom_fichier" widget="download_link" />
<field name="nom_fichier" invisible="1"/>
```
