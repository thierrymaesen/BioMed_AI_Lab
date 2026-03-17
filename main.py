import os
import cv2
import numpy as np
from sklearn.ensemble import IsolationForest

# --- 1. CONFIGURATION DES CHEMINS ---
dossier_projet = os.path.dirname(os.path.abspath(__file__))
chemin_sain = os.path.join(dossier_projet, "dataset", "0_Sain")
chemin_anomalie = os.path.join(dossier_projet, "dataset", "1_Anomalie")

# --- 2. FONCTION POUR EXTRAIRE L'HISTOGRAMME DES COULEURS ---
def extraire_caracteristiques(chemin_dossier):
    caracteristiques = []
    noms_fichiers = []
    
    print(f"Extraction des couleurs depuis : {os.path.basename(chemin_dossier)}")
    for fichier in os.listdir(chemin_dossier):
        chemin_complet = os.path.join(chemin_dossier, fichier)
        img = cv2.imread(chemin_complet)
        
        if img is not None:
            # Calculer la répartition des couleurs (Bleu, Vert, Rouge)
            # C'est beaucoup plus robuste que de regarder pixel par pixel !
            hist_bleu = cv2.calcHist([img], [0], None, [8], [0, 256]).flatten()
            hist_vert = cv2.calcHist([img], [1], None, [8], [0, 256]).flatten()
            hist_rouge = cv2.calcHist([img], [2], None, [8], [0, 256]).flatten()
            
            # Coller les 3 histogrammes ensemble
            profil_couleur = np.concatenate((hist_bleu, hist_vert, hist_rouge))
            
            caracteristiques.append(profil_couleur)
            noms_fichiers.append(fichier)
            
    return np.array(caracteristiques), noms_fichiers

# --- 3. CHARGEMENT DES DONNÉES INTELLIGENTES ---
donnees_saines, noms_sains = extraire_caracteristiques(chemin_sain)
donnees_anomalies, noms_anomalies = extraire_caracteristiques(chemin_anomalie)

print("\n--- DÉBUT DE L'ENTRAÎNEMENT DE L'IA ---")
# --- 4. CRÉATION ET ENTRAÎNEMENT DU MODÈLE ---
modele_ia = IsolationForest(contamination=0.01, random_state=42)
modele_ia.fit(donnees_saines)
print("Entraînement terminé ! L'IA connaît le profil de couleur d'une cellule saine.")

print("\n--- PHASE DE TEST (Vérification) ---")
# --- 5. TEST SUR TOUTES LES IMAGES ---

print("\n>> Test sur 3 images SAINES (devraient être normales) :")
for i in range(3):
    pred = modele_ia.predict([donnees_saines[i]])
    if pred[0] == 1:
        print(f"✅ {noms_sains[i]} : NORMALE")
    else:
        print(f"❌ {noms_sains[i]} : ANORMALE (Fausse alerte)")

print("\n>> Test sur 3 images ANOMALIES (devraient lever une alerte) :")
for i in range(3):
    pred = modele_ia.predict([donnees_anomalies[i]])
    if pred[0] == -1:
        print(f"🚨 {noms_anomalies[i]} : ANOMALIE DÉTECTÉE ! Investigation requise.")
    else:
        print(f"❌ {noms_anomalies[i]} : NORMALE (L'IA l'a ratée)")
