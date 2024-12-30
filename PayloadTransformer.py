import json
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

banner = '''
          
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
          This program loads base payloads from a JSON, TXT, or PY file and saves them into a JSON file without modification or obfuscation.
          It is intended for security testing and should only be used in authorized environments.
'''

for col in banner:
    print(bcolors.BLEU + col, end="")
    sys.stdout.flush()
    time.sleep(0.00005)

def load_base_payloads(input_file):
    """Load base payloads from a JSON, TXT, or PY file without any transformation."""
    try:
        if not os.path.isfile(input_file):
            print(bcolors.YELLOW + f"\n[] Error: The file {input_file} does not exist.")
            return []
        
        # If the file is a JSON
        if input_file.endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                try:
                    payloads = json.load(f)
                    return payloads
                except json.JSONDecodeError as e:
                    print(bcolors.RED + f"\n[] Error: The file {input_file} is not a valid JSON file. Details: {e}")
                    return []
        
        # If the file is a text (txt, py, etc.)
        elif input_file.endswith('.txt') or input_file.endswith('.py'):
            with open(input_file, 'r', encoding='utf-8') as f:
                payloads = f.read().splitlines()
                return payloads

        else:
            print(bcolors.RED + f"\n[] Error: The file {input_file} has an unsupported extension (JSON, TXT, or PY).")
            return []
    
    except Exception as e:
        print(bcolors.RED + f"\n[] Error while processing the file {input_file}: {e}")
        return []

def save_payloads_as_json(payloads, output_file='payloads.json'):
    """Save the payloads to a JSON file without modification."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Save the payloads to the file in JSON format
            json.dump(payloads, f, indent=2)
        print(bcolors.GREEN + f"\n[+] Payloads saved to {output_file}")
    
    except Exception as e:
        print(bcolors.RED + f"\n[] Error while saving to {output_file}: {e}")

# Example usage:
input_file = input(bcolors.YELLOW + "\n[] Enter the name of the input file or Path (e.g., payloads.json, input.txt, script.py): ").strip()  # The input file
output_file = 'payloads.json'  # The output file in JSON format

# Load the base payloads from the input file
base_payloads = load_base_payloads(input_file)

# If the payloads were successfully loaded, save them into a JSON file
if base_payloads:
    save_payloads_as_json(base_payloads, output_file)
