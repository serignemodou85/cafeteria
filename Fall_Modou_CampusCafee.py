class Produit:
    """Classe représentant un produit du campus café."""

    def __init__(self,code, nom, categorie, prix, stock):
        self.code=code
        self.nom = nom
        self.categorie = categorie
        self.prix = prix
        self.stock = stock
        self.rappele= False


    def __repr__(self):
        return f"Produit({self.code!r}, {self.nom!r}, {self.categorie!r}, {self.prix}, {self.stock})"

    def __str__(self):
        return f"{self.nom} - {self.prix:.2f} € - Stock : {self.stock} - Catégorie : {self.categorie} - Code : {self.code}"
    


    def est_disponible(self, quantite, heure):
        """permet de vérifier si le produit est disponible en stock et si la quantité demandée est disponible et le creneau horaire est respecté pour les plats"""
        if self.rappele is True :
            return False, "produit rappelé"
        if quantite <= 0:
            return False,"quantité invalide"
        if quantite > self.stock:
            return False,"rupture de stock"
        if self.categorie == "plat":
            if not ("11:30" <= heure < "14:00"):
                return False,"hors créneau"
        return True ,"produit disponible"
    
    def vendre(self, quantite):
        """permet de vendre une certaine quantité du produit"""
        if quantite <= 0:
            return False,"quantité invalide"
        if quantite > self.stock:
            return False,"rupture de stock"

        self.stock -= quantite
        return True ,"vente effectuée avec succès"

    def reapprovisionner(self, quantite):
        """permet de réapprovisionner le stock du produit"""
        if self.rappele:
            return False, "produit rappelé"
        if quantite <= 0:
            return False,"quantité invalide"
        self.stock += quantite
        return True ,"réapprovisionnement effectué avec succès"

    def __eq__(self, valeur):
        """permet de comparer deux produits en fonction de leur code"""
        if isinstance(valeur, Produit):
            return self.code == valeur.code
        return False
    def __lt__(self, autre):
        """permet de comparer deux produits en fonction de leur prix"""
        if isinstance(autre, Produit):
            return self.prix < autre.prix
        return False


class Client:
    """Classe représentant un client du campus café."""

    PROFIL=("Etudiant","Alternant","Personnel","Visiteur")
    DECOUVERT_PERSONNEL=-10
    PLAFOND_RECHARGE=150
    TAUX_REMISE_REDUIT=0.10
    TAUX_REMISE_AUTRES=0.05

    def __init__(self,nom, profil, solde, pointfidelite):
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.pointfidelite = pointfidelite
        self.points_initiaux = pointfidelite

    def __repr__(self):
        return f"Client({self.nom!r}, {self.profil!r}, {self.solde}, {self.pointfidelite})"
    def __str__(self):
        return f"{self.nom} - Profil : {self.profil} - Solde : {self.solde:.2f} € - Points de fidélité : {self.pointfidelite}"

    def recharger(self, montant):
        """se recharger (en refusant une recharge non conforme etsi il est visiteur pas de recharge ni de fidelite)"""
        if self.profil == "Visiteur":
            return False,"recharge non autorisée pour les visiteurs"
        
        if (5 <= montant <= 100) and (self.solde + montant <= self.PLAFOND_RECHARGE):
            self.solde += montant
            return True ,"recharge effectuée avec succès"
        else:
            return False,"recharge refusee : montant invalide ou dépassement du plafond"
        

    def peut_payer(self, montant):
        """dire s'il peut payer un montant donné """
        if self.profil == "Visiteur":
            return True ,"paiement possible"
        if self.profil == "Personnel":
            if self.solde - montant < self.DECOUVERT_PERSONNEL:
                return False,"solde insuffisant"
            else:
                return True ,"paiement possible"
        else:
            if self.solde - montant < 0:
                return False,"solde insuffisant"
            else:
                return True ,"paiement possible"
    

    def est_debiter(self, montant):
        """permet de retirer un montant du solde du client si le paiement est possible"""
        possible, motif = self.peut_payer(montant)
        if self.profil == "Visiteur":
            return True ,motif
        if possible:
            self.solde -= montant
            return True ,"paiement effectué avec succès"
        else:
            return False,motif
    #Axe_A:Gros panier : si le total atteint 8,00 €, −10 % pour les étudiants et alternants, −5 % pour les autres.
    ##AXE_B1 (fidelite ayant le badge) :Points : 1 point par euro entier payé. À 30 points, la commande suivante reçoit −2,00 € et 30 points sont retirés.

    def avantage_point_fidelite(self):
        """permet de calculer le nombre de points de fidélité gagnés pour un montant donné"""
        if self.profil == "Visiteur":
            return 0,"pas de points de fidélité pour les visiteurs"
        if self.pointfidelite >= 30:
            return 2.00 ,"2,00 € de réduction pour 30 points de fidélité"
        return 0, f"Pas de reduction, il vous manque {30 - self.pointfidelite} points de fidélité pour bénéficier de la réduction de 2,00 €"

    def calculer_reduction(self, montant):
        """vas nous permettre de calculer la réduction applicable en fonction du profil du client et du montant de la commande"""
        if montant >= 8:
            if self.profil in ("Etudiant", "Alternant"):
                return montant * self.TAUX_REMISE_REDUIT, f"réduction de {self.TAUX_REMISE_REDUIT*100:.0f}% appliquée"
            else:
                return montant * self.TAUX_REMISE_AUTRES, f"réduction de {self.TAUX_REMISE_AUTRES*100:.0f}% appliquée"
        return 0,"pas de réduction applicable"

    def ajouter_points_fidelite(self, montant):
        """permet d'ajouter des points de fidélité en fonction du montant payé
        et de vérifier si le client a atteint le seuil de 30 points pour bénéficier d'une réduction de 2,00 €"""
        if self.profil == "Visiteur":
            return "pas de points de fidélité pour les visiteurs"
        points_gagnes = int(montant)
        if self.pointfidelite >= 30:
            self.pointfidelite -= 30
        self.pointfidelite += points_gagnes
        return f"{points_gagnes} points de fidélité ajoutés, total : {self.pointfidelite} points"

    def rejouer_fidelite(self, montant_payes):
        self.pointfidelite = self.points_initiaux
        for montant in montant_payes:
            self.ajouter_points_fidelite(montant)

