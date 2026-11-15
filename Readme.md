# CampusCafé — Modou FALL

**Ma variante : axe A3 (Gros panier) — axe B1 (Points)**

- **A3 – Gros panier** : quand le total d'une commande atteint 8,00 €, les étudiants et les alternants ont −10 %, et tous les autres (personnel et visiteur) ont −5 %.
- **B1 – Points** : un titulaire de badge gagne 1 point par euro entier payé. Quand il a 30 points, sa commande suivante reçoit −2,00 € et on lui retire 30 points. Le visiteur n'a pas de badge, donc pas de points.

---

## Le projet en deux mots

C'est la caisse de la cafétéria du campus. Le programme connaît la carte et les clients. Il accepte ou refuse les commandes, applique la remise et la fidélité de ma variante, rejoue la journée de l'énoncé, puis affiche le rapport de clôture.

Tout est dans un seul fichier : `Fall_Modou_CampusCafee.py`.

## Comment le lancer

Il faut Python 3.10 ou plus, sans aucune bibliothèque à installer.

Depuis le dossier `gestion_cafeteria` :

```
python Fall_Modou_CampusCafee.py
```

Le programme fait deux choses, dans cet ordre :
1. il **rejoue la journée** (les 17 événements de la section 6) et affiche le rapport de clôture ;
2. il **lance les tests** (`unittest`) et affiche `OK` si tout passe.

Pour enregistrer la sortie du scénario dans un fichier :

```
python Fall_Modou_CampusCafee.py > sortie_scenario.txt
```

## Les quatre classes

- **Produit** : un article de la carte (code, nom, catégorie, prix, stock). Il sait dire s'il est disponible pour une quantité à une heure donnée, se vendre, se réapprovisionner, et se comparer aux autres produits (égalité par code, ordre par prix).
- **Client** : un client avec son profil, son solde et ses points. Il sait se recharger, dire s'il peut payer, être débité, et calculer sa remise A3 et son avantage fidélité B1.
- **Commande** : un numéro automatique, un client, une heure et des lignes `(produit, quantité)`. On peut faire `len(commande)` pour le nombre d'articles, `produit in commande` et `for ligne in commande`. Elle sait aussi s'afficher sous forme de ticket.
- **Cafeteria** : elle regroupe tout (la carte, les clients, le journal des commandes, les refus par motif). C'est elle qui traite les commandes, recharge les badges, réapprovisionne et produit le rapport.

## Mes choix, et pourquoi

**Les méthodes renvoient un résultat au lieu d'afficher.** Comme dans l'exercice `vendre` du cours, une méthode qui peut échouer renvoie un tuple `(réussi, message)`, par exemple `(False, "rupture de stock")`. C'est celui qui appelle la méthode qui décide quoi en faire. Seul le scénario utilise `print`.

**La règle du « tout ou rien ».** J'ai séparé les méthodes qui *regardent* ou *calculent* (`peut_payer`, `calculer_reduction`, `avantage_point_fidelite`) de celles qui *modifient* (`est_debiter`, `vendre`, `ajouter_points_fidelite`). Dans `traiter_commande`, je fais d'abord tous les calculs et toutes les vérifications. Je ne touche au solde, au stock, aux points et au journal **que si le paiement est possible**. Si une vérification échoue, rien n'a changé.

**Deux méthodes pour une commande.** `passer_commande` reçoit ce que le client demande au comptoir : une liste de `(code, quantité)`. Elle vérifie que chaque code existe et que chaque ligne est valide. Si tout est bon, elle passe la main à `traiter_commande`, qui calcule, encaisse et enregistre. Au premier problème, on compte le refus avec son motif et on s'arrête.

**Des dictionnaires pour retrouver vite.** Les produits sont rangés par **code** et les clients par **nom**. Comme ça, `self.produits["B01"]` donne directement le café. Les refus sont aussi un dictionnaire `{motif: nombre}`.

**Les constantes sont des attributs de classe.** Le plafond de recharge (150 €), le découvert du personnel (−10 €) et les taux de remise (10 % et 5 %) sont écrits une seule fois, dans la classe `Client`. Le numéro de commande vient d'un **compteur de classe** dans `Commande`.

**Les heures restent des chaînes `"HH:MM"`.** Elles se comparent directement, comme le dit l'énoncé : `"11:30" <= heure < "14:00"`. Le créneau des plats inclut 11:30 et exclut 14:00.

**L'ordre de calcul.** Total → remise A3 → avantage B1 → arrondi au centime. La remise A3 est calculée sur le total **avant** l'avantage fidélité. Les points sont ensuite calculés sur le montant réellement payé.

**Le rapport recalcule les ventes à partir du journal.** Au lieu de tenir un compteur de ventes à part, je parcours les commandes acceptées pour additionner les quantités par produit. Je trie ensuite avec `sorted` pour obtenir le top 3. La carte est triée avec `sorted` sur les produits directement, grâce à `__lt__` (ordre par prix).

**Le visiteur.** Il est enregistré comme un client de profil `"Visiteur"` : il paie comptant, donc son solde ne bouge pas, et il n'a ni recharge ni points. Il a quand même droit à la remise A3 de 5 %, parce qu'il fait partie des « autres ».

## Les tests

Il y a 47 tests `unittest`, à la fin du fichier, avec bien plus que 20 assertions. Ils couvrent les cas limites demandés :
- les heures 11:30 (acceptée), 13:59 (acceptée), 14:00 (refusée) et 11:29 (refusée) ;
- un solde exactement suffisant, et un centime de trop ;
- le découvert du personnel exactement à −10,00 €, et pas au-delà ;
- une recharge de 100,00 € (acceptée), de 100,01 € et de 4,99 € (refusées), et le plafond de 150 € ;
- un stock exactement suffisant, puis la rupture ;
- les seuils de ma variante : 7,99 € / 8,00 € pour la remise, 29 / 30 points pour la fidélité.

## Ce que je sais être imparfait

- **Une commande refusée consomme quand même un numéro.** La `Commande` est créée avant les vérifications, donc les numéros des commandes acceptées ne se suivent pas (1, 2, 4, 5, 7...).
- **L'avantage fidélité peut dépasser le total.** Si un client a 30 points et commande pour moins de 2,00 €, le montant devient négatif. Ce cas n'arrive pas dans le scénario de l'énoncé, mais il faudrait le bloquer à 0.

## Les autres fichiers

- `conception/` : le schéma des classes et les calculs à la main des événements 2, 6 et 11.
- `sortie_scenario.txt` : la sortie du programme sur la journée complète.
