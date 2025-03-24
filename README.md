# Projet d'études de cas AOA – Optimisation des performances des noyaux

dossier src
rm readme.txt
ajouter infos perso readme.md
nettoyer repertoire measures-norman


## Table des matières
- [Introduction](#introduction)
- [Formation des équipes](#formation-des-équipes)
- [Sujet et objectifs du projet](#sujet-et-objectifs-du-projet)
- [Phases du projet](#phases-du-projet)
  - [Phase I : Options de compilation](#phase-i--options-de-compilation)
  - [Phase II : Transformation de code](#phase-ii--transformation-de-code)
    - [Phase II.1 (O2)](#phase-ii1-o2)
    - [Phase II.2 (Options de compilation libres)](#phase-ii2-options-de-compilation-libres)
  - [Questions facultatives (Bonus)](#questions-facultatives-bonus)
- [Conseils pratiques et bonnes pratiques](#conseils-pratiques-et-bonnes-pratiques)
- [Installation et vérification de l'environnement](#installation-et-vérification-de-lenvironnement)
  - [Vérification du processeur et de l'architecture](#vérification-du-processeur-et-de-larchitecture)
  - [Installation des compilateurs](#installation-des-compilateurs)
    - [AMD AOCC pour processeurs AMD](#amd-aocc-pour-processeurs-amd)
    - [Intel oneAPI pour processeurs Intel](#intel-oneapi-pour-processeurs-intel)
  - [Installation de MAQAO](#installation-de-maqao)
  - [Installation de perf-tools et likwid](#installation-de-perf-tools-et-likwid)
- [Ressources et liens utiles](#ressources-et-liens-utiles)
- [Annexes et commandes utiles](#annexes-et-commandes-utiles)

## Introduction

Le présent projet d'études de cas du module AOA a pour objectif de **mesurer, analyser et optimiser les performances de code** (appelé "noyau" ou "kernel"). Vous travaillerez en équipe et utiliserez différents compilateurs ainsi que des outils d’analyse de performance (notamment MAQAO, perf et likwid) pour réaliser des optimisations et mesurer leur impact sur le code.

## Formation des équipes

- **Composition des équipes :**
  - **Équipes de 3 étudiants** (un compilateur par étudiant) sont la norme.
  - En cas d'effectif non divisible par 3, il pourra y avoir 1 ou 2 équipes de 4.
- **Organisation :**
  - Vos choix d'équipes et de sujets doivent être communiqués à vos délégués.
  - La centralisation se fera selon le principe du **premier arrivé, premier servi**.

## Sujet et objectifs du projet

- **Thème général :**  
  Mesurer, analyser et optimiser les performances d’un noyau de code.
- **Compilateurs utilisés :**  
  - GNU gcc  
  - LLVM clang  
  - Compilateur fourni par le constructeur (Intel oneAPI ou AMD AOCC selon le processeur)
- **Mesures et environnement d'exécution :**  
  Les performances seront mesurées sur vos machines personnelles en exécution native.

## Phases du projet

### Phase I : Options de compilation

1. **Mesure de la performance :**
   - Compiler le noyau en **O2** et mesurer les performances.
2. **Comparaison des optimisations :**
   - Recompiler le noyau avec différentes options de compilation et mesurer les performances.
3. **Analyse des performances :**
   - Analyser les différences entre les versions à l’aide des rapports MAQAO.
4. **Justification :**
   - Une **justification détaillée** est attendue pour chaque choix.

### Phase II : Transformation de code

#### Phase II.1 (O2)
- **Objectif :**  
  Améliorer les performances du noyau compilé en O2 par des transformations de code.

#### Phase II.2 (Options de compilation libres)
- **Objectif :**  
  Tester différentes combinaisons d’options et modifications du code.

### Questions facultatives (Bonus)

- **Parallélisation avec OpenMP**
- **Utilisation d’intrinsics**

## Conseils pratiques et bonnes pratiques

- **Prise en main d’un éditeur de code :**
  - Utilisez un éditeur avancé permettant l’indentation automatique.
  - Exemples d'éditeurs :
    - *En ligne de commande* : emacs, vim, nano
    - *Avec interface graphique* : VS Code, Sublime, Notepad++, Geany
- **Familiarisation avec Linux :**
  - Apprenez à compiler des programmes en C avec **gcc**.
  - Compilation simple puis progressive vers des compilations séparées et des éditions de lien.
  - Déboguez avec **gdb** et compilez toujours avec **-g** et **-Wall**.
- **Précision et stabilité des mesures :**
  - Chaque mesure doit durer au moins **100 fois** la résolution du timer.
  - Pour améliorer la précision, utilisez une **boucle de répétition de mesures**.
  - Pour estimer la stabilité, effectuez **31 méta-répétitions** et analysez la variance.
  - Exclure ou inclure l’allocation mémoire selon la pertinence.
- **Optimisation du code :**
  - Toujours préciser un niveau d’optimisation à la compilation :
    - **O0/Og** pour le débogage
    - **O2** pour une optimisation générale
    - **O3** pour pousser l’optimisation (utile pour les calculs vectorisés)
  - Attention : un calcul non utilisé peut être supprimé par le compilateur dès **O2**.

## Installation et vérification de l'environnement

### Vérification du processeur et de l'architecture

- **Sous Linux :**
  ```bash
  uname -m
  ```

### Installation des compilateurs

#### AMD AOCC pour processeurs AMD
- **Téléchargement :**  
  - [AOCC sur le site AMD](https://www.amd.com/en/developer/aocc.html)

#### Intel oneAPI pour processeurs Intel
- **Téléchargement :**  
  - [Intel OneAPI Base Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html)

### Installation de MAQAO

- **Téléchargement :**  
  - [Site officiel MAQAO](http://www.maqao.org)

### Installation de perf-tools et likwid

#### Installation de perf-tools
- **Sous Ubuntu :**
  ```bash
  sudo apt install linux-tools-$(uname -r)
  ```

#### Installation de likwid
- **Cloner et installer :**
  ```bash
  git clone https://github.com/RRZE-HPC/likwid
  cd likwid
  make
  sudo make install
  ```

## Ressources et liens utiles

- **MAQAO :** [http://www.maqao.org](http://www.maqao.org)
- **Likwid :** [https://github.com/RRZE-HPC/likwid](https://github.com/RRZE-HPC/likwid]
