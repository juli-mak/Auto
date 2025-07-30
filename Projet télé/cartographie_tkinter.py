import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import datetime

# FICHIER_TELES = "Tele.json"
PLAN_IMAGE = "PlanCESI-RDC.png"
TAILLE_POINT = 10
BASE_TELES = "tele.db"

couleurs_etat = {
    "Fonctionnelle": "green",
    "En panne": "red",
    "Réservée": "blue"
}

class CartographieTeles:
    def __init__(self, root):
     self.root = root
     self.root.title("Cartographie des télés CESI")

     self.conn = sqlite3.connect(BASE_TELES)
     self.creer_table_si_absente()

    # === Cadre principal pour le canvas scrollable ===
     self.frame_canvas = tk.Frame(root)
     self.frame_canvas.pack(fill=tk.BOTH, expand=True)

    # === Scrollbars ===
     self.scroll_y = tk.Scrollbar(self.frame_canvas, orient=tk.VERTICAL)
     self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

     self.scroll_x = tk.Scrollbar(self.frame_canvas, orient=tk.HORIZONTAL)
     self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
     
     self.etage_selectionne = tk.StringVar()
     self.etage_selectionne.set("RDC")  # ou "1er Étage" si tu veux que ce soit l’étage par défaut

    # === Canvas avec scroll ===
     self.canvas = tk.Canvas(
    self.frame_canvas,
    width=1000, height=700,
    bg="lightgray",
    bd=0,
    highlightthickness=0,
    yscrollcommand=self.scroll_y.set,
    xscrollcommand=self.scroll_x.set,
)

     self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
     self.tooltip = tk.Label(root, text="", bg="lightyellow", fg="black", relief="solid", bd=1)
     self.tooltip.place_forget()

    # Initialisation du canvas et des composants
     self.points = {}  # dictionnaire des points affichés
     self.teles = []   # liste des télés en mémoire

     self.canvas.bind("<Button-3>", self.gestion_clic_droit)
     self.canvas.bind("<Motion>", self.cacher_tooltip)

    # Connexion scrollbars ↔ canvas
     self.scroll_y.config(command=self.canvas.yview)
     self.scroll_x.config(command=self.canvas.xview)

    # Chargement images
     img_rdc = Image.open("PlanCESI-RDC.png").resize((1000, 700))
     self.plan_rdc = ImageTk.PhotoImage(img_rdc)
     self.canvas.create_image(0, 0, anchor="nw", image=self.plan_rdc)

     img_1er = Image.open("PlanCESI-R-1.png").resize((1000, 700))
     self.plan_1er = ImageTk.PhotoImage(img_1er)
     self.canvas.create_image(1000, 0, anchor="nw", image=self.plan_1er)
     self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # Chargement des télés pour tous les étages
     self.teles = self.charger_toutes_les_teles()
     for tele in self.teles:
      self.creer_point(tele)
    
    def charger_toutes_les_teles(self):
     cursor = self.conn.cursor()
     cursor.execute("SELECT nom, etat, x, y, salle, etage FROM teles")
     resultats = cursor.fetchall()
     return [
        {"nom": nom, "etat": etat, "x": x, "y": y, "salle": salle, "etage": etage}
        for nom, etat, x, y, salle, etage in resultats
    ]

    def changer_etage(self, etage):
    # Déterminer le fichier image à charger
     if etage == "RDC":
        plan = "PlanCESI-RDC.png"
     elif etage == "1er Étage":
        plan = "PlanCESI-R-1.png"
     else:
        messagebox.showerror("Erreur", f"Étage inconnu : {etage}")
        return

     if not os.path.exists(plan):
        messagebox.showerror("Erreur", f"Image pour {etage} non trouvée : {plan}")
        return

    # Charger et afficher l'image
     img = Image.open(plan)
     img = img.resize((1000, 700))
     self.plan_tk = ImageTk.PhotoImage(img)
     self.canvas.create_image(0, 0, anchor="nw", image=self.plan_tk)

    # Supprimer les points existants
     for point in list(self.points.keys()):
        self.canvas.delete(point)
     self.points.clear()

    # Recharger les télés de l'étage sélectionné
     self.teles = self.charger_teles(etage)
     for tele in self.teles:
        self.creer_point(tele)
    
    def creer_table_si_absente(self):
     self.conn.execute("""
        CREATE TABLE IF NOT EXISTS teles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            etat TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            etage TEXT DEFAULT 'RDC',
            salle TEXT
        )
    """)
     self.conn.commit()

    def gestion_clic_droit(self, event):
     point = self.canvas.find_closest(event.x, event.y)[0]
     tags = self.canvas.gettags(point)

     if "tele" in tags:
        # Suppression si clic sur une télé
        tele = self.points.get(point)
        if tele:
            reponse = tk.messagebox.askyesno("Suppression", f"Supprimer la télé '{tele['nom']}' ?")
            if reponse:
                self.canvas.delete(point)
                self.supprimer_tele_bdd(tele["nom"])
                del self.points[point]
     else:
        # Ajout si clic en dehors
        self.ajouter_tele_dialogue(event)

    def creer_point(self, tele):
        x, y = tele["x"], tele["y"]
        couleur = couleurs_etat.get(tele["etat"], "gray")
        point = self.canvas.create_oval(
            x - TAILLE_POINT, y - TAILLE_POINT,
            x + TAILLE_POINT, y + TAILLE_POINT,
            fill=couleur, tags="tele"
        )
        self.points[point] = tele

        self.canvas.tag_bind(point, "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind(point, "<B1-Motion>", self.drag_motion)
        self.canvas.tag_bind(point, "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind(point, "<Enter>", self.afficher_tooltip)
        self.canvas.tag_bind(point, "<Leave>", self.cacher_tooltip)
        self.canvas.tag_bind(point, "<Double-Button-1>", self.modifier_tele)
    
    def ajouter_tele_dialogue(self, event):
     nom = simpledialog.askstring("Nouvelle télé", "Nom de la télé :", parent=self.root)
     if not nom:
        return
     self.root.update()  # Met à jour le focus sur la fenêtre principale
     self.root.focus_force()

     etat = simpledialog.askstring("État", "État de la télé (Fonctionnelle, En panne, Réservée) :", parent=self.root)
     if etat not in couleurs_etat:
        messagebox.showerror("Erreur", "État invalide. Choisir : Fonctionnelle, En panne ou Réservée.")
        return
     self.root.update()
     self.root.focus_force()

     salle = simpledialog.askstring("Salle", "Nom de la salle :", parent=self.root)
     if not salle:
        salle = "Non précisée"

     nouvelle_tele = {"nom": nom, "etat": etat, "x": event.x, "y": event.y, "salle": salle}
     etage_actuel = self.etage_selectionne.get()
     self.inserer_tele_bdd(nouvelle_tele, etage_actuel)
     self.teles.append(nouvelle_tele)
     self.creer_point(nouvelle_tele)

    def inserer_tele_bdd(self, tele, etage):
     self.conn.execute(
        "INSERT INTO teles (nom, etat, x, y, etage, salle) VALUES (?, ?, ?, ?, ?, ?)",
        (tele["nom"], tele["etat"], tele["x"], tele["y"], etage, tele["salle"])
    )
     self.conn.commit()


    def supprimer_tele_bdd(self, nom):
        self.conn.execute("DELETE FROM teles WHERE nom = ?", (nom,))
        self.conn.commit()

    def drag_start(self, event):
        self.drag_data = {
            "point": self.canvas.find_closest(event.x, event.y)[0],
            "x": event.x,
            "y": event.y
        }

    def drag_motion(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["point"], dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def drag_stop(self, event):
        point = self.drag_data["point"]
        x, y = event.x, event.y
        self.canvas.coords(point, x - TAILLE_POINT, y - TAILLE_POINT, x + TAILLE_POINT, y + TAILLE_POINT)
        tele = self.points[point]
        tele["x"] = x
        tele["y"] = y
        self.conn.execute("UPDATE teles SET x = ?, y = ? WHERE nom = ?", (x, y, tele["nom"]))
        
        # Nouveau calcul d’étage en fonction de la position
        nouvel_etage = "RDC" if x < 1000 else "1er Étage"
        if tele["etage"] != nouvel_etage:
         tele["etage"] = nouvel_etage
         self.conn.execute("UPDATE teles SET etage = ? WHERE nom = ?", (nouvel_etage, tele["nom"]))
        self.conn.commit()
    
    def modifier_tele(self, event):
     point = self.canvas.find_closest(event.x, event.y)[0]
     tele = self.points.get(point)
     if not tele:
        return
     nouvel_etat = simpledialog.askstring(
        "Modifier état",
        f"Nouvel état pour {tele['nom']} (Fonctionnelle, En panne, Réservée) :",
        initialvalue=tele["etat"]
    )
     if nouvel_etat != tele["etat"]:
      self.conn.execute(
        "INSERT INTO reservations (nom_tele, date, action) VALUES (?, ?, ?)",
        (tele["nom"], datetime.now().isoformat(), f"Changement état → {nouvel_etat}")
    )
     self.conn.commit() 
     if nouvel_etat in couleurs_etat:
        tele["etat"] = nouvel_etat
        # Mettre à jour la couleur sur le canvas
        self.canvas.itemconfig(point, fill=couleurs_etat[nouvel_etat])
        self.sauvegarder_teles()
     else:
        tk.messagebox.showerror("Erreur", "État invalide.")

    def afficher_tooltip(self, event):
     point = self.canvas.find_closest(event.x, event.y)[0]
     tele = self.points.get(point)
     if tele:
        texte = f"{tele['nom']} ({tele['etat']})\nSalle : {tele.get('salle', 'N/A')}\nÉtage : {tele['etage']}"
        self.tooltip.config(text=texte)
        self.tooltip.place(
            x=event.x_root + 10 - self.root.winfo_rootx(),
            y=event.y_root + 10 - self.root.winfo_rooty()
        )

    def cacher_tooltip(self, event=None):
        self.tooltip.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = CartographieTeles(root)
    root.mainloop()