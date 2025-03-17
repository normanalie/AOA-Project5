#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt

def parse_file(filename):
    """
    Lit le fichier et extrait pour chaque section la taille d'entrée, la valeur MED (cycles per inner-iter)
    et la stabilité (en %).
    """
    sizes = []
    med_cycles = []
    stability = []
    current_size = None
    current_med = None
    current_stab = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Détection du début d'une section
            m_size = re.match(r"Mesure pour taille = (\d+)", line)
            if m_size:
                # Si on avait déjà une section en cours, on l'enregistre
                if current_size is not None:
                    sizes.append(current_size)
                    med_cycles.append(current_med)
                    stability.append(current_stab)
                current_size = int(m_size.group(1))
                current_med = None
                current_stab = None
                continue

            # Extraction de la valeur MED (cycles per inner-iter)
            m_med = re.search(r"MED\s+\d+\s+RDTSC-cycles\s+\(([\d\.]+)\s+per inner-iter\)", line)
            if m_med:
                current_med = float(m_med.group(1))
                continue

            # Extraction de la stabilité (en %)
            m_stab = re.search(r"(GOOD|AVERAGE|BAD)\s+STABILITY:\s+([\d\.]+)\s*%", line)
            if m_stab:
                current_stab = float(m_stab.group(2))
                continue

    # Enregistrement de la dernière section
    if current_size is not None:
        sizes.append(current_size)
        med_cycles.append(current_med)
        stability.append(current_stab)

    return sizes, med_cycles, stability

def main():
    if len(sys.argv) != 2:
        print("Usage: python plot_measures.py <mesures.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    sizes, med_cycles, stability = parse_file(filename)

    if not sizes:
        print("Aucune donnée extraite depuis le fichier.")
        sys.exit(1)

    # Création de deux subplots dans une figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Premier graphique : Performance (MED cycles per inner-iter) vs taille d'entrée
    ax1.plot(sizes, med_cycles, marker='o', linestyle='-', color='blue')
    ax1.set_xlabel("Taille de l'entrée")
    ax1.set_ylabel("MED RDTSC-cycles per inner-iter")
    ax1.set_title("Performance vs Taille d'entrée")
    ax1.grid(True)

    # Deuxième graphique : Stabilité vs taille d'entrée
    ax2.plot(sizes, stability, marker='o', linestyle='-', color='red')
    ax2.set_xlabel("Taille de l'entrée")
    ax2.set_ylabel("Stabilité (%)")
    ax2.set_title("Stabilité vs Taille d'entrée")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("performance_stability.png")
    plt.show()

if __name__ == "__main__":
    main()
