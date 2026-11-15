# Journal de bord — CampusCafé (Modou FALL)

## 22/10 — Lecture de l'énoncé, classe Produit
- Fait : lecture du sujet, tirage de la variante A3 + B1, classe Produit.
- Bloqué : j'avais mis des valeurs par défaut (prix=1.20), le plat du jour s'affichait à 1.2 €.
- Solution : suppression des valeurs par défaut, chaque produit reçoit ses vraies valeurs.

## Semaine 2 — Classe Client
- Fait : recharger, peut_payer, est_debiter, remise A3, fidélité B1.
- Bloqué : ma condition de recharge acceptait 150 € et 2 € ; le test du visiteur était après un return (jamais exécuté).
- Solution : correction du `and`, test du visiteur placé en premier.
- Bloqué : je retirais les 30 points trop tôt (avant le paiement).
- Solution : séparer « calculer l'avantage » et « ajouter les points » (règle tout ou rien).

## Semaine 3 — Commande et Cafeteria
- Fait : ajouter_ligne, __len__, __contains__, __iter__, ticket, traiter_commande, passer_commande.
- Bloqué : `return` dans la boucle de __iter__ ; "produit inconnu" impossible à détecter.
- Solution : `return iter(self.lignes)` ; passer_commande reçoit des codes et vérifie avec `in`.

## Semaine 4 — Rapport, scénario, tests
- Fait : rapport de clôture, scénario des 17 événements, 47 tests.
- Calculs à la main des événements 2, 6, 11 : identiques au programme.
- Bloqué : TypeError avec `values` sans parenthèses ; un remplacement global a cassé `reverse`.
- Solution : lecture du message d'erreur, correction



plus de fautes de frappes ....

## Utilisation de l'IA
J'ai utilisé Claude pour les bugs et les explications .
