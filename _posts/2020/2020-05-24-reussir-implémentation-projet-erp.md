---
layout: post
title: Réussir ou échouer l'implémentation de votre projet ERP - ce qu'il faut savoir, ce qu'il ne faut pas faire
description: Conseils et bonnes pratiques pour réussir l'implémentation d'un projet ERP.
permalink: /reussir-implémentation-projet-erp
author: Nasser
date: 2020-05-24 12:11:00 +0200
tags: [ERP, gestion de projet, informatique]
---

![Group of people watching on laptop](https://1.bp.blogspot.com/-_w4lShp4pJI/Xsm55LWlMDI/AAAAAAAADdI/2kDZnIA0kQYA41iWkFIHH-9HDJyM4FTRQCK4BGAsYHg/s320/group-of-people-watching-on-laptop-1595385.jpg)

J'ai travaillé dans l'implémentation de pas mal de projets ERP depuis 2016 : certains se sont soldés par des échecs et d'autres par des réussites. Mais qu'est-ce qui fait en sorte qu'un projet ERP échoue ou réussisse ? Dans cet article, je partagerai quelques éléments avec vous basés sur mon expérience et mes lectures.

## Tout d'abord, sachez que même le géant SAP a échoué des projets d'implémentation ERP

Oui oui, vous avez bien lu ! Parfois même les géants se trompent. Il y a quelques mois, je suis tombé sur [cet article](https://www.lemondeinformatique.fr/actualites/lire-15-deploiements-d-erp-defaillants-ou-calamiteux-1ere-partie-76710.html) et je vous assure que je n'arrivais pas à comprendre ce qui se passait sous mes yeux. Avais-je des hallucinations ou bien était-ce vrai ? Quelques instants plus tard, je me suis ressaisi et j'ai compris que je n'était pas si nul. En fait, j'étais victime du [syndrome de l'imposteur](https://fr.wikipedia.org/wiki/Syndrome_de_l%27imposteur) et je m’interrogeais sur l'avenir du projet sur lequel je travaillais en ce moment. D'ailleurs, c'est pendant cette période que j'ai créé ce blog. Allais-je le réussir ou échouer ce projet sur lequel je travaillais ? Qu'est-ce que je n'avais pas su comprendre ? Est-ce que j'étais nul ? Alors cet article-là me réconfortait. La semaine suivante, Google, grâce à sa merveilleuse intelligence artificielle, me proposait [cet autre article, la suite du premier](https://www.lemondeinformatique.fr/actualites/lire-15-deploiements-d-erp-defaillants-ou-calamiteux-2eme-partie-76711.html). C'est alors que j'ai ancré dans ma cervelle une bonne fois pour toutes que les projets ERP ne sont pas faciles à mettre sur pied.

## Qu'est-ce qui rend les projets ERP complexes jusqu'à ce qu'on puisse être victime de ce terrible syndrome de l'imposteur ?

### 1. L'environnement

Il ne s'agit ni plus ni moins que du client et du prestataire. Généralement, voici ce qui se passe au Cameroun :

1. Le client exprime son besoin sur un fichier Word de quelques pages. Les plus rusés se battent pour faire un cahier des charges. À ce niveau, la plupart ont déjà défini le prix du projet et sa durée. Par exemple, 1 million 200 FCFA, projet réalisable en 3 mois, au plus 4. Hahahaha !!! LOL !!!
2. Le prestataire reçoit l'offre : il doit absolument gagner ce marché sinon il ne pourra pas payer ses factures et les salaires. Le plus marrant, c'est que la majorité des prestataires vont essayer de répondre à l'offre en promettant ciel et terre au client. Ils vont lui proposer des fonctionnalités venues tout droit du futur avec des cas d'utilisations hyper-automatiques. Le but ? Augmenter l'enveloppe : on veut passer de 1 million 200 FCFA à 4 millions par exemple, le tout en 5 ou 6 mois pour la période de réalisation du projet. Le client est stupéfait par l'offre et accepte le deal.
3. J1 du projet : le chef de projet fait une analyse approfondie du projet. Ce dernier le termine en 2 semaines et demande de la ressource humaine. Il dit à son patron : *"Boss, ce projet est réalisable en 6 mois pour un rendement de 2 jour-homme"*. En d'autres termes, si nous avons un développeur, il fera le travail en 2 jours. Et donc si nous ajoutons un autre développeur, nous aurons 2 ressources pour 4 jours de travail et nous pourrons livrer le projet en 3 mois au lieu de 6. Dans les cas extrêmes, nous irons jusqu'à 5 mois de travail.
4. Le premier développeur est déjà là et travaille sur le projet. Il est plus ou moins expérimenté car il ne compte à son actif que 2 ans d'expérience. On recrute alors un junior, on lui donne un salaire de 90 à 100 mille par exemple. Il sort fraîchement d'école et arrive dans l'entreprise. Il a noté dans [son CV](2020-05-10-trouver-emploi-informatique-partie-2.md) qu'il adore travailler sous pression, [il est une rockstar](https://www.jesuisundev.com/tu-nes-pas-un-developpeur-rockstar/) parce qu'il a les premières notes en Algorithmique dans sa classe. Lorsqu'il arrive, il doit comprendre comment on travaille en équipe, comment utiliser Git, etc... Ils ont oublié [la loi de Brooks](https://fr.wikipedia.org/wiki/Loi_de_Brooks) qui stipule que rajouter une personne à un projet qui a déjà débuté peut ralentir sa réalisation.
5. Le boss se rend compte que le planning prévisionnel n'est pas respecté, que les tâches des sprints ne sont pas clôturées et commence à péter les plombs. Il met la pression sur son équipe : les gars font des heures supplémentaires, ils sont énervés tout le temps. Le client qui met la pression au boss : *"Le projet a déjà fait 3 mois et on n'a toujours aucun prototype"*. On décide alors de mettre en pré-production. Le client teste et ajoute de nouvelles fonctionnalités, le chef de projet les valide et demande à l'équipe de les implémenter, etc... Ça prend plus de temps, 8 mois le projet n'est pas terminé, le client est fâché, le boss a perdu beaucoup d'argent sur les ressources du projet et soudainement le projet s'arrête ! Échec total et [beaucoup d'argent dépensé pour rien](https://www.silicon.fr/echec-projet-sap-coute-345-millions-euros-dhl-131307.html).

### 2. Les faibles compétences

Les SSII au Cameroun ont tendance à recruter des juniors pour les mettre sur des projets de grande envergure, puisque cela leur permet de payer un salaire relativement bas. Or, ils sont sans ignorer que les juniors n'ont pas tous les mécanismes et la lucidité qu'il faut pour mener à bien un projet. Conséquences :

1. Le projet n'est pas passé à la loupe en vue d'obtenir une analyse pertinente.
2. L’architecture du projet est mal définie.
3. Le déroulement des phases du projet ne sont pas respectées.
4. La communication n'est pas fluide dans l'équipe projet.
5. Les difficultés techniques ne trouvent pas de bonnes solutions.
6. Les fonctionnalités ne sont pas bien testées.

### 3. L’ego de certains membres de l'équipe

Il y a des équipes dans lesquelles le chef de projet accueille le projet comme s'il s'agissait de son travail personnel. Il n'a de compte à rendre à personne, il accepte tout ce que le client lui dit, il donne des ordres aux développeurs sans comprendre le niveau de faisabilité d'une fonctionnalité sur le plan technique ou interpersonnel. Bref, il est le capitaine du bateau, le Christophe Colomb qui va les faire découvrir les Bahamas !

### 4. La réticence de certains acteurs à utiliser le logiciel

Parfois, une fois le projet mis sur pied, des clans se créent chez le client. Un service X qui a toujours été contre l'implémentation de la solution, un service Y dont le rôle est de dire que rien ne fonctionne et un service Z qui accueille favorablement la solution. C'est alors que les guerres de clans se déclenchent et l'équipe projet est tout au milieu, elle encaisse tout et cela affecte négativement le déroulement du projet.

## Dans ce cas, comment réussir l'implémentation d'un projet ERP ?

![Sélection_004](https://1.bp.blogspot.com/-OuqSSqSrrNs/XsnEgIhDJ7I/AAAAAAAADdk/a4YSfA-aa4soUuiESyUqVBXTi9lPBLbmwCK4BGAsYHg/s320/S%25C3%25A9lection_004.png)

Nous avons l'opportunité d'améliorer la vie des gens et d'augmenter leur productivité et leur épanouissement à travers les solutions que nous leur offrons. Ceci dit, il nous incombe de faire très bien notre travail et de minimiser au maximum les risques d'échecs.

Ayant pris conscience de cette lourde charge, j'ai décidé de me documenter et puis, je suis tombé sur cette brochure d'Odoo : [Comment implémenter Odoo](https://www.odoo.com/openerp_portal/static/src/pdf/odoo_implementation.pdf)? Je trouve ce guide très intéressant et indispensable à toute équipe projet spécialisée dans la mise en place de systèmes logiciels. Ceci dit, voici quelques pistes sur lesquelles vous pouvez vous appuyer pour réussir votre projet.

### 1. Bien définir les rôles

1. **Un chef de projet** : il a plusieurs casquettes et prend les décisions. En tant que chef de projet, il définit le planning du projet et les priorités, il anticipe sur les risques. Il peut aussi configurer le logiciel, décider comment implémenter certaines fonctionnalités, faire la migration de données. Malgré tout, il ne doit pas être hautain et doit accepter les idées des autres si elles sont bonnes.
2. **Le ou les développeurs** : ils sont spécialisés dans l'implémentation de la solution conformément aux exigences fonctionnelles et techniques. Ils ne rencontrent pas le client.
3. **L'expert fonctionnel** : il maîtrise tous les aspects du logiciel. Il comprend comment fonctionnent les inventaires, le marketing, etc... et peut à tout moment débloquer le développeur sur une question d’ordre fonctionnelle qui nécessite une implémentation technique.
4. **Le point de contact** : c'est l'intermédiaire entre le client et l'équipe projet. C'est le seul qui discute avec le client. Généralement, côté client, on aura aussi besoin d'un point de contact. Ceci permet d'éviter d'avoir plusieurs interlocuteurs qui vont se contredire sur un processus à mettre en place.

**Concernant les développeurs juniors**, l'idéal serait de les mettre dans une équipe de pros, leur déléguer de petites tâches et les suivre de plus près. D'autres parts, on se rend compte que les équipes de dev ne sont pas formées : la plupart se forme individuellement le week-end. Il faut savoir que nous sommes dans un domaine hautement compétitif qui évolue à la vitesse de la lumière. Pour cela, il est très important que les entreprises allouent un budget pour la formation de leurs équipes.

### 2. Les phases d'implémentation

Il est important de diviser son projet en phases distinctes comme suit :

| Phases | Temps | But |
|--------|-------|-----|
| Compréhension du projet | 10% | Comprendre les besoins du projet en termes de ressources humaines et matérielles, définir les étapes et le budget |
| Le démarrage | 5% | Définir la méthodologie de travail et les standards à appliquer |
| L'implémentation | 80% | Il s'agit du cycle de vie : analyse, conception, réalisation, tests |
| La pré-production | 5% | Premier déploiement, formation des utilisateurs, correction des bugs, traductions, droits et rôles |
| La mise en production | Variable | Mettre sur pied le système fonctionnel à disposition des utilisateurs |

### 3. Challenges à relever pour réussir

#### La conduite de changement : comment emmener les utilisateurs à embrasser votre logiciel ?

Il faut les convaincre et leur montrer que ce logiciel est là pour leur faciliter la vie. Pour cela, il faut les accompagner, les encourager.

#### Comment gérer les personnes résistantes ?

L'erreur que nous commettons souvent est de les éloigner et de ne pas les impliquer dans le projet. Normalement, il faut passer du temps à leur expliquer pourquoi une telle solution et comment elle en est arrivée là. Il faut les former. Leur montrer les bénéfices du projet, faites-leur des démos, résolvez leurs plus gros problèmes.

#### Pensez à garder les choses simples

Ne donnez pas trop d'options de configurations au client, par exemple.

Etc...

J'espère que cet article vous aura plu ! Si vous avez d'autres challenges, vous pouvez les partager avec nous dans les commentaires et nous dire comment les gagner !

A+
