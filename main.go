package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"

	"github.com/AlecAivazis/survey/v2"
	"github.com/fatih/color"
	"github.com/jedib0t/go-pretty/v6/table"
	"github.com/zalando/go-keyring"
)

type Connection struct {
	IP      string `json:"ip"`
	User    string `json:"user"`
	Port    string `json:"port"`
	KeyPath string `json:"key_path"`
}

var dbFile string

func init() {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("Erreur: Impossible de trouver le dossier utilisateur:", err)
		os.Exit(1)
	}
	dbDir := filepath.Join(homeDir, ".luigissh")
	os.MkdirAll(dbDir, 0755)
	dbFile = filepath.Join(dbDir, "connections.json")
}

func loadConnections() map[string]Connection {
	conns := make(map[string]Connection)
	data, err := os.ReadFile(dbFile)
	if err == nil {
		json.Unmarshal(data, &conns)
	}
	return conns
}

func saveConnections(conns map[string]Connection) {
	data, _ := json.MarshalIndent(conns, "", "    ")
	os.WriteFile(dbFile, data, 0644)
}

func main() {
	for {
		fmt.Println()
		action := ""
		prompt := &survey.Select{
			Message: "Luigi SSH Manager - Menu",
			Options: []string{
				"🚀 Se connecter",
				"📋 Voir la liste",
				"➕ Ajouter un serveur",
				"🗑️ Supprimer un serveur",
				"❌ Quitter",
			},
		}
		survey.AskOne(prompt, &action)

		switch action {
		case "🚀 Se connecter":
			connect()
		case "📋 Voir la liste":
			listConns()
		case "➕ Ajouter un serveur":
			addConn()
		case "🗑️ Supprimer un serveur":
			deleteConn()
		case "❌ Quitter":
			color.New(color.Italic).Println("À bientôt Luigi !")
			return
		default:
			return
		}
	}
}

func connect() {
	conns := loadConnections()
	if len(conns) == 0 {
		color.Red("Erreur : Aucun serveur trouvé.")
		return
	}

	names := []string{"🔙 Retour"}
	for name := range conns {
		names = append(names, name)
	}
	sort.Strings(names)

	choix := ""
	prompt := &survey.Select{
		Message: "🚀 Vers quelle destination voulez-vous aller ?",
		Options: names,
	}
	survey.AskOne(prompt, &choix)

	if choix == "" || choix == "🔙 Retour" {
		return
	}

	cible := conns[choix]
	args := []string{fmt.Sprintf("%s@%s", cible.User, cible.IP), "-p", cible.Port}
	if cible.KeyPath != "" {
		args = append(args, "-i", cible.KeyPath)
	}

	color.Yellow("Connexion en cours vers %s...", choix)

	cmd := exec.Command("ssh", args...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		color.Red("Erreur lors de la connexion : %v", err)
	}
}

func listConns() {
	conns := loadConnections()
	if len(conns) == 0 {
		color.Yellow("Aucune connexion enregistrée.")
		return
	}

	t := table.NewWriter()
	t.SetOutputMirror(os.Stdout)
	t.SetTitle("📋 Liste des Serveurs")
	t.AppendHeader(table.Row{"Nom", "Utilisateur", "Hôte", "Port", "Auth"})

	names := []string{}
	for name := range conns {
		names = append(names, name)
	}
	sort.Strings(names)

	for _, name := range names {
		info := conns[name]
		auth := "🔒 Pwd/Agent"
		if info.KeyPath != "" {
			auth = "🔑 Clé"
		}
		t.AppendRow([]interface{}{name, info.User, info.IP, info.Port, auth})
	}
	t.SetStyle(table.StyleLight)
	t.Render()
}

func addConn() {
	color.Green("➕ AJOUTER UN NOUVEAU SERVEUR")

	nom := ""
	survey.AskOne(&survey.Input{Message: "Nom de la connexion (ex: Serveur-Web) :"}, &nom, survey.WithValidator(survey.Required))

	ip := ""
	survey.AskOne(&survey.Input{Message: "Adresse IP ou Hostname :"}, &ip, survey.WithValidator(survey.Required))

	user := ""
	survey.AskOne(&survey.Input{Message: "Nom d'utilisateur :"}, &user, survey.WithValidator(survey.Required))

	port := "22"
	survey.AskOne(&survey.Input{Message: "Port :", Default: "22"}, &port)

	methode := ""
	survey.AskOne(&survey.Select{
		Message: "Méthode d'authentification :",
		Options: []string{
			"Mot de passe (Sécurisé par Keyring)",
			"Clé SSH (Fichier .pem/.pub)",
			"Aucune / Agent SSH",
		},
	}, &methode)

	keyPath := ""
	if methode == "Mot de passe (Sécurisé par Keyring)" {
		pwd := ""
		survey.AskOne(&survey.Password{Message: "Entrez le mot de passe :"}, &pwd)
		if pwd != "" {
			err := keyring.Set("luigissh", nom, pwd)
			if err != nil {
				color.Red("Erreur lors de l'enregistrement du mot de passe: %v", err)
			}
		}
	} else if methode == "Clé SSH (Fichier .pem/.pub)" {
		survey.AskOne(&survey.Input{Message: "Chemin complet vers la clé :"}, &keyPath)
	}

	conns := loadConnections()
	conns[nom] = Connection{
		IP:      ip,
		User:    user,
		Port:    port,
		KeyPath: keyPath,
	}
	saveConnections(conns)
	color.Green("\n✅ '%s' a été configuré avec succès !\n", nom)
}

func deleteConn() {
	conns := loadConnections()
	if len(conns) == 0 {
		color.Yellow("Aucune connexion enregistrée.")
		return
	}

	names := []string{}
	for name := range conns {
		names = append(names, name)
	}
	sort.Strings(names)

	choix := ""
	survey.AskOne(&survey.Select{Message: "Sélectionnez le serveur à supprimer :", Options: names}, &choix)

	if choix != "" {
		confirm := false
		survey.AskOne(&survey.Confirm{Message: fmt.Sprintf("Êtes-vous sûr de vouloir supprimer %s ?", choix)}, &confirm)
		if confirm {
			delete(conns, choix)
			saveConnections(conns)
			keyring.Delete("luigissh", choix) // ignore err
			color.Red("🗑️ %s supprimé.", choix)
		}
	}
}
