## Aide-mémoire SQLite pour Python
[![Étoiles GitHub](https://img.shields.io/github/stars/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/stargazers)
[![Forks GitHub](https://img.shields.io/github/forks/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/network)
[![Problèmes GitHub](https://img.shields.io/github/issues/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/issues)
[![Licence GitHub](https://img.shields.io/github/license/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice)
[![Visites](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fimshakil%2Fpython-sqlite-practice)](https://imshakil.github.io/python-sqlite-practice/)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fimshakil%2Fpython-sqlite-practice)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fimshakil%2Fpython-sqlite-practice)

SQLite3 est un moteur de base de données très facile à utiliser. Il est autonome, sans serveur, sans configuration et transactionnel.
Il est très rapide et léger, et la base de données entière est stockée dans un seul fichier disque. Il est utilisé dans de nombreuses
applications comme stockage interne de données. La bibliothèque standard Python inclut un module appelé "sqlite3" destiné à
travailler avec cette base de données. Ce module est une interface SQL conforme à la spécification DB-API 2.0.

**Table des matières**
- [Module SQLite Python](#importer-le-module-sqlite)
- [Connexion et création de la base de données](#connexion-et-creation-de-la-base-de-donnees)
- [Créer et supprimer une table](#creation-create-et-suppression-drop-de-tables)
- [Insérer des données dans la table](#insertion-insert-de-donnees-dans-la-base-de-donnees)
- [Récupérer des données (SELECT FROM)](#recuperation-de-donnees-select-from-database)
- [Mettre à jour et supprimer des données](#mise-a-jour-update-et-suppression-delete-de-donnees)
- [Transactions SQLite](#utilisation-des-transactions-sqlite)
- [Gestion des exceptions SQLite](#exceptions-de-la-base-de-donnees-sqlite)
- [Fabrique de lignes SQLite](#fabrique-de-lignes-sqlite-et-types-de-donnees)

## Importer le module SQLite

```python
import random
import sqlite3
```


## Connexion et création de la base de données
Nous utilisons la fonction ```sqlite3.connect``` pour nous connecter à la base de données. Nous pouvons utiliser l'argument ```:memory:``` pour créer 
une base de données temporaire dans la RAM ou passer le nom d'un fichier pour l'ouvrir ou le créer.


```python
# créer une base de données en mémoire
# db = sqlite3.connect(':memory:')

# créer une base de données dans un répertoire
db = sqlite3.connect("./data/test.db")

# obtenir un objet curseur
cursor = db.cursor()
```


## Création (```CREATE```) et suppression (```DROP```) de tables
Pour effectuer une opération sur la base de données, nous devons obtenir un objet curseur et lui passer les instructions SQL pour les exécuter. 
Enfin, il est nécessaire de valider les modifications. Nous allons créer une table "users" avec les colonnes nom, téléphone, email et mot de passe.


```python
# Supprimer la table
cursor.execute("""DROP TABLE IF EXISTS users""")

# Créer la table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT unique,
                    password TEXT
            )"""
)

db.commit()
```

## Insertion (```INSERT```) de données dans la base de données
Pour insérer des données, nous utilisons le curseur pour exécuter la requête. Si vous avez besoin de valeurs provenant de variables Python, 
il est recommandé d'utiliser le caractère de remplacement "?". N'utilisez jamais d'opérations sur les chaînes ou de concaténation pour 
construire vos requêtes car c'est très peu sécurisé. Dans cet exemple, nous allons insérer deux utilisateurs dans la base de données, 
leurs informations sont stockées dans des variables python.

```python
name = 'Halim'
phone = "01234567890"
email = "halim@email.com"
password = "ha1234"
cursor.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (?,?,?,?)""",
    (name, phone, email, password),
)
db.commit()
```


Les valeurs des variables Python sont passées dans un tuple. 
Une autre façon de faire est de passer un dictionnaire en utilisant le caractère de remplacement ```:key name``` :

```python
name = "Alim"
phone = "01234567890"
email = "alim@email.com"
password = "al1234"
cursor.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (:name, :phone, :email, :password)""",
    {
        "name": name,
        "phone": phone,
        "email": email,
        "password": password,
    },
)
db.commit()

# utiliser une liste d'utilisateurs pour insérer plusieurs informations d'utilisateur
users = [
    (
        "Name " + str(i),
        str(random.randint(10000000, 1000000000)),
        "name" + str(i) + "@email.com",
        str(random.randint(10000, 90000)),
    )
    for i in range(10)
]

cursor.executemany(
    """INSERT INTO users(name, phone, email, password) VALUES (?, ?, ?, ?)""", users
)
db.commit()
```

### Obtenir l'ID de la dernière ligne

Si vous avez besoin d'obtenir l'ID de la ligne que vous venez d'insérer, utilisez ```lastrowid```

```python
print(f"ID de la dernière ligne : {cursor.lastrowid}")
```

## Récupération de données (```SELECT```) de la base de données
Pour récupérer des données, exécutez la requête sur l'objet curseur puis utilisez ```fetchone()``` pour récupérer une seule ligne ou 
```fetchall()``` pour récupérer toutes les lignes et ```fetchmany()``` pour récupérer un nombre particulier de lignes.
(note : les lignes récupérées sont sous forme de liste où chaque ligne est un tuple)

```python
cursor.execute("""SELECT name, phone, email FROM users""")
user1 = cursor.fetchone()
print(user1)

user_many = cursor.fetchmany(5)
print(user_many)

user_all = cursor.fetchall()
print(user_all)
```

L'objet curseur fonctionne comme un itérateur, invoquant ```fetchall()``` automatiquement

```python
cursor.execute("""SELECT name, email, phone FROM users""")
for row in cursor:
    print(f"nom : {row[0]} email : {row[1]} téléphone : {row[2]}")
```

Pour récupérer des données avec des conditions, utilisez à nouveau le caractère de remplacement "?"

```python
user_id = 5
cursor.execute("""SELECT name, email, phone FROM users WHERE id=?""", (user_id,))
print(cursor.fetchone())
```

## Mise à jour (```UPDATE```) et suppression (```DELETE```) de données
La procédure pour mettre à jour ou supprimer des données est la même que pour insérer des données

```python
# mettre à jour le téléphone de l'utilisateur avec id = 5
cursor.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01710567890", user_id))
db.commit()

# supprimer la ligne de l'utilisateur avec id = 8
cursor.execute("""DELETE FROM users WHERE id = ?""", (8,))
db.commit()
```

## Utilisation des transactions SQLite
Les transactions sont une propriété utile des systèmes de base de données. Elles garantissent l'atomicité de la base de données. 
Utilisez la méthode ```commit()``` pour enregistrer les modifications et la méthode ```rollback()``` pour annuler toute modification 
apportée à la base de données depuis le dernier appel à commit.

```python
# mettre à jour le téléphone de l'utilisateur avec id = 5
cursor.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01712567890", user_id))
db.rollback()
```

N'oubliez pas de toujours appeler commit pour enregistrer les modifications. Si vous fermez la connexion en utilisant close 
ou si la connexion au fichier est perdue (par exemple si le programme se termine de manière inattendue), les modifications non 
validées seront perdues.


## Exceptions de la base de données SQLite
Pour de meilleures pratiques, entourez toujours les opérations de base de données d'un bloc try ou d'un gestionnaire de contexte.

```python
try:
    # créer ou se connecter à la base de données
    db = sqlite3.connect("./data/test.db")

    # obtenir un objet curseur
    cursor = db.cursor()

    # vérifier si une table 'users' existe ou non et la créer
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT unique, password TEXT)"""
    )
    # valider pour enregistrer les modifications
    db.commit()

except Exception as e:
    # annuler toute modification si quelque chose ne va pas
    db.rollback()
    raise e
finally:
    db.close()
```

### Vérifier l'erreur d'intégrité
Nous pouvons utiliser l'objet Connection comme gestionnaire de contexte pour valider ou annuler automatiquement les transactions

```python
name1 = "Mobarak"
phone1 = "3366858"
email1 = "imshakil@github.com"
# Un mot de passe très sécurisé
password1 = "12345"
try:
    db = sqlite3.connect("./data/test.db")
    with db:
        db.execute(
            """INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)""",
            (name1, phone1, email1, password1),
        )
except sqlite3.IntegrityError:
    print("Les données existent déjà")
finally:
    db.close()
```

Dans l'exemple ci-dessus, si l'instruction insert lève une exception, la transaction sera annulée et le message sera affiché ; 
sinon, la transaction sera validée. Veuillez noter que nous appelons execute sur l'objet db, et non sur l'objet curseur.


## Fabrique de lignes SQLite et types de données 
Le tableau suivant montre la relation entre les types de données SQLite et les types de données Python :

- Le type None est converti en NULL
- Le type int est converti en INTEGER
- Le type float est converti en REAL
- Le type str est converti en TEXT
- Le type bytes est converti en BLOB

La classe de fabrique de lignes ```sqlite3.Row``` est utilisée pour accéder aux colonnes d'une requête par leur nom au lieu de leur index.

```python
db = sqlite3.connect("./data/test.db")
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute("""SELECT name, email, phone FROM users""")
for row in cursor:
    print(f"nom : {row[0]}, email : {row[1]}, téléphone : {row[2]}")

# fermer la connexion à la base de données
db.close()
```

> Merci à Andres Torres pour son excellent article de blog <br> 
> Source : https://www.pythoncentral.io/introduction-to-sqlite-in-python/
