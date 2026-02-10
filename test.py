import mysql.connector
import re


# Connexion à la base

import mysql.connector



try:
    connexion = mysql.connector.connect(
        host="localhost",
        user="amadou",
        password="ama12345",
        database="gestion_stock"
    )
    curseur = connexion.cursor(dictionary=True)
except:
    print(" Erreur de connexion à la base de données")
    exit()

# Vérification de la connexion
if connexion.is_connected():
    print(" Connecté à la base MySQL")



def ajouter_categorie():
    nom_categorie = input("Nom de la catégorie : ").strip()

    if not nom_categorie:
        print(" Le nom de la catégorie ne peut pas être vide.")
        return

    if not re.match(r'^[A-Za-zÀ-ÿ ]+$', nom_categorie):
        print(" Nom invalide : utilisez uniquement des lettres et espaces.")
        return

    # Vérifier si la catégorie existe déjà
    curseur.execute("SELECT * FROM categorie WHERE nom_categorie = %s", (nom_categorie,))
    if curseur.fetchone():
        print(f" La catégorie '{nom_categorie}' existe déjà.")
        return

    try:
        sql = "INSERT INTO categorie (nom_categorie) VALUES (%s)"
        curseur.execute(sql, (nom_categorie,))
        connexion.commit()
        print(f" Catégorie '{nom_categorie}' ajoutée avec succès.")
    except mysql.connector.Error as e:
        print(" Erreur lors de l'ajout de la catégorie :", e)
        connexion.rollback()

def ajouter_produit():
  
    # Saisie du nom du produit
    designation = input("Nom du produit : ").strip()
    if not designation:
        print(" Le nom du produit ne peut pas être vide.")
        return

    # Vérification du nom (lettres, chiffres, espaces, tirets)
    if not re.match(r'^[A-Za-z0-9À-ÿ \-]+$', designation):
        print(" Nom invalide : utilisez seulement lettres, chiffres, espaces ou tirets.")
        return

    # Saisie du prix
    try:
        prix = float(input("Prix du produit : ").strip())
        if prix < 0:
            print(" Le prix ne peut pas être négatif.")
            return
    except ValueError:
        print(" Prix invalide. Entrez un nombre.")
        return

    # Afficher les catégories existantes
    curseur.execute("SELECT * FROM categorie ORDER BY id_categorie")
    categories = curseur.fetchall()

    if not categories:
        print(" Aucune catégorie trouvée. Ajoutez une catégorie d'abord.")
        return

    print("\n Liste des catégories existantes :")
    for cat in categories:
        print(f"{cat['id_categorie']} - {cat['nom_categorie']}")

    # Saisie de la catégorie
    try:
        id_categorie = int(input("ID de la catégorie : ").strip())
    except ValueError:
        print(" ID invalide.")
        return

    # Vérifier que la catégorie existe
    if not any(cat['id_categorie'] == id_categorie for cat in categories):
        print(" Catégorie non trouvée.")
        return

    try:
        sql = """
        INSERT INTO produit (designation_produit, prix_produit, stock, id_categorie)
        VALUES (%s, %s, %s, %s)
        """
        curseur.execute(sql, (designation, prix, 0, id_categorie))
        connexion.commit()
        print(f"Produit '{designation}' ajouté avec succès avec stock initial 0.")
    except mysql.connector.Error as e:
        print(" Erreur lors de l'ajout du produit :", e)
        connexion.rollback()

def supprimer_categorie():
    lister_categories()  # Affiche toutes les catégories

    try:
        id_categorie = int(input("\nID de la catégorie à supprimer : ").strip())
    except ValueError:
        print(" ID invalide.")
        return

    # Vérifier si la catégorie contient des produits
    curseur.execute("SELECT COUNT(*) AS nb FROM produit WHERE id_categorie = %s", (id_categorie,))
    nb = curseur.fetchone()["nb"]

    if nb > 0:
        print(" Suppression impossible : cette catégorie contient des produits.")
        return

    # Suppression si aucun produit
    try:
        curseur.execute("DELETE FROM categorie WHERE id_categorie = %s", (id_categorie,))
        connexion.commit()
        print(" Catégorie supprimée avec succès.")
    except mysql.connector.Error as e:
        print(" Erreur lors de la suppression :", e)
        connexion.rollback()