class Commande:
     
    """cette classe gere les commandes des produit dans le cafeteria """
    compteur=1
    def __init__(self, heure, client):
        self.numero=Commande.compteur
        Commande.compteur += 1
        self.heure= heure
        self.client= client
        self.lignes=[]
        self.statut= "en cours"
        self.paye=0
        self.reduction=0
        self.avantage=0
         

    def __repr__(self):
        return f"Commande({self.numero}, {self.heure!r}, {self.client!r}, {self.lignes!r})"

    def __str__(self):
        lignes_str = "\n".join([f"{ligne[0].nom} x {ligne[1]} - {ligne[0].prix * ligne[1]:.2f} €" for ligne in self.lignes])
        total = sum([ligne[0].prix * ligne[1] for ligne in self.lignes])
        return f"Commande n°{self.numero} - Heure : {self.heure}\nClient : {self.client.nom}\nLignes :\n{lignes_str}\nTotal : {total:.2f} €"

    def ajouter_ligne(self,produit,quantite ):

        """va nous permettre d'ajouter une ligne de commande à la commande en cours ,
        Vérifier que chaque code produit existe, que chaque quantité est positive,
        que chaque produit est disponible (stock suffisant, créneau ouvert pour les plats) """
        # pour chaque commande de cookie -50
        if Produit.est_disponible(produit, quantite, self.heure)[0] and quantite > 0:
            self.lignes.append((produit, quantite))
            return True ,"ligne ajoutée avec succès"
        else:
            return False,Produit.est_disponible(produit, quantite, self.heure)[1]
    def calculer_total(self):
        """va nous permettre de calculer le total de la commande en cours"""
        total = sum([ligne[0].prix * ligne[1] for ligne in self.lignes])
        return total

    def __len__(self):
        """va nous permettre de calculer le nombre d'articles dans la commande en cours"""
        total_articles = 0
        for ligne in self.lignes:
            total_articles += ligne[1]
        return total_articles

    def __contains__(self, produit):
        """va nous permettre de vérifier si un produit est présent dans la commande en cours"""
        for ligne in self.lignes:
            if ligne[0] == produit:
                return True
        return False


    def ticket(self):
        texte = ""
        if self.statut == "annulée":
            texte += "*** ANNULÉE ***\n"
        texte += f"Commande n°{self.numero} - {self.heure}\n"
        texte += f"Client : {self.client.nom}\n"
        texte += f" Profil : {self.client.profil}\n"
        for produit, quantite in self.lignes:
            texte += f"{produit.nom} x {quantite} - {produit.prix * quantite:.2f} €\n"
        texte += f"Total : {self.calculer_total():.2f} €\n"
        if self.reduction > 0:
            texte += f"Remise gros panier : -{self.reduction:.2f} €\n"
        if self.avantage > 0:
            texte += f"Avantage fidélité : -{self.avantage:.2f} €\n"
        texte += f"Payé : {self.paye:.2f} €\n"
        return texte

    def __iter__(self):
            return iter(self.lignes)


