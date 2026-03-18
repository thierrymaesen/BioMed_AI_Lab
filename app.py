import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="BioMed AI Lab", page_icon="🔬", layout="wide")

# --- SYSTÈME DE MÉMOIRE (Session State) ---
# On utilise des clés internes (_sensibilite) pour éviter le conflit avec les widgets
if '_sensibilite' not in st.session_state:
    st.session_state._sensibilite = 50
if '_tolerance' not in st.session_state:
    st.session_state._tolerance = 5
if 'is_calibrated' not in st.session_state:
    st.session_state.is_calibrated = False

# Fonctions de mise à jour quand l'utilisateur touche manuellement les jauges
def update_sensibilite():
    st.session_state._sensibilite = st.session_state.widget_sensibilite
    
def update_tolerance():
    st.session_state._tolerance = st.session_state.widget_tolerance


# --- MOTEUR MATHÉMATIQUE D'AUTO-CALIBRATION ---
def auto_calibration(image_cv2, masque_ia):
    gris = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) if len(image_cv2.shape) == 3 else image_cv2.copy()
    gris_lisse = cv2.GaussianBlur(gris, (5, 5), 0)
    
    sobelx = cv2.Sobel(gris_lisse, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gris_lisse, cv2.CV_64F, 0, 1, ksize=3)
    contours = cv2.magnitude(sobelx, sobely)
    contours_8u = cv2.normalize(contours, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    pixels_in_mask = contours_8u[masque_ia == 255]
    
    if len(pixels_in_mask) > 0:
        seuil_calcule = int(np.mean(pixels_in_mask) + np.std(pixels_in_mask))
        seuil_calcule = max(10, min(seuil_calcule, 200))
    else:
        seuil_calcule = 50
        
    _, contours_forts = cv2.threshold(contours, seuil_calcule, 255, cv2.THRESH_BINARY)
    contours_forts = contours_forts.astype(np.uint8)
    anomalies_cibles = cv2.bitwise_and(contours_forts, contours_forts, mask=masque_ia)
    
    pixels_cellule = cv2.countNonZero(masque_ia)
    pixels_anormaux = cv2.countNonZero(anomalies_cibles)
    densite = (pixels_anormaux / pixels_cellule) * 100 if pixels_cellule > 0 else 0
    
    tolerance_calculee = int(densite) + 2
    tolerance_calculee = max(1, min(tolerance_calculee, 50))
    
    return seuil_calcule, tolerance_calculee


# --- BARRE LATÉRALE DE RÉGLAGE ---
st.sidebar.header("⚙️ Calibration du Laboratoire")

if st.session_state.is_calibrated:
    st.sidebar.success("✅ Appareil Calibré Automatiquement")
else:
    st.sidebar.warning("⚠️ Non Calibré (Réglages par défaut ou manuels)")

st.sidebar.info("💡 **Note Importante :** Si vous changez de microscope ou modifiez l'éclairage, refaites une Auto-Calibration avec une image saine de référence.")

st.sidebar.markdown("---")

# Les jauges utilisent la valeur interne comme valeur par défaut, et la mettent à jour quand on les bouge
st.sidebar.slider("Sensibilité aux contrastes", min_value=10, max_value=200, value=st.session_state._sensibilite, key='widget_sensibilite', on_change=update_sensibilite, step=5)
st.sidebar.slider("Tolérance de surface (%)", min_value=1, max_value=50, value=st.session_state._tolerance, key='widget_tolerance', on_change=update_tolerance, step=1)

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Créé par Thierry Maesen**")
st.sidebar.markdown("[📂 Code Source sur GitHub](https://github.com/thierrymaesen/BioMed_AI_Lab)")


# --- EN-TÊTE PRINCIPAL ---
st.title("🔬 BioMed AI : Analyse & Segmentation Cellulaire")
st.markdown("**Outil d'assistance au tri.** L'IA isole la matière biologique, puis analyse la densité des anomalies structurelles.")


# --- MOTEUR 1 : INTELLIGENCE ARTIFICIELLE (Segmentation K-Means) ---
def segmenter_avec_ia(image_cv2):
    pixels = image_cv2.reshape((-1, 3)) if len(image_cv2.shape) == 3 else image_cv2.reshape((-1, 1))
    pixels = np.float32(pixels)
    criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centres = cv2.kmeans(pixels, 3, None, criteres, 10, cv2.KMEANS_RANDOM_CENTERS)
    centres = np.uint8(centres)
    image_segmentee_ia = centres[labels.flatten()].reshape(image_cv2.shape)
    valeur_fond = np.argmax(np.sum(centres, axis=1) if len(centres.shape) > 1 else centres)
    masque_ia = np.zeros(labels.shape, dtype=np.uint8)
    masque_ia[labels != valeur_fond] = 255
    masque_ia = masque_ia.reshape((image_cv2.shape[0], image_cv2.shape[1]))
    return image_segmentee_ia, masque_ia

# --- MOTEUR 2 : COMPUTER VISION (Analyse de densité) ---
def analyser_cellule(image_cv2, masque_ia, seuil_sobel):
    gris = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) if len(image_cv2.shape) == 3 else image_cv2.copy()
    gris_lisse = cv2.GaussianBlur(gris, (5, 5), 0)
    sobelx = cv2.Sobel(gris_lisse, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gris_lisse, cv2.CV_64F, 0, 1, ksize=3)
    contours = cv2.magnitude(sobelx, sobely)
    _, contours_forts = cv2.threshold(contours, seuil_sobel, 255, cv2.THRESH_BINARY)
    contours_forts = contours_forts.astype(np.uint8)
    anomalies_cibles = cv2.bitwise_and(contours_forts, contours_forts, mask=masque_ia)
    pixels_cellule = cv2.countNonZero(masque_ia)
    pixels_anormaux = cv2.countNonZero(anomalies_cibles)
    densite_anomalie = (pixels_anormaux / pixels_cellule) * 100 if pixels_cellule > 0 else 0
    return densite_anomalie, gris, anomalies_cibles


