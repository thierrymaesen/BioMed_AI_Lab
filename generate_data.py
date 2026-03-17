import os
import cv2
import numpy as np

print("Génération du Dataset Synthétique (Microscopie simulée)...")

dossier_projet = os.path.dirname(os.path.abspath(__file__))
chemin_sain = os.path.join(dossier_projet, "dataset", "0_Sain")
chemin_anomalie = os.path.join(dossier_projet, "dataset", "1_Anomalie")

# Vider les dossiers
for dossier in [chemin_sain, chemin_anomalie]:
    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            os.remove(os.path.join(dossier, fichier))
    else:
        os.makedirs(dossier)

def creer_cellule_saine(taille=256):
    # Créer un fond de lamelle de microscope (dégradé très doux)
    img = np.ones((taille, taille), dtype=np.float32) * 200
    
    # Dessiner la membrane (un cercle flouté)
    cv2.circle(img, (taille//2, taille//2), 60, 100, -1)
    img = cv2.GaussianBlur(img, (21, 21), 0)
    
    # Ajouter le noyau (un peu plus sombre et centré)
    cv2.circle(img, (taille//2, taille//2), 20, 50, -1)
    img = cv2.GaussianBlur(img, (15, 15), 0)
    
    # Ajouter le bruit thermique du microscope (grain fin)
    bruit = np.random.normal(0, 5, (taille, taille))
    img = img + bruit
    return np.clip(img, 0, 255).astype(np.uint8)

def creer_cellule_anormale(taille=256):
    img = np.ones((taille, taille), dtype=np.float32) * 200
    cv2.circle(img, (taille//2, taille//2), 60, 100, -1)
    
    # L'ANOMALIE : Une dysplasie du noyau (beaucoup plus gros, excentré et sombre)
    cv2.circle(img, (taille//2 - 15, taille//2 + 10), 35, 20, -1)
    
    # Et une bordure déchirée (texture anormale)
    cv2.ellipse(img, (taille//2 + 40, taille//2), (20, 10), 45, 0, 360, 200, -1)
    
    img = cv2.GaussianBlur(img, (11, 11), 0)
    bruit = np.random.normal(0, 5, (taille, taille))
    img = img + bruit
    return np.clip(img, 0, 255).astype(np.uint8)

print("Création de 40 images Saines...")
for i in range(40):
    img = creer_cellule_saine()
    cv2.imwrite(os.path.join(chemin_sain, f"sain_{i}.png"), img)

print("Création de 10 images Anormales (pour vos tests)...")
for i in range(10):
    img = creer_cellule_anormale()
    cv2.imwrite(os.path.join(chemin_anomalie, f"anomalie_{i}.png"), img)

print("✅ Terminé ! Le dataset est prêt à l'emploi.")
