"""
Vérificateur de mots de passe - 100 % local
Aucun mot de passe n'est envoyé sur Internet ni enregistré.
"""
import re
import secrets
import string
import tkinter as tk
from tkinter import ttk

# Petite liste de mots de passe très courants (tu peux l'agrandir)
MOTS_COURANTS = {
    "123456", "12345678", "123456789", "password", "motdepasse", "azerty",
    "qwerty", "000000", "111111", "soleil", "bonjour", "admin", "iloveyou",
    "abc123", "password1", "football", "princesse", "loulou", "doudou",
}

SUITES = ["0123456789", "abcdefghijklmnopqrstuvwxyz", "azertyuiop", "qwertyuiop"]


def contient_suite(mdp):
    """Détecte les suites de 3 caractères comme 123, abc, aze."""
    m = mdp.lower()
    for suite in SUITES:
        for i in range(len(suite) - 2):
            if suite[i:i + 3] in m or suite[i:i + 3][::-1] in m:
                return True
    return False


def analyser(mdp):
    """Retourne les critères, le score sur 100 et les recommandations."""
    criteres = {
        "Longueur (12+)": len(mdp) >= 12,
        "Majuscules": bool(re.search(r"[A-Z]", mdp)),
        "Minuscules": bool(re.search(r"[a-z]", mdp)),
        "Chiffres": bool(re.search(r"[0-9]", mdp)),
        "Symboles": bool(re.search(r"[^A-Za-z0-9]", mdp)),
    }
    conseils = []

    if not mdp:
        return criteres, 0, ["Tapez un mot de passe pour l'analyser."]

    # Points positifs
    score = min(40, max(0, (len(mdp) - 4) * 3))
    score += sum(list(criteres.values())[1:]) * 10
    if len(set(mdp)) >= len(mdp) * 0.7:
        score += 20  # bonne variété de caractères

    # Pénalités
    if re.search(r"(.)\1\1", mdp):
        score -= 15
        conseils.append("Évitez les caractères répétés (aaa, 111).")
    if contient_suite(mdp):
        score -= 15
        conseils.append("Évitez les suites comme 123, abc ou azerty.")
    if mdp.lower() in MOTS_COURANTS:
        score = min(score, 5)
        conseils.append("Ce mot de passe est très connu : changez-le immédiatement !")

    # Conseils selon les critères manquants
    if not criteres["Longueur (12+)"]:
        conseils.append("Utilisez au moins 12 caractères.")
    if not criteres["Majuscules"]:
        conseils.append("Ajoutez des lettres majuscules.")
    if not criteres["Minuscules"]:
        conseils.append("Ajoutez des lettres minuscules.")
    if not criteres["Chiffres"]:
        conseils.append("Ajoutez des chiffres.")
    if not criteres["Symboles"]:
        conseils.append("Ajoutez un symbole comme ! # @ ou ?")

    conseils.append("Utilisez un mot de passe unique pour chaque compte.")
    conseils.append("Activez la double authentification (MFA).")

    return criteres, max(0, min(100, score)), conseils


