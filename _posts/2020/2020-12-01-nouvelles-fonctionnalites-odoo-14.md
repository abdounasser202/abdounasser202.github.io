---
layout: post
title: Découvrir les nouveautés apportées à Odoo 14
description: Découvrez les nouveautés et améliorations d'Odoo 14.
permalink: /nouvelles-fonctionnalites-odoo-14
author: Nasser
date: 2020-12-01 12:11:00 +0200
tags: [tech, Odoo, Logiciel]
---

![Odoo 14](https://1.bp.blogspot.com/-Kpxstr3DaNA/X8YiyrtwMKI/AAAAAAAAEVk/bjY5yus2vUUP_jU-sSV4NC9xuJB4has0gCLcBGAsYHQ/s320/01-000-1-scrnli_12_1_2020_10-40-31%2BAM.png)

Hello world!

Cet article est dans mon placard depuis un bon bout de temps et j'avoue que j'ai eu la flemme d'écrire. Je n'arrive même pas à croire que [mon dernier article](2020-07-19-supprimer-vue-kanban-res-partner-odoo.md) remonte au mois de juillet 😅

*OK, passons aux choses sérieuses*

En octobre dernier, [Odoo](https://odoo.com) SA a dévoilé les nouveautés d'Odoo 14 lors du [Odoo Experience](https://www.odoo.com/fr_FR/event/odoo-experience-2020-2020-09-30-2020-10-01-2622/page/introduction-odoo-experience-2020-online), qui à cause de Mr Corona, s'est déroulé entièrement en ligne. D'ailleurs, j'ai suivi cet événement avec enthousiasme comme jamais auparavant, puisque [l'entreprise pour laquelle je travaille](https://bloopark.de) s'est bien organisée pour que tous les développeurs de la boîte puissent suivre l'événement en ligne.

J'avais alors pris mon petit cahier et noter quelques nouveautés du logiciel pour les publier ici immédiatement, mais la flemme a eu raison de moi. C'est aujourd'hui que j'ai décidé de le publier, après plusieurs semaines de rédaction 😆😆

## Quelles sont les nouveautés qui ont marqué mon esprit sur Odoo 14? Est-ce l'IA, ou bien React? Je vous dévoile toutes mes notes ici

### 1. La comptabilité

La vue liste est toute nouvelle: de nouveaux widgets ont été ajoutés vous permettant ainsi de faire directement ce que vous voulez accomplir. Vous avez l'affichage du statut des documents, l'affichage des activités que vous voulez exécuter comme par exemple passer un appel, consulter un détail, etc...

![Comptabilité](https://1.bp.blogspot.com/-izRtXcBOk7I/X8YiyYV1sDI/AAAAAAAAEWA/gWdVXyTCdg4xQBMAdR0YRslCaYSJpERFQCPcBGAYYCw/s320/01-account-1-scrnli_12_1_2020_10-40-31%2BAM.png)

L'IA et la gestion de documents: avec un taux de reconnaissance de 95,88%, vous pouvez scanner une facture physique et le système reconnaît tous les éléments de la facture et les enregistre automatiquement.

![Gestion de documents](https://1.bp.blogspot.com/-YFxfnNrdhs4/X8YiyP8nzpI/AAAAAAAAEV8/NclCTFGNmR0HvXKR5w1Rk6OFKVln_Tp2ACPcBGAYYCw/s320/01-account-2-scrnli_12_1_2020_10-40-31%2BAM.png)

À ce propos, je vous renvoie vers cette vidéo de présentation:

<iframe width="320" height="266" src="https://www.youtube.com/embed/z_ADEpQdtUo" frameborder="0" allowfullscreen></iframe>

### 2. Les documents

Avec Odoo, devenez une entreprise sans papier (paperless company) parce que vous pouvez désormais importer vos documents puis les séparer ou les fusionner directement sur Odoo. Vous pourrez alors classer vos documents par département et y assigner les droits d'accès.

![Documents](https://1.bp.blogspot.com/-P2x2WyoblTA/X8YizDl837I/AAAAAAAAEWI/QPLBqfXbz5QGGz5ydoKw9i04DgO-XF8CQCPcBGAYYCw/s320/01-document-1-scrnli_12_1_2020_10-40-31%2BAM.png)

Vous avez aussi accès à Odoo Spreadsheet qui est un MS Excel entièrement fonctionnel sur Odoo: il vous permet d'éditer le tableau croisé dynamique, d'y ajouter ou de supprimer des colonnes et enfin de l'exporter au format Excel.

![Odoo Spreadsheet](https://1.bp.blogspot.com/-_bVL4SC9vIU/X8YizqtHfXI/AAAAAAAAEWE/Fze8v0E8cnUQCQ9VY9EChfA82_2zdY_LgCPcBGAYYCw/s320/01-document-2-scrnli_12_1_2020_10-40-31%2BAM.png)

![Odoo Spreadsheet](https://1.bp.blogspot.com/-zSfO6AIglqY/X8YiziMbLtI/AAAAAAAAEWI/3-IOUk3oC0AGrC4plgyic9wWqMq8uiUbgCPcBGAYYCw/s320/01-document-3-scrnli_12_1_2020_10-40-31%2BAM.png)

Vous pouvez aussi créer de nouveaux documents à partir de templates prédéfinis

![Nouveaux documents](https://1.bp.blogspot.com/-PMDn64pW_jo/X8Yi0DcEP1I/AAAAAAAAEWM/uXbwnS6jWqclMCfqST8qBdoPnw5D3n2rgCPcBGAYYCw/s320/01-document-4-scrnli_12_1_2020_10-40-31%2BAM.png)

### 3. Data cleaning

Le module data cleaning permet de retirer tous les doublons de votre base de données et de fusionner des champs

![Data Cleaning](https://1.bp.blogspot.com/-70kurg6RmZ4/X8Yiy0bCiYI/AAAAAAAAEWE/Egv68cBArZogUt8u2L-rv9Au7NBfUpigQCPcBGAYYCw/s320/01-datacleaning-1-scrnli_12_1_2020_10-40-31%2BAM.png)

### 4. Le framework JS

[OWL](https://github.com/odoo/owl) (Odoo Web Library) est le nouveau framework JS d'Odoo. Basée sur la logique de web component, OWL est proche de React à quelques exceptions près :

1. L'utilisation du [Qweb template engine](https://github.com/odoo/owl/blob/master/doc/reference/qweb_templating_language.md) basé sur du XML: vos codes XML peuvent être stockés en base de données et modifiés dynamiquement avec des **xpath**.
2. Compilation des templates dans le navigateur, ce qui est bien si vous avez besoin de générer des interfaces utilisateur dynamiques dans le navigateur. Par exemple, un composant de la vue formulaire peut générer une interface utilisateur de type form (form view) spécifique pour chaque modèle, à partir de la vue XML.

En réalité, Odoo SA a développé son propre framework JS parce qu'il veut garder le contrôle de sa technologie et ne veut pas dépendre de Facebook par exemple, bien que React soit open source puisque React pourrait changer de licence ou de direction. Il faut aussi noter qu'Odoo n'est pas une application JavaScript classique, et que ses besoins sont différents de ceux de la plupart des autres applications en termes de réactivité et de modularité par exemple. Si vous voulez en savoir plus sur ces raisons, je vous invite à lire cet article: [Pourquoi OWL](https://github.com/odoo/owl/blob/master/doc/miscellaneous/why_owl.md).

Dans un prochain article purement technique, je vais aller un peu plus en détail à propos de OWL.

Découvrez toutes les nouveautés d'Odoo 14 ici: [Odoo 14 Release Notes](https://www.odoo.com/fr_FR/odoo-14-release-notes)

Je vous laisse sur cette jolie vidéo de présentation:

<iframe width="320" height="266" src="https://www.youtube.com/embed/1SMm2VHXv1Y" frameborder="0" allowfullscreen></iframe>

That's it, see you next time!
