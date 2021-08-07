# CI_SentiDock

## Objectif

L'objectif est de crier un pipeline CI/CD pour tester une API. Nous allons nous placer dans la peau d'une équipe censé créer une batterie de test à appliquer automatiquement avant déploiement.

Dans ce scénario, une équipe a créé une application qui permet d'utiliser un algorithme de sentiment analysis: il permet de prédire si une phrase (en anglais) a plutôt un caractère positif ou négatif. Cette API va être déployée dans un container dont l'image est pour l'instant :
```
datascientest/fastapi:1.0.0
```
Les endpoints de cette API sont les suivants :
   - _**status**_: renvoie 1 si l'API fonctionne
  - _**permissions**_: renvoie les permissions d'un utilisateur
   - _**/v1/sentiment**_: renvoie l'analyse de sentiment en utilisant un vieux modèle
  -  _**/v2/sentiment**_: renvoie l'analyse de sentiment en utilisant un nouveau modèle

Le point d'entrée /`status` permet simplement de vérifier que l'API fonctionne bien. Le point d'entrée `/permissions` permet à quelqu'un, identifié par un `username/password` de voir à quelle version du modèle il a accès. Enfin les deux derniers prennent une phrase en entrée, vérifie que l'utilisateur est bien identifiée, vérifie que l'utilisateur a bien le droit d'utiliser ce modèle et si c'est le cas, renvoie le score de sentiment: -1 est négatif; +1 est positif.

L'API est disponible sur le port `8000` de la machine hôte. Une description détaillée des points d'entrée est disponible sur le point d'entrée /docs.

## Tests

Nous allons définir certains scénarios de tests qui se feront via des containers distincts.

### Authentication

Dans ce premier test, nous allons vérifier que la logique d'identification fonctionne bien. Pour cela, il va falloir effectuer requêtes de type `GET` sur le point d'entrée `/permissions`. Nous savons que deux utilisateurs existent `alice` et `bob` et leurs mots de passes sont `wonderland` et `builder`. Nous allons essayer un 3e test avec un mot de passe qui ne fonctionne pas: `clementine` et `mandarine`.

### Authorization

Dans ce deuxième test, nous allons vérifier que la logique de gestion des droits de nos utilisateurs fonctionne correctement. Nous savons que `bob` a accès uniquement à la `v1` alors que `alice` a accès aux deux versions. Pour chacun des utilisateurs, nous allons faire une requête sur les points d'entrée `/v1/sentiment` et `/v2/sentiment`: on doit alors fournir les arguments `username`, `password` et `sentence` qui contient la phrase à analyser.

### Content

Dans ce dernier test, nous vérifions que l'API fonctionne comme elle doit fonctionner. Nous allons tester les phrases suivantes avec le compte d'`alice`:
-  _life is beautiful_
-  _that sucks_

Pour chacune des versions du modèle, on devrait récupérer un score positif pour la première phrase et un score négatif pour la deuxième phrase. Le test consistera à vérifier la positivité ou négativité du score.

## Construction des tests

Pour chacun des tests, nous créons un container séparé qui effectuera ces tests. L'idée d'avoir un container par test permet de ne pas changer tout le pipeline de test si jamais une des composantes seulement a changé.

Le testeur se dispose de deux variables d’environnements. Si le variable **LOG** vaut 1, on imprime une trace dans un fichier `api_test.log`. Si **PRINT** vaut 1, on l'imprime sur la console.

Trois type de tests sont disponibles : _Authentication_, _Authorization_ et _Content_. Les trois types partagent la même structure, à savoir :

- Un fichier de la partie métier (**_authentication.py_**, **_authorization.py_** et **_content.py_**)
- Un fichier de configuration _**(config. py)**_ rassemblant l’essentiel des variables utilisés pour chaque type de test, e.g. _adresse de l'API, port, log file,_ etc.
- Un fichier _**database. py**_ contenant l'ensembles des utilisateurs _(users_database)_ et des phrases _(sentences_database)_ requises pour les tests.

## Redis

Pour une meilleure performance, les variables de configurations _(ainsi que les données des utilisateurs/phrases de test)_ sont sollicités depuis une base de donnée de type _**redis**_, avec les couples _**key/value**_ suivants :

- _**api_address :**_ adresse du serveur d'API
    
- _**api_port :**_ port de l'API
    
-  _**logfile :**_ nom du fichier de trace
    
-  _**volume :**_ nom du volume contenant le fichier de trace (dans notre cas api_test.py)
    
-  _**authentication_output :**_ un template de trace pour la partie authentification.
    
    _Exemple_ :
    ```
    ============================
         Authentication test_
    ============================
    request done at "/permissions"
         | username="alice"
         | password="wonderland"
    expected result = 200
    actual restult = {status_code}
    ==> {test_status}
    ```
- _**authorization_output, content_output,**_ i.e. des templates relatives aux tests d'autorisation et de contenu
- _**users :**_ l'ensemble des utilisateurs de test _(nécessaires pour les requêtes de test)_
- _**sentences**_ : l'ensemble des phrases de test (requise notamment lors des test de type "_content_")

A noter que _Redis_, par défault, ne supporte pas des structures de type _**nested_dictionnaries**_. Pour remédier à ce problème, on a diviser chaque base de donnée en deux parties, une englobant uniquement les logins _(e.g. "alice", "bob", etc)_ et l'autre listant les détails de chaque utilisateurs _(e.g. 'alice': {'password': "xxxx", 'v1': 1, 'v2': 1})_.

Le lancement du serveur se fait via un script shell _(start-redis.sh)_. Le fichier permet également d'insérer les données _(keys)_ vues précédemment via le client _redis-cli_ avec un fichier nommé _redis-dump.csv_ dont voici un extrait :

```
SET api_address 'sentiment'
SET api_port '8000'
...
```

### Docker Compose

On construira par la suite les images Docker via des DockerFile (fichiers présent à l'intérieur de chaque répertoire de test)

Pour une meilleure automatisation, on utilise _Docker Compose_ qui est un outil très utilisé pour les pipelines de CI/CD. Il nous permet de lancer nos différents tests d'un coup tout en facilitant le partage de données entre les différents tests. _docker-compose.yml_ est notre fichier qui organise ce pipeline.

Le fichier au final décrit cinq conteneurs (services), à savoir : _authentication, authorization, content_ ainsi que les deux derniers : _sentiment_ (serveur d'API) et _redis_ (base de donnée).

A noter les routines _**depends_on**_ et _**networks**_. La première assure le lancement des deux service (_sentiment et redis_) avant l'exécution des tests. La deuxième déclare et précise que l'ensemble de l'infrastructure est interconnectée via un réseau virtuel baptisé _**cicd_networkd**_

## Comming soon

Dans le cadre d'un déploiement en production, il se peut nécessaire d'ajouter _**l'authentification**_ au serveur _Redis_. Le stockage en clair des password est également à éviter. L'utilisation de la bibliothèque _**bcrypt**_ me semble un choix judicieux dans ce cas. 
