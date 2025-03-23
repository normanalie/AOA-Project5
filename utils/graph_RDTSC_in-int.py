import os
import re
import matplotlib.pyplot as plt

def extract_median_inner_iter(file_path):
    """
    Extrait la valeur RDTSC Median per inner-iter à partir du fichier.
    On recherche une ligne du type :
    "MED 354641916 RDTSC-cycles (28.78 per inner-iter)"
    et on récupère la valeur 28.78.
    """
    median_inner_iter = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("MED"):
                # Expression régulière pour récupérer la valeur entre parenthèses
                match = re.search(r"\(([\d.]+)\s+per inner-iter\)", line)
                if match:
                    median_inner_iter = float(match.group(1))
                    break
    return median_inner_iter

def extract_n_from_filename(filename):
    """
    Extrait la valeur de n à partir d'un nom de fichier de type:
    measure_<n>_3_<repm>.txt
    """
    match = re.search(r"measure_(\d+)_3_", filename)
    if match:
        return int(match.group(1))
    return None

# Liste des dossiers à traiter
folders = ["measures_O2", "measures_O3", "measures_Ofast", "measures_Ofast-march"]

# Dictionnaire pour stocker les données sous la forme : { dossier: [(n, median_inner_iter), ...] }
data = {}

for folder in folders:
    data[folder] = []
    # Parcourir tous les fichiers texte dans le dossier
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            n_val = extract_n_from_filename(filename)
            file_path = os.path.join(folder, filename)
            median_value = extract_median_inner_iter(file_path)
            if n_val is not None and median_value is not None:
                data[folder].append((n_val, median_value))
    # Trier les données par n
    data[folder] = sorted(data[folder], key=lambda x: x[0])

# ----------------------------
# Graphique avec points de mesure
# ----------------------------
plt.figure(figsize=(10, 6))
for folder in folders:
    n_values = [item[0] for item in data[folder]]
    median_values = [item[1] for item in data[folder]]
    # On extrait l'indicateur d'optimisation (O2, O3, Ofast) à partir du nom du dossier
    label = folder.split('_')[1]
    plt.plot(n_values, median_values, marker='o', label=label)
plt.xlabel('n')
plt.ylabel('RDTSC Median per inner-iter')
plt.title('RDTSC Median per inner-iter en fonction de n (avec points de mesure)')
plt.legend()
plt.grid(True)
plt.savefig("graph_with_points_median_inner_iter.png", format="png", dpi=300)
plt.show()

# ----------------------------
# Graphique sans points de mesure (uniquement la courbe)
# ----------------------------
plt.figure(figsize=(10, 6))
for folder in folders:
    n_values = [item[0] for item in data[folder]]
    median_values = [item[1] for item in data[folder]]
    label = folder.split('_')[1]
    plt.plot(n_values, median_values, label=label)
plt.xlabel('n')
plt.ylabel('RDTSC Median per inner-iter')
plt.title('RDTSC Median per inner-iter en fonction de n (sans points de mesure)')
plt.legend()
plt.grid(True)
plt.savefig("graph_without_points_median_inner_iter.png", format="png", dpi=300)
plt.show()
