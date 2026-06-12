# 🚀 Luigi's SSH Manager

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat&logo=go)](https://go.dev/)
[![Platform](https://img.shields.io/badge/Plateformes-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Luigi's SSH Manager** est un outil en ligne de commande (CLI) ultra-rapide, léger et interactif, conçu pour simplifier la gestion et la connexion à vos multiples serveurs SSH. 

Fini les commandes longues à mémoriser et les fichiers de configuration obscurs : naviguez de manière visuelle et sécurisée !

---

## ✨ Fonctionnalités

- ⚡ **Démarrage instantané** : Entièrement réécrit en Go (Golang), l'application est compilée en un binaire natif. Aucune machine virtuelle, aucun interpréteur. Temps de lancement : `< 10ms`.
- 📦 **Zéro dépendance** : Pas besoin d'installer Python, Node.js ou quoi que ce soit d'autre. Téléchargez l'exécutable, lancez-le, ça fonctionne.
- 🔐 **Sécurité Absolue** : Vos mots de passe ne sont **jamais** enregistrés en texte brut. L'application communique directement avec le **Gestionnaire d'informations d'identification** (Windows), le **Trousseau d'accès** (macOS) ou **Secret Service** (Linux) pour chiffrer vos clés avec la sécurité de votre système d'exploitation.
- 🎨 **Interface Interactive** : Menus visuels intuitifs, saisie masquée des mots de passe, et tableaux propres pour lister vos serveurs.
- 🌐 **Cross-Platform** : Fonctionne parfaitement sous Windows, macOS (Intel & Apple Silicon) et Linux.

---

## 📥 Installation

Allez dans la page [**Releases**](https://github.com/DeltaForce53/Luigi-s-SSH-Manager/releases) de ce dépôt pour télécharger la dernière version.

### 🪟 Windows
1. Téléchargez le fichier **`LuigiSSHManager-Setup.exe`**.
2. Lancez-le pour installer l'application.
3. Lors de l'installation, cochez l'option pour ajouter l'application au `PATH`. 
4. Ouvrez un terminal (CMD ou PowerShell) et lancez simplement :
   ```powershell
   luigi-ssh-manager
   ```
   *(Astuce : Si vous préférez la commande courte, vous pouvez renommer l'exécutable `luigi-ssh-manager.exe` en `ssh-luigi.exe` dans `C:\Program Files\LuigiSSHManager`)*

### 🍎 macOS & 🐧 Linux
1. Téléchargez l'exécutable correspondant à votre architecture (ex: `luigi-ssh-manager-macos` ou `luigi-ssh-manager-linux`).
2. Rendez le fichier exécutable via votre terminal :
   ```bash
   chmod +x luigi-ssh-manager-macos
   ```
3. Déplacez-le et renommez-le en `ssh-luigi` dans un dossier appartenant à votre `$PATH` (comme `/usr/local/bin`) pour y avoir accès partout :
   ```bash
   sudo mv luigi-ssh-manager-macos /usr/local/bin/ssh-luigi
   ```

---

## 🛠️ Utilisation

Il suffit de lancer l'application via votre terminal avec la commande :
```bash
ssh-luigi
```

Un menu interactif apparaîtra vous permettant de :
- `🚀 Se connecter` : Choisir un serveur pré-enregistré et lancer immédiatement une session SSH.
- `📋 Voir la liste` : Afficher un tableau clair de vos serveurs (Nom, IP, Port, Type d'authentification).
- `➕ Ajouter un serveur` : Ajouter une nouvelle machine (par mot de passe ou clé SSH `.pem`/`.pub`).
- `🗑️ Supprimer un serveur` : Retirer proprement une configuration et nettoyer le trousseau de clés de l'OS.

### 📂 Où sont stockées mes données ?
- **Adresses et IP** : Sauvegardées localement dans le fichier `~/.luigissh/connections.json` sur votre propre machine.
- **Mots de passe** : Chiffrés au sein du Keychain de votre OS (aucun risque de fuite de données si vous partagez le fichier json).

---

## 💻 Développement (Compiler soi-même)

Si vous souhaitez modifier le code source et recompiler l'outil vous-même :

1. Assurez-vous d'avoir [Go (1.21 ou supérieur)](https://go.dev/dl/) installé.
2. Clonez ce dépôt :
   ```bash
   git clone https://github.com/DeltaForce53/Luigi-s-SSH-Manager.git
   cd Luigi-s-SSH-Manager
   ```
3. Téléchargez les dépendances :
   ```bash
   go mod tidy
   ```
4. Compilez :
   ```bash
   go build -o luigi-ssh-manager main.go
   ```

*(Sous Linux, le paquet `libsecret-1-dev` est requis pour la compilation du module de sécurité).*

---
*Créé avec passion par LuigiLePoussin & AI* 🚀
