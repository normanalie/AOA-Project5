import os
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_measure_file(file_path):
    """
    Lit le fichier measure_30_3_10.txt et en extrait :
      - la médiane des cycles/itération (float)
      - la stabilité (float)
    Renvoie (median_cycles, stability).
    """
    median_cycles = None
    stability = None
    
    if not os.path.isfile(file_path):
        print(f"Fichier introuvable : {file_path}")
        return None, None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Recherche de la médiane (ex. "MED 354405508 RDTSC-cycles (28.76 per inner-iter)")
            if line.startswith("MED"):
                match = re.search(r"\(([\d.]+)\s+per inner-iter\)", line)
                if match:
                    median_cycles = float(match.group(1))
            
            # Recherche de la stabilité (ex. "GOOD STABILITY: 0.07 %")
            if line.startswith("GOOD STABILITY:"):
                match = re.search(r"GOOD STABILITY:\s+([\d.]+)", line)
                if match:
                    stability = float(match.group(1))
    
    return median_cycles, stability

# Dictionnaire dossier -> label à afficher
folders = {
    "measures_O2":         "gcc O2",
    "measures_O3":         "gcc O3",
    "measures_O3-march":   "gcc O3 march",
    "measures_Ofast":      "gcc Ofast",
    "measures_Ofast-march":"gcc Ofast march"
}

variants = []
cycles_median = []
stability_vals = []

# Parcours des dossiers, extraction des données
for folder, label in folders.items():
    file_path = os.path.join(folder, "measure_30_3_10.txt")
    med_cyc, stab = parse_measure_file(file_path)
    variants.append(label)
    cycles_median.append(med_cyc if med_cyc is not None else 0)
    stability_vals.append(stab if stab is not None else 0)

# Vérification : s'il manque des données, on peut le signaler
if any(val == 0 for val in cycles_median + stability_vals):
    print("Attention : certaines valeurs sont à 0, vérifier la présence/validité des fichiers.")

# Préparation du graphique
x = np.arange(len(variants))  # positions en X pour les barres
bar_width = 0.6

fig, ax1 = plt.subplots(figsize=(8, 5))

# --- Barres pour la médiane des cycles/itération (axe de gauche) ---
bars = ax1.bar(
    x, cycles_median, 
    width=bar_width, 
    color='tomato', 
    label='Médiane (cycles/itération)'
)

ax1.set_xlabel("Variantes de compilation")
ax1.set_ylabel("Cycles/itération (médiane)")
ax1.set_xticks(x)
ax1.set_xticklabels(variants)
ax1.set_ylim(0, max(cycles_median) * 1.2 if cycles_median else 1)

# --- Courbe pour la stabilité (axe de droite) ---
ax2 = ax1.twinx()
ax2.set_ylabel("Stabilité (%)")
ax2.set_ylim(0, max(stability_vals) * 1.2 if stability_vals else 1)

line = ax2.plot(
    x, stability_vals, 
    color='gold', 
    marker='o', 
    linewidth=2, 
    label="(med - min) / min"
)

# --- Légende commune ---
bars_labels, bars_texts = ax1.get_legend_handles_labels()
line_labels, line_texts = ax2.get_legend_handles_labels()
ax1.legend(bars_labels + line_labels, bars_texts + line_texts, loc='upper right')

# --- Titre ---
plt.title("Performance des variantes de compilation en cache L1 (n = 60)")

plt.tight_layout()
plt.savefig("perf_compilation_cacheL1.png", dpi=300)
plt.show()
