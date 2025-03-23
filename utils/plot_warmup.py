#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt

def parse_calibration_file(filename):
    """
    Lit le fichier et extrait pour chaque instance :
      - l'indice de la mesure (Instance N/100)
      - la valeur MIN (ex. : 29.08 per inner-iter)
      - la valeur MED (ex. : 32.04 per inner-iter)
    Retourne trois listes : instances, med_vals, min_vals.
    """
    instances = []
    med_vals = []
    min_vals = []
    
    # Regex pour détecter "Instance X/..."
    instance_regex = re.compile(r'^Instance\s+(\d+)/\d+')
    # Regex pour extraire la valeur dans "MIN ..." : par exemple "(29.08 per inner-iter)"
    min_regex = re.compile(r'^MIN\s+\d+\s+RDTSC-cycles\s+\(([\d\.]+)\s+per inner-iter\)')
    # Regex pour extraire la valeur dans "MED ..." : par exemple "(32.04 per inner-iter)"
    med_regex = re.compile(r'^MED\s+\d+\s+RDTSC-cycles\s+\(([\d\.]+)\s+per inner-iter\)')

    current_instance = None
    current_min = None
    current_med = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Si on trouve une ligne d'instance
            m_inst = instance_regex.match(line)
            if m_inst:
                # Si on a déjà des données pour une instance, on les sauvegarde
                if current_instance is not None and current_min is not None and current_med is not None:
                    instances.append(current_instance)
                    min_vals.append(current_min)
                    med_vals.append(current_med)
                current_instance = int(m_inst.group(1))
                current_min = None
                current_med = None
                continue

            m_min = min_regex.match(line)
            if m_min:
                current_min = float(m_min.group(1))
                continue

            m_med = med_regex.match(line)
            if m_med:
                current_med = float(m_med.group(1))
                continue

    # Sauvegarder le dernier bloc si complet
    if current_instance is not None and current_min is not None and current_med is not None:
        instances.append(current_instance)
        min_vals.append(current_min)
        med_vals.append(current_med)
    
    return instances, med_vals, min_vals

def main():
    if len(sys.argv) != 2:
        print("Usage: python plot_calibration.py <calibrate-gcc-10-100.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    instances, med_vals, min_vals = parse_calibration_file(filename)
    
    if not instances:
        print("Aucune donnée extraite du fichier.")
        sys.exit(1)
    
    # Calcul de (MED - MIN)/MIN en pourcentage
    stability = [ (med - mn) / mn * 100.0 for med, mn in zip(med_vals, min_vals) ]
    
    # Préparer la figure avec deux axes y (courbe MED et courbe stabilité)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Axe gauche pour MED (cycles per inner-iter)
    color_med = 'tab:blue'
    ax1.set_xlabel("Rang de la mesure (répétition)")
    ax1.set_ylabel("MED (cycles/iter)", color=color_med)
    ax1.plot(instances, med_vals, marker='o', linestyle='-', color=color_med, label="MED/iter")
    ax1.tick_params(axis='y', labelcolor=color_med)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Axe droit pour (MED-MIN)/MIN en pourcentage
    ax2 = ax1.twinx()
    color_stab = 'tab:red'
    ax2.set_ylabel("(MED - MIN)/MIN (%)", color=color_stab)
    ax2.plot(instances, stability, marker='s', linestyle='--', color=color_stab, label="Stabilité (%)")
    ax2.tick_params(axis='y', labelcolor=color_stab)
    
    plt.title("Mesures : MED/iter et (MED-MIN)/MIN en fonction du rang de la mesure")
    fig.tight_layout()
    plt.savefig("calibration_plot.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()