# --- INTERFACE ---
fichier_upload = st.file_uploader("Insérez une image issue du microscope :", type=["png", "jpg", "jpeg"])

if fichier_upload is not None:
    image_pil = Image.open(fichier_upload)
    img_cv2 = np.array(image_pil)
    
    vue_ia, masque_ia = segmenter_avec_ia(img_cv2)
    
    # Bouton d'auto-calibration
    if st.button("🎯 Prendre cette image comme référence saine (Auto-Calibrer)"):
        nouveau_seuil, nouvelle_tol = auto_calibration(img_cv2, masque_ia)
        st.session_state._sensibilite = nouveau_seuil
        st.session_state._tolerance = nouvelle_tol
        st.session_state.is_calibrated = True
        st.rerun() # Recharge la page pour que les jauges affichent les nouvelles valeurs
    
    # Analyse standard avec les paramètres en mémoire
    densite, vue_grise, vue_alerte = analyser_cellule(img_cv2, masque_ia, st.session_state._sensibilite)
    
    st.markdown("---")
    if densite <= st.session_state._tolerance:
        st.success(f"🟢 NORMAL : Biologie conforme. (Perturbation : {densite:.1f}% / Tolérance de la machine : {st.session_state._tolerance}%)")
    else:
        st.error(f"🔴 ANOMALIE DÉTECTÉE ! Le niveau de perturbation ({densite:.1f}%) dépasse la tolérance de la machine ({st.session_state._tolerance}%).")
        
    img_resultat = cv2.cvtColor(vue_grise, cv2.COLOR_GRAY2BGR)
    img_resultat[vue_alerte > 0] = [255, 0, 0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(image_pil, caption="1. Image originale", use_container_width=True)
    with col2:
        st.image(vue_ia, caption="2. Cartographie IA", use_container_width=True)
    with col3:
        st.image(img_resultat, caption="3. Détection des anomalies", use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><small>BioMed AI Lab - Développé par Thierry Maesen | <a href='https://github.com/thierrymaesen/BioMed_AI_Lab' target='_blank'>Voir le code sur GitHub</a></small></div>", unsafe_allow_html=True)
