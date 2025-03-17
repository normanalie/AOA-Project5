#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt

def parse_file(filename):
    """
    Lit le fichier et extrait pour chaque instance le numéro et la valeur de stabilité.
    """
    instances = []
    stabilities = []
    current_instance = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Cherche la ligne indiquant l'instance (ex: "Instance 3/100")
            instance_match = re.search(r'^Instance\s+(\d+)/\d+', line)
            if instance_match:
                current_instance = int(instance_match.group(1))
            
            # Cherche la ligne indiquant la stabilité (ex: "GOOD STABILITY: 0.15 %")
            stability_match = re.search(r'(GOOD|AVERAGE|BAD)\s+STABILITY:\s+([\d\.]+)\s*%', line)
            if stability_match and current_instance is not None:
                stability_value = float(stability_match.group(2))
                instances.append(current_instance)
                stabilities.append(stability_value)
                # Réinitialisation (optionnelle si l'ordre est garanti)
                current_instance = None

    return instances, stabilities

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_stability.py <calibration_file.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    instances, stabilities = parse_file(filename)

    if not instances:
        print("Aucune donnée trouvée dans le fichier.")
        sys.exit(1)

    # Tracé de la stabilité en fonction de l'instance
    plt.figure(figsize=(10,6))
    plt.plot(instances, stabilities, marker='o', linestyle='-', color='blue')
    plt.xlabel('Instance')
    plt.ylabel('Stabilité (%)')
    plt.title('Évolution de la stabilité par instance')
    plt.grid(True)
    plt.savefig('stability_plot.png')
    plt.show()
