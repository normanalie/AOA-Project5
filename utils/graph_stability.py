import os
import re
import matplotlib.pyplot as plt

def extract_stability(file_path):
    """
    Extrait la valeur de stabilité depuis le fichier.
    On recherche une ligne commençant par "GOOD STABILITY:" suivi d'une valeur numérique.
    Par exemple : "GOOD STABILITY: 0.07 %"
    """
    stability_value = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("GOOD STABILITY:"):
                match = re.search(r"GOOD STABILITY:\s+([\d.]+)", line)
                if match:
                    stability_value = float(match.group(1))
                    break
    return stability_value

def extract_n_from_filename(filename):
    """
    Extrait la valeur de n à partir du nom de fichier de type:
    measure_<n>_3_<repm>.txt
    """
    match = re.search(r"measure_(\d+)_3_", filename)
    if match:
        return int(match.group(1))
    return None

# Liste des dossiers à traiter
folders = ["measures_O2", "measures_O3", "measures_Ofast"]

# Dictionnaire pour stocker les données sous la forme : { dossier: [(n, stability), ...] }
data = {}

for folder in folders:
    data[folder] = []
    # Parcourir tous les fichiers texte dans le dossier
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            n_val = extract_n_from_filename(filename)
            file_path = os.path.join(folder, filename)
            stability_value = extract_stability(file_path)
            if n_val is not None and stability_value is not None:
                data[folder].append((n_val, stability_value))
    # Trier les données par n
    data[folder] = sorted(data[folder], key=lambda x: x[0])

# ----------------------------
# Graphique avec points de mesure
# ----------------------------
plt.figure(figsize=(10, 6))
for folder in folders:
    n_values = [item[0] for item in data[folder]]
    stability_values = [item[1] for item in data[folder]]
    # Utiliser le nom du dossier pour la légende (O2, O3, Ofast)
    label = folder.split('_')[1]
    plt.plot(n_values, stability_values, marker='o', label=label)
plt.xlabel('n')
plt.ylabel('Stabilité (%)')
plt.title('Stabilité en fonction de n (avec points de mesure)')
plt.legend()
plt.grid(True)
plt.savefig("graph_with_points_stability.png", format="png", dpi=300)
plt.show()

# ----------------------------
# Graphique sans points de mesure (uniquement la courbe)
# ----------------------------
plt.figure(figsize=(10, 6))
for folder in folders:
    n_values = [item[0] for item in data[folder]]
    stability_values = [item[1] for item in data[folder]]
    label = folder.split('_')[1]
    plt.plot(n_values, stability_values, label=label)
plt.xlabel('n')
plt.ylabel('Stabilité (%)')
plt.title('Stabilité en fonction de n (sans points de mesure)')
plt.legend()
plt.grid(True)
plt.savefig("graph_without_points_stability.png", format="png", dpi=300)
plt.show()
