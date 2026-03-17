🔬 BioMed AI Lab : Analyse & Segmentation Cellulaire Hybride
Une application web locale (Open-Source) développée en Python et Streamlit. Elle est conçue pour assister les technologues de laboratoire médical dans l'analyse morphologique d'imagerie cellulaire (frottis sanguins, coupes tissulaires) en combinant l'Intelligence Artificielle et la Computer Vision classique.

🌟 L'Histoire du Développement : Pourquoi une approche hybride ?
Au départ de ce projet, l'objectif était de créer un modèle de Deep Learning classique capable de "deviner" si une cellule était malade ou saine.

Le problème fondamental de l'imagerie médicale :
Nous nous sommes heurtés au problème des "faux-positifs". Une IA entraînée sur un dataset limité a tendance à sur-réagir au "bruit" inhérent à la microscopie (poussière sur l'objectif, variation de la lumière halogène, artefacts de coloration). Le taux d'erreur de diagnostic était trop élevé pour être fiable en laboratoire.

La Solution Hybride implémentée :
Plutôt que de demander à l'IA de poser un diagnostic risqué, nous avons divisé le travail en deux moteurs distincts pour garantir une fiabilité à 100% :

L'IA "Localisatrice" (Machine Learning Non-Supervisé) :
L'algorithme de K-Means Clustering cartographie l'image à la volée. Il comprend la structure de l'image et sépare intelligemment la lumière de fond du microscope de la véritable matière biologique (cytoplasme et noyau). Il n'a besoin d'aucun entraînement préalable !

La Computer Vision (Algorithmique déterministe) :
Un filtre topographique (Sobel) prend le relais. Il scanne exclusivement la zone biologique détourée par l'IA pour y chercher des anomalies structurelles (déchirures de membrane, vacuoles, inclusions parasites) en calculant leur densité.

L'Expertise Humaine :
Le système ne remplace pas le technologue, il l'assiste. L'utilisateur garde le contrôle total via deux jauges de calibration en temps réel.

🚀 Guide d'Installation (100% Local et Sécurisé)
Aucune donnée médicale, aucune image de patient ne quitte votre ordinateur. L'intégralité du traitement s'exécute localement sur votre machine.

Prérequis
Avoir installé Python 3.8 (ou une version supérieure).

Avoir installé Git.

Procédure pas-à-pas
Ouvrez votre terminal (ou invite de commande) et tapez successivement ces commandes :

Cloner le projet sur votre ordinateur :
git clone https://github.com/VOTRE_PSEUDO/BioMed_AI_Lab.git
cd BioMed_AI_Lab

Créer un environnement virtuel (fortement recommandé) :
python -m venv venv

Activer l'environnement virtuel :

Sur Windows : venv\Scripts\activate

Sur Mac / Linux : source venv/bin/activate

Installer les dépendances requises :
pip install -r requirements.txt

Lancer le laboratoire virtuel :
python -m streamlit run app.py

Une page web s'ouvrira automatiquement dans votre navigateur !

👩‍🔬 Manuel d'Utilisation & Protocole de Calibration
Le paramétrage est le cœur du système.
Une image saine contenant des dizaines de globules rouges possède naturellement des "bords" (les membranes des cellules) que la machine pourrait confondre avec des anomalies ou des déchirures. Il est donc indispensable d'établir une ligne de base (Baseline) propre à votre microscope avant toute analyse.

Étape 1 : Établir la ligne de base (Calibration initiale)
Lancez l'application et insérez une image SAINE typique de votre lot d'analyse actuel.

Observez l'Image n°2 générée par l'IA : vérifiez qu'elle a correctement isolé les cellules du fond lumineux.

Observez le résultat textuel : Le système va détecter les contours naturels de vos cellules saines. Il affichera par exemple : "Niveau de perturbation mesuré : 22.8%".

Le réglage clé : Ajustez la jauge "Tolérance de surface (%)" dans la barre latérale pour qu'elle soit juste au-dessus de cette valeur (par exemple : 23%).

L'alerte passe au Vert 🟢. Votre outil est désormais parfaitement calibré pour ignorer le "bruit normal" de ce type d'échantillon !

Étape 2 : Analyser les échantillons suspects
Insérez maintenant les images de vos patients ou échantillons à tester.

Si une pathologie grave, une agglutination anormale ou un parasite est présent, la densité de texture de l'image va bondir.

Le pourcentage dépassera votre tolérance fixée à 23%. L'alerte passera immédiatement au Rouge 🔴 et ciblera l'anomalie visuellement sur l'Image n°3.

Étape 3 : Traquer les anomalies subtiles (Taches claires, vacuoles fines)
Si vous cherchez des pathologies structurelles très peu visibles à l'œil nu (comme un cytoplasme très légèrement décoloré) :

Baissez la première jauge "Sensibilité aux contrastes" (vers 30 ou 40).

L'algorithme de Sobel deviendra beaucoup plus sensible et pointilleux. Il affichera la moindre variation de gris ou de texture sur l'Image n°3, vous permettant de repérer l'invisible.

🛠️ Stack Technique
Ce projet repose sur des bibliothèques standards et éprouvées de l'écosystème Python :

Streamlit : Création de l'interface web interactive et réactive.

OpenCV (cv2) : Bibliothèque majeure de Computer Vision utilisée pour le filtre de Sobel et l'extraction des contours.

NumPy : Moteur mathématique de calcul matriciel gérant l'algorithme d'Intelligence Artificielle (K-Means Clustering).

Pillow (PIL) : Traitement et conversion des images uploadées par l'utilisateur.

🧠 Roadmap & Idées de Développement Futur
Le projet est fonctionnel, mais plusieurs pistes d'amélioration sont envisageables pour une future "Version 2.0" :

 Auto-Calibration par IA : Intégration de la méthode de seuillage d'Otsu pour que le système analyse l'histogramme de l'image et pré-règle automatiquement les deux jauges de calibration de manière optimale.

 Export PDF : Création d'un bouton pour exporter un "Rapport d'analyse de laboratoire" complet en format PDF (incluant les 3 images et les pourcentages mesurés).

 Support Médical Standard : Ajout de la bibliothèque pydicom pour permettre la lecture directe des fichiers d'imagerie médicale bruts au format .dcm (DICOM).