class Cafeteria:
    """traiter une commande (section 3) ; recharger un badge ; réapprovisionner ; produire le rapport de clôture """
    def __init__(self):
        self.produits = {}
        self.commandes = []
        self.clients = {}  #dictionnaires
        self.refus= {}
        self.chiffres_affaires=0
        self.total_remises = 0
        self.nb_annulations = 0
        self.total_rembourse = 0
        self.rappels = []


    def __repr__(self):
        return f"Cafeteria({len(self.produits)} produits, {len(self.clients)} clients, {len(self.commandes)} commandes)"


    def ajouter_produit(self,produit):
            self.produits[produit.code] = produit
    
    
    def ajouter_client(self,client):
            self.clients[client.nom] = client



    def traiter_commande(self, commande):
        """va nous permettre de traiter une commande en cours"""
        total = commande.calculer_total()
        reduction,message_reduction= commande.client.calculer_reduction(total)
        total -= reduction
        avantage_fidelite, message_fidelite= commande.client.avantage_point_fidelite()
        avantage_fidelite = min(avantage_fidelite, total)   # l'avantage ne dépasse pas le total
        total -= avantage_fidelite
        total = round(total, 2)

        possible, motif = commande.client.peut_payer(total)
        if possible:
            commande.paye = total
            commande.reduction = reduction
            commande.avantage = avantage_fidelite
            commande.statut = "acceptée"
            self.chiffres_affaires += total
            self.total_remises +=reduction + avantage_fidelite
            commande.client.est_debiter(total)
            for produit, quantite in commande.lignes:
                produit.vendre(quantite)
            commande.client.ajouter_points_fidelite(total)
            self.commandes.append(commande)
            return True ,commande.ticket()
        else:
            if motif in self.refus:
                self.refus[motif] += 1
            else:
                self.refus[motif] = 1
            return False ,motif

    def annuler_commande(self, numero):
        commande = None
        for c in self.commandes:
            if c.numero == numero:
                commande = c
        if commande is None:
            return False, "commande inconnue",0
        if commande.statut == "annulée":
            return False, "commande déjà annulée",0
            
        commande.statut = "annulée"
        for produit, quantite in commande:
            produit.reapprovisionner(quantite)

        # b. le remboursement : pas recharger(), donc pas de plafond
        client = commande.client

        if client.profil != "Visiteur":
            client.solde = round(client.solde + commande.paye, 2)

        # c. la fidélité : rejouer les commandes acceptées de ce client, dans l'ordre
        montants = []
        for c in self.commandes:
            if c.client == client and c.statut == "acceptée":
                montants.append(c.paye)
        client.rejouer_fidelite(montants)

        self.total_rembourse = round(self.total_rembourse + commande.paye, 2)
        return True, "commande annulée", commande.paye
            



    def passer_commande(self, articles, heure, client):
        commande = Commande(heure, client)
        if len(articles) == 0 :
            return False,"Commande vide"
        
        for code, quantite in articles:
            if code not in self.produits:
                motif = "produit inconnu"
                if motif in self.refus:
                    self.refus[motif] += 1
                else:
                    self.refus[motif] = 1
                return False, motif
            else:
                produit = self.produits[code]
                verifie, motif = commande.ajouter_ligne(produit, quantite)
                if not verifie:
                    if motif in self.refus:
                        self.refus[motif] += 1
                    else:
                        self.refus[motif] = 1
                    return False, motif
        return self.traiter_commande(commande)


    def recharger_badge(self, nom, montant ):
        if nom not in self.clients:
            return False, "client inconnu"
        client = self.clients[nom]
        return client.recharger(montant)
       

    def compter_refus(self, motif):
        if motif in self.refus:
            self.refus[motif] += 1
        else:
            self.refus[motif] = 1    

    def reapprovisionner(self, code, quantite):
        if code not in self.produits:
            return False, "produit inconnu"
        produit = self.produits[code]
        ok, motif = produit.reapprovisionner(quantite)
        if not ok:
            self.compter_refus(motif)
        return ok, motif
    
    def rappeler_produit(self, code):
        if code not in self.produits:
            return False, "produit inconnu", None
        produit = self.produits[code]
        if produit.rappele:
            self.compter_refus("déjà rappelé")
            return False, "déjà rappelé", None
        produit.rappele= True
        produit.stock=0
        resume = {"produit": produit.nom, "commandes": [], "remboursements": [], "total": 0}
        for commande in self.commandes:
            if commande.statut == "acceptée" and produit in commande:
                annulee, motif, montant = self.annuler_commande(commande.numero)
                resume["commandes"].append(commande.numero)
                resume["remboursements"].append((commande.client.nom, montant))
                resume["total"] += montant
        resume["total"] = round(resume["total"], 2)
        self.rappels.append(resume)
        return True, "produit rappelé", resume


    def rapport(self):
        """ nombre de commandes acceptées, refus par motif,
        chiffre d'affaires, remises, top 3 des produits"""
        ventes={}
        nb_acceptees = 0
        nb_annulees = 0
        chiffre_affaires = 0
        remises = 0
        for commande in self.commandes:
            if commande.statut == "annulée":
                nb_annulees += 1
                continue                  # une commande annulée ne compte pas dans les ventes
            nb_acceptees += 1
            chiffre_affaires += commande.paye
            remises += commande.reduction + commande.avantage
            for produit, quantite in commande.lignes:
                if produit.code in ventes:
                    ventes[produit.code]+= quantite
                else:
                     ventes[produit.code]= quantite
        top3= sorted(ventes.items(),key=lambda x: x[1] ,reverse=True)[0:3]
        nb_annulees_rappel = 0
        for rappel in self.rappels:
            nb_annulees_rappel += len(rappel["commandes"])

        texte = " RAPPORT DE CLÔTURE \n"
        texte += f"Commandes acceptées : {nb_acceptees}\n"
        texte += f"Commandes annulées : {nb_annulees} (dont {nb_annulees_rappel} dues au rappel)\n"
        texte += f"Chiffre d'affaires : {chiffre_affaires:.2f} €\n"
        texte += f"Total des remises : {remises:.2f} €\n"
        texte += f"Total remboursé : {self.total_rembourse:.2f} €\n"

        texte += "\n Rappels \n"
        if self.rappels:
            for rappel in self.rappels:
                texte += f"- {rappel['produit']} : {rappel['total']:.2f} € remboursés\n"
                par_client = {}
                for nom, montant in rappel["remboursements"]:
                    if nom in par_client:
                        par_client[nom] += montant
                    else:
                        par_client[nom] = montant
                for nom, montant in sorted(par_client.items(), key=lambda x: x[1], reverse=True):
                    texte += f"    {nom} : {montant:.2f} €\n"
        else:
            texte += "Aucun rappel.\n"

        texte += "\n Refus par motif \n"
        if self.refus:
            for motif, nombre in self.refus.items():
                texte += f"- {motif} : {nombre}\n"
        else:
            texte += "Aucun refus.\n"

        texte += "\n Top 3 des produits vendus \n"
        if top3:
            for code, quantite in top3:
                nom = self.produits[code].nom
                texte += f"- {nom} : {quantite} vendus\n"
        else:
            texte += "Aucun produit vendu.\n"

        texte += "\n Carte par prix croissant \n"
        for produit in sorted(self.produits.values()):
            if produit.rappele:
                texte += f"- {produit.nom} : {produit.prix:.2f} € RAPPELÉ\n"
            elif produit.stock == 0:
                texte += f"- {produit.nom} : {produit.prix:.2f} € ÉPUISÉ\n"
            else:
                texte += f"- {produit.nom} : {produit.prix:.2f} € (stock : {produit.stock})\n"

        texte += "\n Badges sous 3,00 € \n"
        for client in self.clients.values():
            if client.solde < 3.00 and client.profil != "Visiteur":
                texte += f"- {client.nom} : {client.solde:.2f} €\n"

        return texte


