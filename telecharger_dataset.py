import os
import cv2
import numpy as np

print("Génération du Dataset Synthétique Lisse (Test de Sobel)...")

dossier_projet = os.path.dirname(os.path.abspath(__file__))
chemin_sain = os.path.join(dossier_projet, "dataset", "0_Sain")
chemin_anomalie = os.path.join(dossier_projet, "dataset", "1_Anomalie")

for dossier in [chemin_sain, chemin_anomalie]:
    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            os.remove(os.path.join(dossier, fichier))
    else:
        os.makedirs(dossier)

# 1. Génération des Cellules SAINES (Membrane très floue, aucun choc)
print("Génération de 10 images saines parfaites...")
for i in range(10):
    img = np.ones((256, 256), dtype=np.uint8) * 200 # Fond clair
    
    # Un grand cercle gris clair très doux
    cv2.circle(img, (128, 128), 70, 100, -1)
    # Un noyau très doux
    cv2.circle(img, (128, 128), 30, 50, -1)
    
    # On floute ENORMEMENT pour que Sobel ne trouve aucune "falaise"
    img = cv2.GaussianBlur(img, (31, 31), 0)
    
    cv2.imwrite(os.path.join(chemin_sain, f"cellule_saine_parfaite_{i}.png"), img)

# 2. Génération des ANOMALIES (La même cellule, mais avec un pic / déchirure)
print("Génération de 10 images anormales...")
for i in range(10):
    img = np.ones((256, 256), dtype=np.uint8) * 200
    cv2.circle(img, (128, 128), 70, 100, -1)
    cv2.circle(img, (128, 128), 30, 50, -1)
    
    img = cv2.GaussianBlur(img, (31, 31), 0)
    
    # L'ANOMALIE : Une déchirure noire très dure (pas floutée !)
    # C'est cette différence de dureté (la falaise) que l'outil va détecter
    cv2.circle(img, (150, 100), 10, 0, -1) 
    cv2.ellipse(img, (128, 60), (20, 5), 30, 0, 360, 0, -1)
    
    cv2.imwrite(os.path.join(chemin_anomalie, f"cellule_anormale_dure_{i}.png"), img)

print("✅ Génération terminée. Les cellules saines sont 100% lisses pour Sobel.")
