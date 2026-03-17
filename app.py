import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="BioMed AI Lab", page_icon="🔬", layout="wide")

# --- BARRE LATÉRALE DE RÉGLAGE ---
st.sidebar.header("⚙️ Calibration du Laboratoire")
st.sidebar.markdown("""
**Étape 1 : Sensibilité du scan**
Définit ce que l'algorithme considère comme une anomalie (une tache claire, un bord flou...). *Baissez cette valeur pour détecter les anomalies subtiles.*
""")
sensibilite_contraste = st.sidebar.slider("Sensibilité aux contrastes", min_value=10, max_value=200, value=50, step=5)

st.sidebar.markdown("""
**Étape 2 : Tolérance biologique**
Combien de "bruit" (bordures normales des globules) tolérez-vous avant de sonner l'alarme ?
""")
tolerance_pourcentage = st.sidebar.slider("Tolérance de surface (%)", min_value=1, max_value=25, value=5, step=1)

# --- EN-TÊTE PRINCIPAL ---
st.title("🔬 BioMed AI : Analyse & Segmentation Cellulaire")
st.markdown("**Outil d'assistance au tri.** L'IA isole la matière biologique de la lumière du microscope, puis analyse la densité des anomalies structurelles.")

# --- MOTEUR 1 : INTELLIGENCE ARTIFICIELLE (Segmentation K-Means) ---
def segmenter_avec_ia(image_cv2):
    pixels = image_cv2.reshape((-1, 3)) if len(image_cv2.shape) == 3 else image_cv2.reshape((-1, 1))
    pixels = np.float32(pixels)
    
    # L'IA divise l'image en 3 groupes (Lumière du fond, Cytoplasme, Noyau/Taches)
    criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centres = cv2.kmeans(pixels, 3, None, criteres, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centres = np.uint8(centres)
    image_segmentee_ia = centres[labels.flatten()].reshape(image_cv2.shape)
    
    # CORRECTION : On trouve le groupe le plus CLAIR (le fond du microscope)
    valeur_fond = np.argmax(np.sum(centres, axis=1) if len(centres.shape) > 1 else centres)
    
    # MASQUE GLOBAL : On garde TOUTE la matière biologique (tout ce qui n'est pas le fond)
    masque_ia = np.zeros(labels.shape, dtype=np.uint8)
    masque_ia[labels != valeur_fond] = 255
    masque_ia = masque_ia.reshape((image_cv2.shape[0], image_cv2.shape[1]))
    
    return image_segmentee_ia, masque_ia

# --- MOTEUR 2 : COMPUTER VISION (Analyse de densité dans le masque) ---
def analyser_cellule(image_cv2, masque_ia, seuil_sobel, tolerance_pct):
    gris = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) if len(image_cv2.shape) == 3 else image_cv2.copy()
    gris_lisse = cv2.GaussianBlur(gris, (5, 5), 0) # Flou réduit pour ne pas effacer les petites anomalies
    
    # Filtre de Sobel
    sobelx = cv2.Sobel(gris_lisse, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gris_lisse, cv2.CV_64F, 0, 1, ksize=3)
    contours = cv2.magnitude(sobelx, sobely)
    
    # On utilise la jauge de "Sensibilité aux contrastes"
    _, contours_forts = cv2.threshold(contours, seuil_sobel, 255, cv2.THRESH_BINARY)
    contours_forts = contours_forts.astype(np.uint8)
    
    # Symbiose IA/CV
    anomalies_cibles = cv2.bitwise_and(contours_forts, contours_forts, mask=masque_ia)
    
    # Calcul des pourcentages
    pixels_cellule = cv2.countNonZero(masque_ia)
    pixels_anormaux = cv2.countNonZero(anomalies_cibles)
    
    if pixels_cellule > 0:
        densite_anomalie = (pixels_anormaux / pixels_cellule) * 100
    else:
        densite_anomalie = 0
        
    return densite_anomalie, gris, anomalies_cibles

# --- INTERFACE ---
fichier_upload = st.file_uploader("Insérez une image issue du microscope :", type=["png", "jpg", "jpeg"])

if fichier_upload is not None:
    image_pil = Image.open(fichier_upload)
    img_cv2 = np.array(image_pil)
    
    # 1. Cartographie IA
    vue_ia, masque_ia = segmenter_avec_ia(img_cv2)
    # 2. Scan algorithmique
    densite, vue_grise, vue_alerte = analyser_cellule(img_cv2, masque_ia, sensibilite_contraste, tolerance_pourcentage)
    
    st.markdown("---")
    
    if densite <= tolerance_pourcentage:
        st.success(f"🟢 NORMAL : Biologie conforme. (Perturbation : {densite:.1f}% / Toléré : {tolerance_pourcentage}%)")
    else:
        st.error(f"🔴 ANOMALIE DÉTECTÉE ! Le niveau de perturbation ({densite:.1f}%) dépasse la tolérance ({tolerance_pourcentage}%).")
        
    st.subheader("Rapport de l'Analyse :")
    
    img_resultat = cv2.cvtColor(vue_grise, cv2.COLOR_GRAY2BGR)
    img_resultat[vue_alerte > 0] = [255, 0, 0] # Zones suspectes en rouge
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(image_pil, caption="1. Image originale", use_container_width=True)
    with col2:
        st.image(vue_ia, caption="2. Cartographie IA (Toute la cellule)", use_container_width=True)
    with col3:
        st.image(img_resultat, caption="3. Détection des textures anormales", use_container_width=True)