# ======================= SCÉNARIO DE LA JOURNÉE (section 6) =======================

def afficher(numero, heure, evenement, resultat):
    """affiche le résultat d'un événement : le ticket / message si accepté, le motif si refusé"""
    ok, message = resultat
    print(f"\n[{numero}] {heure} - {evenement}")
    if ok:
        print(message)
    else:
        print(f"REFUSÉ : {message}")


def jouer_scenario():
    """rejoue les 17 événements de la journée puis affiche le rapport de clôture"""
    cafet = Cafeteria()

    # La carte (section 2.1)
    cafet.ajouter_produit(Produit("B01", "Café expresso", "boisson chaude", 1.20, 100))
    cafet.ajouter_produit(Produit("B02", "Thé", "boisson chaude", 1.30, 60))
    cafet.ajouter_produit(Produit("B03", "Chocolat chaud", "boisson chaude", 1.60, 40))
    cafet.ajouter_produit(Produit("B04", "Jus d'orange", "boisson froide", 2.00, 24))
    cafet.ajouter_produit(Produit("B05", "Eau 50 cl", "boisson froide", 1.00, 40))
    cafet.ajouter_produit(Produit("V01", "Croissant", "viennoiserie", 1.20, 30))
    cafet.ajouter_produit(Produit("P01", "Sandwich jambon-beurre", "plat", 4.00, 15))
    cafet.ajouter_produit(Produit("P02", "Wrap végétarien", "plat", 4.60, 10))
    cafet.ajouter_produit(Produit("P03", "Plat du jour", "plat", 7.20, 20))
    cafet.ajouter_produit(Produit("D01", "Cookie", "dessert", 1.40, 25))
    cafet.ajouter_produit(Produit("D02", "Fruit de saison", "dessert", 0.80, 30))

    # Les clients (section 2.2)
    cafet.ajouter_client(Client("Alice", "Etudiant", 12.00, 0))
    cafet.ajouter_client(Client("Bruno", "Alternant", 3.50, 0))
    cafet.ajouter_client(Client("Chloé", "Etudiant", 25.00, 0))
    cafet.ajouter_client(Client("Farid", "Personnel", 0.00, 0))
    cafet.ajouter_client(Client("Visiteur", "Visiteur", 0, 0))

    alice = cafet.clients["Alice"]
    bruno = cafet.clients["Bruno"]
    chloe = cafet.clients["Chloé"]
    farid = cafet.clients["Farid"]
    visiteur = cafet.clients["Visiteur"]

    print("[1] 07:30 - Ouverture")
    print(repr(cafet))
    afficher(2, "07:45", "Commande Alice", cafet.passer_commande([("B01", 1), ("V01", 1)], "07:45", alice))
    afficher(3, "08:10", "Commande Farid", cafet.passer_commande([("B01", 2)], "08:10", farid))
    afficher(4, "08:30", "Commande Bruno", cafet.passer_commande([("B03", 1), ("V01", 3)], "08:30", bruno))
    afficher(5, "08:35", "Recharge Bruno 20,00 €", cafet.recharger_badge("Bruno", 20.00))
    afficher(6, "08:40", "Commande Bruno", cafet.passer_commande([("B03", 1), ("V01", 3)], "08:40", bruno))
    afficher(7, "09:15", "Commande visiteur", cafet.passer_commande([("B02", 1), ("D01", 1)], "09:15", visiteur))
    afficher(8, "11:00", "Commande Chloé", cafet.passer_commande([("P03", 1)], "11:00", chloe))
    afficher(9, "12:05", "Commande Chloé", cafet.passer_commande([("P03", 1), ("B04", 1), ("D01", 1)], "12:05", chloe))
    afficher(10, "12:10", "Recharge Alice 150,00 €", cafet.recharger_badge("Alice", 150.00))
    # --- v2 ---
    afficher("v2", "12:15", "Commande Bruno", cafet.passer_commande([("P02", 2)], "12:15", bruno))
    afficher("v2", "12:18", "Commande Chloé", cafet.passer_commande([("P02", 1)], "12:18", chloe))
    commande_chloe = cafet.commandes[-1].numero
    afficher(11, "12:20", "Commande Alice", cafet.passer_commande([("P02", 1), ("B05", 1), ("D02", 1), ("B01", 1)], "12:20", alice))
    # --- v2 ---
    print("\n[v2] 12:25 - Annulation Chloé :", cafet.annuler_commande(commande_chloe))
    print("\n[v2] 12:26 - Annulation Chloé (2e fois) :", cafet.annuler_commande(commande_chloe))
    print("\n[v2] 12:27 - Annulation n°999 :", cafet.annuler_commande(999))
    print("\n[v2] 12:30 - Rappel wrap :", cafet.rappeler_produit("P02"))
    afficher("v2", "12:35", "Commande Bruno", cafet.passer_commande([("P02", 1)], "12:35", bruno))
    afficher("v2", "12:36", "Réapprovisionnement wrap +10", cafet.reapprovisionner("P02", 10))
    print("\n[v2] 12:40 - Rappel wrap (2e fois) :", cafet.rappeler_produit("P02"))
    afficher(12, "12:45", "Commande visiteur", cafet.passer_commande([("P01", 16)], "12:45", visiteur))
    afficher(13, "13:00", "Commande Bruno", cafet.passer_commande([("P01", 1), ("Smoothie mangue", 1)], "13:00", bruno))
    afficher(14, "15:30", "Commande Alice", cafet.passer_commande([("B01", 1), ("D01", 1)], "15:30", alice))
    afficher(15, "16:00", "Réapprovisionnement Sandwich +10", cafet.reapprovisionner("P01", 10))
    afficher(16, "17:30", "Commande Farid", cafet.passer_commande([("B02", 2)], "17:30", farid))

    print("\n[17] 18:30 - Clôture")
    print(cafet.rapport())


