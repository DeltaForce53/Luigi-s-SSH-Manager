# 🚀 Luigi's SSH Manager

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**Luigi's SSH Manager** est un utilitaire en ligne de commande (CLI) simple, interactif et sécurisé pour gérer et lancer rapidement vos connexions SSH sans avoir à mémoriser les adresses IP, les clés ou les mots de passe.

Créé avec une interface moderne grâce à `rich` et `questionary`, il offre une excellente expérience utilisateur directement depuis votre terminal.

---

## ✨ Fonctionnalités

- 📋 **Interface Interactive** : Menus visuels pour naviguer facilement entre vos serveurs.
- 🔒 **Gestion Sécurisée** : Stockage sécurisé des mots de passe grâce au gestionnaire d'informations d'identification de votre système (via `keyring`).
- 🔑 **Support des Clés SSH** : Lancez vos sessions en utilisant vos fichiers de clés (`.pem`, `.pub`).
- 💾 **Stockage Local** : Vos configurations sont enregistrées localement dans `~/.luigissh/connections.json`.
- ⚡ **Prêt à l'emploi** : Pas besoin d'installer Python. Des exécutables autonomes sont disponibles pour tous les systèmes !

---

## 📥 Installation Rapide (Recommandée)

Vous n'avez **pas besoin d'installer Python**. Téléchargez simplement la dernière version exécutable pour votre système d'exploitation depuis la section **[Releases](../../releases/latest)**.

1. Rendez-vous sur la page des [Releases](../../releases/latest).
2. Téléchargez l'exécutable correspondant à votre système :
   - **Windows** : `luigi-ssh-manager.exe`
   - **macOS** : `luigi-ssh-manager`
   - **Linux** : `luigi-ssh-manager`
3. Lancez le fichier dans votre terminal !

---

## 💻 Utilisation

Ouvrez votre terminal et exécutez le programme. Vous serez accueilli par le menu interactif :

```bash
# Sur Windows
.\luigi-ssh-manager.exe

# Sur Linux / macOS
./luigi-ssh-manager
```

### Options du menu :
1. **🚀 Se connecter** : Lance une connexion SSH vers le serveur sélectionné.
2. **📋 Voir la liste** : Affiche un beau tableau récapitulatif de tous vos serveurs enregistrés.
3. **➕ Ajouter un serveur** : Enregistre une nouvelle connexion (IP, port, utilisateur, méthode d'authentification).
4. **🗑️ Supprimer un serveur** : Retire un serveur de votre liste.
5. **❌ Quitter** : Ferme le programme.

---

## 🛠️ Pour les Développeurs (Exécuter depuis les sources)

Si vous souhaitez modifier le code ou exécuter le script directement avec Python :

### Prérequis
- Python 3.7 ou supérieur

### Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/DeltaForce53/Luigi-s-SSH-Manager.git
   cd Luigi-s-SSH-Manager
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez le script :
   ```bash
   python ssh-manager.py
   ```

---

## 📜 Licence

Ce projet est conçu pour un usage personnel. N'hésitez pas à forker et à l'adapter à vos besoins !
