# 🔬 BioMed AI Lab : Analyse & Segmentation Cellulaire Hybride

Une application web locale (Open-Source) Python/Streamlit conçue pour assister les technologues de laboratoire dans l'analyse morphologique d'imagerie cellulaire (frottis, coupes). 

![Aperçu du projet](https://via.placeholder.com/800x400.png?text=BioMed+AI+Lab+-+Interface+Streamlit) *(Ajoutez une capture d'écran de votre interface ici)*

## 🌟 Pourquoi ce projet ? (L'Histoire du Développement)

Au départ, l'objectif était de créer une Intelligence Artificielle classique qui "devine" si une cellule est malade ou saine. 
**Nous nous sommes heurtés à un mur majeur de l'imagerie médicale :** le manque de données parfaites et les faux-positifs. Une IA entraînée sur un petit dataset a tendance à sur-réagir à la moindre poussière ou variation de lumière du microscope.

**La Solution Hybride :**
Plutôt que de demander à l'IA de faire un *diagnostic* risqué, nous utilisons l'IA pour faire de la *segmentation* (comprendre l'image), et des mathématiques déterministes pour faire la *détection*.
1. **L'IA (Machine Learning Non-Supervisé) :** L'algorithme **K-Means Clustering** cartographie l'image à la volée. Il sépare intelligemment la lumière du microscope de la matière biologique.
2. **Computer Vision (Algorithmique pure) :** Un filtre topographique (Sobel) scanne ensuite *uniquement* la zone biologique définie par l'IA pour calculer la densité des anomalies de texture (déchirures, vacuoles).
3. **Le Technologue (L'Humain) :** Il calibre l'outil selon la réalité physique de son échantillon.

---

## 🚀 Installation (100% Local)

Aucune donnée médicale ne quitte votre ordinateur.

```bash
# 1. Cloner le projet
git clone https://github.com/VOTRE_NOM/BioMed_AI_Lab.git
cd BioMed_AI_Lab

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
# Windows : venv\Scripts\activate
# Mac/Linux : source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le laboratoire virtuel
python -m streamlit run app.py

👩‍🔬 Guide d'Utilisation et Protocole de Calibration
Le paramétrage est le cœur du système. Une image saine avec 100 globules rouges possède naturellement des "bords" que la machine peut confondre avec des déchirures. Il est donc crucial d'établir une ligne de base (Baseline).

Étape 1 : Établir la ligne de base (Calibration)
Insérez une image SAINE issue de votre lot d'analyse actuel.

Observez l'Image n°2 : vérifiez que l'IA a bien isolé les cellules (en noir) du fond lumineux.

Observez le résultat : Le système va détecter les contours naturels de vos cellules saines. Par exemple, il peut afficher : "Perturbation mesurée : 22.8%".

Réglez la jauge "Tolérance de surface (%)" juste au-dessus de cette valeur (ex: 23%).

L'alerte passe au Vert 🟢. Votre microscope est calibré pour ce type d'échantillon !

Étape 2 : Analyser les échantillons
Insérez maintenant vos images à tester.

Si une anomalie grave, une agglutination ou un parasite est présent, la densité de texture va bondir (ex: 35%) et dépasser votre tolérance de 23%.

L'alerte passera au Rouge 🔴.

Étape 3 : Traquer les anomalies subtiles (Taches claires, vacuoles)
Si vous cherchez des maladies très subtiles (ex: un cytoplasme très légèrement décoloré) :

Baissez la jauge "Sensibilité aux contrastes" (vers 30 ou 40).

L'algorithme deviendra beaucoup plus "pointilleux" et affichera les moindres variations de gris sur l'Image n°3.

🧠 Roadmap & Idées pour le futur
 Auto-Calibration par IA : Implémentation d'un algorithme (ex: méthode d'Otsu) pour que le système propose automatiquement les meilleures valeurs de jauges en analysant l'histogramme de l'image.

 Export des rapports au format PDF.

 Support des images DICOM.

Projet créé pour explorer la symbiose entre le Machine Learning, la Computer Vision et l'expertise médicale humaine.