---
layout: post
title: Comment supprimer la vue Kanban sur le modèle res.partner dans Odoo
description: Découvrez comment supprimer la vue Kanban sur le modèle res.partner dans Odoo.
permalink: /supprimer-vue-kanban-res-partner-odoo
author: Nasser
date: 2020-07-19 12:11:00 +0200
tags: [dev, Odoo]
---

D'abord, il faut savoir que cette vue est affichée par ce code dans le module **base**:

## Définition des vues

```xml
<record id="base.action_partner_form" model="ir.actions.act_window">
    <field name="name">Customers</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">res.partner</field>
    <field name="view_type">form</field>
    <field name="view_mode">kanban,tree,form</field>
    <field name="context">{&quot;search_default_customer&quot;:1}</field>
    <field name="search_view_id" ref="base.view_res_partner_filter"/>
    <field name="help" type="html">
        <p class="oe_view_nocontent_create">
            Click to add a contact in your address book.
        </p><p>
            Odoo helps you easily track all activities related to
            a customer: discussions, history of business opportunities,
            documents, etc.
        </p>
    </field>
</record>
```

## Définition de l'action

```xml
<record id="action_partner_form_view1" model="ir.actions.act_window.view">
    <field eval="0" name="sequence"/>
    <field name="view_mode">kanban</field>
    <field name="view_id" ref="res_partner_kanban_view"/>
    <field name="act_window_id" ref="action_partner_form"/>
</record>
```

Maintenant, le principe est le suivant

## Supprimer l'action qui affiche le kanban

```xml
<delete model="ir.actions.act_window.view" id="base.action_partner_form_view1"/>
```

## Retirer le mode kanban dans les vues

```xml
<record model="ir.actions.act_window" id="base.action_partner_form">
    <field name="view_mode">tree,form</field>
</record>
```

Vous pouvez utiliser le même principe pour tout type de vue :)
