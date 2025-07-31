import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import csv
from PIL import Image, ImageTk

# Dossier des scripts
dossier_selectionne = ""
SCRIPT_DIR = r"L:\Scripts\scripts"

# Mapping des scripts : nom du bouton -> (nom du script, description)
SCRIPTS = {
    "Créer Dossiers apprenants": ("Arbo_Etudiants.BAT", "Création arborescence dans les dossiers d’apprenants"),
    #"Copier fichiers apprenants": ("Fichiers_etudiants.bat", "Copie des fichiers dans les dossiers des apprenants"),
    "Créer Dossiers promotions": ("script_arbo.bat", "Création arborescence dans les dossiers de promotions"),
    #"Copier fichiers promotions": ("copie_promotion fichiers.bat", "Copie fichiers dans les dossiers de promotions"),
    "Archiver dossiers promotions": ("Archivage_promo.bat", "Archive les dossiers promotions selon une liste"),
    # Tu peux ajouter archivage.bat si tu veux lancer sans argument
    # "Archivage personnalisé": ("archivage.bat", "Archivage avec argument promotion ou étudiant"),
}

def lancer_script(nom_script):
    if not dossier_source:
        messagebox.showwarning("Dossier requis", "Veuillez d'abord sélectionner un dossier source.")
        return
    chemin_script = os.path.join(SCRIPT_DIR, nom_script)
    if os.path.isfile(chemin_script):
        try:
            #subprocess.run(['cmd', '/c', chemin_script], check=True)
            result = subprocess.run(['cmd', '/c', chemin_script], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Succès", f"Script exécuté : {nom_script}")
            else:
                messagebox.showerror("Erreur dans le script", f"Erreur lors de l'exécution de {nom_script} :\n\n{result.stderr.strip() or result.stdout.strip()}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Exception lors de l'exécution :\n{e}")
    else:
        messagebox.showerror("Fichier introuvable", f"Le script suivant est introuvable :\n{chemin_script}")
def lancer_script_avec_source(nom_script):
    if not dossier_source:
        messagebox.showwarning("Dossier requis", "Veuillez d'abord sélectionner un dossier source.")
        return
    chemin_script = os.path.join(SCRIPT_DIR, nom_script)
    if os.path.isfile(chemin_script):
        try:
            result = subprocess.run(['cmd', '/c', chemin_script, dossier_source], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Succès", f"Script exécuté avec source : {nom_script}")
            else:
                messagebox.showerror("Erreur dans le script", f"Erreur :\n\n{result.stderr.strip() or result.stdout.strip()}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Exception :\n{e}")
    else:
        messagebox.showerror("Fichier introuvable", f"Le script suivant est introuvable :\n{chemin_script}")
# Lancement personnalisé du script d’archivage avec argument
def lancer_archivage(personne, mode):
    script = os.path.join(SCRIPT_DIR, "archivage.bat")
    if os.path.exists(script):
        try:
            result = subprocess.run(
                ['cmd', '/c', script, personne],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                messagebox.showinfo("Succès", f"Archivage {mode} exécuté pour : {personne}")
            else:
                messagebox.showerror("Erreur dans l'archivage", f"Erreur lors de l’archivage pour {personne} :\n\n{result.stderr.strip() or result.stdout.strip()}")
        except Exception as e:
            messagebox.showerror("Exception", f"Une exception s'est produite :\n{e}")
    else:
        messagebox.showerror("Introuvable", "Le script archivage.bat est introuvable.")
# Lecture des promotions depuis etudiants.csv (colonne 3 = promotion)
def charger_promotions():
    promotions = set()
    try:
        with open(os.path.join(SCRIPT_DIR, "etudiants.csv"), newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # skip header
            for row in reader:
                if len(row) > 2:
                    promotions.add(row[2].strip())
            print("✅ Promotions mises à jour :", promotions)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier etudiants.csv\n{e}")
    return sorted(promotions) if promotions else ["Aucune"]

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Interface de gestion des scripts")
fenetre.geometry("800x850")
fenetre.resizable(False, False)

# Titre
titre = tk.Label(fenetre, text="Outils de gestion des apprenants et promotions", font=("Helvetica", 14, "bold"))
titre.pack(pady=10)
btn_fichiers_apprenants = tk.Button(
    fenetre,
    text="Copier fichiers apprenants",
    command=lambda: lancer_script_avec_source("Fichiers_etudiants.bat"),
    width=50,
    height=2,
    bg="#5EAC94",
    fg="white"
)
btn_fichiers_apprenants.pack(pady=4)

btn_fichiers_promotions = tk.Button(
    fenetre,
    text="Copier fichiers promotions",
    command=lambda: lancer_script_avec_source("copie_promotion fichiers.bat"),
    width=50,
    height=2,
    bg="#5EAC94",
    fg="white"
)
btn_fichiers_promotions.pack(pady=4)

# === Boutons pour les scripts généraux ===
for libelle, (nom_script, description) in SCRIPTS.items():
    btn = tk.Button(
        fenetre,
        text=libelle,
        command=lambda s=nom_script: lancer_script(s),
        width=50,
        height=2,
        bg="#5EAC94",
        fg="white"
    )
    btn.pack(pady=4)
def choisir_dossier_source():
    global dossier_source
    chemin = filedialog.askdirectory(title="Choisir le dossier source des fichiers à copier")
    if chemin:
        dossier_source = chemin
        label_source.config(text=f"Dossier sélectionné : {chemin}")

label_source = tk.Label(fenetre, text="Aucun dossier source sélectionné", fg="blue")
label_source.pack()

btn_choisir_source = tk.Button(fenetre, text="📂 Choisir le dossier source de fichiers", command=choisir_dossier_source, bg="#FF9800", fg="white")
btn_choisir_source.pack(pady=5)

def charger_promotions_et_mettre_a_jour_menu():
    promotions = charger_promotions()
    if not promotions:
        promotions = ["Aucune"]
    promo_var.set(promotions[0])
    
    menu = promo_menu["menu"]
    menu.delete(0, "end")
    for p in promotions:
        menu.add_command(label=p, command=lambda value=p: promo_var.set(value))

bouton_actualiser = tk.Button(
    fenetre,
    text="Actualiser les promotions",
    command=charger_promotions_et_mettre_a_jour_menu
)
bouton_actualiser.pack(pady=5)

# === Zone pour archivage personnalisé ===
tk.Label(fenetre, text="Archivage Des Apprenants :", font=("Helvetica", 12, "bold")).pack(pady=10)

frame_archivage = tk.Frame(fenetre)
frame_archivage.pack(pady=5)

tk.Label(frame_archivage, text="Mode :").grid(row=0, column=0, sticky="e")
mode_var = tk.StringVar(value="promotion")
mode_menu = tk.OptionMenu(frame_archivage, mode_var, "promotion", "etudiant")
mode_menu.grid(row=0, column=1, padx=5)

tk.Label(frame_archivage, text="Promotion :").grid(row=1, column=0, sticky="e")
promo_var = tk.StringVar()
promotions = charger_promotions()
promo_var.set(promotions[0])
promo_menu = tk.OptionMenu(frame_archivage, promo_var, *promotions)
promo_menu.grid(row=1, column=1, padx=5)

tk.Label(frame_archivage, text="Nom étudiant :").grid(row=0, column=2, sticky="e")
nom_var = tk.StringVar()
nom_entry = tk.Entry(frame_archivage, textvariable=nom_var, width=30)
nom_entry.grid(row=0, column=3, padx=5)

def actualiser_champs(*args):
    mode = mode_var.get()
    if mode == "promotion":
        promo_menu.config(state="normal")
        nom_entry.config(state="disabled")
    else:
        promo_menu.config(state="disabled")
        nom_entry.config(state="normal")

mode_var.trace_add('write', actualiser_champs)
actualiser_champs()

def lancer_archivage_depuis_interface():
    mode = mode_var.get()
    if mode == "promotion":
        nom = promo_var.get()
        if nom == "Aucune":
            messagebox.showwarning("Attention", "Aucune promotion trouvée dans le fichier CSV.")
            return
    else:
        nom = nom_var.get().strip()
        if not nom:
            messagebox.showwarning("Saisie requise", "Veuillez entrer le nom de l’étudiant.")
            return
    lancer_archivage(nom, mode)

tk.Button(frame_archivage, text="Lancer l’archivage", command=lancer_archivage_depuis_interface, bg="#2196F3", fg="white").grid(row=0, column=4, rowspan=2, padx=10)

# === Explorateur de fichiers avec recherche ===
tk.Label(fenetre, text="Explorateur de dossiers :", font=("Helvetica", 12, "bold")).pack(pady=10)

frame_explorer = tk.Frame(fenetre)
frame_explorer.pack()

# Dossier en cours
chemin_dossier = tk.StringVar()

def choisir_dossier():
    global dossier_selectionne
    chemin = filedialog.askdirectory()
    if chemin:
        afficher_contenu_dossier(chemin)

def retour_dossier():
    global dossier_selectionne
    if dossier_selectionne:
        dossier_parent = os.path.dirname(dossier_selectionne)
        if os.path.isdir(dossier_parent):
            afficher_contenu_dossier(dossier_parent)

def afficher_contenu_dossier(chemin):
    global dossier_selectionne
    dossier_selectionne = chemin
    liste_fichiers.delete(0, tk.END)
    image_label.config(image="")  # Nettoyer image
    image_label.image = None
    try:
        contenu = sorted(os.listdir(chemin), key=lambda x: (not os.path.isdir(os.path.join(chemin, x)), x.lower()))
        for item in contenu:
            chemin_item = os.path.join(chemin, item)
            if os.path.isdir(chemin_item):
                liste_fichiers.insert(tk.END, f"📁 {item}")
            else:
                liste_fichiers.insert(tk.END, f"📄 {item}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def double_clic(event):
    selection = liste_fichiers.curselection()
    if not selection:
        return
    nom_item = liste_fichiers.get(selection[0])[2:]  # Retire l’icône 📁/📄
    chemin = os.path.join(dossier_selectionne, nom_item)
    if os.path.isdir(chemin):
        afficher_contenu_dossier(chemin)
    else:
        try:
            if chemin.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                image = Image.open(chemin)
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                image_label.config(image=photo)
                image_label.image = photo
            else:
                os.startfile(chemin)
                image_label.config(image="")
                image_label.image = None
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir :\n{chemin}")

# Fonction de recherche
def rechercher(event):
    texte = champ_recherche.get().lower()
    liste_fichiers.delete(0, tk.END)
    if dossier_selectionne:
        try:
            contenu = sorted(os.listdir(dossier_selectionne),
                             key=lambda x: (not os.path.isdir(os.path.join(dossier_selectionne, x)), x.lower()))
            for item in contenu:
                if texte in item.lower():
                    chemin_item = os.path.join(dossier_selectionne, item)
                    if os.path.isdir(chemin_item):
                        liste_fichiers.insert(tk.END, f"📁 {item}")
                    else:
                        liste_fichiers.insert(tk.END, f"📄 {item}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

# Gestion du placeholder
def on_focus_in(event):
    if champ_recherche.get() == "🔍 Rechercher":
        champ_recherche.delete(0, tk.END)
        champ_recherche.config(fg="black")

def on_focus_out(event):
    if champ_recherche.get() == "":
        champ_recherche.insert(0, "🔍 Rechercher")
        champ_recherche.config(fg="grey")

# Widget Entry avec placeholder
champ_recherche = tk.Entry(frame_explorer, width=40, fg="grey")
champ_recherche.insert(0, "🔍 Rechercher")
champ_recherche.bind("<FocusIn>", on_focus_in)
champ_recherche.bind("<FocusOut>", on_focus_out)
champ_recherche.bind("<KeyRelease>", rechercher)
champ_recherche.pack()

btn_dossier = tk.Button(frame_explorer, text="📁 Choisir un dossier", command=choisir_dossier)
btn_dossier.pack(pady=5)
bouton_retour = tk.Button(frame_explorer, text="⬅ Retour", command=retour_dossier)
bouton_retour.pack()


sb = tk.Scrollbar(frame_explorer, orient="vertical")
liste_fichiers = tk.Listbox(frame_explorer, width=70, height=15, yscrollcommand=sb.set)
sb.config(command=liste_fichiers.yview)

liste_fichiers.pack(side="left", fill="both", expand=True)
sb.pack(side="right", fill="y")
liste_fichiers.bind("<Double-Button-1>", double_clic)
# --- Interface ---
#fenetre = tk.Tk()
#frame_explorer = tk.Frame(fenetre)
#frame_explorer.pack()

# Image Label défini globalement
image_label = tk.Label(frame_explorer)
image_label.pack()

# Exemple : appel initial avec un dossier par défaut
dossier_selectionne = os.getcwd()
afficher_contenu_dossier(dossier_selectionne)

# Lancement de l’interface
fenetre.mainloop()
