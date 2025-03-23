#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt

def parse_measures(filename):
    """
    Parcourt le fichier pour chaque bloc 'Mesure pour taille = X' et extrait :
      - size : la taille du problème (64, 128, 256, etc.)
      - min_cycles_iter : la valeur 'MIN' en cycles/iter
      - med_cycles_iter : la valeur 'MED' en cycles/iter

    Retourne trois listes : sizes, mins, meds (par inner-iter).
    """
    # Regex pour détecter "Mesure pour taille = X"
    measure_title_re = re.compile(r'^Mesure\s+pour\s+taille\s*=\s*(\d+)')
    # Regex pour la ligne MIN, ex : "MIN 585208 RDTSC-cycles (28.57 per inner-iter)"
    min_re = re.compile(r'^MIN\s+\d+\s+RDTSC-cycles\s+\(([\d\.]+)\s+per inner-iter\)')
    # Regex pour la ligne MED, ex : "MED 585284 RDTSC-cycles (28.58 per inner-iter)"
    med_re = re.compile(r'^MED\s+\d+\s+RDTSC-cycles\s+\(([\d\.]+)\s+per inner-iter\)')

    sizes = []
    mins = []
    meds = []

    current_size = None
    current_min_iter = None
    current_med_iter = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Détection d'un nouveau bloc "Mesure pour taille = X"
            m_title = measure_title_re.match(line)
            if m_title:
                # Si on a déjà un bloc complet, on l'enregistre
                if current_size is not None and current_min_iter is not None and current_med_iter is not None:
                    sizes.append(current_size)
                    mins.append(current_min_iter)
                    meds.append(current_med_iter)

                # Initialisation pour le nouveau bloc
                current_size = int(m_title.group(1))
                current_min_iter = None
                current_med_iter = None
                continue

            # Détection de la ligne MIN
            m_min = min_re.match(line)
            if m_min:
                current_min_iter = float(m_min.group(1))
                continue

            # Détection de la ligne MED
            m_med = med_re.match(line)
            if m_med:
                current_med_iter = float(m_med.group(1))
                continue

        # En fin de fichier, si le dernier bloc est complet, on l'enregistre
        if current_size is not None and current_min_iter is not None and current_med_iter is not None:
            sizes.append(current_size)
            mins.append(current_min_iter)
            meds.append(current_med_iter)

    return sizes, mins, meds

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <mesures.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    sizes, min_vals, med_vals = parse_measures(filename)

    if not sizes:
        print("Aucune donnée trouvée dans le fichier.")
        sys.exit(1)

    # Exemple : on trace uniquement la courbe MED en cycles/iter
    # Vous pouvez adapter pour tracer min_vals, ou tracer deux courbes
    plt.figure(figsize=(8,5))
    plt.plot(sizes, med_vals, marker='o', linestyle='-', color='blue', label='MED cycles/iter')
    plt.xlabel("Taille du problème (n)")
    plt.ylabel("Cycles/iter")
    plt.title("Évolution de la durée (cycles/iter) en fonction de la taille")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("measures_plot.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()
