import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from tkinter import simpledialog
#from subprocess import CREATE_NO_WINDOW

# Dossier des scripts
SCRIPT_DIR = r"L:\Scripts"

# Mapping des scripts : nom du bouton -> (nom du script, description)
SCRIPTS = {
    "Créer arborescence apprenants": ("Arbo_Etudiants.BAT", "Création arborescence dans les dossiers d’apprenants"),
    "Copier fichiers apprenants": ("Fichiers_etudiants.bat", "Copie des fichiers dans les dossiers des apprenants"),
    "Archiver dossiers apprenants": ("archivage.bat", "Archive les dossiers apprenants par promotion"),
    "Créer arborescence promotions": ("script_arbo.bat", "Création arborescence dans les dossiers de promotions"),
    "Copier fichiers promotions": ("copie_promotion fichiers.bat", "Copie fichiers dans les dossiers de promotions"),
    "Archiver dossiers promotions": ("Archivage_promo.bat", "Archive les dossiers promotions selon une liste"),
}

def lancer_script(nom_script):
    chemin_script = os.path.join(SCRIPT_DIR, nom_script)

    if not os.path.isfile(chemin_script):
        messagebox.showerror("Fichier introuvable", f"Le script suivant est introuvable :\n{chemin_script}")
        return

    # Si on veut archiver les apprenants, demander une saisie utilisateur
    if nom_script.lower() == "archivage.bat":
        input_value = tk.simpledialog.askstring("Saisie requise", "Entrez le nom de la promotion ou de l'étudiant à archiver :")
        if input_value:
            try:
                #subprocess.run(['cmd', '/c', chemin_script], check=True)
                subprocess.Popen(chemin_script, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                messagebox.showinfo("Succès", f"Archivage terminé pour : {input_value}")
            except subprocess.CalledProcessError:
                messagebox.showerror("Erreur", f"Erreur lors de l’archivage de : {input_value}")
        else:
            messagebox.showinfo("Annulé", "Aucune promotion ou étudiant saisi.")
    else:
        try:
            #subprocess.run(['cmd', '/c', chemin_script], check=True)
            subprocess.Popen(chemin_script, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            messagebox.showinfo("Succès", f"Script exécuté : {nom_script}")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", f"Échec lors de l'exécution du script : {nom_script}")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Interface de gestion des scripts")
fenetre.geometry("500x400")
fenetre.resizable(False, False)

# Titre
titre = tk.Label(fenetre, text="Outils de gestion des apprenants et promotions", font=("Helvetica", 14, "bold"))
titre.pack(pady=20)

# Création des boutons
for libelle, (nom_script, description) in SCRIPTS.items():
    btn = tk.Button(
        fenetre,
        text=libelle,
        command=lambda s=nom_script: lancer_script(s),
        width=50,
        height=2,
        bg="#4CAF50",
        fg="white"
    )
    btn.pack(pady=5)

# Lancement de l'interface
fenetre.mainloop()