# Gestion de Stock – README

## 1. Présentation du projet

Ce projet consiste à mettre en place une application simple de gestion d’inventaire permettant de suivre les produits, leurs catégories et les mouvements de stock (entrées et sorties).
Il est conçu pour aider une structure (magasin, école, organisation, etc.) à connaître l’état réel de son stock, à éviter les pertes et à garder une trace claire de toutes les opérations effectuées.

L’application utilise Python pour la logique métier et MySQL pour la gestion de la base de données.
Elle fonctionne en ligne de commande et reste  simple afin d’être compréhensible et utilisable même par des débutants.
Elle  permet de:

* Ajouter des catégories et des produits,
* Suivre le stock de chaque produit,
* Enregistrer les entrées et sorties de produits,
* Alerter sur les stocks faibles,
* Consulter l’historique des mouvements.

L’objectif est de faciliter le suivi des produits et éviter les pertes ou vols.



2. Étapes de création de la base de données

Voici les grandes étapes pour créer la base de données :

##Étape 1 : MCD (Modèle Conceptuel des Données)

1. Identifier les entités : `Categorie`, `Produit`, `Mouvement`.
2. Identifier les relations :

   * Une catégorie peut contenir plusieurs produits (1,n).
   * Un produit peut avoir plusieurs mouvements (1,n).
3. Définir les attributs de chaque entité :

   * `Categorie` : id_categorie, nom_categorie
   * `Produit` : id_produit, designation_produit, prix_produit, stock, id_categorie
   * `Mouvement` : id_mouvement, id_produit, quantite_mouvement, type_mouvement, date_mouvement

### Étape 2 : MLD (Modèle Logique des Données)

1. Transformer le MCD en tables et clés primaires/étrangères.
2. Définir les types de données pour chaque attribut.
3. Vérifier les relations et cardinalités entre les tables.

### Étape 3 : MPD (Modèle Physique des Données)

1. Traduire le MLD en commandes SQL.
2. Créer les tables dans MySQL avec les types et clés définis.
3. Ajouter les contraintes (clé primaire, clé étrangère, contraintes d’unicité).

### Étape 4 : Création de la base dans MySQL

1. Installer MySQL et créer la base `gestion_stock`.
2. Exécuter les commandes SQL pour créer les tables :

```sql
CREATE TABLE categorie (
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE produit (
    id_produit INT AUTO_INCREMENT PRIMARY KEY,
    designation_produit VARCHAR(100) NOT NULL,
    prix_produit FLOAT NOT NULL,
    stock INT DEFAULT 0,
    id_categorie INT,
    FOREIGN KEY (id_categorie) REFERENCES categorie(id_categorie)
);

CREATE TABLE mouvement (
    id_mouvement INT AUTO_INCREMENT PRIMARY KEY,
    id_produit INT,
    quantite_mouvement INT NOT NULL,
    type_mouvement ENUM('ENTREE','SORTIE') NOT NULL,
    date_mouvement DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_produit) REFERENCES produit(id_produit)
);


Ces étapes permettent de passer du concept au code SQL et de préparer la base pour l’application Python.

---

## 3. Connexion à la base depuis Python

```python
import mysql.connector

try:
    connexion = mysql.connector.connect(
        host="localhost",
        user="amadou",
        password="ama12345",
        database="gestion_stock"
    )
    curseur = connexion.cursor(dictionary=True)
    print("Connecté à la base MySQL")
except:
    print("Erreur de connexion à la base de données")
    exit()
```

---

## 4. Fonctionnalités principales

1. Ajouter une catégorie
2. Ajouter un produit
3. Afficher les produits
4. Gérer les mouvements de stock
5. Supprimer une catégorie
6. Afficher l’historique des mouvements



## 5. Menu principal

1. Ajouter une catégorie
2. Ajouter un produit
3. Afficher les catégories
4. Faire un mouvement de produits
5. Afficher la liste des produits
6. Voir les produits en stock faible
7. Supprimer une catégorie
8. Afficher l’historique des mouvements
9. Quitter

---

## 6. Conclusion
Ce projet de gestion d’inventaire permet de comprendre les étapes essentielles de la conception d’une base de données (MCD, MLD, MPD) ainsi que leur mise en œuvre concrète avec MySQL et Python.
Grâce au système de dump, la base peut être facilement sauvegardée, restaurée ou transférée vers un autre environnement.

Cette application permet de **suivre et gérer facilement un stock de produits**, d’éviter les pertes et de garder un historique clair des mouvements.