jouer_scenario()


# ======================= TESTS =======================
import unittest


class TestProduit(unittest.TestCase):
    def setUp(self):
        # Un plat neuf avant chaque test : stock de 5 unités
        self.produit = Produit("P1", "Sandwich", "plat", 4.0, 5)

    # 11:30 (début du créneau) est accepté
    def test_est_disponible_heure_11h30_acceptee(self):
        disponible, message = self.produit.est_disponible(1, "11:30")
        self.assertTrue(disponible)

    # 13:59 (dernière minute du créneau) est accepté
    def test_est_disponible_heure_13h59_acceptee(self):
        disponible, message = self.produit.est_disponible(1, "13:59")
        self.assertTrue(disponible)

    # 14:00 est refusé : l'énoncé dit "fin exclue"
    def test_est_disponible_heure_14h00_refusee(self):
        disponible, message = self.produit.est_disponible(1, "14:00")
        self.assertFalse(disponible)
        self.assertEqual(message, "hors créneau")

    # 11:29 (juste avant le créneau) est refusé
    def test_est_disponible_heure_11h29_refusee(self):
        disponible, message = self.produit.est_disponible(1, "11:29")
        self.assertFalse(disponible)

    # Un produit qui n'est pas un plat n'a pas de créneau
    def test_boisson_sans_creneau(self):
        cafe = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
        self.assertTrue(cafe.est_disponible(1, "07:30")[0])

    # Une demande égale au stock est acceptée (stock exactement suffisant)
    def test_est_disponible_stock_exactement_suffisant(self):
        disponible, message = self.produit.est_disponible(5, "12:00")
        self.assertTrue(disponible)

    # Une demande supérieure au stock d'une unité est refusée
    def test_est_disponible_stock_insuffisant(self):
        disponible, message = self.produit.est_disponible(6, "12:00")
        self.assertFalse(disponible)
        self.assertEqual(message, "rupture de stock")

    # Vendre tout le stock le ramène à 0, puis toute vente est bloquée
    def test_vendre_tout_le_stock(self):
        self.assertTrue(self.produit.vendre(5)[0])
        self.assertEqual(self.produit.stock, 0)
        self.assertFalse(self.produit.vendre(1)[0])
        self.assertEqual(self.produit.stock, 0)

    # Réapprovisionnement valide, puis quantités invalides
    def test_reapprovisionner(self):
        self.assertTrue(self.produit.reapprovisionner(10)[0])
        self.assertEqual(self.produit.stock, 15)
        self.assertFalse(self.produit.reapprovisionner(0)[0])
        self.assertFalse(self.produit.reapprovisionner(-3)[0])
        self.assertEqual(self.produit.stock, 15)

    # Égalité par code et comparaison par prix
    def test_egalite_et_comparaison(self):
        meme_code = Produit("P1", "Autre nom", "plat", 9.0, 1)
        plus_cher = Produit("P2", "Wrap", "plat", 4.60, 1)
        self.assertEqual(self.produit, meme_code)
        self.assertNotEqual(self.produit, plus_cher)
        self.assertTrue(self.produit < plus_cher)


class TestClientRecharge(unittest.TestCase):
    # Recharge de 100,00 € (borne haute) acceptée
    def test_recharge_de_100_euros_acceptee(self):
        client = Client("Lamine", "Etudiant", 0, 0)
        succes, message = client.recharger(100.00)
        self.assertTrue(succes)
        self.assertAlmostEqual(client.solde, 100.00)

    # Recharge de 100,01 € refusée
    def test_recharge_au_dessus_de_100_refusee(self):
        client = Client("Lamine", "Etudiant", 0, 0)
        succes, message = client.recharger(100.01)
        self.assertFalse(succes)
        self.assertEqual(client.solde, 0)

    # Borne basse : 5,00 € accepté, 4,99 € refusé
    def test_recharge_borne_basse_5_euros(self):
        client = Client("Coumba", "Alternant", 0, 0)
        self.assertTrue(client.recharger(5.00)[0])
        client2 = Client("Liliane", "Alternant", 0, 0)
        self.assertFalse(client2.recharger(4.99)[0])

    # Plafond de 150 € : atteignable pile, mais pas dépassable
    def test_recharge_plafond_150_euros(self):
        client = Client("Khadija", "Etudiant", 50, 0)
        self.assertTrue(client.recharger(100)[0])
        self.assertEqual(client.solde, 150)
        self.assertFalse(client.recharger(5)[0])
        self.assertEqual(client.solde, 150)

    # Un visiteur ne peut pas recharger
    def test_recharge_visiteur_refusee(self):
        client = Client("Moustapha", "Visiteur", 0, 0)
        succes, message = client.recharger(20)
        self.assertFalse(succes)
        self.assertEqual(client.solde, 0)


