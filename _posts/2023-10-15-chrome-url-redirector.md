---
layout: post
title: URL Redirector, mon extension chrome pour activer la redirection d'URL
description: Extension chrome pour redirection URL - pourquoi et comment ?
permalink: /dev/extension-chrome-redirection-url
author: Nasser
date: 2023-10-15 02:40:00 +0200
tags: dev
image: screenshot.png
---

## Pourquoi ?

Depuis 2 ans, j'ai décidé de contrôler mon expérience en ligne et éliminer le flot d'informations 
que je reçois sur les RS.

Fatigué d'être submergé par toutes ces publications, j'ai pris des mesures radicales : 

> 📵 j'ai désinstallé tous les RS de mon téléphone et n'y accède que sur PC à partir d'un navigateur. 

Je suis même allé jusqu'à supprimer mes comptes et fais un an sans Twitter de février 2022 à février 2023.

J'étais très actif sur ce RS mais dernièrement, je suis devenu passif : je consomme plus de contenu que je n'en 
produit.

Ensuite, j'étais vexé par le fil d'actualité qui ne faisait que m'afficher du contenu 
qui ne m'intéresse pas. J'ai alors créé une liste privée dans laquelle j'ai ajouté des personnes avec 
qui je partage les mêmes intérêts, mais cela n'étais pas suffisant.

C'est alors que j'ai décidé de développer une extension chrome qui me redirige vers ma liste chaque fois 
que j'ouvre Twitter.

![screenshot](/images/screenshot.png)

## 🛠️ Comment ça marche ?

L'idée est toute simple : j'enregistre l'URL d'origine et l'URL de destination et le tour est joué. 
Chaque fois que j'ouvre l'URL d'origine, en l'occurrence twitter.com, je suis immédiatement redirigé vers 
l'URL de ma liste.

Je peux l'étendre à GitHub, à [Peef](https://peef.dev) ou à tout autre site.

> 🌟 Des extensions similaires existent mais je voulais en profiter pour 
> me frotter au développement d'extensions Chrome et comprendre comment ça fonctionne

## Au final

J'ai acquis des bases pour le développement d'extension chrome et j'ai résolu mon problème.

💡 Désormais, lorsque j'ouvre Twitter, l'extension **URL Redirector** me redirige
directement vers ma liste soigneusement élaborée !

Actuellement, l'extension est en bêta et n'est pas encore sur le chrome webstore, mais il est disponible 
sur GitHub à l'adresse [github.com/abdounasser202/url-redirector](https://github.com/abdounasser202/url-redirector)

**🚀 Maintenant, place au contenu que j'adore et aux conversations qui me tiennent à cœur**