def generer(longueur, maj, minu, chif, symb):
    """Génère un mot de passe avec le module sécurisé 'secrets'."""
    groupes = []
    if maj:
        groupes.append(string.ascii_uppercase)
    if minu:
        groupes.append(string.ascii_lowercase)
    if chif:
        groupes.append(string.digits)
    if symb:
        groupes.append("!@#$%&*?-_+=")
    if not groupes:
        return ""
    # Au moins un caractère de chaque type choisi
    mdp = [secrets.choice(g) for g in groupes]
    tous = "".join(groupes)
    mdp += [secrets.choice(tous) for _ in range(longueur - len(mdp))]
    secrets.SystemRandom().shuffle(mdp)
    return "".join(mdp)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vérificateur de mots de passe")
        self.geometry("480x720")
        self.resizable(False, True)
        self.configure(padx=20, pady=15)

        # --- Titre ---
        tk.Label(self, text="🔐 Vérificateur de mots de passe",
                 font=("Segoe UI", 16, "bold")).pack(pady=(0, 4))
        tk.Label(self, text="🔒 Votre mot de passe n'est jamais envoyé ni enregistré.",
                 fg="green", font=("Segoe UI", 9)).pack(pady=(0, 12))

        # --- Saisie ---
        cadre_saisie = tk.Frame(self)
        cadre_saisie.pack(fill="x")
        self.var_mdp = tk.StringVar()
        self.var_mdp.trace_add("write", lambda *a: self.mettre_a_jour())
        self.champ = tk.Entry(cadre_saisie, textvariable=self.var_mdp, show="•",
                              font=("Consolas", 14))
        self.champ.pack(side="left", fill="x", expand=True, ipady=4)
        self.visible = False
        tk.Button(cadre_saisie, text="👁", command=self.basculer_affichage,
                  width=3).pack(side="left", padx=(5, 0))

        # --- Barre de force ---
        self.barre = tk.Canvas(self, height=14, bg="#e0e0e0", highlightthickness=0)
        self.barre.pack(fill="x", pady=(12, 4))
        self.label_score = tk.Label(self, text="Score : 0/100",
                                    font=("Segoe UI", 12, "bold"))
        self.label_score.pack()

        # --- Critères ---
        cadre_crit = tk.LabelFrame(self, text=" Critères ", padx=10, pady=5)
        cadre_crit.pack(fill="x", pady=10)
        self.labels_criteres = {}
        for nom in ["Longueur (12+)", "Majuscules", "Minuscules", "Chiffres", "Symboles"]:
            lbl = tk.Label(cadre_crit, text=f"✗  {nom}", fg="red",
                           font=("Segoe UI", 10), anchor="w")
            lbl.pack(fill="x")
            self.labels_criteres[nom] = lbl

        # --- Recommandations ---
        cadre_reco = tk.LabelFrame(self, text=" Recommandations ", padx=10, pady=5)
        cadre_reco.pack(fill="x")
        self.label_reco = tk.Label(cadre_reco, text="", justify="left",
                                   anchor="w", wraplength=400, font=("Segoe UI", 9))
        self.label_reco.pack(fill="x")

        # --- Générateur ---
        cadre_gen = tk.LabelFrame(self, text=" Générateur ", padx=10, pady=8)
        cadre_gen.pack(fill="x", pady=10)

        ligne = tk.Frame(cadre_gen)
        ligne.pack(fill="x")
        tk.Label(ligne, text="Longueur :").pack(side="left")
        self.var_longueur = tk.IntVar(value=16)
        tk.Spinbox(ligne, from_=8, to=64, textvariable=self.var_longueur,
                   width=5).pack(side="left", padx=5)

        self.var_maj = tk.BooleanVar(value=True)
        self.var_min = tk.BooleanVar(value=True)
        self.var_chi = tk.BooleanVar(value=True)
        self.var_sym = tk.BooleanVar(value=True)
        options = tk.Frame(cadre_gen)
        options.pack(fill="x", pady=4)
        for texte, var in [("A-Z", self.var_maj), ("a-z", self.var_min),
                           ("0-9", self.var_chi), ("!@#", self.var_sym)]:
            tk.Checkbutton(options, text=texte, variable=var).pack(side="left")

        boutons = tk.Frame(cadre_gen)
        boutons.pack(fill="x", pady=(4, 0))
        tk.Button(boutons, text="🎲 Générer", command=self.generer_mdp,
                  bg="#4a7bd8", fg="white").pack(side="left")
        tk.Button(boutons, text="📋 Copier", command=self.copier).pack(side="left", padx=5)
        tk.Button(boutons, text="🧹 Effacer", command=self.effacer).pack(side="left")

        self.label_info = tk.Label(cadre_gen, text="", fg="gray", font=("Segoe UI", 9))
        self.label_info.pack(anchor="w", pady=(4, 0))

        self.mettre_a_jour()

    # --- Actions ---
    def basculer_affichage(self):
        self.visible = not self.visible
        self.champ.config(show="" if self.visible else "•")

    def mettre_a_jour(self):
        criteres, score, conseils = analyser(self.var_mdp.get())

        for nom, ok in criteres.items():
            self.labels_criteres[nom].config(
                text=f"{'✓' if ok else '✗'}  {nom}",
                fg="green" if ok else "red")

        if score < 40:
            couleur, niveau = "#e53935", "Faible"
        elif score < 70:
            couleur, niveau = "#fb8c00", "Moyen"
        else:
            couleur, niveau = "#43a047", "Fort"

        self.barre.delete("all")
        largeur = self.barre.winfo_width() or 440
        self.barre.create_rectangle(0, 0, largeur * score / 100, 14,
                                    fill=couleur, width=0)
        self.label_score.config(text=f"Score : {score}/100  ({niveau})", fg=couleur)
        self.label_reco.config(text="\n".join("• " + c for c in conseils))

    def generer_mdp(self):
        try:
            longueur = max(8, min(64, int(self.var_longueur.get())))
        except (ValueError, tk.TclError):
            longueur = 16
        mdp = generer(longueur, self.var_maj.get(), self.var_min.get(),
                      self.var_chi.get(), self.var_sym.get())
        if not mdp:
            self.label_info.config(text="Cochez au moins un type de caractère.")
            return
        self.var_mdp.set(mdp)
        self.label_info.config(text="Mot de passe généré.")

    def copier(self):
        mdp = self.var_mdp.get()
        if not mdp:
            return
        self.clipboard_clear()
        self.clipboard_append(mdp)
        self.label_info.config(text="Copié ! Le presse-papiers sera vidé dans 30 s.")
        self.after(30000, self.vider_presse_papiers)

    def vider_presse_papiers(self):
        self.clipboard_clear()
        self.label_info.config(text="Presse-papiers vidé par sécurité.")

    def effacer(self):
        self.var_mdp.set("")
        self.label_info.config(text="Champ effacé.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
