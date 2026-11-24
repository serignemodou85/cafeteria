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

Il y a 47 tests `unittest` pour la version 1 (55 avec l'évolution v2.0), à la fin du fichier, avec bien plus que 20 assertions. Ils couvrent les cas limites demandés :
- les heures 11:30 (acceptée), 13:59 (acceptée), 14:00 (refusée) et 11:29 (refusée) ;
- un solde exactement suffisant, et un centime de trop ;
- le découvert du personnel exactement à −10,00 €, et pas au-delà ;
- une recharge de 100,00 € (acceptée), de 100,01 € et de 4,99 € (refusées), et le plafond de 150 € ;
- un stock exactement suffisant, puis la rupture ;
- les seuils de ma variante : 7,99 € / 8,00 € pour la remise, 29 / 30 points pour la fidélité.

## Ce que je sais être imparfait

- **Une commande refusée consomme quand même un numéro.** La `Commande` est créée avant les vérifications, donc les numéros des commandes acceptées ne se suivent pas (1, 2, 4, 5, 7...).
- **L'avantage fidélité pouvait dépasser le total** (un client à 30 points qui commande pour moins de 2,00 €). C'est corrigé : dans `traiter_commande`, l'avantage est limité au total avec `min(avantage_fidelite, total)`.

---

## Évolution v2.0 — annulation, rappel et rapport de crise

### Ce qui a été ajouté

- **Annuler une commande** : `Cafeteria.annuler_commande(numero)` renvoie le triplet `(annulée, motif, montant remboursé)`. Les motifs de refus sont `commande inconnue` et `commande déjà annulée`.
- **Rappeler un produit** : `Cafeteria.rappeler_produit(code)` renvoie `(réussi, motif, résumé)`. Le résumé contient le produit, les numéros des commandes annulées, la liste `(client, montant)` des remboursements et le total remboursé.
- **Le rapport de crise** : le chiffre d'affaires, les remises et le top 3 ne comptent plus que les commandes non annulées. Il affiche aussi le nombre d'annulations (dont celles dues au rappel), le total remboursé, et, pour chaque rappel, les clients remboursés triés par montant décroissant. Dans la carte, un produit rappelé est marqué « RAPPELÉ » au lieu de « ÉPUISÉ ».
- **Le scénario v2** : `jouer_scenario()` rejoue maintenant la journée avec les événements v2 insérés à leur heure. Sa sortie est dans `sortie_scenario_v2.txt`.

### Mes choix de conception

**Une commande garde ce qu'il faut pour être défaite.** Au moment du paiement, `traiter_commande` enregistre dans la commande le montant réellement payé (`paye`), la remise (`reduction`) et l'avantage fidélité (`avantage`). Ces valeurs n'existaient avant que pendant le calcul. Sans elles, on ne saurait pas combien rembourser.

**Un statut plutôt qu'une suppression.** Chaque commande a un attribut `statut` : `"en cours"` à sa création, `"acceptée"` après le paiement, `"annulée"` après une annulation. Une commande annulée reste dans le journal, comme demandé. C'est aussi ce qui empêche de l'annuler deux fois. Comme le journal garde tout, le rapport filtre selon le statut, au lieu d'utiliser `len(self.commandes)`.

**L'annulation respecte le « tout ou rien ».** `annuler_commande` fait d'abord toutes les vérifications (la commande existe, elle n'est pas déjà annulée) sans rien modifier. Ensuite seulement, elle passe le statut à `"annulée"`, remet le stock, rembourse et corrige la fidélité. Une fois les vérifications passées, aucune de ces étapes ne peut échouer.

**Un remboursement n'est pas une recharge.** Le badge est crédité directement (`client.solde += commande.paye`), sans passer par `recharger()`. Le plafond de 150 € ne s'applique donc pas. Un visiteur, qui a payé comptant, n'a pas de solde à modifier, mais son remboursement est bien compté dans `total_rembourse`.

**Le rappel réutilise l'annulation.** `rappeler_produit` ne réécrit ni le remboursement, ni le stock, ni la fidélité : il appelle `annuler_commande` pour chaque commande concernée. L'ordre suit la consigne. Le produit est marqué rappelé et son stock passe à 0 **avant** les annulations. Du coup, quand l'annulation essaie de remettre ce produit en stock, `reapprovisionner` le refuse, et il reste à 0, alors que les autres produits de la commande retournent bien en stock. Le journal est parcouru dans l'ordre, donc les annulations se font dans l'ordre chronologique. `produit in commande` utilise `__contains__`.

**Un produit rappelé est bloqué à la source.** `Produit` a un attribut `rappele`. `est_disponible` et `reapprovisionner` le vérifient en premier et renvoient `"produit rappelé"`. Comme `passer_commande` comptait déjà tous les motifs renvoyés par `ajouter_ligne`, le nouveau motif apparaît dans le rapport sans code supplémentaire. Pour le réapprovisionnement et le second rappel (`"déjà rappelé"`), j'ai ajouté une petite méthode `compter_refus(motif)`.

**Le rapport recalcule tout à partir du journal.** Le chiffre d'affaires et les remises sont la somme des `paye`, `reduction` et `avantage` des commandes non annulées. Il n'y a qu'une seule source de vérité : le journal.

### Le rejeu de la fidélité avec ma variante B1

La règle demande qu'après une annulation, les points du client soient ceux qu'on obtient en rejouant, dans l'ordre, ses commandes acceptées et non annulées, sans jamais recalculer le montant payé d'une autre commande.

**Où je l'ai placé :** le rejeu est partagé entre les deux classes qui détiennent chacune une partie de l'information.
- `Cafeteria` a le **journal** : c'est elle qui choisit les commandes à rejouer (celles de ce client, avec le statut `"acceptée"`, dans l'ordre du journal) et qui en extrait les montants payés.
- `Client` a la **règle** : la méthode `rejouer_fidelite(montants_payes)` remet les points à leur valeur de départ (`points_initiaux`, enregistrés dans `__init__`), puis appelle `ajouter_points_fidelite` sur chaque montant.

Je n'ai pas fait de fonction séparée, parce que la règle B1 existe déjà dans `ajouter_points_fidelite`. En la réutilisant, elle n'est écrite qu'**à un seul endroit** : si la règle change, le rejeu change avec elle.

**Comment ça se passe avec B1 :** pour chaque montant payé, si le client a au moins 30 points, on lui en retire 30, puis on ajoute 1 point par euro entier payé. Les montants payés ne sont jamais recalculés : un avantage de −2,00 € déjà obtenu reste acquis. Avec cette règle, les points ne peuvent pas devenir négatifs, puisqu'on ne retire 30 points que si le client en a au moins 30.

**Exemple (scénario v2, 12:25) :** Chloé annule sa commande de 12:18 (4,60 €). Avant, elle avait 13 points. Il ne reste qu'une commande acceptée : celle de 12:05, où elle a payé 9,54 €. Le rejeu donne 0 + 9 = **9 points**, exactement son état d'avant 12:18.

### Les tests ajoutés

8 tests d'annulation (55 tests au total) : annuler la dernière commande remet exactement le solde, le stock et la fidélité (avec un instantané avant / après) ; commande inconnue ; commande déjà annulée ; une annulation refusée ne modifie rien ; remboursement d'un visiteur ; remboursement qui fait dépasser 150 € ; annulation d'une commande qui avait utilisé l'avantage fidélité ; ticket d'une commande annulée.

---

## Les autres fichiers

- `conception/` : le schéma des classes et les calculs à la main des événements 2, 6 et 11.
- `conception/evolution/` : les calculs à la main des événements 12:18, 12:25 et 12:30 du scénario v2.
- `sortie_scenario.txt` : la sortie du programme sur la journée v1.
- `sortie_scenario_v2.txt` : la sortie du programme sur la journée v2.
- `JOURNAL.md` : mon journal de bord.
