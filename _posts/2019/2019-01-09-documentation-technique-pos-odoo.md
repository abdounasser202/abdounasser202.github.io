---
layout: post
title: Documentation technique du POS Odoo - versions 10 à 13
description: Découvrez comment prendre en main rapidement l'API JS d'Odoo pour modifier le module POS.
permalink: /documentation-technique-pos-odoo
author: Nasser
date: 2019-01-09 10:12:00 +0200
tags: [dev, Odoo, POS]
---

![POS Screen](https://1.bp.blogspot.com/-oFidk51NJGw/X8Uba5Jos2I/AAAAAAAAEVI/TeOSoC1z4d8-GFKBSAXPpep3G_BxDJ9jgCLcBGAsYHQ/s320/1-pos-scrnli_11_30_2020_5-16-06%2BPM.png)

Hello world!

Dans cet article, je vous montre brièvement comment prendre en main rapidement l'API JS d'Odoo des versions 10 à 13 notamment pour modifier le module POS. Je vais compléter cet article au fur et à mesure et parlerai de l'architecture des composants JS du POS, les composants (Widgets) eux-mêmes, les interactions entre les composants et la communication avec le back-end.

⚠ **Attention!** Avant de développer une fonctionnalité, je vous recommande de chercher si cette dernière n'a pas été implémentée par la communauté. Vous pouvez chercher ici:

- [OCA POS GitHub](https://github.com/OCA/pos/tree/11.0)
- [ITPP Labs POS Addons GitHub](https://github.com/itpp-labs/pos-addons/tree/11.0)
- [Odoo Apps - Point of Sale](https://apps.odoo.com/apps/modules/category/Point%20of%20Sale/browse)

## Commençons avec un peu de pratique

Nous allons mettre sur pied un module qui bloque ou désactive un bouton dans le POS Odoo. Il s'agit du bouton qui permet d'appliquer la remise au niveau du point de vente que voici (encadré en rouge):

![Discount Button](https://1.bp.blogspot.com/-VxXXnTtoAbs/X8UblgLbvEI/AAAAAAAAEVM/-5g0Wzd4vB4dFNzI5uV-40kzc3bTMSSawCLcBGAsYHQ/s320/2-pos-scrnli_11_30_2020_5-18-19%2BPM.png)

Nous allons appeler ce module **pos_disable_discount** et voici son architecture:

```
odoo-custom/
  pos_disable_discount/
    static/
      src/
        js/
          disable_discount_btn.js
    views/
      templates.xml
    __init__.py
    __manifest__.py
```

### 1. On définit le contenu du fichier `__manifest__.py`

```python
{
    'name': 'POS disable discount',
    'category': 'Point of Sale',
    'version': '1.0.0',
    'depends': ['point_of_sale'],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
```

### 2. Après avoir créé le fichier `disable_discount_btn.js` dans le dossier `/static/js`, il faut le charger dans le fichier `templates.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <data>
    <template id="assets" inherit_id="point_of_sale.assets">
      <xpath expr="." position="inside">
        <script type="text/javascript" src="/pos_disable_discount/static/src/js/disable_discount_btn.js"/>
      </xpath>
    </template>
  </data>
</odoo>
```

### 3. Définir le module dans `disable_discount_btn.js`

```javascript
odoo.define('disable_discount_btn', function(require) {
    'use strict';
});
```

### 4. Importer le widget natif que nous allons modifier

Le bouton que nous allons désactiver se trouve au niveau du widget `screens.NumpadWidget` et c'est pourquoi nous allons importer le module screens.

```javascript
odoo.define('disable_discount_btn', function(require) {
    'use strict';

    var screens = require('point_of_sale.screens');

});
```

### 5. Nous pouvons maintenant apporter nos changements dans la fonction `renderElement()` afin qu'elles soient appliquées au chargement du Widget

```javascript
screens.NumpadWidget.include({

    renderElement: function() {
        this._super();
        this.$el.find('.mode-button[data-mode="discount"]').prop('disabled', true);
    }

});
```

Pour en savoir plus, vous pouvez vous rendre sur ce document: [Odoo POS Development Documentation](https://odoo-development.readthedocs.io/en/latest/dev/pos/)