class TestClientPaiement(unittest.TestCase):
    # Solde exactement égal au montant : paiement possible
    def test_payer_solde_exactement_suffisant(self):
        client = Client("Khadija", "Etudiant", 5.00, 0)
        self.assertTrue(client.peut_payer(5.00)[0])

    # Un centime de trop : refusé
    def test_payer_un_centime_de_trop_refuse(self):
        client = Client("Khadija", "Etudiant", 5.00, 0)
        possible, motif = client.peut_payer(5.01)
        self.assertFalse(possible)
        self.assertEqual(motif, "solde insuffisant")

    # Débiter le solde exact le ramène à 0, puis un nouveau débit est refusé
    def test_debiter_solde_exact_puis_refus(self):
        client = Client("Khadija", "Etudiant", 5.00, 0)
        self.assertTrue(client.est_debiter(5.00)[0])
        self.assertEqual(client.solde, 0)
        self.assertFalse(client.est_debiter(0.01)[0])
        self.assertEqual(client.solde, 0)

    # Le personnel peut descendre exactement à -10,00 €
    def test_personnel_decouvert_moins_10_euros_accepte(self):
        client = Client("Coumba", "Personnel", 0.00, 0)
        self.assertTrue(client.peut_payer(10.00)[0])
        self.assertTrue(client.est_debiter(10.00)[0])
        self.assertAlmostEqual(client.solde, -10.00)

    # Le personnel ne peut pas dépasser -10,00 €
    def test_personnel_decouvert_depasse_refuse(self):
        client = Client("Coumba", "Personnel", 0.00, 0)
        self.assertFalse(client.peut_payer(10.01)[0])
        client.est_debiter(10.00)
        self.assertFalse(client.est_debiter(0.01)[0])
        self.assertAlmostEqual(client.solde, -10.00)

    # Un étudiant n'a pas de découvert
    def test_etudiant_sans_decouvert(self):
        client = Client("Cheikh", "Etudiant", 0.00, 0)
        self.assertFalse(client.peut_payer(0.01)[0])

    # Un visiteur paie comptant : son solde ne change pas
    def test_visiteur_paie_sans_solde(self):
        client = Client("Moustapha", "Visiteur", 0.00, 0)
        self.assertTrue(client.peut_payer(50)[0])
        client.est_debiter(50)
        self.assertEqual(client.solde, 0)


class TestRemiseA3(unittest.TestCase):
    # 7,99 € : pas de remise
    def test_pas_de_remise_sous_8_euros(self):
        client = Client("Khadija", "Etudiant", 50, 0)
        self.assertEqual(client.calculer_reduction(7.99)[0], 0)

    # 8,00 € pile : -10 % pour un étudiant
    def test_remise_etudiant_10_pourcent_a_8_euros(self):
        client = Client("Khadija", "Etudiant", 50, 0)
        self.assertAlmostEqual(client.calculer_reduction(8.00)[0], 0.80)

    # Alternant : -10 %
    def test_remise_alternant_10_pourcent(self):
        client = Client("Coumba", "Alternant", 50, 0)
        self.assertAlmostEqual(client.calculer_reduction(10.00)[0], 1.00)

    # Personnel et visiteur : -5 %
    def test_remise_autres_5_pourcent(self):
        personnel = Client("Modou", "Personnel", 50, 0)
        visiteur = Client("Moustapha", "Visiteur", 0, 0)
        self.assertAlmostEqual(personnel.calculer_reduction(10.00)[0], 0.50)
        self.assertAlmostEqual(visiteur.calculer_reduction(20.00)[0], 1.00)


class TestFideliteB1(unittest.TestCase):
    # 29 points : pas d'avantage
    def test_pas_d_avantage_a_29_points(self):
        client = Client("Lamine", "Etudiant", 50, 29)
        self.assertEqual(client.avantage_point_fidelite()[0], 0)

    # 30 points : -2,00 €
    def test_avantage_2_euros_a_30_points(self):
        client = Client("Lamine", "Etudiant", 50, 30)
        self.assertEqual(client.avantage_point_fidelite()[0], 2.00)

    # 1 point par euro entier : 28 + 5,60 € = 33 points
    def test_points_par_euro_entier(self):
        client = Client("Lamine", "Etudiant", 50, 28)
        client.ajouter_points_fidelite(5.60)
        self.assertEqual(client.pointfidelite, 33)

    # À 30 points ou plus, on retire 30 points avant d'ajouter les nouveaux
    def test_retrait_30_points(self):
        client = Client("Lamine", "Etudiant", 50, 33)
        client.ajouter_points_fidelite(1.00)
        self.assertEqual(client.pointfidelite, 4)

    # Un visiteur n'a ni avantage ni points
    def test_visiteur_sans_fidelite(self):
        client = Client("Moustapha", "Visiteur", 0, 0)
        self.assertEqual(client.avantage_point_fidelite()[0], 0)
        client.ajouter_points_fidelite(19.00)
        self.assertEqual(client.pointfidelite, 0)


