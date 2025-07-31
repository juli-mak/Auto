import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def renommer_fichiers(dossier):
    fichiers = os.listdir(dossier)
    renommés = []

    for fichier in fichiers:
        chemin_complet = os.path.join(dossier, fichier)
        if os.path.isfile(chemin_complet):
            nom, ext = os.path.splitext(fichier)
            
            nom_utilisateur = simpledialog.askstring("Nom", f"Entrer le **Nom** pour : {fichier}")
            prenom_utilisateur = simpledialog.askstring("Prénom", f"Entrer le **Prénom** pour : {fichier}")
            rubrique = simpledialog.askstring("Rubrique", f"Entrer la **RUBRIQUE** (ex : FACTURATION, IR...) pour : {fichier}")
            description = simpledialog.askstring("Description", f"Entrer la **Description** pour : {fichier}")

            if not all([nom_utilisateur, prenom_utilisateur, rubrique, description]):
                messagebox.showwarning("Annulé", f"Renommage annulé pour : {fichier}")
                continue

            nouveau_nom = f"{nom_utilisateur.strip().upper()} {prenom_utilisateur.strip().capitalize()}_{rubrique.upper()}_{description}{ext}"
            nouveau_chemin = os.path.join(dossier, nouveau_nom)

            os.rename(chemin_complet, nouveau_chemin)
            renommés.append(nouveau_nom)

    if renommés:
        messagebox.showinfo("Succès", f"{len(renommés)} fichier(s) renommé(s) avec succès.")
    else:
        messagebox.showinfo("Aucun renommage", "Aucun fichier n'a été renommé.")

# Interface graphique minimale
def choisir_dossier_et_lancer():
    dossier = filedialog.askdirectory(title="Sélectionner le dossier contenant les fichiers à renommer")
    if dossier:
        renommer_fichiers(dossier)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    choisir_dossier_et_lancer()
