#!/usr/bin/env python3
import subprocess

def run_command(cmd):
    """Exécute la commande et retourne sa sortie."""
    print("Exécution :", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def main():
    tailles = ["32", "64", "128", "256", "512", "1024", "2048"]
    output_filename = "mesures.txt"
    
    with open(output_filename, "w") as f:
        for taille in tailles:
            # Commande : ./measure <taille> 5 5
            cmd = ["./../bin/measure", taille, "5", "5"]
            sortie = run_command(cmd)
            # Écrire un en-tête pour la section correspondante à cette taille
            f.write(f"Mesure pour taille = {taille}\n")
            f.write(sortie)
            f.write("\n" + "="*50 + "\n\n")
    
    print(f"Les mesures ont été enregistrées dans {output_filename}")

if __name__ == "__main__":
    main()
