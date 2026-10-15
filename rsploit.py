
#!/usr/bin/env python3
import hashlib
import re
import getpass
import os
import sys

# RSPLOIT - Cyber Security Toolkit
R = "\033[0m"
B = "\033[1m"
C = "\033[96m"
P = "\033[95m"
G = "\033[92m"
Y = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
WHITE = "\033[97m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def line():
    print(C + "  " + "━" * 54 + R)


def banner():
    clear()
    print(C + B + r"""
  ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
  ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
  ██████╔╝███████╗██████╔╝██║     ██║   ██║██║   ██║
  ██╔══██╗╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║
  ██║  ██║███████║██║     ╚██████╗╚██████╔╝██║   ██║
  ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═════╝ ╚═╝   ╚═╝
""" + R)
    print(P + B + "              C Y B E R   S E C U R I T Y" + R)
    print(GRAY + "              HASH INSPECTOR / v2.0" + R)
    line()
    print("  " + G + "● " + R + "Python engine : " + G + "READY" + R)
    print("  " + G + "● " + R + "Analysis mode : " + Y + "LOCAL LAB" + R)
    line()


def pause():
    input("\n  Appuie sur Entrée pour continuer...")


def detect(value):
    value = value.strip()

    if re.fullmatch(r"\$2[aby]\$\d{2}\$.{53}", value):
        return "bcrypt", "Structure bcrypt reconnue"

    if value.startswith(("$argon2i$", "$argon2id$", "$argon2d$")):
        return "Argon2", "Préfixe Argon2 détecté"

    if value.startswith("scrypt:"):
        return "Werkzeug scrypt", "Préfixe scrypt détecté"

    if re.fullmatch(r"[0-9a-fA-F]{32}", value):
        return "MD5 possible", "32 caractères hexadécimaux"

    if re.fullmatch(r"[0-9a-fA-F]{40}", value):
        return "SHA-1 possible", "40 caractères hexadécimaux"

    if re.fullmatch(r"[0-9a-fA-F]{64}", value):
        return "SHA-256 possible", "64 caractères hexadécimaux"

    if re.fullmatch(r"[0-9a-fA-F]{96}", value):
        return "SHA-384 possible", "96 caractères hexadécimaux"

    if re.fullmatch(r"[0-9a-fA-F]{128}", value):
        return "SHA-512 possible", "128 caractères hexadécimaux"

    return "Inconnu", "Format non reconnu par cet inspecteur"


def inspect_hash():
    clear()
    line()
    print(C + B + "  [01] HASH INSPECTOR" + R)
    line()

    value = input("\n  Entre le hash : ").strip()
    if not value:
        print(RED + "\n  Aucun hash fourni." + R)
        pause()
        return

    fmt, details = detect(value)
    print("\n  " + GRAY + "RÉSULTAT DE L'ANALYSE" + R)
    print("  " + "─" * 40)
    print(f"  Longueur        : {C}{len(value)} caractères{R}")
    print(f"  Format probable : {Y}{fmt}{R}")
    print(f"  Observation     : {WHITE}{details}{R}")

    if fmt.endswith("possible"):
        print(Y + "\n  Attention : plusieurs algorithmes peuvent")
        print("  produire des empreintes de même longueur." + R)

    print(GRAY + "\n  Aucun mot de passe n'a été récupéré." + R)
    pause()


def verify_password():
    clear()
    line()
    print(C + B + "  [02] PASSWORD VERIFIER" + R)
    line()
    print("  Vérifie un mot de passe que tu connais.")
    print("  Algorithmes de démonstration uniquement.\n")

    algorithms = {
        "1": ("md5", "MD5"),
        "2": ("sha1", "SHA-1"),
        "3": ("sha256", "SHA-256"),
        "4": ("sha384", "SHA-384"),
        "5": ("sha512", "SHA-512"),
    }

    for key, (_, name) in algorithms.items():
        print(f"  [{key}] {name}")

    choice = input("\n  Algorithme > ").strip()
    if choice not in algorithms:
        print(RED + "  Choix invalide." + R)
        pause()
        return

    name, label = algorithms[choice]
    target = input("  Hash attendu > ").strip().lower()

    if not re.fullmatch(r"[0-9a-f]+", target):
        print(RED + "  Hash hexadécimal invalide." + R)
        pause()
        return

    candidate = getpass.getpass("  Mot de passe connu > ")
    result = hashlib.new(name, candidate.encode("utf-8")).hexdigest()

    if result == target:
        print(G + "\n  [MATCH] Correspondance confirmée." + R)
    else:
        print(RED + "\n  [NO MATCH] Aucune correspondance." + R)

    print(GRAY + f"  Algorithme utilisé : {label}" + R)
    pause()


def demo():
    clear()
    line()
    print(P + B + "  [03] LOCAL DEMO" + R)
    line()

    word = "hello"
    digest = hashlib.sha256(word.encode()).hexdigest()

    print(f"\n  Texte fictif : {Y}{word}{R}")
    print(f"  SHA-256      : {C}{digest}{R}")

    fmt, details = detect(digest)
    print(f"\n  Format       : {G}{fmt}{R}")
    print(f"  Résultat     : {details}")
    print("\n  Démonstration terminée.")
    pause()


def system_info():
    clear()
    line()
    print(C + B + "  [04] SYSTEM INFORMATION" + R)
    line()
    print(f"\n  Python : {sys.version.split()[0]}")
    print(f"  OS     : {sys.platform}")
    print("  Module : Python standard library")
    print("  Mode   : Local / Educational")
    pause()


def main():
    while True:
        banner()
        print("\n  " + WHITE + B + "MENU PRINCIPAL" + R + "\n")
        print(f"  {C}[01]{R}  Hash Inspector")
        print(f"  {P}[02]{R}  Password Verifier")
        print(f"  {G}[03]{R}  Local Demo")
        print(f"  {Y}[04]{R}  System Information")
        print(f"  {RED}[00]{R}  Quitter")

        choice = input(f"\n  {G}RSPLOIT {C}>{R} ").strip()

        if choice in ("1", "01"):
            inspect_hash()
        elif choice in ("2", "02"):
            verify_password()
        elif choice in ("3", "03"):
            demo()
        elif choice in ("4", "04"):
            system_info()
        elif choice in ("0", "00"):
            print(G + "\n  Fermeture de RSPLOIT. À bientôt !" + R)
            break
        else:
            print(RED + "\n  Option invalide." + R)
            pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(R + "\n\n  Arrêt de RSPLOIT.")
