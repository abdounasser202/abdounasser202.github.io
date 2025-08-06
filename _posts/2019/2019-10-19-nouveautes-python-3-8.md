---
layout: post
title: Découvrez les nouveautés de Python 3.8
description: Explorez les nouvelles fonctionnalités introduites dans Python 3.8.
permalink: /nouveautes-python-3-8
author: Nasser
date: 2019-10-19 20:45:00 +0200
tags: [Python, Programmation, Développement]
---

> Cet article a été publié en tant que [thread sur Twitter](https://twitter.com/eliaswalyba/status/1185540939361767425?s=20) par [Elias Walyba](https://twitter.com/eliaswalyba), data scientist et machine learner au Sénégal. Néanmoins, j'ai retouché quelques mots.

![Python Logo](https://www.python.org/static/img/python-logo.png)

Python 3.8 est sorti le 14 octobre dernier. Cette nouvelle version de Python vient avec quelques fonctionnalités plutôt intéressantes en termes de développement. Dans ce thread, je vous présente quelques-unes de ces fonctionnalités que j’ai eu à tester.

## 1/ L’opérateur de Walrus «:=»

Cet opérateur vous permet de faire des assignations de valeurs à des variables dans des expressions ou des blocs d’expressions. Son signe est `:=`. Il est très utile pour éviter de se répéter dans des structures de contrôle.

```python
# Le bout de code suivant (3.7):
if len(dataset) > 1000:
    print(f"moins de {len(dataset)} éléments attendus")

# Devient (3.8):
if (n := len(dataset)) > 1000:
    print(f"moins de {n} éléments attendus")
```

## 2/ Les paramètres «/» et «*» des fonctions

Cette version de Python introduit ce qu’ils appellent : **positional-only parameter** et qui se note `/`. Cette fonctionnalité permet de dire que certains paramètres d’une fonction (ou méthode) ne peuvent être passés que par position et pas par clé-valeur. Elle introduit aussi le **keywords only parameter** qui se note `*` qui lui permet de dire que certains paramètres ne peuvent être passés que par clé-valeur.

Dans la fonction suivante, `a` et `b` ne peuvent être passés que par position, `c` peut être à la fois passé par position et par clé-valeur, et `d` ne peut être passé que par clé-valeur.

```python
def func(a, b, /, c, *, d):
    pass

func(2, 5, c=40, d=1.7)
```

ou

```python
func(2, 5, 40, d=1.7)
```

**Cette fonctionnalité est très utile pour écrire du code avec le paradigme fonctionnel.**

## 3/ Ajout du signe «=» dans les f-strings

L’autre fonctionnalité super sympa de cette version c’est l’ajout du signe `=` dans les **f-strings** pour faciliter l’inspection de variable et la self-documentation.

La f-string suivante: `f"{expr=}"` produit la chaîne `"expr=valeur_de_expr"`.

Le code suivant:

```python
twitto = "@eliaswalyba"
age = 26
print(f"{twitto=} {age=}")
```

Produit:

```
twitto=@eliaswalyba age=26
```

**PS: On peut l’utiliser avec les formatages de f-strings pour plus de contrôle.**

```python
print(f'{theta=} {cos(radians(theta))=:.3f}')
# theta=30 cos(radians(theta))=0.866
```

## 4/ Plus de précision sur le typage

Avec l’introduction de types de données tels que:

- **Literal types**
- **Type dictionaries**
- **Final objects**
- **Protocols**

Python prend en charge les indicateurs de type facultatifs, généralement sous forme d'annotations sur le code:

```python
def double(number: float) -> float:
    return 2 * number
```

Dans cet exemple, `number` doit être un `float` et la fonction `double()` doit également renvoyer un `float`. Cependant, Python traite ces annotations comme des astuces. Ils ne sont pas appliqués à l'exécution:

```python
double(2)
# retourne 4

double("Dakar")
# retourne "DakarDakar"
```

Même si cela ne permet pas de faire de Python un langage à typage statique et fort, ça a une réelle importance pour les programmes de **type-checking** tels que **mypy** qui pourront l’utiliser pour faire du type-checking avant ou lors de l’édition.

Les types **Literal**, **Protocoles**, etc. sont accessibles via le package `typing`.

```python
from typing import Literal
```

## 5/ La fonction reversed() sur les dictionnaires

Depuis Python 3.7, les dictionnaires conservent l'ordre d'insertion des clés. Avec Python 3.8, `reversed()` peut maintenant être utilisé pour accéder au dictionnaire dans l'ordre inverse de l'insertion - exactement comme `OrderedDict`.

## 6/ L’unpacking avec return et yield

Depuis Python 3.2, l’unpacking des éléments itérables sans parenthèses dans les instructions `return` et `yield` est interdit:

```python
# interdit
def func():
    res = (4, 5, 6)
    return 1, 2, 3, *res

def func():
    res = (4, 5, 6)
    yield 1, 2, 3, *res
```

Les deux fonctions renvoient des `SyntaxError`.

Avec Python 3.8, ce problème a été corrigé et donc possible maintenant.

## 7/ Syntax Warning

Python 3.8 permet de faire des alertes en cas d’erreurs de syntaxe dans certains cas.

Le code suivant:

```python
data = [
    (1, 2, 3)  # absence de virgule
    (4, 5, 6)
]
```

Au lieu de générer l’erreur: `TypeError: 'tuple' object is not callable` qui est une horreur 😱🤯, vous avez maintenant une **Syntax Warning** qui vous dit que vous avez probablement oublié une virgule. C’est ce qui est beaucoup mieux pour le débogage.

Voilà, c’est tout ce que j’avais à partager avec vous concernant les nouvelles fonctionnalités de Python. Je suis sûr que vous allez les adorer 😍. Pour ma part, je ne les trouve pas très nombreuses, mais je pense qu’elles sont super utiles et arrivent au bon moment.

Pour plus de détails, vous pouvez consulter la documentation de Python dans la partie **Whatsnew** ou bien le blog **realpython**:

- [https://docs.python.org/3/whatsnew/3.8.html](https://docs.python.org/3/whatsnew/3.8.html)
- [https://realpython.com/python38-new-features/](https://realpython.com/python38-new-features/)

Merci à [Elias Walyba](https://twitter.com/eliaswalyba) sans qui cet article aurait été beaucoup moins sympa à lire!
