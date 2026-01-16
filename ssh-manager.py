#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

import keyring
import questionary
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

# Initialisation de la console Rich pour les couleurs et styles
console = Console()

# Configuration des chemins (Stockage dans le dossier utilisateur)
DB_DIR = Path.home() / ".luigissh"
DB_DIR.mkdir(exist_ok=True)
DB_FILE = DB_DIR / "connections.json"


def charger_connexions():
    """Charge les données du fichier JSON."""
    if not DB_FILE.exists():
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def sauvegarder_connexions(connexions):
    """Sauvegarde les données dans le fichier JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(connexions, f, indent=4)


def ajouter_connexion():
    """Interface stylisée pour ajouter un serveur."""
    console.print(
        Panel("[bold green]➕ AJOUTER UN NOUVEAU SERVEUR[/bold green]", expand=False)
    )

    nom = questionary.text("Nom de la connexion (ex: Serveur-Web) :").ask()
    if not nom:
        return

    ip = questionary.text("Adresse IP ou Hostname :").ask()
    user = questionary.text("Nom d'utilisateur :").ask()
    port = questionary.text("Port (par défaut 22) :", default="22").ask()

    methode = questionary.select(
        "Méthode d'authentification :",
        choices=[
            "Mot de passe (Sécurisé par Keyring)",
            "Clé SSH (Fichier .pem/.pub)",
            "Aucune / Agent SSH",
        ],
    ).ask()

    path_cle = ""
    if methode == "Mot de passe (Sécurisé par Keyring)":
        pwd = questionary.password("Entrez le mot de passe :").ask()
        if pwd:
            keyring.set_password("luigissh", nom, pwd)
    elif methode == "Clé SSH (Fichier .pem/.pub)":
        path_cle = questionary.text("Chemin complet vers la clé :").ask()

    connexions = charger_connexions()
    connexions[nom] = {"ip": ip, "user": user, "port": port, "key_path": path_cle}
    sauvegarder_connexions(connexions)
    console.print(
        f"\n[bold green]✅ '{nom}' a été configuré avec succès ![/bold green]\n"
    )


def afficher_liste():
    """Affiche un beau tableau des serveurs enregistrés."""
    connexions = charger_connexions()
    if not connexions:
        console.print("[yellow]Aucune connexion enregistrée.[/yellow]")
        return

    table = Table(
        title="📋 Liste des Serveurs", header_style="bold magenta", border_style="blue"
    )
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("Utilisateur", style="green")
    table.add_column("Hôte", style="white")
    table.add_column("Port", style="dim")
    table.add_column("Auth", style="italic")

    for nom, info in connexions.items():
        auth = "🔑 Clé" if info.get("key_path") else "🔒 Pwd/Agent"
        table.add_row(nom, info["user"], info["ip"], info["port"], auth)

    console.print(table)


def se_connecter():
    """Menu interactif pour lancer une session SSH."""
    connexions = charger_connexions()
    if not connexions:
        console.print("[bold red]Erreur : Aucun serveur trouvé.[/bold red]")
        return

    choix = questionary.select(
        "🚀 Vers quelle destination voulez-vous aller ?",
        choices=list(connexions.keys()) + [questionary.Separator(), "🔙 Retour"],
    ).ask()

    if choix and choix != "🔙 Retour":
        cible = connexions[choix]
        cmd = ["ssh", f"{cible['user']}@{cible['ip']}", "-p", cible["port"]]

        if cible.get("key_path"):
            cmd.extend(["-i", cible["key_path"]])

        console.print(
            Panel(
                f"[bold yellow]Connexion en cours vers {choix}...[/]",
                border_style="yellow",
            )
        )

        # Note : On laisse SSH gérer la demande de mot de passe interactivement.
        # Keyring est utilisé ici pour la gestion future ou pour des scripts automatisés.
        try:
            subprocess.run(cmd)
        except Exception as e:
            console.print(f"[bold red]Erreur lors de la connexion : {e}[/bold red]")


def supprimer_connexion():
    """Supprime proprement une connexion et son secret."""
    connexions = charger_connexions()
    choix = questionary.select(
        "Sélectionnez le serveur à supprimer :", choices=list(connexions.keys())
    ).ask()

    if choix:
        confirm = questionary.confirm(
            f"Êtes-vous sûr de vouloir supprimer {choix} ?"
        ).ask()
        if confirm:
            del connexions[choix]
            sauvegarder_connexions(connexions)
            try:
                keyring.delete_password("luigissh", choix)
            except:
                pass
            console.print(f"[red]🗑️ {choix} supprimé.[/red]")


def menu_principal():
    """Boucle principale du gestionnaire."""
    while True:
        console.print("\n")
        action = questionary.select(
            "Luigi SSH Manager - Menu",
            choices=[
                "🚀 Se connecter",
                "📋 Voir la liste",
                "➕ Ajouter un serveur",
                "🗑️ Supprimer un serveur",
                "❌ Quitter",
            ],
            style=questionary.Style(
                [
                    ("pointer", "fg:#00ff00 bold"),
                    ("highlighted", "fg:#00ff00 bold"),
                ]
            ),
        ).ask()

        if action == "🚀 Se connecter":
            se_connecter()
        elif action == "📋 Voir la liste":
            afficher_liste()
        elif action == "➕ Ajouter un serveur":
            ajouter_connexion()
        elif action == "🗑️ Supprimer un serveur":
            supprimer_connexion()
        elif action == "❌ Quitter":
            console.print("[italic]À bientôt Luigi ![/italic]")
            break


if __name__ == "__main__":
    # Correction encodage Windows
    if sys.platform == "win32":
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    menu_principal()
