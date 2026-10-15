#!/usr/bin/env python3
# RSPLOIT — interface d'audit pédagogique de hashes
# Compatible Python 3 / Tkinter (Kali Linux)
# Cette application identifie des formats courants ; elle ne casse pas les mots de passe
# et ne lit/modifie aucun fichier de comptes système.

import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

BG = "#080d12"
PANEL = "#101a22"
PANEL_2 = "#0b131a"
GREEN = "#39ff88"
CYAN = "#38d9ff"
PURPLE = "#c084fc"
PINK = "#ff4fd8"
YELLOW = "#ffe66d"
WHITE = "#e7f4f4"
MUTED = "#8aa3ad"
RED = "#ff647c"

def identify_hash(value: str):
    """Retourne une estimation du format d'un hash fourni manuellement."""
    value = value.strip()

    if not value:
        return ("Aucune entrée", "Colle un hash dans le champ ci-dessus.", "—")

    # Formats avec préfixes caractéristiques
    if value.startswith("$2a$") or value.startswith("$2b$") or value.startswith("$2y$"):
        return ("bcrypt", "Hash de mot de passe conçu pour ralentir les essais. Coût indiqué dans le préfixe.", "Élevée")
    if value.startswith("$argon2id$") or value.startswith("$argon2i$") or value.startswith("$argon2d$"):
        return ("Argon2", "Fonction de dérivation de mot de passe moderne. Le préfixe indique sa variante.", "Élevée")
    if value.startswith("$scrypt$"):
        return ("scrypt", "Fonction de dérivation de clé conçue pour être coûteuse en mémoire.", "Élevée")
    if value.startswith("pbkdf2:") or value.startswith("$pbkdf2-"):
        return ("PBKDF2", "Fonction de dérivation de mot de passe. Les paramètres exacts comptent.", "Variable")
    if value.startswith("$6$"):
        return ("sha512crypt", "Format crypt utilisé par certains systèmes Linux. Ce n'est pas un SHA-512 brut.", "Variable")
    if value.startswith("$5$"):
        return ("sha256crypt", "Format crypt utilisé par certains systèmes Linux. Ce n'est pas un SHA-256 brut.", "Variable")
    if value.startswith("$1$"):
        return ("md5crypt", "Ancien format crypt basé sur MD5, considéré comme obsolète.", "Faible")

    # Les formats bruts se chevauchent : le résultat reste une hypothèse.
    if re.fullmatch(r"[0-9a-fA-F]{32}", value):
        return ("MD5 possible", "32 caractères hexadécimaux : MD5 est possible, mais d'autres formats peuvent avoir la même forme.", "Faible")
    if re.fullmatch(r"[0-9a-fA-F]{40}", value):
        return ("SHA-1 possible", "40 caractères hexadécimaux : SHA-1 est possible, sans certitude sur le format.", "Faible")
    if re.fullmatch(r"[0-9a-fA-F]{64}", value):
        return ("SHA-256 possible", "64 caractères hexadécimaux : SHA-256 est possible, mais ce n'est pas une identification certaine.", "Variable")
    if re.fullmatch(r"[0-9a-fA-F]{96}", value):
        return ("SHA-384 possible", "96 caractères hexadécimaux : SHA-384 est possible.", "Variable")
    if re.fullmatch(r"[0-9a-fA-F]{128}", value):
        return ("SHA-512 possible", "128 caractères hexadécimaux : SHA-512 est possible.", "Variable")

    return ("Format inconnu", "Le format ne correspond pas aux motifs courants reconnus. Il peut être encodé, tronqué ou spécifique à une application.", "Inconnue")


class RSPLOITApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSPLOIT | Security Lab")
        self.root.geometry("1120x760")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)

        self.title_colors = [GREEN, CYAN, PURPLE, PINK, YELLOW, GREEN, CYAN]
        self.title_labels = []
        self._build_ui()
        self._animate_title()
        self._log("RSPLOIT Security Lab démarré.")
        self._log("Mode pédagogique : aucune lecture du système ni cassage de mots de passe.")

    def _build_ui(self):
        # Bandeau supérieur
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 8))

        title_row = tk.Frame(header, bg=BG)
        title_row.pack(anchor="w")
        for ch in "RSPLOIT":
            label = tk.Label(
                title_row, text=ch, font=("DejaVu Sans Mono", 34, "bold"),
                bg=BG, fg=GREEN
            )
            label.pack(side="left")
            self.title_labels.append(label)

        tk.Label(
            header, text="SECURITY TOOLKIT  //  LOCAL HASH FORMAT INSPECTOR",
            font=("DejaVu Sans Mono", 10, "bold"), bg=BG, fg=CYAN
        ).pack(anchor="w", pady=(3, 0))

        tk.Frame(self.root, bg=GREEN, height=2).pack(fill="x", padx=24, pady=(8, 16))

        # Barre d'état
        status = tk.Frame(self.root, bg=PANEL, highlightbackground="#1c3b43", highlightthickness=1)
        status.pack(fill="x", padx=24, pady=(0, 14))
        tk.Label(status, text="●", fg=GREEN, bg=PANEL, font=("DejaVu Sans Mono", 12)).pack(side="left", padx=(12, 7), pady=8)
        tk.Label(status, text="LAB STATUS: READY", fg=GREEN, bg=PANEL, font=("DejaVu Sans Mono", 10, "bold")).pack(side="left", pady=8)
        tk.Label(status, text="LOCAL ONLY  •  SAFE MODE", fg=MUTED, bg=PANEL, font=("DejaVu Sans Mono", 9)).pack(side="right", padx=12)

        # Corps en deux colonnes
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 14))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=PANEL, highlightbackground="#1c3b43", highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(body, bg=PANEL, highlightbackground="#1c3b43", highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        tk.Label(left, text="01  /  HASH INSPECTOR", bg=PANEL, fg=CYAN,
                 font=("DejaVu Sans Mono", 13, "bold")).pack(anchor="w", padx=18, pady=(18, 6))
        tk.Label(left, text="Colle ici une empreinte que tu es autorisé à analyser.",
                 bg=PANEL, fg=MUTED, font=("DejaVu Sans Mono", 9)).pack(anchor="w", padx=18, pady=(0, 10))

        self.hash_entry = tk.Text(
            left, height=5, wrap="word", bg=PANEL_2, fg=GREEN,
            insertbackground=GREEN, relief="flat", bd=0,
            font=("DejaVu Sans Mono", 11), padx=12, pady=12,
            highlightbackground="#28515b", highlightthickness=1
        )
        self.hash_entry.pack(fill="x", padx=18, pady=(0, 12))

        buttons = tk.Frame(left, bg=PANEL)
        buttons.pack(fill="x", padx=18, pady=(0, 16))
        self._button(buttons, "ANALYSER", self._analyze, GREEN, BG).pack(side="left", padx=(0, 8))
        self._button(buttons, "EFFACER", self._clear, "#243640", WHITE).pack(side="left")

        tk.Frame(left, bg="#20343d", height=1).pack(fill="x", padx=18, pady=(0, 14))
        tk.Label(left, text="RÉSULTAT", bg=PANEL, fg=PURPLE,
                 font=("DejaVu Sans Mono", 11, "bold")).pack(anchor="w", padx=18, pady=(0, 8))

        self.result_name = tk.Label(left, text="En attente d'une analyse", bg=PANEL, fg=WHITE,
                                    font=("DejaVu Sans Mono", 16, "bold"), anchor="w")
        self.result_name.pack(fill="x", padx=18, pady=(0, 8))
        self.result_detail = tk.Label(left, text="Le résultat apparaîtra ici.", bg=PANEL, fg=MUTED,
                                      font=("DejaVu Sans Mono", 10), justify="left",
                                      wraplength=560, anchor="w")
        self.result_detail.pack(fill="x", padx=18, pady=(0, 12))
        self.strength = tk.Label(left, text="NIVEAU ESTIMÉ : —", bg=PANEL, fg=YELLOW,
                                 font=("DejaVu Sans Mono", 10, "bold"), anchor="w")
        self.strength.pack(fill="x", padx=18, pady=(0, 18))

        tk.Label(right, text="02  /  LIVE CONSOLE", bg=PANEL, fg=PINK,
                 font=("DejaVu Sans Mono", 13, "bold")).pack(anchor="w", padx=16, pady=(18, 8))
        self.console = tk.Text(
            right, bg="#05090c", fg=GREEN, insertbackground=GREEN,
            relief="flat", bd=0, wrap="word", state="disabled",
            font=("DejaVu Sans Mono", 9), padx=12, pady=12,
            highlightbackground="#28515b", highlightthickness=1
        )
        self.console.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Barre inférieure
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=24, pady=(0, 16))
        tk.Label(footer, text="RSPLOIT // EDUCATIONAL BUILD", bg=BG, fg=MUTED,
                 font=("DejaVu Sans Mono", 8)).pack(side="left")
        tk.Label(footer, text="Use only on data you are authorized to inspect.", bg=BG, fg=MUTED,
                 font=("DejaVu Sans Mono", 8)).pack(side="right")

    def _button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=CYAN, activeforeground=BG,
            relief="flat", bd=0, padx=16, pady=9,
            cursor="hand2", font=("DejaVu Sans Mono", 9, "bold")
        )

    def _animate_title(self):
        # Effet de couleurs cycliques sur le titre.
        for i, label in enumerate(self.title_labels):
            label.configure(fg=self.title_colors[(i + self._color_offset) % len(self.title_colors)])
        self._color_offset = (self._color_offset + 1) % len(self.title_colors)
        self.root.after(350, self._animate_title)

    _color_offset = 0

    def _log(self, message):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.console.configure(state="normal")
        self.console.insert("end", f"[{stamp}] {message}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def _analyze(self):
        value = self.hash_entry.get("1.0", "end").strip()
        name, detail, level = identify_hash(value)
        self.result_name.configure(text=name, fg=CYAN if name != "Format inconnu" else YELLOW)
        self.result_detail.configure(text=detail)
        self.strength.configure(text=f"NIVEAU DU FORMAT : {level}")
        self._log(f"Analyse locale lancée ({len(value)} caractères).")
        self._log(f"Résultat : {name} | niveau indicatif : {level}.")
        if name.endswith("possible"):
            self._log("Attention : longueur/forme seules ne prouvent pas l'algorithme.")

    def _clear(self):
        self.hash_entry.delete("1.0", "end")
        self.result_name.configure(text="En attente d'une analyse", fg=WHITE)
        self.result_detail.configure(text="Le résultat apparaîtra ici.")
        self.strength.configure(text="NIVEAU DU FORMAT : —")
        self._log("Champ d'analyse vidé.")

def main():
    root = tk.Tk()
    RSPLOITApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
