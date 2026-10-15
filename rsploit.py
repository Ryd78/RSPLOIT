
#!/usr/bin/env python3
# RSPLOIT | RDB Edition
# Outil local de démonstration et de diagnostic

import os
import sys
import time
import hashlib
import platform
import shutil

# ━━━━━━━━━━━━━━━ COULEURS NÉON ━━━━━━━━━━━━━━━

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[96m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
GRAY = "\033[90m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    input(
        f"\n  {CYAN}[{WHITE}RDB{CYAN}] "
        f"{GRAY}Appuie sur Entrée pour continuer...{RESET}"
    )


def line(char="━", width=58, color=CYAN):
    print(f"{color}{char * width}{RESET}")


def banner():
    clear()
    print(f"""
{CYAN}{BOLD}
    ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
    ██████╔╝███████╗██████╔╝██║     ██║   ██║██║   ██║
    ██╔══██╗╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║
    ██║  ██║███████║██║     ███████╗╚██████╔╝██║   ██║
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝
{RESET}
                  {PURPLE}{BOLD}R D B{RESET}
           {GRAY}LOCAL SECURITY TOOLKIT{RESET}
""")
    line()
    print(
        f"  {GREEN}●{RESET} {WHITE}STATUS : ONLINE{RESET}"
        f"       {PURPLE}◆{RESET} {WHITE}VERSION : 3.1{RESET}"
    )
    line()


def menu():
    banner()
    print(f"""
  {CYAN}{BOLD}╭─────────────── MAIN MENU ───────────────╮{RESET}
  {CYAN}│{RESET}  {PURPLE}[01]{RESET}  {WHITE}Hash Inspector{RESET}                 {CYAN}│{RESET}
  {CYAN}│{RESET}  {PURPLE}[02]{RESET}  {WHITE}Lire une liste TXT{RESET}              {CYAN}│{RESET}
  {CYAN}│{RESET}  {PURPLE}[03]{RESET}  {WHITE}Démo SHA-256{RESET}                    {CYAN}│{RESET}
  {CYAN}│{RESET}  {PURPLE}[04]{RESET}  {WHITE}Informations système{RESET}           {CYAN}│{RESET}
  {CYAN}│{RESET}  {RED}[00]{RESET}  {WHITE}Quitter RSPLOIT{RESET}                 {CYAN}│{RESET}
  {CYAN}{BOLD}╰────────────────────────────────────────╯{RESET}
""")


def detect_hash(value):
    value = value.strip()

    if value.startswith(("$2a$", "$2b$", "$2y$")):
        return "bcrypt"

    if value.startswith("$argon2"):
        return "Argon2"

    if value.startswith("scrypt:"):
        return "Werkzeug scrypt"

    if value and all(
        c in "0123456789abcdefABCDEF" for c in value
    ):
        types = {
            32: "MD5 possible",
            40: "SHA-1 possible",
            64: "SHA-256 possible",
            96: "SHA-384 possible",
            128: "SHA-512 possible",
        }
        return types.get(
            len(value), "Format hexadécimal inconnu"
        )

    return "Format inconnu"


def hash_inspector():
    banner()
    print(f"\n  {PURPLE}{BOLD}» HASH INSPECTOR{RESET}")
    line("─", 44, GRAY)

    value = input(
        f"  {CYAN}Entre un hash de test : {RESET}"
    ).strip()

    if not value:
        print(f"\n  {RED}Aucune valeur saisie.{RESET}")
    else:
        print(
            f"\n  {GREEN}Type probable : "
            f"{WHITE}{detect_hash(value)}{RESET}"
        )
        print(
            f"  {GREEN}Longueur      : "
            f"{WHITE}{len(value)} caractères{RESET}"
        )

    pause()


def read_list():
    print(
        f"\n  {GRAY}Tu peux utiliser un fichier TXT local, "
        f"par exemple un fichier de test.{RESET}"
    )

    path = input(
        f"\n  {CYAN}Chemin du fichier .txt : {RESET}"
    ).strip().strip("\"'")

    if not path:
        print(f"\n  {RED}Aucun chemin fourni.{RESET}")
        return None

    try:
        # latin-1 évite les erreurs d'encodage
        # lors de la lecture de fichiers texte variés.
        with open(
            path, "r", encoding="latin-1"
        ) as file:
            entries = [
                line.rstrip("\r\n")
                for line in file
                if line.rstrip("\r\n")
            ]

        print(
            f"\n  {GREEN}[+] {len(entries)} entrées "
            f"chargées avec succès.{RESET}"
        )
        return entries

    except FileNotFoundError:
        print(f"\n  {RED}[-] Fichier introuvable.{RESET}")

    except PermissionError:
        print(f"\n  {RED}[-] Permission refusée.{RESET}")

    except OSError as error:
        print(f"\n  {RED}[-] Erreur de lecture : {error}{RESET}")

    return None


def test_list():
    banner()
    print(f"\n  {PURPLE}{BOLD}» LECTURE DE LISTE TXT{RESET}")
    line("─", 44, GRAY)

    entries = read_list()

    if entries is None:
        pause()
        return

    if not entries:
        print(f"\n  {YELLOW}Le fichier est vide.{RESET}")
        pause()
        return

    print(f"\n  {GREEN}Fichier lu correctement.{RESET}")
    print(
        f"  {WHITE}Nombre d'entrées : "
        f"{len(entries)}{RESET}"
    )
    print(
        f"  {GRAY}Le contenu du fichier n'est "
        f"pas affiché.{RESET}"
    )

    pause()


def demo_sha256():
    banner()
    print(f"\n  {PURPLE}{BOLD}» SHA-256 DEMONSTRATION{RESET}")
    line("─", 44, GRAY)

    sample = "hello"
    result = hashlib.sha256(
        sample.encode("utf-8")
    ).hexdigest()

    print(
        f"\n  {GRAY}Texte de démonstration : "
        f"{WHITE}{sample}{RESET}"
    )
    print(f"\n  {CYAN}Hash SHA-256 :{RESET}")
    print(f"  {GREEN}{result}{RESET}")

    print(
        f"\n  {GRAY}Cette démonstration montre "
        f"comment calculer un hash.{RESET}"
    )

    pause()


def system_info():
    banner()
    print(f"\n  {PURPLE}{BOLD}» SYSTEM INFORMATION{RESET}")
    line("─", 44, GRAY)

    info = [
        ("Système", platform.system()),
        ("Version", platform.release()),
        ("Architecture", platform.machine()),
        ("Python", platform.python_version()),
        (
            "Terminal",
            f"{shutil.get_terminal_size().columns} colonnes"
        ),
    ]

    for label, value in info:
        print(
            f"  {PURPLE}› {label:<16}{RESET} "
            f"{WHITE}{value}{RESET}"
        )

    pause()


def main():
    while True:
        menu()
        choice = input(
            f"  {CYAN}{BOLD}RSPLOIT {PURPLE}» {RESET}"
        ).strip()

        if choice in ("1", "01"):
            hash_inspector()

        elif choice in ("2", "02"):
            test_list()

        elif choice in ("3", "03"):
            demo_sha256()

        elif choice in ("4", "04"):
            system_info()

        elif choice in ("0", "00"):
            clear()
            print(f"\n  {PURPLE}{BOLD}RSPLOIT{RESET}")
            print(
                f"  {CYAN}RDB{RESET} "
                f"{GRAY}— Session terminée.{RESET}\n"
            )
            sys.exit(0)

        else:
            print(f"\n  {RED}[!] Option invalide.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}[!] Arrêt demandé.{RESET}")
        sys.exit(0)
