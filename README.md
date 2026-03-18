<div align="center">

# 🔬 BioMed AI Lab
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biomed-ai-lab.streamlit.app/)

### Analyse & Segmentation Cellulaire Hybride

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Actif-brightgreen?style=for-the-badge)

**Une application web locale (Open-Source) développée en Python et Streamlit.**
Elle est conçue pour assister les technologues de laboratoire médical dans l'analyse morphologique d'imagerie cellulaire (frottis sanguins, coupes tissulaires) en combinant **l'Intelligence Artificielle** et la **Computer Vision** classique.

[🇬🇧 English Version](#-biomed-ai-lab-1)


</div>

---

## 🌟 L'Histoire du Développement : Pourquoi une approche hybride ?

Au départ de ce projet, l'objectif était de créer un modèle de Deep Learning classique capable de "deviner" si une cellule était malade ou saine.

### ❌ Le problème fondamental de l'imagerie médicale

Nous nous sommes heurtés au problème des **"faux-positifs"**. Une IA entraînée sur un dataset limité a tendance à sur-réagir au "bruit" inhérent à la microscopie (poussière sur l'objectif, variation de la lumière halogène, artefacts de coloration). Le taux d'erreur de diagnostic était trop élevé pour être fiable en laboratoire.

### ✅ La Solution Hybride implémentée

Plutôt que de demander à l'IA de poser un diagnostic risqué, nous avons divisé le travail en **deux moteurs distincts** pour garantir une fiabilité à 100% :

#### 🤖 L'IA "Localisatrice" (Machine Learning Non-Supervisé)

L'algorithme de **K-Means Clustering** cartographie l'image à la volée. Il comprend la structure de l'image et sépare intelligemment la lumière de fond du microscope de la véritable matière biologique (cytoplasme et noyau). Il n'a besoin d'**aucun entraînement préalable** !

#### 🔍 La Computer Vision (Algorithmique déterministe)

Un filtre topographique (**Sobel**) prend le relais. Il scanne exclusivement la zone biologique détourée par l'IA pour y chercher des anomalies structurelles (déchirures de membrane, vacuoles, inclusions parasites) en calculant leur densité.

#### 🎯 L'Auto-Calibration Intelligente
L'outil intègre un algorithme d'analyse statistique de la rugosité (Moyenne + Écart-type). En un clic sur une image saine, la machine calcule l'intensité des textures naturelles et ajuste automatiquement ses jauges de tolérance pour le microscope utilisé.

#### 👨‍🔬 L'Expertise Humaine

Le système ne remplace pas le technologue, il l'**assiste**. L'utilisateur garde le contrôle total via deux jauges de calibration en temps réel.

---

## 🚀 Guide d'Installation (100% Local et Sécurisé)

> 🔒 **Aucune donnée médicale, aucune image de patient ne quitte votre ordinateur.**
> L'intégralité du traitement s'exécute localement sur votre machine.

### Prérequis

- ✅ Avoir installé **Python 3.8** (ou une version supérieure).
- ✅ Avoir installé **Git**.

### Procédure pas-à-pas

Ouvrez votre terminal (ou invite de commande) et tapez successivement ces commandes :

**1. Cloner le projet sur votre ordinateur :**

```bash
git clone https://github.com/thierrymaesen/BioMed_AI_Lab.git
cd BioMed_AI_Lab
```

**2. Créer un environnement virtuel (fortement recommandé) :**

```bash
python -m venv venv
```

**3. Activer l'environnement virtuel :**

```bash
# Sur Windows :
venv\Scripts\activate

# Sur Mac / Linux :
source venv/bin/activate
```

**4. Installer les dépendances requises :**

```bash
pip install -r requirements.txt
```

**5. Lancer le laboratoire virtuel :**

```bash
python -m streamlit run app.py
```

> 🎉 Une page web s'ouvrira automatiquement dans votre navigateur !

---

## 👩‍🔬 Manuel d'Utilisation & Protocole de Calibration

Le paramétrage est le cœur du système. Une image saine contenant des dizaines de globules rouges possède naturellement des "bords" (les membranes des cellules) que la machine pourrait confondre avec des anomalies ou des déchirures. Il est donc indispensable d'établir une **ligne de base (Baseline)** propre à votre microscope avant toute analyse.

### Étape 1 : Établir la ligne de base (Auto-Calibration)
Chaque microscope et chaque type d'éclairage génère un "bruit" visuel différent (les membranes des cellules).
Il est donc indispensable d'établir une ligne de base avant toute analyse :

1. Lancez l'application et insérez une image **SAINE** typique de votre lot actuel.
2. Observez l'**Image n°2** générée par l'IA : vérifiez qu'elle a correctement isolé les cellules du fond lumineux.
3. Cliquez sur le bouton magique **"🎯 Prendre cette image comme référence saine (Auto-Calibrer)"**.
4. Le système va analyser la texture normale, ajuster visuellement les jauges de tolérance dans la barre latérale, et afficher le statut **"✅ Appareil Calibré Automatiquement"**.
5. *Note : Tant que vous ne changez pas les réglages physiques de votre microscope, vous pouvez enchaîner l'analyse de dizaines d'images avec ces réglages mémorisés.*

### Étape 2 : Analyser les échantillons suspects

1. Insérez maintenant les images de vos patients ou échantillons à tester.
2. Si une pathologie grave, une agglutination anormale ou un parasite est présent, la densité de texture de l'image va bondir.
3. Le pourcentage dépassera votre tolérance fixée à 23%.

> 🔴 L'alerte passera immédiatement au **Rouge** et ciblera l'anomalie visuellement sur l'**Image n°3**.

### Étape 3 : Traquer les anomalies subtiles (Taches claires, vacuoles fines)

Si vous cherchez des pathologies structurelles très peu visibles à l'œil nu (comme un cytoplasme très légèrement décoloré) :

1. Baissez la première jauge **"Sensibilité aux contrastes"** (vers 30 ou 40).
2. L'algorithme de Sobel deviendra beaucoup plus sensible et pointilleux. Il affichera la moindre variation de gris ou de texture sur l'**Image n°3**, vous permettant de repérer l'invisible.

---

## 🛠️ Stack Technique

Ce projet repose sur des bibliothèques standards et éprouvées de l'écosystème Python :

| Technologie | Rôle |
|:---:|---|
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Création de l'interface web interactive et réactive. |
| ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Bibliothèque majeure de Computer Vision utilisée pour le filtre de Sobel et l'extraction des contours. |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) | Moteur mathématique de calcul matriciel gérant l'algorithme d'Intelligence Artificielle (K-Means Clustering). |
| ![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square&logo=python&logoColor=white) | Traitement et conversion des images uploadées par l'utilisateur. |

---

## 🧠 Roadmap & Idées de Développement Futur

Le projet est fonctionnel, mais plusieurs pistes d'amélioration sont envisageables pour une future **"Version 2.0"** :

- [ ] **Export PDF** — Création d'un bouton pour exporter un "Rapport d'analyse de laboratoire" complet en format PDF (incluant les 3 images et les pourcentages mesurés).
- [ ] **Support Médical Standard** — Ajout de la bibliothèque `pydicom` pour permettre la lecture directe des fichiers d'imagerie médicale bruts au format `.dcm` (DICOM).

---

<div align="center">

# 🔬 BioMed AI Lab
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biomed-ai-lab.streamlit.app/)

### Hybrid Cell Analysis & Segmentation

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A local (Open-Source) web application built with Python and Streamlit.**
Designed to assist medical laboratory technologists in the morphological analysis of cell imaging (blood smears, tissue sections) by combining **Artificial Intelligence** and classical **Computer Vision**.

[🇫🇷 Version Française](#-biomed-ai-lab)

</div>

---

## 🌟 The Development Story: Why a Hybrid Approach?

At the beginning of this project, the goal was to create a classic Deep Learning model capable of "guessing" whether a cell was diseased or healthy.

### ❌ The Fundamental Problem of Medical Imaging

We ran into the problem of **"false positives"**. An AI trained on a limited dataset tends to overreact to the "noise" inherent in microscopy (dust on the objective lens, halogen light variation, staining artifacts). The diagnostic error rate was too high to be reliable in a laboratory setting.

### ✅ The Implemented Hybrid Solution

Rather than asking the AI to make a risky diagnosis, we divided the work into **two distinct engines** to guarantee 100% reliability:

#### 🤖 The "Locator" AI (Unsupervised Machine Learning)

The **K-Means Clustering** algorithm maps the image on the fly. It understands the image structure and intelligently separates the microscope's background light from the actual biological matter (cytoplasm and nucleus). It requires **no prior training**!

#### 🔍 Computer Vision (Deterministic Algorithm)

A topographic filter (**Sobel**) takes over. It exclusively scans the biological zone outlined by the AI to search for structural anomalies (membrane tears, vacuoles, parasitic inclusions) by calculating their density.

#### 🎯 Smart Auto-Calibration
The tool features a statistical roughness analysis algorithm (Mean + Standard Deviation). With a single click on a healthy reference image, the machine calculates the intensity of natural textures and automatically adjusts its tolerance sliders for the specific microscope being used.

#### 👨‍🔬 Human Expertise

The system does not replace the technologist — it **assists** them. The user retains full control via two real-time calibration gauges.

---

## 🚀 Installation Guide (100% Local and Secure)

> 🔒 **No medical data, no patient images ever leave your computer.**
> All processing runs entirely locally on your machine.

### Prerequisites

- ✅ **Python 3.8** or higher installed.
- ✅ **Git** installed.

### Step-by-Step Procedure

Open your terminal (or command prompt) and type the following commands:

**1. Clone the project to your computer:**

```bash
git clone https://github.com/thierrymaesen/BioMed_AI_Lab.git
cd BioMed_AI_Lab
```

**2. Create a virtual environment (strongly recommended):**

```bash
python -m venv venv
```

**3. Activate the virtual environment:**

```bash
# On Windows:
venv\Scripts\activate

# On Mac / Linux:
source venv/bin/activate
```

**4. Install the required dependencies:**

```bash
pip install -r requirements.txt
```

**5. Launch the virtual laboratory:**

```bash
python -m streamlit run app.py
```

> 🎉 A web page will automatically open in your browser!

---

## 👩‍🔬 User Manual & Calibration Protocol

Calibration is the heart of the system. A healthy image containing dozens of red blood cells naturally has "edges" (cell membranes) that the machine could mistake for anomalies or tears. It is therefore essential to establish a **baseline** specific to your microscope before any analysis.

### Step 1: Establish the Baseline (Auto-Calibration)
Every microscope and lighting setup generates different visual "noise" (cell membranes). It is therefore crucial to establish a baseline before any analysis:

1. Launch the app and upload a typical **HEALTHY** image from your current batch.
2. Look at **Image #2** generated by the AI: verify that it has correctly isolated the cells from the light background.
3. Click the magic button **"🎯 Take this image as healthy reference (Auto-Calibrate)"**.
4. The system will analyze the normal texture, visually adjust the tolerance sliders in the sidebar, and display the status **"✅ Device Automatically Calibrated"**.
5. *Note: As long as you don't change the physical settings of your microscope, you can analyze dozens of subsequent images with these saved settings.*

### Step 2: Analyze Suspect Samples

1. Now insert images of your patients or samples to be tested.
2. If a serious pathology, abnormal agglutination, or a parasite is present, the image's texture density will spike.
3. The percentage will exceed your tolerance set at 23%.

> 🔴 The alert will immediately turn **Red** and visually target the anomaly on **Image #3**.

### Step 3: Track Subtle Anomalies (Light Spots, Fine Vacuoles)

If you are looking for structural pathologies that are barely visible to the naked eye (such as very slightly discolored cytoplasm):

1. Lower the first **"Contrast Sensitivity"** gauge (to around 30 or 40).
2. The Sobel algorithm will become much more sensitive and meticulous. It will display the slightest variation in gray or texture on **Image #3**, allowing you to spot the invisible.

---

## 🛠️ Tech Stack

This project relies on standard and proven libraries from the Python ecosystem:

| Technology | Role |
|:---:|---|
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Creation of the interactive and reactive web interface. |
| ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Major Computer Vision library used for the Sobel filter and contour extraction. |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) | Mathematical engine for matrix computation powering the AI algorithm (K-Means Clustering). |
| ![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square&logo=python&logoColor=white) | Processing and conversion of user-uploaded images. |

---

## 🧠 Roadmap & Future Development Ideas

The project is functional, but several improvement paths are being considered for a future **"Version 2.0"**:

- [ ] **PDF Export** — Creation of a button to export a complete "Laboratory Analysis Report" in PDF format (including all 3 images and measured percentages).
- [ ] **Medical Standard Support** — Addition of the `pydicom` library to enable direct reading of raw medical imaging files in `.dcm` (DICOM) format.