def afficher_produits():
    try:
        sql = """
        SELECT 
            p.id_produit,
            p.designation_produit,
            p.prix_produit,
            p.stock,
            c.nom_categorie
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id_categorie
        ORDER BY c.nom_categorie, p.designation_produit
        """
        curseur.execute(sql)
        produits = curseur.fetchall()

        if not produits:
            print(" Aucun produit trouvé.")
            return

        print("\n LISTE DES PRODUITS PAR CATÉGORIE\n")
        for p in produits:
            print(
                f"ID: {p['id_produit']} | "
                f"Produit: {p['designation_produit']} | "
                f"Catégorie: {p['nom_categorie']} | "
                f"Prix: {p['prix_produit']} | "
                f"Stock: {p['stock']}"
            )

    except mysql.connector.Error as e:
        print(" Erreur lors de l'affichage des produits :", e)

def menu_categories():
    while True:
        print("\n========== GESTION DES CATEGORIES ==========")
        print("1. Ajouter une catégorie")
        print("2. Ajouter produit")
        print("3. Afficher categorie")
        print("4. Faire un mouvement de produits")
        print("5. Afficher la liste de toutes les produits")
        print("6. Afficher les produits en faible stock")
        print("7.Supprimer categorie")
        print("7.Afficher l'historique")

        print("7. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            ajouter_categorie()
        elif choix == "2":
            ajouter_produit()  

  

        elif choix == "3":
            lister_categories()
        elif choix == "4":
            mouvement_stock()
        elif choix == "5":
            afficher_produits()
        elif choix == "6":
            alerte_stock() 
        elif choix == "7":  
            supprimer_categorie() 
        elif choix == "8":  
            afficher_mouvements()
        
        else:
            print("Choix invalide, veuillez réessayer.")



def afficher_produits():
    """
    Affiche tous les produits avec leur catégorie et leur stock.
    Met en évidence les produits dont le stock est inférieur à 5.
    """

    try:
        curseur.execute("""
            SELECT p.id_produit, p.designation_produit, p.stock, c.nom_categorie
            FROM produit p
            JOIN categorie c ON p.id_categorie = c.id_categorie
            ORDER BY p.id_produit
        """)
        produits = curseur.fetchall()

        if not produits:
            print("ℹAucun produit trouvé.")
            return

        print("\n Liste des produits :")
        for p in produits:
            alerte = " Stock faible !" if p['stock'] < 5 else ""
            print(f"{p['id_produit']} - {p['designation_produit']} | Catégorie: {p['nom_categorie']} | Stock: {p['stock']} {alerte}")

    except mysql.connector.Error as e:
        print(" Erreur lors de la récupération des produits :", e)

def alerte_stock():
    try:
        sql = """
        SELECT 
            p.id_produit,
            p.designation_produit,
            p.stock,
            c.nom_categorie
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id_categorie
        WHERE p.stock < 5
        ORDER BY p.stock ASC
        """
        curseur.execute(sql)
        produits = curseur.fetchall()

        if not produits:
            print(" Aucun produit en stock faible ")
            return

        print("\n ALERTE : STOCK FAIBLE (< 5 unités)\n")
        for p in produits:
            print(
                f"ID: {p['id_produit']} | "
                f"Produit: {p['designation_produit']} | "
                f"Catégorie: {p['nom_categorie']} | "
                f"Stock restant: {p['stock']}"
            )

    except mysql.connector.Error as e:
        print(" Erreur lors de l'affichage des alertes :", e)

def lister_categories():
    try:
        curseur.execute("SELECT * FROM categorie ORDER BY id_categorie")
        categories = curseur.fetchall()

        if not categories:
            print("ℹ Aucune catégorie trouvée.")
            return

        print("\n Liste des catégories :")
        for cat in categories:
            print(f"{cat['id_categorie']} - {cat['nom_categorie']}")

    except mysql.connector.Error as e:
        print(" Erreur lors de l'affichage des catégories :", e)

def mouvement_stock():
    # Afficher les produits 
    curseur.execute("""
        SELECT p.id_produit, p.designation_produit, p.stock, c.nom_categorie
        FROM produit p
        JOIN categorie c ON p.id_categorie = c.id_categorie
        ORDER BY p.id_produit
    """)
    produits = curseur.fetchall()

    if not produits:
        print(" Aucun produit disponible.")
        return

    print("\n Liste des produits :")
    for p in produits:
        print(f"{p['id_produit']} - {p['designation_produit']} | Catégorie: {p['nom_categorie']} | Stock: {p['stock']}")

    # Choix du produit
    try:
        id_produit = int(input("\nID du produit : ").strip())
    except ValueError:
        print(" ID invalide.")
        return

    produit = next((p for p in produits if p['id_produit'] == id_produit), None)
    if not produit:
        print(" Produit non trouvé.")
        return

    # Type de mouvement
    type_mouvement = input("Type de mouvement (E = Entrée / S = Sortie) : ").strip().upper()

    if type_mouvement not in ("E", "S"):
        print(" Type invalide. Tapez E ou S.")
        return

    # Quantité
    try:
        quantite = int(input("Quantité : ").strip())
        if quantite <= 0:
            print(" La quantité doit être positive.")
            return
    except ValueError:
        print(" Quantité invalide.")
        return

    stock_actuel = produit["stock"]

  
    if type_mouvement == "S" and quantite > stock_actuel:
        print(" Stock insuffisant pour cette sortie.")
        return

    try:
        
        if type_mouvement == "E":
            nouveau_stock = stock_actuel + quantite
            type_sql = "ENTREE"
        else:
            nouveau_stock = stock_actuel - quantite
            type_sql = "SORTIE"

        # Mise à jour du stock
        curseur.execute(
            "UPDATE produit SET stock = %s WHERE id_produit = %s",
            (nouveau_stock, id_produit)
        )

        # Insertion dans l'historique
        curseur.execute(
            """
            INSERT INTO mouvement (id_produit, quantite_mouvement, type_mouvement, date_mouvement)
            VALUES (%s, %s, %s, NOW())
            """,
            (id_produit, quantite, type_sql)
        )

        connexion.commit()
        print(f" Mouvement {type_sql} effectué avec succès. Nouveau stock : {nouveau_stock}")

    except mysql.connector.Error as e:
        connexion.rollback()
        print(" Erreur lors du mouvement :", e)
def afficher_mouvements():
    try:
        curseur.execute("""
            SELECT 
                m.id_mouvement,
                p.designation_produit,
                c.nom_categorie,
                m.type_mouvement,
                m.quantite_mouvement,
                m.date_mouvement
            FROM mouvement m
            JOIN produit p ON m.id_produit = p.id_produit
            JOIN categorie c ON p.id_categorie = c.id_categorie
            ORDER BY m.date_mouvement DESC
        """)

        mouvements = curseur.fetchall()

        if not mouvements:
            print("ℹ Aucun mouvement enregistré.")
            return

        print("\n HISTORIQUE DES MOUVEMENTS DE STOCK\n")
        for m in mouvements:
            print(
                f"ID: {m['id_mouvement']} | "
                f"Produit: {m['designation_produit']} | "
                f"Catégorie: {m['nom_categorie']} | "
                f"Type: {m['type_mouvement']} | "
                f"Quantité: {m['quantite_mouvement']} | "
                f"Date: {m['date_mouvement']}"
            )

    except mysql.connector.Error as e:
        print(" Erreur lors de l'affichage des mouvements :", e)


menu_categories()

