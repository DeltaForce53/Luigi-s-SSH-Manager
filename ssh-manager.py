#!/usr/bin/env python3
import json
import os

# Nom du fichier où seront stockées les connexions
DB_FILE = "connections.json"


def charger_connexions():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def sauvegarder_connexions(connexions):
    with open(DB_FILE, "w") as f:
        json.dump(connexions, f, indent=4)


def ajouter_connexion():
    nom = input("Nom de la connexion (ex: Serveur-Web) : ")
    ip = input("Adresse IP ou Host : ")
    user = input("Nom d'utilisateur : ")
    connexions = charger_connexions()
    connexions[nom] = {"ip": ip, "user": user}
    sauvegarder_connexions(connexions)
    print(f"✅ Connexion '{nom}' enregistrée !")


def se_connecter():
    connexions = charger_connexions()
    if not connexions:
        print("❌ Aucune connexion enregistrée.")
        return

    print("\n--- Tes Connexions ---")
    liste_noms = list(connexions.keys())
    for i, nom in enumerate(liste_noms, 1):
        print(f"{i}. {nom} ({connexions[nom]['user']}@{connexions[nom]['ip']})")

    choix = input("\nChoisir le numéro (ou 'q' pour quitter) : ")
    if choix.isdigit() and 0 < int(choix) <= len(liste_noms):
        cible = connexions[liste_noms[int(choix) - 1]]
        cmd = f"ssh {cible['user']}@{cible['ip']}"
        print(f"🚀 Connexion à {liste_noms[int(choix) - 1]}...")
        os.system(cmd)  # Lance la commande SSH du système


def menu():
    while True:
        print("\n=== GESTIONNAIRE SSH ===")
        print("1. Se connecter")
        print("2. Ajouter une connexion")
        print("3. Quitter")
        choix = input("Action : ")

        if choix == "1":
            se_connecter()
        elif choix == "2":
            ajouter_connexion()
        elif choix == "3":
            break


if __name__ == "__main__":
    menu()