class TestCommande(unittest.TestCase):
    def setUp(self):
        # Client et plat (stock de 3) communs aux tests
        self.client = Client("Coumba", "Etudiant", 50, 0)
        self.produit = Produit("P4", "Salade", "plat", 4.0, 3)

    # Le numéro de commande augmente à chaque création
    def test_numero_incremente(self):
        commande1 = Commande("12:00", self.client)
        commande2 = Commande("12:00", self.client)
        self.assertEqual(commande2.numero, commande1.numero + 1)

    # Ligne dont la quantité égale exactement le stock : len, total, in
    def test_ajouter_ligne_stock_exactement_suffisant(self):
        commande = Commande("12:00", self.client)
        self.assertTrue(commande.ajouter_ligne(self.produit, 3)[0])
        self.assertEqual(len(commande), 3)
        self.assertAlmostEqual(commande.calculer_total(), 12.0)
        self.assertIn(self.produit, commande)

    # Quantité supérieure au stock : refusée, commande vide
    def test_ajouter_ligne_stock_insuffisant(self):
        commande = Commande("12:00", self.client)
        self.assertFalse(commande.ajouter_ligne(self.produit, 4)[0])
        self.assertEqual(len(commande), 0)
        self.assertNotIn(self.produit, commande)

    # Quantités nulles ou négatives : refusées
    def test_ajouter_ligne_quantite_invalide(self):
        commande = Commande("12:00", self.client)
        self.assertEqual(commande.ajouter_ligne(self.produit, 0), (False, "quantité invalide"))
        self.assertFalse(commande.ajouter_ligne(self.produit, -1)[0])

    # Bornes horaires vues à travers la commande
    def test_ajouter_ligne_bornes_horaires(self):
        self.assertTrue(Commande("11:30", self.client).ajouter_ligne(self.produit, 1)[0])
        self.assertTrue(Commande("13:59", self.client).ajouter_ligne(self.produit, 1)[0])
        self.assertFalse(Commande("11:29", self.client).ajouter_ligne(self.produit, 1)[0])
        self.assertFalse(Commande("14:00", self.client).ajouter_ligne(self.produit, 1)[0])

    # for ligne in commande : on retrouve bien les lignes
    def test_iteration(self):
        commande = Commande("12:00", self.client)
        commande.ajouter_ligne(self.produit, 2)
        self.assertEqual(list(commande), [(self.produit, 2)])


