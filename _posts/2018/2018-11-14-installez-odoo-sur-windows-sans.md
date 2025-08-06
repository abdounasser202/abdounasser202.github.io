---
layout: post
title: "Installez Odoo 8 sur Windows sans utiliser le .exe"
description: "Guide détaillé pour installer Odoo 8 sur Windows en mode développeur sans utiliser l'installateur exe. Configuration complète avec Python, PostgreSQL et environnement virtuel."
permalink: /installez-odoo-8-sur-windows-sans-utiliser-exe
author: Nasser
date: 2018-11-14 12:11:00 +0200
tags: [dev, odoo, windows, python, postgresql, développement]
image: "/assets/images/odoo8-windows-banner.jpg"
---

Salut !

Aujourd'hui je vais vous montrer comment installer Odoo sur Windows sans utiliser le fichier **.exe**. Avec cette procédure, vous pourrez développer des modules Odoo simplement comme si vous étiez sur un environnement Linux. 

L'exemple que je présente ici concerne **Odoo 8.0** qui fonctionne avec la version **9.4** de PostgreSQL. La même procédure peut être utilisée pour les versions les plus récentes d'Odoo.

## Prérequis système

- Windows 7/8/10 ou plus récent
- Droits administrateur
- Connexion internet stable
- Au moins 2 GB d'espace disque libre

## Étape 1 : Installation des composants de base

### Base de données et outils de développement

1. **Installez [PostgreSQL 9.4](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)** 
   - Notez bien le mot de passe du superutilisateur
   - Gardez le port par défaut (5432)

2. **Installez [Git](https://git-scm.com/downloads)**
   - Sélectionnez "Git from the command line and also from 3rd-party software"

3. **Installez [PgAdmin 4](https://www.pgadmin.org/download/pgadmin-4-windows/)**
   - Interface graphique pour gérer PostgreSQL

## Étape 2 : Configuration des variables d'environnement

### Ajout de PostgreSQL au PATH

1. Ouvrez les **Propriétés système** → **Variables d'environnement**
2. Ajoutez le répertoire **bin** de PostgreSQL à votre **PATH** :
   ```
   C:\Program Files\PostgreSQL\9.4\bin
   ```

## Étape 3 : Installation de Python et dépendances

### Python et gestionnaire de packages

4. **Installez [Python 2.7](https://www.python.org/downloads/)**
   - ⚠️ **Important** : Cochez "Add Python to PATH" lors de l'installation

5. **Installez [pip](https://bootstrap.pypa.io/get-pip.py)**
   ```cmd
   python get-pip.py
   ```
   Puis ajoutez `C:\Python27\Scripts` à votre **PATH**

6. **Installez [virtualenv](https://virtualenv.pypa.io/en/latest/)**
   ```cmd
   pip install virtualenv
   ```

## Étape 4 : Outils de compilation et rendu

### Compilateur et générateur PDF

7. **Installez le [compilateur Microsoft Visual C++ pour Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)**
   - Nécessaire pour compiler certaines dépendances Python

8. **Installez [Wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)**
   - Pour la génération de rapports PDF dans Odoo

### Node.js et préprocesseurs CSS

9. **Installez [NodeJS](https://nodejs.org/en/download/) LTS**
   Puis installez les packages requis :
   ```cmd
   npm install -g less less-plugin-clean-css
   ```

## Étape 5 : Configuration de la base de données

### Création de l'utilisateur Odoo

10. **Créez l'utilisateur odoo dans PostgreSQL**
    
    Ouvrez PgAdmin et exécutez :
    ```sql
    CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';
    ```

## Étape 6 : Installation et configuration d'Odoo

### Création de l'environnement virtuel

11. **Installez et exécutez Odoo 8.0**

    Ouvrez l'invite de commande et tapez :

    ```cmd
    # Créer un environnement virtuel
    virtualenv odoo-env
    
    # Activer l'environnement virtuel
    odoo-env\Scripts\activate
    
    # Cloner Odoo 8.0
    git clone --single-branch -b 8.0 https://github.com/odoo/odoo.git
    
    # Naviguer dans le dossier Odoo
    cd odoo
    
    # Installer les dépendances
    pip install -r requirements.txt
    ```

### Structure des dossiers recommandée

```
votre-workspace/
├── odoo-env/           # Environnement virtuel
├── odoo/              # Code source Odoo
├── custom-addons/     # Vos modules personnalisés
└── config/           # Fichiers de configuration
```

## Étape 7 : Lancement d'Odoo

### Commande de démarrage

```cmd
# Depuis le dossier odoo, avec l'environnement virtuel activé
python odoo.py -w odoo -r odoo --addons-path=addons,../custom-addons --db-filter=mydb
```

### Paramètres de la commande :
- `-w odoo` : nom d'utilisateur de la base de données
- `-r odoo` : mot de passe de la base de données  
- `--addons-path` : chemins vers les modules (séparés par des virgules)
- `--db-filter` : filtre pour les bases de données

## Configuration avancée

### Fichier de configuration (optionnel)

Créez un fichier `odoo.conf` :

```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = addons,../custom-addons
```

Puis lancez avec :
```cmd
python odoo.py -c odoo.conf
```

## Accès à l'application

Une fois lancé, ouvrez votre navigateur et accédez à :
- **URL** : `http://localhost:8069`
- **Base de données** : Créez une nouvelle DB ou connectez-vous à une existante
- **Login par défaut** : admin / admin

## Développement de modules

Maintenant que vous avez installé Odoo, vous pouvez le personnaliser et développer toutes sortes de modules que vous voulez.

### Structure d'un module basique :

```
custom-addons/
└── mon_module/
    ├── __init__.py
    ├── __openerp__.py
    ├── models/
    ├── views/
    └── security/
```

## Dépannage courant

### Problèmes fréquents :
- **Erreur de compilation** : Vérifiez que Visual C++ est installé
- **Module non trouvé** : Vérifiez votre PATH et l'activation du virtualenv
- **Connexion DB échouée** : Vérifiez que PostgreSQL est démarré et accessible

## Conclusion

Cette installation manuelle vous donne un contrôle total sur votre environnement de développement Odoo. Vous pouvez maintenant créer, modifier et tester vos modules personnalisés facilement.

Sur ce, à bientôt !

## Ressources utiles

- [Documentation Odoo 8.0](https://www.odoo.com/documentation/8.0/)
- [Guide de développement Odoo](https://www.odoo.com/documentation/8.0/howtos.html)
- [PostgreSQL sur Windows](https://www.postgresql.org/docs/9.4/tutorial-install.html)