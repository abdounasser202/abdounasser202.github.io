---
layout: post
title: Comment développer une extension Flask et rendre son projet web Python plus fun
description: Guide pour développer une extension Flask et améliorer vos projets web Python.
permalink: /developper-extension-flask
author: Nasser
date: 2020-06-14 12:11:00 +0200
tags: [Flask, Python, développement web]
---

![Téléchargement](https://1.bp.blogspot.com/-8_X0s5jT_oU/XuYM3EZCfyI/AAAAAAAADlQ/cynHcBPTYJs5dLQxSixMDAKegqqpLaNDACK4BGAsYHg/t%25C3%25A9l%25C3%25A9chargement.png)

Hello! Si vous utilisez le [framework Flask](https://flask.palletsprojects.com/) pour vos projets web en Python, cet article pourrait très bien vous être utile. En effet, je vous explique comment développer une extension Flask.

## Tout d'abord, c'est quoi une extension?

Tous les frameworks connaissent des extensions ou plugins. **Il s'agit en effet de packages ou librairies qui viennent se greffer à votre application pour en ajouter des fonctionnalités qui n'y existent pas par défaut.** L'un des exemples que je pourrais vous proposer est le cas des [extensions Chrome](https://chrome.google.com/webstore/category/extensions). Nous les utilisons tous sur nos navigateurs. Chacun d'entre nous a peut-être déjà installé une extension qui permet de faire des captures d'écran à partir de son navigateur. Vous noterez aussi que les frameworks populaires comme [Laravel](https://laravelcm.com/) et [Django](https://www.djangoproject.com/) possèdent aussi leurs magasins d'extensions. Vous pouvez utiliser [GeoDjango](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/) pour ajouter un système de cartographie à votre application, [Laravel Notify](https://github.com/mckenziearts/laravel-notify) pour afficher des notifications dans votre application.

## Du coup, Flask n'est pas en reste

**Flask est un microframework c'est-à-dire qu'il vient avec le strict minimum dont votre application web aura besoin.** Il s'agit entre autres d'un système de routage et d'un système de gestion de template. Un tel framework ne vient pas par défaut avec un système d'authentification ou un système de gestion d'utilisateurs.

[Armin Ronacher](https://twitter.com/mitsuhiko), lorsqu'il a développé ce framework en 2010, s'était fixé l'objectif de mettre sur pied un framework simple qui ne tiendrait que sur un seul fichier. Le développeur serait alors libre d'en faire ce qu'il veut et d'y ajouter ce qu'il veut, sans aucune contrainte à travers des extensions.

Aujourd'hui, Flask, tout comme les autres frameworks, a un large éventail d'extensions parmi lesquelles:

1. [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) pour connecter l'ORM SQLAlchemy et les BD SQL à votre application.
2. [Flask-Login](https://flask-login.readthedocs.io/en/latest/) pour la gestion des authentifications.
3. [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/) pour faciliter le développement des interfaces administrateurs.
4. [Flask-Mail](https://pythonhosted.org/Flask-Mail/) pour l'envoi des mails via SMTP.
5. [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) pour la gestion des formulaires et le chargement des fichiers.

> *En utilisant les extensions, vous multipliez votre productivité par 10 et contrôlez les éléments qui constituent votre application. Elle n'est pas belle la vie ?*

Vous pouvez vous aussi créer vos propres extensions et éviter de recréer la roue d'un projet à l'autre. Imaginez un peu : vous travaillez sur un projet e-commerce avec Flask. Vous développez une extension pour le paiement par mobile money, puis une autre pour la page produit, une autre pour le blog. Lorsque vous gagnez un second client, tout ce que vous aurez à faire sera de réutiliser ces extensions et d'y ajouter quelques fonctionnalités à cette dernière en fonction des besoins de ce client. Vous pourrez aussi faciliter leur maintenance dans le temps et gagnez hautement en termes de productivité. Vous aurez ainsi mis sur pied un système modulaire qui pourra s'adapter à différents types d'architectures.

## Comment développer une extension Flask ?

### 1. Comment se présente une extension Flask ?

Je vous présente d'abord cette capture :

![Sélection_001](https://1.bp.blogspot.com/-2YlwgQeHt8s/XuX-n3f2XgI/AAAAAAAADkk/kQynd6mZnUsEK5Y-a1VP2KPu3SGhcVexQCK4BGAsYHg/S%25C3%25A9lection_001.png)

Cette capture est l'illustration parfaite de l’architecture d'une extension Flask. Elle est constituée de 2 fichiers principaux :

1. **setup.py** : il s'agit du fichier de configuration qui est utilisé pour installer votre extension.
2. **__init__.py** : le fichier d'initialisation de l'extension qui peut aussi contenir toute sa logique.

Les autres fichiers et dossiers sont juste là pour vous permettre de respecter quelques standards de développement, par exemple le modèle MVC.

### 2. Ce que vous devez absolument savoir lorsque vous mettez en place votre extension

1. L'extension Flask est toujours mise dans un dossier appelé **Flask-NomExtension** ou **NomExtension-Flask**.
2. Ce dossier doit contenir votre extension proprement dite qui sera nommée **flask_nom_extension**.
3. Votre extension doit être publiée sous une licence permissive (**BSD** ou **MIT**).

### 3. Un peu de pratique : développons Flask-Simple ensemble !

Il s'agit d'une simple extension qui affiche une petite phrase, un truc assez simple pour vous permettre de comprendre ce que j'explique.

#### D'abord notre setup.py

```python
from setuptools import setup

setup(
    name='Flask-Simple',
    version='1.0',
    url='https://github.com/abdounasser202/Flask-Simple',
    license='BSD',
    author='Nasser',
    author_email='nasser@example.com',
    description='A simple Flask extension',
    py_modules=['flask_simple'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
```

Dans ce fichier, on définit le nom de l'application, sa version, ses dépendances, etc.

#### Ensuite notre __init__.py

Il s'agit du contenu de notre extension proprement dite. On peut l'organiser de telle sorte qu'on puisse appeler des objets à partir des modèles (dossier **models**) et afficher les vues à partir du dossier **views**.

```python
from flask import Blueprint

class Simple:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.register(app)

    def register(self, app):
        simple_page = Blueprint('simple_page', __name__,
                               template_folder='templates')

        @simple_page.route('/hello/<name>')
        def hello(name):
            return f"Hello {name}"

        app.register_blueprint(simple_page)
```

1. Tout d'abord, je commence par importer la classe [Blueprint](https://flask.palletsprojects.com/en/1.1.x/blueprints/) : `from flask import Blueprint`. La classe Blueprint de Flask est un objet qui permet d'avoir des applications modulaires. En effet, chaque Blueprint a ses propres modèles, ses propres vues et ses propres routes.
2. Ensuite, je définis la classe **Simple** qui contiendra la logique de mon extension.
3. Dans la méthode **__init__()**, j’instancie mon extension à travers la méthode **init_app()**. **init_app()** va permettre d'enregistrer mon Blueprint à travers la méthode **register()**.
4. Dans la méthode **register()**, j'initialise mon Blueprint et utilise la fonction **add_url_rule()** qui prend en paramètre la route et la fonction qui sera exécutée lorsque cette route est appelée.

On peut maintenant obtenir une extension Flask qui affiche Hello `<name>` lorsque j'accède à la route `/hello/<name>`. Par exemple, `/hello/nasser` affichera `Hello nasser`.

Vous pouvez accéder au code entier de cette petite extension sur GitHub à l'adresse [https://github.com/abdounasser202/Flask-Simple](https://github.com/abdounasser202/Flask-Simple).

Je vous propose également de lire la documentation officielle sur le développement des extensions ici : [https://flask.palletsprojects.com/en/1.1.x/extensiondev/](https://flask.palletsprojects.com/en/1.1.x/extensiondev/).

## Conclusion

Ça fait plusieurs années que je développe souvent avec Flask et lorsque [j'ai découvert Odoo](../2018/2018-09-18-odoo-cest-quoi-au-juste.md), j'ai été ébloui par sa modularité parce que sur Odoo, [il y a un module pour tout](https://apps.odoo.com/apps), on peut hériter et modifier tout ce qu'on veut. Alors je me suis dit : pourquoi ne pas utiliser la même logique sur Flask en exploitant la puissance des Blueprints ? C'est alors que j'ai commencé à me documenter dans le but de comprendre comment cela fonctionne et je vous assure que [cet article de Bruno Rocha](http://brunorocha.org/python/flask/flask-google-maps-plus-how-to-write-a-flask-extension.html) m'a été d'une grande aide. C'est alors que j'ai décidé de partager avec vous le peu que j'ai appris.

Si vous avez des remarques et suggestions, les commentaires sont ouverts !