class TestCafeteria(unittest.TestCase):
    def setUp(self):
        # Une cafétéria neuve avec une salade (plat) en stock de 2
        self.cafeteria = Cafeteria()
        self.salade = Produit("S1", "Salade", "plat", 4.0, 2)
        self.cafeteria.ajouter_produit(self.salade)

    # Solde et stock exactement suffisants (8,00 € -10 % = 7,20 €)
    def test_commande_solde_et_stock_exacts(self):
        client = Client("Khadija", "Etudiant", 7.20, 0)
        self.cafeteria.ajouter_client(client)
        succes, message = self.cafeteria.passer_commande([("S1", 2)], "12:00", client)
        self.assertTrue(succes)
        self.assertAlmostEqual(client.solde, 0)
        self.assertEqual(self.salade.stock, 0)
        self.assertAlmostEqual(self.cafeteria.chiffres_affaires, 7.20)
        self.assertAlmostEqual(self.cafeteria.total_remises, 0.80)
        self.assertEqual(client.pointfidelite, 7)
        self.assertEqual(len(self.cafeteria.commandes), 1)

    # Stock épuisé : refus, rien ne change
    def test_commande_refusee_stock_epuise(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.salade.vendre(2)
        succes, message = self.cafeteria.passer_commande([("S1", 1)], "12:00", client)
        self.assertFalse(succes)
        self.assertEqual(message, "rupture de stock")
        self.assertEqual(client.solde, 100)

    # Code inconnu : refus
    def test_commande_refusee_code_inconnu(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        succes, message = self.cafeteria.passer_commande([("XXX", 1)], "12:00", client)
        self.assertFalse(succes)
        self.assertEqual(message, "produit inconnu")

    # Plat hors créneau : refus
    def test_commande_refusee_hors_creneau(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        succes, message = self.cafeteria.passer_commande([("S1", 1)], "14:00", client)
        self.assertFalse(succes)
        self.assertEqual(message, "hors créneau")

    # Solde insuffisant : tout ou rien (stock, solde, points, journal inchangés)
    def test_commande_refusee_solde_insuffisant(self):
        client = Client("Coumba", "Etudiant", 3.99, 0)
        succes, message = self.cafeteria.passer_commande([("S1", 1)], "12:00", client)
        self.assertFalse(succes)
        self.assertEqual(message, "solde insuffisant")
        self.assertEqual(self.salade.stock, 2)
        self.assertAlmostEqual(client.solde, 3.99)
        self.assertEqual(client.pointfidelite, 0)
        self.assertEqual(len(self.cafeteria.commandes), 0)
        self.assertEqual(self.cafeteria.refus, {"solde insuffisant": 1})

    # Le personnel peut utiliser son découvert (4,00 € < 8 € : pas de remise)
    def test_commande_personnel_avec_decouvert(self):
        client = Client("Modou", "Personnel", 0, 0)
        succes, message = self.cafeteria.passer_commande([("S1", 1)], "12:00", client)
        self.assertTrue(succes)
        self.assertAlmostEqual(client.solde, -4.00)

    # Avantage fidélité B1 dans une vraie commande : 4,00 - 2,00 = 2,00 €
    def test_commande_avec_avantage_fidelite(self):
        client = Client("Cheikh", "Etudiant", 10, 30)
        succes, message = self.cafeteria.passer_commande([("S1", 1)], "12:00", client)
        self.assertTrue(succes)
        self.assertAlmostEqual(client.solde, 8.00)
        self.assertEqual(client.pointfidelite, 2)

    # Recharge via la cafétéria (100,00 €) puis client inconnu
    def test_recharger_badge(self):
        client = Client("Coumba", "Etudiant", 3.99, 0)
        self.cafeteria.ajouter_client(client)
        self.assertTrue(self.cafeteria.recharger_badge("Coumba", 100.00)[0])
        self.assertAlmostEqual(client.solde, 103.99)
        self.assertFalse(self.cafeteria.recharger_badge("Inconnu", 10)[0])

    # Réapprovisionnement via la cafétéria
    def test_reapprovisionner(self):
        self.assertTrue(self.cafeteria.reapprovisionner("S1", 10)[0])
        self.assertEqual(self.salade.stock, 12)
        self.assertFalse(self.cafeteria.reapprovisionner("XXX", 10)[0])

    # Rapport : commandes acceptées, refus par motif, top des ventes
    def test_rapport(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.cafeteria.passer_commande([("S1", 2)], "12:00", client)
        self.cafeteria.passer_commande([("S1", 1)], "12:00", client)
        self.cafeteria.passer_commande([("XXX", 1)], "12:00", client)
        self.assertEqual(len(self.cafeteria.commandes), 1)
        self.assertEqual(self.cafeteria.refus, {"rupture de stock": 1, "produit inconnu": 1})
        rapport = self.cafeteria.rapport()
        self.assertIn("Commandes acceptées : 1", rapport)
        self.assertIn("Salade : 2", rapport)

class TestAnnulation(unittest.TestCase):
    def setUp(self):
        # Une cafétéria neuve : un menu à 10 € (pas de créneau) et un café
        self.cafeteria = Cafeteria()
        self.menu = Produit("X1", "Menu", "viennoiserie", 10.0, 100)
        self.cafe = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
        self.cafeteria.ajouter_produit(self.menu)
        self.cafeteria.ajouter_produit(self.cafe)

    def derniere_commande(self):
        return self.cafeteria.commandes[-1]

    # 1. Annuler la dernière commande remet solde, stock et fidélité comme avant
    def test_annuler_derniere_commande_etat_identique(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.cafeteria.passer_commande([("X1", 1)], "10:00", client)
        avant = (client.solde, client.pointfidelite, self.cafe.stock, self.menu.stock)
        self.cafeteria.passer_commande([("B01", 2)], "10:05", client)
        annulee, motif, montant = self.cafeteria.annuler_commande(self.derniere_commande().numero)
        self.assertTrue(annulee)
        self.assertAlmostEqual(montant, 2.40)
        apres = (client.solde, client.pointfidelite, self.cafe.stock, self.menu.stock)
        self.assertAlmostEqual(apres[0], avant[0])
        self.assertEqual(apres[1:], avant[1:])

    # 2. Commande inconnue
    def test_annulation_commande_inconnue(self):
        self.assertEqual(self.cafeteria.annuler_commande(99999), (False, "commande inconnue", 0))

    # 3. Commande déjà annulée
    def test_annulation_commande_deja_annulee(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.cafeteria.passer_commande([("B01", 1)], "10:00", client)
        numero = self.derniere_commande().numero
        self.assertTrue(self.cafeteria.annuler_commande(numero)[0])
        self.assertEqual(self.cafeteria.annuler_commande(numero), (False, "commande déjà annulée", 0))

    # 4. Annulation refusée : rien n'est modifié
    def test_annulation_refusee_rien_ne_change(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.cafeteria.passer_commande([("B01", 1)], "10:00", client)
        numero = self.derniere_commande().numero
        self.cafeteria.annuler_commande(numero)
        avant = (client.solde, client.pointfidelite, self.cafe.stock, self.cafeteria.total_rembourse)
        self.cafeteria.annuler_commande(numero)          # refusée : déjà annulée
        self.cafeteria.annuler_commande(99999)           # refusée : inconnue
        apres = (client.solde, client.pointfidelite, self.cafe.stock, self.cafeteria.total_rembourse)
        self.assertEqual(apres, avant)

    # 5. Visiteur : remboursé comptant, compté dans le rapport, solde inchangé
    def test_remboursement_visiteur(self):
        visiteur = Client("Moustapha", "Visiteur", 0, 0)
        self.cafeteria.passer_commande([("X1", 1)], "10:00", visiteur)   # 10 € - 5 % = 9,50 €
        annulee, motif, montant = self.cafeteria.annuler_commande(self.derniere_commande().numero)
        self.assertTrue(annulee)
        self.assertAlmostEqual(montant, 9.50)
        self.assertEqual(visiteur.solde, 0)
        self.assertAlmostEqual(self.cafeteria.total_rembourse, 9.50)
        self.assertIn("Total remboursé : 9.50", self.cafeteria.rapport())

    # 6. Un remboursement n'est pas une recharge : il peut dépasser 150 €
    def test_remboursement_depasse_150_euros(self):
        client = Client("Khadija", "Etudiant", 150, 0)
        self.cafeteria.passer_commande([("X1", 1)], "10:00", client)     # paie 9 € → 141 €
        self.assertTrue(client.recharger(9)[0])                          # recharge → 150 €
        self.cafeteria.annuler_commande(self.derniere_commande().numero)
        self.assertAlmostEqual(client.solde, 159.00)

    # 7. Annuler une commande qui avait utilisé l'avantage fidélité : les 30 points reviennent
    def test_annulation_avec_avantage_fidelite(self):
        client = Client("Coumba", "Etudiant", 50, 30)
        self.cafeteria.passer_commande([("X1", 1)], "10:00", client)     # 10 - 1 - 2 = 7 €
        self.assertEqual(client.pointfidelite, 7)                        # 30 - 30 + 7
        annulee, motif, montant = self.cafeteria.annuler_commande(self.derniere_commande().numero)
        self.assertAlmostEqual(montant, 7.00)
        self.assertAlmostEqual(client.solde, 50.00)
        self.assertEqual(client.pointfidelite, 30)

    # 8. Le ticket d'une commande annulée affiche ANNULÉE
    def test_ticket_commande_annulee(self):
        client = Client("Lamine", "Etudiant", 100, 0)
        self.cafeteria.passer_commande([("B01", 1)], "10:00", client)
        commande = self.derniere_commande()
        self.assertNotIn("ANNULÉE", commande.ticket())
        self.cafeteria.annuler_commande(commande.numero)
        self.assertIn("ANNULÉE", commande.ticket())
        self.assertEqual(commande.statut, "annulée")

# Lancement des tests
unittest.main(argv=["ignored"], exit=False)




        
        







