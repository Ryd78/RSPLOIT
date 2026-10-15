
#!/usr/bin/env python3
# RSPLOIT - RDB Edition
# Outil local de démonstration et de vérification

import os
import sys
import time
import hashlib
import platform
import getpass

# Couleurs du terminal
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    input(f"\n{CYAN}[RDB]{RESET} Appuie sur Entrée pour continuer...")


def banner():
    print(f"""{CYAN}{BOLD}
██████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔══██╗
██████╔╝██║  ██║██████╔╝
██╔══██╗██║  ██║██╔══██╗
██║  ██║██████╔╝██║  ██║
╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
{RESET}{MAGENTA}          RSPLOIT{RESET}
{GREEN}             RDB{RESET}
{WHITE}    Local Security Toolkit{RESET}
""")


def menu():
    clear()
    banner()

    print(f"{BLUE}╔══════════════════════════════════════╗")
    print("║             MENU PRINCIPAL           ║")
    print("╠══════════════════════════════════════╣")
    print("║  [01] Hash Inspector                 ║")
    print("║  [02] Vérifier une liste .txt        ║")
    print("║  [03] Démonstration SHA-256           ║")
    print("║  [04] Informations système           ║")
    print("║  [00] Quitter                        ║")
    print("╚══════════════════════════════════════╝" + RESET)


def detect_hash(value):
    value = value.strip()

    if value.startswith("$2a$") or value.startswith("$2b$") \
            or value.startswith("$2y$"):
        return "bcrypt"

    if value.startswith("$argon2"):
        return "Argon2"

    if value.startswith("scrypt:"):
        return "Werkzeug scrypt"

    if all(c in "0123456789abcdefABCDEF" for c in value):
        lengths = {
            32: "MD5 (possible)",
            40: "SHA-1 (possible)",
            64: "SHA-256 (possible)",
            96: "SHA-384 (possible)",
            128: "SHA-512 (possible)"
        }

        if len(value) in lengths:
            return lengths[len(value)]

    return "Format inconnu"


def hash_inspector():
    clear()
    banner()

    print(f"{YELLOW}=== HASH INSPECTOR ==={RESET}")
    value = input("Entre une chaîne ou un hash de test : ").strip()

    if not value:
        print(f"{RED}Aucune valeur saisie.{RESET}")
    else:
        print(f"\n{GREEN}Type probable : {detect_hash(value)}{RESET}")
        print(f"Longueur      : {len(value)} caractères")

    pause()


def read_password_list():
    path = input(
        f"{CYAN}Chemin du fichier .txt "
        "(exemple : mots_de_passe_test.txt) : {RESET}"
    ).strip()

    # Accepte aussi un chemin entouré de guillemets
    path = path.strip("\"'")

    if not path:
        print(f"{RED}Aucun chemin fourni.{RESET}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as file:
            passwords = [
                line.rstrip("\r\n")
                for line in file
                if line.rstrip("\r\n")
            ]

        print(f"{GREEN}{len(passwords)} entrées chargées.{RESET}")
        return passwords

    except FileNotFoundError:
        print(f"{RED}Fichier introuvable : {path}{RESET}")
    except PermissionError:
        print(f"{RED}Permission refusée pour lire ce fichier.{RESET}")
    except UnicodeDecodeError:
        print(f"{RED}Le fichier doit être encodé en UTF-8.{RESET}")
    except OSError as error:
        print(f"{RED}Erreur de lecture : {error}{RESET}")

    return None


def verify_test_list():
    clear()
    banner()

    print(f"{YELLOW}=== VÉRIFICATION D'UNE LISTE .TXT ==={RESET}")
    print("Mode démo : vérification d'un mot de passe de test local.")
    print("Utilise uniquement des données que tu es autorisé à tester.\n")

    passwords = read_password_list()

    if passwords is None:
        pause()
        return

    if not passwords:
        print(f"{RED}La liste ne contient aucune entrée.{RESET}")
        pause()
        return

    algorithms = {
        "1": "md5",
        "2": "sha1",
        "3": "sha256",
        "4": "sha384",
        "5": "sha512"
    }

    print("\nChoisis l'algorithme pour la démonstration :")
    print("[1] MD5")
    print("[2] SHA-1")
    print("[3] SHA-256")
    print("[4] SHA-384")
    print("[5] SHA-512")

    choice = input("\nChoix : ").strip()

    if choice not in algorithms:
        print(f"{RED}Choix invalide.{RESET}")
        pause()
        return

    algorithm = algorithms[choice]

    # Le mot de passe de référence est saisi par l'utilisateur.
    # Son hash est créé ici pour la démonstration.
    reference = getpass.getpass(
        "Saisis ton mot de passe de test de référence : "
    )

    reference_hash = hashlib.new(
        algorithm, reference.encode("utf-8")
    ).hexdigest()

    print(f"\n{CYAN}Algorithme : {algorithm.upper()}{RESET}")
    print("Comparaison avec le mot de passe de test fourni.")
    print("Les mots de passe de la liste ne seront pas affichés.\n")

    found = False

    for candidate in passwords:
        candidate_hash = hashlib.new(
            algorithm, candidate.encode("utf-8")
        ).hexdigest()

        if candidate_hash == reference_hash:
            found = True
            break

    if found:
        print(f"{GREEN}[OK] Une entrée correspond au test.{RESET}")
    else:
        print(
            f"{YELLOW}[INFO] Aucune entrée de la liste "
            f"ne correspond au test.{RESET}"
        )

    print(f"\nNombre d'entrées vérifiées : {len(passwords)}")
    pause()


def demo_sha256():
    clear()
    banner()

    print(f"{YELLOW}=== DÉMONSTRATION SHA-256 ==={RESET}")

    sample = "hello"
    result = hashlib.sha256(sample.encode("utf-8")).hexdigest()

    print(f"Texte de démonstration : {sample}")
    print(f"Hash SHA-256           : {result}")

    print(
        f"\n{GREEN}La même entrée produit "
        f"le même hash avec SHA-256.{RESET}"
    )

    pause()


def system_info():
    clear()
    banner()

    print(f"{YELLOW}=== INFORMATIONS SYSTÈME ==={RESET}")
    print(f"Système      : {platform.system()}")
    print(f"Version      : {platform.release()}")
    print(f"Architecture : {platform.machine()}")
    print(f"Python       : {platform.python_version()}")

    pause()


def main():
    while True:
        menu()
        choice = input(f"{MAGENTA}RDB > {RESET}").strip()

        if choice == "1" or choice == "01":
            hash_inspector()
        elif choice == "2" or choice == "02":
            verify_test_list()
        elif choice == "3" or choice == "03":
            demo_sha256()
        elif choice == "4" or choice == "04":
            system_info()
        elif choice == "0" or choice == "00":
            clear()
            print(f"{GREEN}RDB — Fermeture de RSPLOIT. À bientôt !{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Option invalide.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Arrêt demandé. À bientôt !{RESET}")
        sys.exit(0)
