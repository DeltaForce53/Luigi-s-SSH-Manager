#!/usr/bin/env python3
import json
import os
import subprocess
import sys

# Nom du fichier où seront stockées les connexions
DB_FILE = "connections.json"


def charger_connexions():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def sauvegarder_connexions(connexions):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(connexions, f, indent=4)


def ajouter_connexion():
    print("\n--- ➕ Ajouter une connexion ---")
    nom = input("Nom (ex: Serveur-Web) : ")
    ip = input("Adresse IP ou Host : ")
    user = input("Nom d'utilisateur : ")

    connexions = charger_connexions()
    connexions[nom] = {"ip": ip, "user": user}
    sauvegarder_connexions(connexions)
    print(f"✅ '{nom}' enregistré !")


def supprimer_connexion():
    connexions = charger_connexions()
    if not connexions:
        print("❌ Aucune connexion à supprimer.")
        return

    print("\n--- 🗑️ Supprimer une connexion ---")
    liste_noms = list(connexions.keys())
    for i, nom in enumerate(liste_noms, 1):
        print(f"{i}. {nom}")

    choix = input("\nNuméro à supprimer (ou 'q') : ")
    if choix.isdigit() and 0 < int(choix) <= len(liste_noms):
        nom_a_suppr = liste_noms[int(choix) - 1]
        del connexions[nom_a_suppr]
        sauvegarder_connexions(connexions)
        print(f"🗑️ '{nom_a_suppr}' a été supprimé.")


def modifier_connexion():
    connexions = charger_connexions()
    if not connexions:
        print("❌ Aucune connexion à modifier.")
        return

    print("\n--- ✏️ Modifier une connexion ---")
    liste_noms = list(connexions.keys())
    for i, nom in enumerate(liste_noms, 1):
        print(f"{i}. {nom}")

    choix = input("\nNuméro à modifier (ou 'q') : ")
    if choix.isdigit() and 0 < int(choix) <= len(liste_noms):
        ancien_nom = liste_noms[int(choix) - 1]
        info = connexions[ancien_nom]

        print(f"Modif de {ancien_nom} (Laissez vide pour garder l'actuel)")
        nouvel_ip = input(f"Nouvel IP [{info['ip']}] : ") or info["ip"]
        nouveau_user = input(f"Nouvel User [{info['user']}] : ") or info["user"]

        connexions[ancien_nom] = {"ip": nouvel_ip, "user": nouveau_user}
        sauvegarder_connexions(connexions)
        print(f"✅ '{ancien_nom}' mis à jour !")


def se_connecter():
    connexions = charger_connexions()
    if not connexions:
        print("❌ Aucune connexion enregistrée.")
        return

    print("\n--- 🚀 Connexions Disponibles ---")
    liste_noms = list(connexions.keys())
    for i, nom in enumerate(liste_noms, 1):
        print(f"{i}. {nom} ({connexions[nom]['user']}@{connexions[nom]['ip']})")

    choix = input("\nChoisir le numéro (ou 'q') : ")
    if choix.isdigit() and 0 < int(choix) <= len(liste_noms):
        cible = connexions[liste_noms[int(choix) - 1]]

        # Environnement UTF-8 pour les icônes eza
        env_ssh = os.environ.copy()
        env_ssh["LC_ALL"] = "en_US.UTF-8"
        env_ssh["LANG"] = "en_US.UTF-8"

        subprocess.run(["ssh", f"{cible['user']}@{cible['ip']}"], env=env_ssh)


def menu():
    while True:
        print("\n" + "=" * 25)
        print("   Luigi's SSH Manager 🚀")
        print("=" * 25)
        print("1. Se connecter")
        print("2. Ajouter une connexion")
        print("3. Modifier une connexion")
        print("4. Supprimer une connexion")
        print("5. Quitter")

        choix = input("\nAction : ")

        if choix == "1":
            se_connecter()
        elif choix == "2":
            ajouter_connexion()
        elif choix == "3":
            modifier_connexion()
        elif choix == "4":
            supprimer_connexion()
        elif choix == "5":
            break
        else:
            print("❌ Option invalide.")


if __name__ == "__main__":
    if sys.platform == "win32":
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    menu()
